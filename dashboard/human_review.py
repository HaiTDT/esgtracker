"""Local review controls reusing the current UI; original extraction is immutable."""
from copy import deepcopy
import json

from dash import Input, Output, State, dcc, html, no_update

from src.quality.records import FIELDS, native_snapshots, versions
from src.quality.review_store import ReviewStore, ReviewConflict
from src.quality.checks import record_checks
from src.extraction.source_v2 import file_hash


def review_controls():
    return html.Div([
        html.H3('Rà soát & bản sửa của người dùng'),
        html.P('Chọn record, mở PDF gốc rồi chỉ đánh dấu các field đã kiểm tra. Bản sửa lưu riêng; không ghi đè OCR và không tự kết luận đối chiếu tài chính.'),
        dcc.Store(id='human-review-selection'), dcc.Store(id='human-review-refresh',data=0),
        html.Div(id='human-review-current',role='status'),
        html.Iframe(id='human-review-pdf',title='PDF gốc để đối chiếu',className='human-review-pdf',src='about:blank'),
        html.Div([
            html.Div([html.Label('Tên người rà soát',htmlFor='human-review-reviewer'),
                      dcc.Input(id='human-review-reviewer',type='text',placeholder='Nhập tên của bạn',maxLength=120)],className='extract-field'),
            html.Div([html.Label('Hành động',htmlFor='human-review-action'),
                      dcc.Dropdown(id='human-review-action',clearable=False,value='accept',options=[
                          {'label':'Xác nhận các field đã chọn','value':'accept'},
                          {'label':'Lưu bản sửa các field','value':'correct'},
                          {'label':'Từ chối record','value':'reject'},
                          {'label':'Mở lại / bỏ hiệu lực bản duyệt','value':'reset'}])],className='extract-field')
        ],className='human-review-form'),
        html.Label('Field đã thực sự kiểm tra trong PDF'),
        dcc.Checklist(id='human-review-fields',options=[{'label':f,'value':f} for f in FIELDS],value=[],className='human-review-fields'),
        html.Label('Bản sửa dạng JSON — chỉ điền khi chọn “Lưu bản sửa”',htmlFor='human-review-patch'),
        dcc.Textarea(id='human-review-patch',value='{}',placeholder='{"value": "1594", "unit": "people", "observation_year": 2025}',className='human-review-patch'),
        html.Label('Lý do / vị trí kiểm tra trong nguồn',htmlFor='human-review-reason'),
        dcc.Textarea(id='human-review-reason',placeholder='Ví dụ: đã kiểm tra đúng hàng và cột năm tại trang PDF…',className='human-review-patch'),
        dcc.Checklist(id='human-review-confirm',options=[{'label':'Tôi đã mở và đối chiếu PDF gốc, không chỉ đọc kết quả OCR.','value':'pdf'}],value=[]),
        html.Button('Lưu rà soát / bản sửa',id='human-review-save',n_clicks=0,className='ui-button ui-button--primary'),
        html.Div(id='human-review-feedback',role='status',**{'aria-live':'polite'}),
        html.Small('Tên reviewer do người dùng khai báo; đây chưa phải hệ thống đăng nhập/phân quyền hoặc chữ ký xác nhận.')
    ],className='workspace-card human-review-card')


def reviewed_result(result,root):
    if not result or result.get('status')!='completed':
        return result
    result_copy=deepcopy(result)
    store=ReviewStore(root)
    if not store.path.exists():
        return result_copy
    version=versions(root)
    latest=store.latest()
    snapshots={r['selection_id']:r for r in native_snapshots(result)}
    for doc in result_copy['documents']:
        for record in doc['output']['records']:
            snapshot=snapshots[f"{doc['document_index']}:{record['record_id']}"]
            if snapshot['record_key'] in latest:
                current=store.current(snapshot,version,events=[latest[snapshot['record_key']]])
                record['human_review']=current
    return result_copy


def review_export(result,root):
    return ReviewStore(root).export(native_snapshots(result),versions(root))


