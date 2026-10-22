# 06. Công cụ và dependency

Phiên bản/license **quan sát từ metadata môi trường hiện tại**, không giả định từ
requirements range: [dependencies.json](reference/dependencies.json). Đây chưa là
SBOM đầy đủ mọi dependency bắc cầu hoặc ý kiến pháp lý. Không tự đặt LICENSE cho dự án.

| Công cụ | Vai trò và điểm gọi | Cài/cấu hình/đầu vào → ra | Mạng/giới hạn/lý do có căn cứ |
| --- | --- | --- | --- |
| Python 3.12 | Tất cả CLI và worker | requirements trong .venv; source → process | Windows đã kiểm thử, cross-platform chưa xác minh |
| Dash, dash-bootstrap-components | `app.py`, upload_analysis, workspace | pip; callbacks → layout/JSON/download | Không có auth/RBAC; chỉ bind local |
| pandas, Plotly | Archive dataframe/charts trong app | pip; DB rows → bảng/biểu đồ | Không tự suy ra mọi biểu đồ là dữ liệu extract được |
| Docling 2.135.0 | `docling_backend.create_converter` | pip; PDF page → native document/markdown/table cells | TableFormer accurate + cell matching; weights có thể tải, RAM chưa benchmark |
| pypdfium2 | Docling PDF backend | transitive package; PDF → layout pipeline | Profile đang chọn thay backend từng crash; không bảo đảm mọi native crash được chữa |
| PyMuPDF | Page count/render/text, fragment, PDF hash workflow | pip; PDF → page/text/pixmap | Installed metadata: AGPL/commercial; owner phải rà quyền trước phân phối |
| Tesseract | `source_v2._ocr_docling_page`, `ocr_profile` | Executable ngoài + vie/eng local; scan → searchable PDF | Profile scale 4, --psm 3, timeout subprocess 180s; không blind OSD rotation |
| RapidOCR ONNX | `create_converter` khi thiếu Tesseract/data | pip; scan → OCR | Không có số accuracy tiếng Việt; force full page trong profile |
| pdfplumber, pypdf | Có trong requirements/môi trường | pip; chưa tìm thấy import/gọi trực tiếp trong first-party code khảo sát | Không gán vai trò extraction/fallback chỉ từ tên dependency; không tự xóa vì có thể thuộc dependency/tooling bên ngoài |
| PyYAML | Parser/dictionary/rules config | pip; YAML → dict | Không có hot reload toàn hệ thống được bảo đảm; restart sau sửa |
| jsonschema | Capture/native/corporate gates | Draft202012Validator; JSON → errors | PASS cấu trúc không phải đúng số liệu |
| rapidfuzz | Legacy similarity và quality edit distance | text/labels → scores/CER/WER | Similarity không chứng minh hai chỉ tiêu tương đương |
| spaCy | `src/preprocessing/text.py`: blank vi/sentence splitting | pip; text → sentences, có fallback theo implementation | Không phải pretrained NER hoặc LLM |
| SQLite / sqlite3 | `src/database/db.py` và review store | Standard library; SQL/schema → local DB | SQLAlchemy có trong requirements nhưng chưa tìm thấy import/gọi trực tiếp first-party; không suy ra ORM/server DB |
| Gemini API | `gemini.GeminiClient.generate` | HTTPS standard library; PDF fragment + prompt/schema → model JSON | Consent/key riêng, cloud; request cap không phải USD cap; phí thật chưa đo |
| Ollama | `local_llm.OllamaClient` | Cài service/model ngoài; source text/cells → JSON riêng | Loopback only, `/api/tags` preflight, no pull/cloud alias; text-only |
| pytest | Regression/worker/fake API tests | pip; tests → JUnit/log | Không phải corpus benchmark |
| python-docx/Pillow | `scripts/build_user_manual.py` | Công cụ build DOCX/ảnh, không phải pipeline upload | Có trong máy hiện tại nhưng chưa khai báo trực tiếp manifest công cụ phụ |
| Node/Playwright/artifact-tool | verify_*.cjs / generator ngoài app | Phụ thuộc tooling ngoài, chưa npm manifest | Không bắt buộc cho Dash production; không bundle junction |

Lý do lựa chọn kiến trúc đọc được trong docstring/profile: bảo toàn source, worker
cô lập native crash, local Ollama cấm cloud, literal evidence để không làm giả
boundary. Lý do lịch sử/so sánh với mọi thư viện khác **chưa xác định** nếu không có
ADR; không viết như một quyết định thiết kế đã được đo benchmark.

## LLM: prompt, context và structured output

| Mục | Gemini | Ollama |
| --- | --- | --- |
| Model | `config/gemini.yml`, UI/CLI override; default ID do cấu hình, không tự lấy AI Studio UI | `config/local_llm.yml`, exact installed tag/digest |
| Prompt | `gemini.PROMPT`, `PROMPT_VERSION` | `local_llm.SYSTEM_PROMPT` và version/hash trong profile |
| Context | PDF primary page + context lân cận, mapping original physical page | `build_chunks`: text/cell spans, primary/context headers, character budget không phải tokenizer-exact |
| Parameters | 1 primary page, context 1 mặc định; 16.384 output tokens; timeout 180s; retry 0 | timeout 180s, retry 1, num_ctx 8192, num_predict 2048, temperature 0, seed 0 |
| Schema | responseJsonSchema + JSON validator + page/literal guards | format schema + schema/literal/source validators |
| JSON lỗi/cắt | Batch failed, issue, giữ response/checkpoint, không gọi là thành công | Chunk failed/retry, chưa complete nếu done_reason không stop |
| Usage/cost | usageMetadata lưu ở checkpoint; chưa có bộ tính USD/invoice đối soát | prompt_eval_count/eval_count/duration khi provider trả; chưa định lượng điện/RAM |
| Tái lập | Model/prompt/code/profile ghi nhận, không có guarantee deterministic | Seed/temperature không bảo đảm tuyệt đối qua model/runtime/hardware |

Gemini gửi PDF trang (cả context có thể chứa thông tin không cần cho một claim),
prompt và page mapping. Key chỉ ở HTTP header. Chỉ quote model không đủ chứng minh
PDF thật; `quote_check` là substring check, không phải đánh giá thị giác độc lập.
Không có cloud failover tự động. Hết RAM/disk hoặc đổi version có thể làm kết quả
khác; pinning không thay cho gold/PDF review.
