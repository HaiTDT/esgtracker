from copy import deepcopy
import json
import pytest

from src.quality.records import digest, MEASUREMENT_FIELDS
from src.quality.review_store import ReviewStore, ReviewConflict


def snapshot():
    return {'record_key':'k','record_id':'r','source_sha256':'a'*64,'physical_page':1,'anchor':'/document/texts/0',
            'fingerprint':'f','record_type':'measurement','fields':{**{k:None for k in MEASUREMENT_FIELDS},'value':100,'unit':'people'}}


def save(store,s,**kwargs):
    args={'action':'correct','corrections':{'value':10},'reviewed_fields':['value'],'reviewer':'Reviewer fixture',
          'reason':'Test source check','source_confirmed':True,'versions':{'parser':'1'},'expected_revision':0}
    args.update(kwargs)
    return store.save(s,**args)


def test_corrections_persist_separately_and_do_not_overwrite_snapshot(tmp_path):
    store=ReviewStore(tmp_path)
    s=snapshot();original=deepcopy(s)
    out=save(store,s)
    assert out['status']=='partially_reviewed'
    assert out['effective_fields']['value']==10
    assert s==original
    reopened=ReviewStore(tmp_path).current(s,{'parser':'1'})
    assert reopened['revision']==1 and reopened['effective_fields']['value']==10
    assert reopened['dependent_analysis']=='NeedsReview'


def test_concurrent_stale_write_and_wrong_types_rejected(tmp_path):
    store=ReviewStore(tmp_path);s=snapshot()
    save(store,s)
    with pytest.raises(ReviewConflict):save(store,s)
    with pytest.raises(ValueError):save(store,s,source_confirmed=False,expected_revision=1)
    with pytest.raises(ValueError):save(store,s,corrections={'record_id':'new'},reviewed_fields=['record_id'],expected_revision=1)
    with pytest.raises(ValueError):save(store,s,corrections={'value':float('nan')},expected_revision=1)


def test_source_or_dictionary_change_invalidates_without_applying_old_values(tmp_path):
    store=ReviewStore(tmp_path);s=snapshot()
    save(store,s)
    current=store.current(s,{'parser':'2'})
    assert current['status']=='stale' and current['effective_fields']['value']==100
    s['fingerprint']='new'
    assert store.current(s,{'parser':'1'})['status']=='stale'


def test_incremental_edits_accumulate_and_reset_is_a_new_event(tmp_path):
    store=ReviewStore(tmp_path);s=snapshot()
    save(store,s)
    out=save(store,s,corrections={'unit':'people'},reviewed_fields=['unit'],expected_revision=1)
    assert out['effective_fields']['value']==10 and out['reviewed_fields']==['unit','value']
    assert len(store.history('k'))==2
    assert store.history('k')[1]['previous_event_hash']==store.history('k')[0]['event_hash']
    reset=save(store,s,action='reset',corrections={},reviewed_fields=[],expected_revision=2)
    assert reset['status']=='pending_human_review' and reset['effective_fields']['value']==100
    assert len(store.history('k'))==3


def test_full_review_requires_all_fields_and_still_has_no_financial_verdict(tmp_path):
    store=ReviewStore(tmp_path);s=snapshot()
    result=save(store,s,reviewed_fields=list(MEASUREMENT_FIELDS))
    assert result['status']=='reviewed' and result['financial_verdict'] is None
    export=store.export([s],{'parser':'1'})
    assert export['is_gold'] is False and export['source_immutable']