def register_review_callbacks(app,root,result_loader,source_loader,pdf_loader):
    @app.callback(Output('human-review-selection','data'),Output('human-review-current','children'),
                  Output('human-review-fields','value'),Output('human-review-patch','value'),
                  Output('human-review-pdf','src'),
                  Input('analysis-records','selected_row_ids'),Input('analysis-job','data'),Input('human-review-refresh','data'))
    def bind(selected,job,refresh):
        result=result_loader(job,root)
        if not result or result.get('status')!='completed' or not selected:
            return None,'Chưa chọn record để rà soát.',[],'{}','about:blank'
        snapshot=next((r for r in native_snapshots(result) if r['selection_id']==selected[0]),None)
        if not snapshot:
            return None,'Record không còn trong kết quả hiện tại.',[],'{}','about:blank'
        current=ReviewStore(root).current(snapshot,versions(root))
        notes=record_checks(snapshot)
        history=ReviewStore(root).history(snapshot['record_key'])
        index=int(selected[0].split(':',1)[0])
        try:
            found=pdf_loader(result,index)
        except (ValueError,OSError):
            found=None
        pdf=f"/extract-source/{job['id']}/{index}#page={snapshot['physical_page']}" if found else 'about:blank'
        return {'record_key':snapshot['record_key'],'revision':current['revision'],'fingerprint':snapshot['fingerprint']},[
            html.Strong(f"Trạng thái: {current['status']} · Phiên bản rà soát {current['revision']}"),
            html.P('Field có hiệu lực dưới đây là lớp rà soát, không thay thế nguyên văn OCR.'),
            html.Pre(json.dumps(current['effective_fields'],ensure_ascii=False,indent=2),className='human-review-json'),
            html.Ul([html.Li(n['code']+' — '+n['message']) for n in notes]),
            html.Details([html.Summary(f'Lịch sử sửa ({len(history)} sự kiện)'),html.Pre(json.dumps(history[-5:],ensure_ascii=False,indent=2),className='human-review-json')]),
            html.P('Nếu source/parser/từ điển thay đổi, bản duyệt chuyển stale. Mọi cặp phụ thuộc vẫn cần rà soát lại.')
        ],current['reviewed_fields'],'{}',pdf

    @app.callback(Output('human-review-feedback','children'),Output('human-review-refresh','data'),
                  Input('human-review-save','n_clicks'),State('analysis-records','selected_row_ids'),State('analysis-job','data'),
                  State('human-review-selection','data'),State('human-review-action','value'),State('human-review-patch','value'),
                  State('human-review-fields','value'),State('human-review-reviewer','value'),State('human-review-reason','value'),
                  State('human-review-confirm','value'),State('human-review-refresh','data'),prevent_initial_call=True)
    def save(clicks,selected,job,selection,action,patch,fields,reviewer,reason,confirm,refresh):
        result=result_loader(job,root)
        if not result or result.get('status')!='completed' or not selected or not selection:
            return 'Chọn một record có nguồn trước khi lưu.',no_update
        snapshot=next((r for r in native_snapshots(result) if r['selection_id']==selected[0]),None)
        if not snapshot or selection['record_key']!=snapshot['record_key'] or selection['fingerprint']!=snapshot['fingerprint']:
            return 'Record đã thay đổi. Chọn lại để tải phiên bản hiện tại.',no_update
        try:
            doc_index=int(selected[0].split(':',1)[0])
            pdf_found=pdf_loader(result,doc_index)
            if not pdf_found:
                raise ValueError('Không tìm thấy PDF gốc.')
            if file_hash(pdf_found[0])!=snapshot['source_sha256']:
                raise ValueError('SHA-256 của record không khớp PDF gốc đang mở.')
            parsed=json.loads(patch or '{}')
            state=ReviewStore(root).save(snapshot,action=action,corrections=parsed,reviewed_fields=fields or [],reviewer=reviewer,
                                         reason=reason,source_confirmed='pdf' in (confirm or []),versions=versions(root),expected_revision=selection['revision'])
        except (ValueError,OSError,KeyError) as exc:
            return 'Chưa lưu: '+str(exc),no_update
        return f"Đã lưu phiên bản {state['revision']} — {state['status']}. OCR gốc giữ nguyên; các cặp phụ thuộc cần kiểm tra lại.",(refresh or 0)+1

    @app.callback(Output('analysis-records','data',allow_duplicate=True),
                  Input('human-review-refresh','data'),State('analysis-job','data'),prevent_initial_call=True)
    def refresh_table(refresh,job):
        from dashboard.components.presentation import display_rows
        result=result_loader(job,root)
        return display_rows(reviewed_result(result,root)) if result and result.get('status')=='completed' else no_update
