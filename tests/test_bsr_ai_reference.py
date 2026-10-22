import importlib.util
from copy import deepcopy
from pathlib import Path

import pytest


def module():
    spec=importlib.util.spec_from_file_location('bsr_ai_reference',Path(__file__).resolve().parents[1]/'scripts/build_bsr_ai_reference.py')
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_numeric_transcription_preserves_scale_and_does_not_guess_separator():
    m=module()
    assert m.number('1.790.388','tCO2e')[:2]==(1790388,'tCO2e')
    assert m.number('3.666,43','tấn')[:2]==(3666.43,'t')
    assert m.number('54,3 triệu','giờ')[:2]==(54300000,'hours')
    assert m.number('179, 5','tỷ đồng')[:2]==(179500000000,'VND')
    assert m.number('100% đạt QCVN','%')[:2]==(100,'%')
    assert m.number('3.319','GJ/tấn SP','ambiguous_separator')[0] is None
    assert m.number('BB+','-','categorical')[0] is None


def record():
    m=module()
    return m.make_reference('a'*64,1,'Tổng số lao động','1.594','Người','2025',[.1,.2,.8,.3],table='test',year=2025)


def test_ai_sidecar_is_not_human_gold_and_null_lists_are_synchronised():
    m=module()
    r=record()
    d={'schema_version':'oil-gas-ai-reference/1.0','annotation_status':m.STATUS,'is_gold':False,
       'source_inventory':{'a'*64:{'pages':1}},'records':[r]}
    assert m.validate_reference(d)['human_approved_records']==0
    broken=deepcopy(d)
    broken['is_gold']=True
    with pytest.raises(ValueError,match='must not claim'): m.validate_reference(broken)
    broken=deepcopy(d)
    broken['records'][0]['boundary']['included_entities']=['inferred']
    with pytest.raises(ValueError,match='missing-fields'): m.validate_reference(broken)
    broken=deepcopy(d)
    broken['records'][0]['field_evidence']['value'][0]['source_sha256']='b'*64
    with pytest.raises(ValueError,match='field-level'): m.validate_reference(broken)


def test_links_do_not_copy_wrong_prediction_values_or_mutate_ids():
    m=module()
    r=record()
    rows=[{'record_id':'keep-id','source_sha256':'a'*64,'physical_page':1,
        'label':'Tổng số lao động','anchor':'/original/pointer','record_type':'measurement',
        'fingerprint':'original-hash','fields':{'value':999,'unit':'VND','observation_year':2025}}]
    before=deepcopy(rows)
    m.attach_bindings([r],rows)
    assert r['expected']['value']==1594
    assert r['extract_record_bindings'][0]['record_id']=='keep-id'
    assert r['extract_record_bindings'][0]['json_pointer']=='/original/pointer'
    changes=m.comparison_proposals([r],rows)
    assert changes[0]['field_differences']['value']['extracted']==999
    assert changes[0]['field_differences']['value']['ai_reference']==1594
    assert changes[0]['auto_applied'] is False
    assert rows==before


def test_existing_gold_evaluator_refuses_ai_reference():
    from src.quality.evaluation import evaluate
    with pytest.raises(ValueError,match='Unsupported gold schema'):
        evaluate([],{'schema_version':'oil-gas-ai-reference/1.0','annotation_status':'AI_reviewed_pending_human_review'})
