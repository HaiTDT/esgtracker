import importlib.util
import json
from pathlib import Path


def module():
    spec=importlib.util.spec_from_file_location('quality_cli',Path(__file__).resolve().parents[1]/'scripts/quality_benchmark.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def test_known_development_pdfs_cannot_be_templated_as_independent_test(tmp_path,monkeypatch):
    m=module()
    source=tmp_path/'predictions.json'
    source.write_text(json.dumps({'schema_version':'esg-quality-predictions/1.0','versions':{},'records':[
        {'record_id':'r','source_sha256':'a'*64,'physical_page':1,'anchor':'/text/0','record_type':'claim','fields':{'text':'example'}}]}),encoding='utf-8')
    monkeypatch.setattr(m,'known_development_sources',lambda:{'a'*64})
    monkeypatch.setattr(m.sys,'argv',['quality_benchmark.py','template',str(source),'--destination',str(tmp_path/'draft'),'--split','test'])
    assert m.main()==2
    assert not (tmp_path/'draft').exists()
    monkeypatch.setattr(m.sys,'argv',['quality_benchmark.py','template',str(source),'--destination',str(tmp_path/'draft')])
    assert m.main()==0
    gold=json.loads((tmp_path/'draft/gold_draft.json').read_text(encoding='utf-8'))
    assert gold['evaluation_units'][0]['split']=='dev'
    assert gold['annotation_status']=='draft' and gold['development_source_sha256']==['a'*64]


def test_prediction_metadata_does_not_claim_current_code_produced_old_extraction():
    m=module()
    meta=m.benchmark_versions()
    assert 'benchmark_environment' in meta
    assert 'NOT historical extractor version proof' in meta['extraction_version_source']
