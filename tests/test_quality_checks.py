from src.quality.checks import financial_formula_checks,record_checks
from src.quality.dictionary import load_dictionary,identify_metric


def test_dictionary_is_provisional_and_ambiguous_mapping_is_not_forced():
    d=load_dictionary()
    assert len(d['local_metrics'])==10
    assert d['source_references']==[]
    assert identify_metric('Phải trả người lao động')=='employee_payables'
    assert identify_metric('Tổng doanh thu') is None
    assert identify_metric('Lợi nhuận sau thuế chưa phân phối') is None
    assert identify_metric('Phải trả người lao động và tạm ứng cho nhân viên') is None


def native_row(code,value,label,year=2024,scope='separate'):
    return {'record_id':code+str(year),'record_type':'measurement','content_period':{'year':year},
            'payload':{'item_code_raw':code,'parsed_value':value,'row_label_raw':label,
                       'unit':'VND','scale':1,'statement_scope':scope,'table_anchor_id':'table','column_index':4}}


def test_formula_residual_is_review_signal_not_contradiction():
    rows=[native_row('50',100,'Trước thuế'),native_row('51',10,'Thuế'),native_row('52',5,'Hoãn lại'),native_row('60',90,'Lợi nhuận (60=50-51-52)')]
    report=financial_formula_checks({'records':rows})
    assert report['formulas_evaluated']==1
    assert report['findings'][0]['residual']=='5'
    assert report['findings'][0]['status']=='NeedsReview'
    rows[0]['content_period']['year']=2023
    assert financial_formula_checks({'records':rows})['formulas_evaluated']==0


def test_headcount_unit_and_value_review():
    r={'record_id':'r','physical_page':1,'anchor':'/table/0','label':'Tổng số lao động',
       'fields':{'value':-1.5,'unit':'VND','observation_year':2024}}
    codes={x['code'] for x in record_checks(r)}
    assert 'METRIC_UNIT_REVIEW' in codes and 'HEADCOUNT_NON_INTEGER_OR_NEGATIVE' in codes
