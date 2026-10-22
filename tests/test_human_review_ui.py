from copy import deepcopy
import json
from pathlib import Path

import pymupdf
from dash import Dash

from dashboard import upload_analysis as ui
from dashboard.human_review import reviewed_result,review_export
from dashboard.components.presentation import display_rows,session_summary
from src.extraction.source_v2 import file_hash
from src.quality.records import native_snapshots,FIELDS


def result_fixture(root):
    root.mkdir(parents=True,exist_ok=True)
    with pymupdf.open() as pdf:
        pdf.new_page();pdf.save(root/'source.pdf')
    record={'record_id':'record','record_type':'measurement','company_id':'BSR','original_text':'100',
            'classification':{'pillar':'S'},'payload':{'parsed_value':'100','unit':'people'},'review':{'status':'needs_review'},
            'content_period':{'year':2025},'reported_entity':None,'boundary':{},'field_sources':{
                '/payload/raw_value':[{'pdf_page':1,'native_json_pointer':'/document/texts/0','raw_text':'100'}]},
            'source_refs':[],'interpretation_notes':[],'missing_fields':[],'original_cells':[]}
    return {'status':'completed','manifest':{'document_count':1,'failures':[]},'documents':[
        {'document_index':0,'filename':'BSR.pdf','workspace':str(root),'capture_status':'completed',
         'coverage':{'counts':{'processed':1},'total_pages':1},'output':{'records':[record],'source_blocks':[],
          'reports':[{'source_sha256':file_hash(root/'source.pdf'),'company_id':'BSR','reporting_year':2025}],
          'source_artifacts':[{'kind':'pdf','path':'source.pdf','sha256':file_hash(root/'source.pdf')}],'issues':[]}}]}


def callback(app,name):
    return next(v['callback'].__wrapped__ for k,v in app.callback_map.items() if name in k)


def test_ui_save_requires_pdf_confirmation_survives_reopen_and_exports_overlay(tmp_path):
    result=result_fixture(tmp_path/'fixture')
    before=deepcopy(result)
    app=Dash(__name__);app.layout=ui.upload_panel();ui.register_upload_callbacks(app,tmp_path)
    key='quality-ui-test';ui.JOBS[key]=result
    try:
        bind=callback(app,'human-review-selection.data')
        save=callback(app,'human-review-feedback.children')
        row='0:record';job={'id':key}
        selection=bind([row],job,0)[0]
        response=save(1,[row],job,selection,'correct','{"value":"10"}',['value'],'Reviewer','Checked source',[],0)
        assert 'Chưa lưu' in response[0]
        response=save(2,[row],job,selection,'correct','{"value":"10"}',['value'],'Reviewer','Checked source',['pdf'],0)
        assert 'partially_reviewed' in response[0] and response[1]==1
        view=reviewed_result(result,tmp_path)
        assert display_rows(view)[0]['value']=='10'
        assert display_rows(view)[0]['review_status']=='NOT_REVIEWED'
        assert review_export(result,tmp_path)['entries'][0]['current']['revision']==1
        assert bind([row],job,1)[0]['revision']==1
        # A stale tab cannot overwrite revision 1 using its revision 0 token.
        assert 'Chưa lưu' in save(3,[row],job,selection,'correct','{"value":"9"}',['value'],'Other','Checked',['pdf'],0)[0]
        assert result==before
    finally:ui.JOBS.pop(key,None)


def test_changed_source_or_missing_pdf_cannot_keep_review_effective(tmp_path):
    from src.quality.review_store import ReviewStore
    from src.quality.records import versions
    result=result_fixture(tmp_path/'fixture')
    snapshot=native_snapshots(result)[0]
    ReviewStore(tmp_path).save(snapshot,action='correct',corrections={'value':'10'},reviewed_fields=['value'],reviewer='A',reason='Source check',source_confirmed=True,versions=versions(tmp_path),expected_revision=0)
    result['documents'][0]['output']['records'][0]['payload']['parsed_value']='200'
    changed=reviewed_result(result,tmp_path)
    assert changed['documents'][0]['output']['records'][0]['human_review']['status']=='stale'
    assert display_rows(changed)[0]['value']=='200'
