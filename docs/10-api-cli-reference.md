# 10. UI, HTTP và CLI thực tế

Chạy các lệnh từ thư mục chứa `app.py`, dùng đường dẫn file thật. Ví dụ Windows
PowerShell đều viết một dòng, không dùng backtick của PowerShell trong CMD.
`--help` kiểm cú pháp, không chứng minh dữ liệu chạy thành công.

## UI/HTTP

Dash callbacks là giao diện upload/job chính. Chưa có API REST extract công khai
được version/auth hỗ trợ. Route `GET /extract-source/<job_id>/<int:document_index>`
ở `upload_analysis.register_upload_callbacks` trả PDF sau kiểm local artifact/hash;
UUID là capability, không phải RBAC. Không xây consumer phụ thuộc internal Dash
callback POST như một API được hỗ trợ. Gemini generateContent là outgoing provider,
không phải API do ESG Tracker phục vụ.

## Lệnh chính

| Script / symbol | Đầu vào / lựa chọn | Đầu ra / exit code | Lưu ý |
| --- | --- | --- | --- |
| `extract_source_v2.py:main` | PDF, --company, --report-type, --report-year, --start-page, --max-pages, --retries | workspace canonical; 0 complete capture, 2 partial, 1 exception | Chỉ capture, chưa records semantic |
| `extract_financial_v2.py:main` | Workspace canonical; --number-format auto/vi/en | financial JSON, counts; 0/1 | Không chạy OCR lại |
| `extract_esg_v2.py:main` | Workspace ESG/annual; --config, --number-format | esg_records.json; 0/1 | Annual không financial parser |
| `extract_gemini.py:main` | PDF --company --year --type --model --max-requests --allow-cloud | native Gemini path/coverage; 0 có thể partial, 2 config ValueError | --check-config chỉ presence, 0/1; không thử key thật |
| `extract_local_llm.py:main` | canonical, --model --base-url --max-chunks/--max-pages | local LLM JSON; 2 review-only bình thường, 1 failed | --check gọi Ollama local preflight; không generation |
| `extract_corpus.py:main` | PDF/thư mục; --dry-run --registered-only --engine | Inventory/run legacy JSON | CLI cũ, default engine legacy; không đồng nhất UI v2 |
| `export_corporate_handoff.py:main` | --saved-id hoặc --result (workspace thật) hoặc --bsr-history; --destination mới --zip | Delivery schema/manifest/notes/validation | Portable JSON không có workspace bị từ chối |
| `quality_benchmark.py` | dictionary/template/evaluate/check | review/gold draft/quality JSON | Xem --help từng subcommand, không tự phê gold |
| `oil_gas_gold.py` | build/verify theo help | codebook/drafts/gates | Standards không cấp giá trị đúng cho công ty |
| `handover_smoke.py:run` | --destination thư mục mới | 3 synthetic native + upload + smoke report | Không OCR/model; 0 hoặc exception |
| `check_handover.py:check` | Không input | links/evidence/example schema report; 0/1 | Không start app/gọi mạng |
| `handover_reference.py:run` | --destination optional | index/dictionary/dependency metadata | Sinh lại từ môi trường hiện tại, không tự sửa runtime |
| `package_handover.py:package` | --version --destination mới ngoài app; --dry-run optional | Review ZIP/manifest/SHA256; 0/1 | Không phải public release, không cài/upload/deploy |

## Ví dụ thật cần PDF và OCR/model đã sẵn sàng

```powershell
.\.venv\Scripts\python.exe scripts/extract_source_v2.py "C:\bao-cao-thuc\BCTC_BSR_2024.pdf" --company BSR --report-type financial_statements --report-year 2024 --max-pages 1
.\.venv\Scripts\python.exe scripts/extract_financial_v2.py "C:\workspace-tra-ve" --number-format vi
.\.venv\Scripts\python.exe scripts/extract_source_v2.py "C:\bao-cao-thuc\ESG_BSR_2025.pdf" --company BSR --report-type ESG --report-year 2025 --max-pages 1
.\.venv\Scripts\python.exe scripts/extract_esg_v2.py "C:\workspace-tra-ve"
.\.venv\Scripts\python.exe scripts/extract_source_v2.py "C:\bao-cao-thuc\BCTN_BSR_2025.pdf" --company BSR --report-type annual_report --report-year 2025 --max-pages 1
.\.venv\Scripts\python.exe scripts/extract_corpus.py "C:\bao-cao-thuc" --dry-run
.\.venv\Scripts\python.exe scripts/export_corporate_handoff.py --saved-id JOB_UUID --destination outputs/delivery_moi --zip
```

Các placeholder không phải file đi kèm. Chỉ bỏ --max-pages khi đã cho phép đọc toàn
report. Batch UI chạy v2; batch corpus CLI cũ có schema/behavior khác. Các script
BSR-specific như build_bsr_ai_reference/finish_bsr_esg_with_native_fallback không
được coi là lệnh generic an toàn cho mọi công ty.

Validator corporate là `delivery/validation/validate.py --manifest ... --pdf-dir ...`.
`audit_corporate_handoff.py DELIVERY --pending-only` có thể ghi validation report
vào delivery; sao lưu gói bất biến trước dùng nếu muốn giữ báo cáo kiểm tra trước.
