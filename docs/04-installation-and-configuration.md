# 04. Cài đặt và cấu hình

**ĐÃ XÁC MINH:** Windows, Python 3.12 64-bit trên môi trường hiện có. **CHƯA XÁC
MINH:** cài dependency mới hoàn toàn, Linux/macOS, RAM tối thiểu/GPU sizing. Không
đưa con số RAM tối thiểu từ suy đoán; Docling/model có thể dùng nhiều RAM và disk.

## Máy mới

Nhận gói source nội bộ đã được chủ dự án cho phép; kiểm SHA256SUMS trước giải nén.
Mở PowerShell tại thư mục chứa `app.py` (không phải parent Git root):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -B scripts/check_handover.py
.\.venv\Scripts\python.exe -B scripts/handover_smoke.py --destination outputs/first_smoke_moi
.\.venv\Scripts\python.exe app.py
```

Lệnh install cần mạng và có thể tải nhiều dependency. Không cần activate venv.
Mở http://127.0.0.1:8050; giữ terminal mở. Dừng Ctrl+C, chạy lại `python.exe app.py`,
Ctrl+F5 trên browser. Không xóa DB/history để “nạp lại”. App import có thể tạo/import
DB/demo nếu thiếu; không start nó trên DB thật chỉ để kiểm cài đặt.

Script tùy chọn: `scripts/setup_handover.ps1` mặc định chỉ preview; `-Install` từ
chối ghi đè `.venv` đang có. `scripts/run_handover.ps1 -CheckOnly` không start app;
bỏ cờ sẽ start app và giữ hành vi DB hiện tại. Không tự load `.env`.

## Constraints và phụ thuộc phụ

`docs/reference/dependency-constraints.txt` là bản pin version **đã quan sát**, không
phải lockfile có wheel/hash hoặc bảo đảm cài portable/offline. Có thể thử thêm
`-c docs/reference/dependency-constraints.txt` vào pip install trên máy Windows/
Python tương ứng. Fresh install chưa được kiểm thử; xem [verification](reference/verification.md).
Build manual cũ còn dùng python-docx/Pillow; Node QA cần Playwright; workbook cần
`@oai/artifact-tool`. Chúng không phải mọi dependency trực tiếp của runtime upload
và chưa có manifest cài độc lập đầy đủ cho Node. Không copy junction từ máy tác giả.

## Cấu hình ứng dụng

| Nguồn | Người dùng thay gì | Cách nạp / lưu ý |
| --- | --- | --- |
| `config/extraction_toolkit.yml` | Registry/filename rules | `build_document_spec`; input UI override, tên không xác minh scope |
| `config/metrics.yml`, `metric_dictionary.yml` | Vocabulary/đơn vị/exclusions | Parser/quality/corporate; sửa cần version và review lại |
| `config/esg_v2.yml` | Keyword taxonomy | `extract_esg`; provisional, không phải luật chuẩn đã chứng nhận |
| `config/gemini.yml` | API model ID/batch/timeout/retry | `gemini.settings`; không tự dò model mặc định AI Studio |
| `config/local_llm.yml` | Ollama model/loopback/context | CLI riêng, không tự pull |
| `GEMINI_API_KEY` hoặc `GOOGLE_API_KEY` | Key trên máy chủ | `gemini.api_key`; hai giá trị khác nhau bị từ chối |
| `TESSDATA_PREFIX` | OCR integration | Code scope/restore khi dùng chế độ tesseract_cli; không thay cấu hình PDF profile tùy tiện |
| `PYTHONIOENCODING` | Worker encoding | Worker đặt UTF-8; không phải secret |

`.env.example` chỉ là tài liệu biến môi trường, **không được app tự đọc**. Dùng key
mới không lộ trong chat/Git, nhập bằng PowerShell Read-Host như
[GEMINI_INTEGRATION](GEMINI_INTEGRATION.md). API của project có quota/billing riêng,
không mặc định miễn phí vì có gói Gemini Pro; không bật billing để sửa lỗi chưa rõ.

OCR Việt: cài Tesseract executable riêng; `scripts/setup_vietnamese_ocr.py` tải
vie/eng language data (cần mạng, không tự cài executable). Nếu không đủ Tesseract
và data local, profile chọn RapidOCR; không chứng minh tiếng Việt chính xác.
Docling weights có thể tải khi chạy lần đầu, chưa có bộ model offline được đóng gói.
