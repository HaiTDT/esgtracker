"""Isolated browser QA server using SYNTHETIC data; never user report history."""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import pymupdf
from dash import Dash
from dashboard.components.workspace import workspace_shell
from dashboard import upload_analysis as ui
from src.extraction.source_v2 import file_hash


def serve(root,port):
    root.mkdir(parents=True,exist_ok=True)
    pdf=root/'synthetic_qa.pdf'
    if not pdf.exists():
        with pymupdf.open() as doc:
            page=doc.new_page()
            page.insert_text((50,80),'SYNTHETIC QA ONLY: HEADCOUNT 100')
            doc.save(pdf)
    sha=file_hash(pdf)
    record={'record_id':'synthetic_quality_record','record_type':'measurement','company_id':'QA',
            'original_text':'100','classification':{'pillar':'S'},'reported_entity':None,
            'payload':{'parsed_value':'100','value':'100','unit':'people','name_raw':'Tổng số lao động'},
            'content_period':{'year':2025,'period_type':'year_label'},
            'review':{'status':'needs_review'},'boundary':{'included_entities':None,'excluded_entities':None,'consolidation_method':None},
            'missing_fields':['/reported_entity'],'source_refs':[], 'interpretation_notes':[], 'original_cells':[],
            'field_sources':{'/payload/raw_value':[{'pdf_page':1,'native_json_pointer':'/document/texts/0','raw_text':'100'}]}}
    output={'records':[record],'reports':[{'source_sha256':sha,'company_id':'QA','reporting_year':2025,'report_type':'ESG'}],
            'issues':[],'source_blocks':[],'source_artifacts':[{'kind':'pdf','path':pdf.name,'sha256':sha}]}
    result={'status':'completed','manifest':{'document_count':1,'failures':[]},'documents':[
        {'document_index':0,'filename':'SYNTHETIC_QA.pdf','workspace':str(root),'output':output,
         'coverage':{'counts':{'processed':1},'total_pages':1},'capture_status':'completed'}]}
    ui.JOBS['quality-qa']=result
    app=Dash(__name__)
    app.layout=workspace_shell(ui.upload_panel(),'Synthetic QA only')
    def seed(node):
        if getattr(node,'id',None)=='analysis-job':node.data={'id':'quality-qa','files':['SYNTHETIC_QA.pdf']}
        children=getattr(node,'children',None)
        for child in children if isinstance(children,list) else [children]:
            if hasattr(child,'to_plotly_json'):seed(child)
    seed(app.layout)
    ui.register_upload_callbacks(app,root)
    # Serve the actual project CSS; don't require fixture root to copy UI assets.
    @app.server.get('/quality-qa-assets.css')
    def css():
        from flask import Response
        return Response('\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'dashboard/assets').glob('*.css')),mimetype='text/css')
    app.index_string=app.index_string.replace('</head>','<link rel="stylesheet" href="/quality-qa-assets.css"></head>')
    print(json.dumps({'qa_owned_process':os.getpid(),'root':str(root),'port':port}),flush=True)
    app.run(host='127.0.0.1',port=port,debug=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--port',type=int,default=8052)
    args=parser.parse_args()
    serve(args.root.resolve(),args.port)
