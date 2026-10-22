"""Append-only, optimistic-concurrency human corrections stored separately from OCR."""
from copy import deepcopy
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import uuid

from src.quality.records import FIELDS, digest, required_fields, valid_corrections


class ReviewConflict(ValueError):
    pass


class ReviewStore:
    def __init__(self, root):
        self.path = Path(root)/'data/processed/human_review/reviews.sqlite3'

    @contextmanager
    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, record_key TEXT NOT NULL, revision INTEGER NOT NULL, body TEXT NOT NULL, UNIQUE(record_key,revision))')
        db.commit()
        try:
            with db:
                yield db
        finally:
            db.close()

    def history(self, key):
        if not self.path.exists():
            return []
        with self.connect() as db:
            return [json.loads(r['body']) for r in db.execute('SELECT body FROM events WHERE record_key=? ORDER BY revision',(key,))]

    def latest(self):
        if not self.path.exists():return {}
        with self.connect() as db:
            return {r['record_key']:json.loads(r['body']) for r in db.execute('SELECT e.record_key,e.body FROM events e JOIN (SELECT record_key,MAX(revision) revision FROM events GROUP BY record_key) x ON e.record_key=x.record_key AND e.revision=x.revision')}

    def current(self, snapshot, versions, events=None):
        events = self.history(snapshot['record_key']) if events is None else events
        if not events:
            return {'status':'pending_human_review','revision':0,'effective_fields':deepcopy(snapshot['fields']), 'reviewed_fields':[], 'dependent_analysis':'not_reviewed'}
        event = events[-1]
        stale = event['snapshot']['fingerprint'] != snapshot['fingerprint'] or event['versions'] != versions
        fields = deepcopy(snapshot['fields'])
        if not stale and event['action'] not in ('reset','reject'):
            fields.update(event['corrections'])
        return {**event, 'status':'stale' if stale else event['status'], 'effective_fields':fields,
                'reviewed_fields':[] if stale else event['reviewed_fields'],
                'dependent_analysis':'NeedsReview' if event['action'] != 'reset' else 'not_reviewed',
                'source_or_dictionary_changed':stale}

    def save(self, snapshot, *, action, corrections, reviewed_fields, reviewer, reason, source_confirmed, versions, expected_revision):
        if action not in ('accept','correct','reject','reset'):
            raise ValueError('Hành động không hợp lệ.')
        if not isinstance(reviewer,str) or not reviewer.strip() or not isinstance(reason,str) or not reason.strip():
            raise ValueError('Cần tên người rà soát và lý do.')
        if source_confirmed is not True:
            raise ValueError('Cần xác nhận đã đối chiếu PDF; không tự duyệt từ OCR.')
        if not snapshot.get('source_sha256') or not snapshot.get('physical_page') or not snapshot.get('anchor'):
            raise ValueError('Record chưa có nguồn/trang/anchor đủ để lưu xác nhận.')
        corrections = valid_corrections(corrections)
        if not isinstance(reviewed_fields,list) or set(reviewed_fields)-set(FIELDS):
            raise ValueError('Danh sách field đã rà soát không hợp lệ.')
        if not set(reviewed_fields) <= set(snapshot['fields']):
            raise ValueError('Không được đánh dấu field không có trong projection hiện tại.')
        if action in ('accept','reject','reset') and corrections:
            raise ValueError('Chỉ hành động correct được mang bản sửa.')
        if action == 'correct' and (not corrections or not set(corrections) <= set(reviewed_fields)):
            raise ValueError('Bản sửa phải có field và các field đó phải được chọn đã rà soát.')
        if action in ('accept','correct') and not reviewed_fields:
            raise ValueError('Chọn các field đã thực sự rà soát.')
        if action in ('reset','reject'):
            reviewed_fields=[]
        effective = deepcopy(snapshot['fields'])
        effective.update(corrections)
        complete = set(required_fields(snapshot)) <= set(reviewed_fields)
        status = 'rejected' if action=='reject' else 'pending_human_review' if action=='reset' else 'reviewed' if complete else 'partially_reviewed'
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            previous = db.execute('SELECT MAX(revision) FROM events WHERE record_key=?',(snapshot['record_key'],)).fetchone()[0] or 0
            if expected_revision != previous:
                raise ReviewConflict('Dữ liệu đã được sửa ở phiên khác. Mở lại record trước khi lưu.')
            previous_body = db.execute('SELECT body FROM events WHERE record_key=? ORDER BY revision DESC LIMIT 1',(snapshot['record_key'],)).fetchone()
            prior = json.loads(previous_body[0]) if previous_body else None
            if action in ('accept','correct') and prior and prior['action'] not in ('reject','reset') and prior['snapshot']['fingerprint']==snapshot['fingerprint'] and prior['versions']==versions:
                inherited = dict(prior['corrections'])
                inherited.update(corrections)
                corrections = inherited
                reviewed_fields = sorted(set(reviewed_fields) | set(prior['reviewed_fields']))
                effective.update(corrections)
                status = 'reviewed' if set(required_fields(snapshot)) <= set(reviewed_fields) else 'partially_reviewed'
            event = {'event_id':uuid.uuid4().hex,'record_key':snapshot['record_key'],'revision':previous+1,
                     'created_at_utc':datetime.now(timezone.utc).isoformat(),'reviewer':reviewer.strip(),'reason':reason.strip(),
                     'action':action,'status':status,'source_confirmed':True,'reviewed_fields':sorted(set(reviewed_fields)),
                     'corrections':corrections,'snapshot':deepcopy(snapshot),'versions':deepcopy(versions),
                     'effective_fields':effective,'event_hash':None,
                     'dependent_analysis':'NeedsReview','financial_verdict':None}
            event['previous_event_hash'] = json.loads(previous_body[0])['event_hash'] if previous_body else None
            event['event_hash'] = digest({k:v for k,v in event.items() if k!='event_hash'})
            db.execute('INSERT INTO events VALUES (?,?,?,?)',(event['event_id'],snapshot['record_key'],event['revision'],json.dumps(event,ensure_ascii=False,allow_nan=False)))
        return self.current(snapshot, versions)

    def export(self, snapshots, versions):
        entries = []
        for snapshot in snapshots:
            history = self.history(snapshot['record_key'])
            if history:
                entries.append({'record_key':snapshot['record_key'],'current':self.current(snapshot,versions),'history':history})
        return {'schema_version':'esg-human-review/1.0','entries':entries,'versions':versions,
                'source_immutable':True,'is_gold':False,'automatic_financial_verdict':False,
                'dependent_pairs':'All affected candidates must be rechecked; corrections are not auto-merged into native/corporate extraction.'}
