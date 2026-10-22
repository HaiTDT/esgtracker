from copy import deepcopy
import pytest

from src.quality.evaluation import make_template, evaluate, ocr_errors
from src.quality.records import MEASUREMENT_FIELDS


def prediction(rid='a',anchor='/tables/0/cells/1',value=10,year=2024):
    return {'record_id':rid,'source_sha256':'a'*64,'physical_page':1,'anchor':anchor,'record_type':'measurement',
            'fields':{'metric_id':'local:test:v1','value':value,'unit':'people','observation_year':year,
                      'period_type':'at_date','reporting_entity':'BSR','consolidation':'Separate','scope':'Công ty'}}


def gold_for(rows):
    gold=make_template(rows)
    gold['annotation_status']='human_reviewed'
    for unit in gold['evaluation_units']:
        unit.update(annotator='TEST FIXTURE ONLY',reviewed_against_pdf=True,fully_annotated=True)
        for item in unit['items']:
            item['expected']=deepcopy(item['suggested_prediction'])
            item['reviewed_fields']=list(item['expected'])
    return gold


def test_draft_cannot_report_precision_or_auto_gold():
    row=prediction()
    draft=make_template([row])
    assert draft['evaluation_units'][0]['items'][0]['expected']=={}
    with pytest.raises(ValueError,match='human_reviewed'):
        evaluate([row],draft)


def test_wrong_year_is_not_a_correct_record_even_when_value_matches():
    rows=[prediction(),prediction('b','/tables/0/cells/2')]
    gold=gold_for(rows)
    rows[1]['fields']['observation_year']=2023
    report=evaluate(rows,gold)
    assert report['strict_record']['precision']==.5
    assert report['strict_record']['recall']==.5
    assert report['strict_record']['f1']==.5
    assert report['field_accuracy']['value']['accuracy']==1
    assert report['field_accuracy']['observation_year']['accuracy']==.5


def test_missing_extra_duplicate_and_partial_scope():
    a,b=prediction(),prediction('b','/tables/0/cells/2')
    gold=gold_for([a,b])
    report=evaluate([a,deepcopy(a),prediction('c','/tables/0/cells/3')],gold)
    assert {k:report['strict_record'][k] for k in ('tp','fp','fn')}=={'tp':1,'fp':2,'fn':1}
    gold['evaluation_units'][0]['fully_annotated']=False
    report=evaluate([a,prediction('c','/tables/0/cells/3')],gold)
    assert report['strict_record']['fp']==0
    assert report['scope']['selected_anchor_units']==1


def test_null_is_not_zero_and_no_predictions_is_not_100_percent():
    a=prediction(value=0)
    gold=gold_for([a])
    a['fields']['value']=None
    assert evaluate([a],gold)['strict_record']['tp']==0
    report=evaluate([],gold)
    assert report['strict_record']['precision'] is None
    assert report['strict_record']['recall']==0


def test_document_level_development_leakage_and_incomplete_gold_rejected():
    row=prediction()
    gold=gold_for([row])
    with pytest.raises(ValueError,match='leakage'):
        evaluate([row],gold,development_sources=['a'*64])
    del gold['evaluation_units'][0]['items'][0]['expected']['unit']
    with pytest.raises(ValueError,match='bắt buộc'):
        evaluate([row],gold)


def test_ocr_uses_accents_and_separate_prediction_not_gold_suggestions():
    assert ocr_errors('đầu','dau')['cer']>0
    assert ocr_errors('','bad')['cer'] is None
    a=prediction()
    gold=gold_for([a])
    gold['evaluation_units'][0]['ocr_reference']='đầu khí'
    gold['evaluation_units'][0]['ocr_prediction']='đầu khí' # ignored
    with pytest.raises(ValueError,match='separately'):
        evaluate([a],gold)
    report=evaluate([a],gold,ocr_predictions=[{'source_sha256':'a'*64,'physical_page':1,'text':'dau khi'}])
    assert report['ocr']['cer']>0 and report['ocr']['wer']==1
