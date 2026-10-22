# 08. Hợp đồng JSON và data dictionary

Đã đọc code writers, runtime schemas, các output tổng hợp mới và native output BSR
được khảo sát trước. Không chọn một JSON làm mẫu chung cho mọi engine. Catalog
runtime ở [schemas](../schemas/README.md); bảng property/required/conditional đầy
đủ sinh trực tiếp từ schemas ở [schema-fields.md](reference/schema-fields.md).

## Các lớp hợp đồng, không tự coi là interchangeable

| Lớp | Version / writer | Cấu trúc chính | Required/khả năng dùng |
| --- | --- | --- | --- |
| Capture | `batch.schema_version=esg-source/2.0.0`; capture_pdf | batch/reports/artifacts/blocks/coverage/issues; records=[] | contracts/source_v2.schema.json; chưa semantics |
| BCTC native | esg-financial-candidates/2.3.0; extract_financial | metadata, records, links, notes/continuations, semantic_coverage, arithmetic/hierarchy | contracts/financial_v2.schema.json, parser hiện 6 |
| ESG/annual native | esg-candidates/2.1.0; extract_esg | reports, records, evidence, links, issues, coverage source_pages/blocks | contracts/esg_v2.schema.json, parser hiện 3 |
| Gemini | gemini-report-candidates/1.0; gemini.extract_pdf | model/profile/batches/usage, model source_blocks/records, pages | contracts/gemini_extract.schema.json; candidate only |
| Ollama | local-llm-extract/1.0; extract_local_llm | model/chunks/records/coverage | local_llm_extract.schema.json; adapter riêng chưa có |
| UI download | esg-upload/2.0.0; export_result | documents[].output + native_artifacts, failures | schema suy ra mới chỉ kiểm envelope, không đổi runtime |
| Corporate | corporate-extract-1.0; build_delivery | document/coverage/records/issue_log + manifest ngoài | corporate_extract_v1/schema.json; pending_human_review |

Giá trị required chính xác theo object cha/record_type trong schema, không giả định
mọi payload cùng shape. Schema hiện tại còn object ít ràng buộc/type chưa khai báo;
validator Python bổ sung source/hash/consistency nhưng không thành proof semantic.

## Dictionary nghiệp vụ cho các field quan trọng

Các ví dụ bên dưới là **minh họa**, không phải dữ liệu doanh nghiệp.

| Đường dẫn | Ý nghĩa | Kiểu / bắt buộc | Đơn vị | Nguồn | Quy tắc / ví dụ |
| --- | --- | --- | --- | --- | --- |
| `/reports/*/source_sha256` | Identity bytes PDF | string, capture required | SHA-256 | file_hash(source.pdf) | Không phải chứng nhận nguồn công bố chính thức |
| `/reports/*/reporting_year` | Năm người dùng/nhận diện cung cấp | int/null, tùy envelope | năm | UI/filename; metadata origin | Không dùng thay năm từng số đo; ví dụ 2025 |
| `/metadata/*/{value,status,sources}` | Metadata PDF candidate | object, tùy branch/schema | theo field | title/header/text | unknown/ambiguous không tự điền từ tên |
| `/source_artifacts/*/{artifact_id,path,sha256,kind}` | PDF/checkpoint ledger | object, required capture | hash | file trên disk | path relative workspace, chặn traversal/hash đổi |
| `/source_blocks/*/original_text` | Text của block | string/null | nguyên văn | native document | Table có thể null, xem original_cells |
| `/records/*/record_id` | ID versioned record | string, required | ID | stable_id(source/anchor/type/slot) | Không phải mã chỉ tiêu, đổi profile có thể đổi ID |
| `/records/*/record_type` | Vai trò record | enum theo schema | n/a | parser/keyword/LLM | metric/measurement/claim/policy/action/target/governance/context |
| `/records/*/original_text` | Nội dung nguyên bản parser giữ | string/null | raw | cell hoặc đoạn nguồn | BCTC measurement có thể chỉ “100”, không phải câu label+year+value |
| `/records/*/original_cells` | Các ô nguồn | array/null theo branch | raw cells | native table | Không tự tạo ô ghép cho giống câu tự nhiên |
| `/records/*/interpretation_notes` | Diễn giải riêng | array | n/a | parser/reviewer | Không dùng ghi đè original_text |
| `/records/*/field_sources/*/*` | Nguồn cho từng field | object refs | page/hash/pointer | native/checkpoint | Ví dụ pointer /document/tables/0/data/table_cells/3 |
| `.../pdf_page`, `printed_page` | Trang vật lý và số in | int/null | 1-based / theo nguồn | PDF + nhận diện | Hai hệ khác nhau; null nếu chưa biết |
| `.../bbox`, `native_provenance` | Tọa độ nếu có | object/array/null | theo backend | Docling prov | Xem coordinate origin/units của backend; không suy bbox khi không có |
| `/records/*/payload/item_code_raw` | Mã dòng tài chính | string/null | mã | cell code | “10” khác conceptual metric_id |
| `.../metric_record_id` | Link measurement→metric row | string | ID | parser | Không biến row ID thành tên metric chuẩn |
| `.../metric_id` | Khái niệm metric nếu có | string/null | vocabulary | local dictionary | local:*:v1 chưa phải GRI/SASB được chuyên gia duyệt |
| `.../raw_value` | Chuỗi số nguồn | string, measurement BCTC required | presentation unit | cell value | “(100)” giữ dấu ngoặc; không đổi blank thành 0 |
| `.../parsed_value` | Số parse chưa scale | decimal string/null | đơn vị trình bày | parse_number | “-100”, tránh float round-off |
| `.../unit`, `currency`, `scale` | Đơn vị, tiền tệ, hệ số | string/null | VND/USD, 1/1000/1e6/1e9 | header/table/row cụ thể | Triệu VND: scale=1000000; không suy VND cho headcount/shares |
| `.../normalized_value` | Số đã scale nếu đủ bằng chứng | native string/null | base unit | Decimal(parsed)*scale | Scale áp dụng một lần; Gemini native có thể chưa normalize |
| `/records/*/content_period` | Kỳ của observation | object/null | năm/ngày | header/date/rule | year/as_of_date/start_date/end_date/period_type; không đồng nhất với report_year |
| `.../column_headers_raw`, `period_role` | Header và vai trò cột | array/string/null | raw/current/comparative | đúng column | Comparative/opening có thể chưa xác định ISO date |
| `.../restatement_status` | Nhãn điều chỉnh/trình bày lại | string/null | n/a | explicit label | not_labelled không chứng minh không restate |
| `/records/*/boundary` | Included/excluded/consolidation | object, native required | pháp nhân/phương pháp | KPI source nếu có | null còn thiếu; materiality list không xác minh mọi KPI |
| `/records/*/field_status`, `missing_fields` | Trạng thái field và thiếu | object/array | JSON pointer | sync_missing_fields | Cập nhật cả boundary.missing_fields và list ngoài |
| `/records/*/review` | Candidate review state | object | n/a | parser/UI overlay | needs_review; verified_fields=[] trước duyệt |
| `/coverage`, `/issues`, `/pending` | Phạm vi xử lý/lỗi/tồn đọng | branch-specific | page/block/table | ledger/validators | processed ≠ all information extracted |
| `/validation/{valid,scope,errors}` | Mechanical gate | bool/string/array | n/a | schema + Python checks | valid=true không phải accuracy=true |
| `/graph_ready`, `/semantic_status` | Khả năng bàn giao ngữ nghĩa | false/partial hiện tại | n/a | code writer | Không ép true chỉ vì đủ trang |
| `/gemini_evidence/*/source/source_origin` | Observation của model | string | n/a | Gemini response | gemini_visual_observation, không Docling truth |
| `/model`, `/profile_id`, `/batches` | LLM provenance và checkpoint | object/string/array | version/token usage | request/response | Giữ requested vs returned version; không lưu key |
| Corporate `/records/*/value` | Raw + normalized + factor/status | object, required | original/base | adapter | normalized JSON number có exactness gate, khác native decimal string |
| Corporate `/records/*/period` | Observation/baseline/deadline/year_basis | object, required | ISO/year | source/rule | year_basis chỉ rõ căn cứ; unknown/null không phải thiếu báo cáo |
| Corporate `/records/*/evidence/*` | Quote/page/headers/locator | object, required | source | original artifact | exact_quote có thể là OCR/model observation, chưa tự xác minh PDF |
| Corporate `/records/*/quality` | Parser/model/prompt/uncertainty/review | object, required | n/a | adapter | pending_human_review, không tự tạo gold |
| `/human_review` hoặc notes/human_review.json | Overlay/event/corrections | xuất bổ sung theo UI | n/a | review_store | Không thay raw native; stale nếu nguồn/version đổi |

## Null, 0, empty, absent và normalize

- `null`: chưa có giá trị/căn cứ hoặc chưa parse được; xem field_status/issue.
  Không diễn giải thành 0, không công bố hoặc không áp dụng nếu chưa chứng minh.
- `0`: observation bằng zero có nguồn thật, không thay blank/dash bằng zero.
- `""`: chuỗi rỗng nếu source/writer cho phép; không luôn bằng null. Kiểm raw cell.
- Field không có: có thể khác branch/record type/phiên bản; xem schema, không tự
  thêm giá trị mặc định khi downstream chưa định nghĩa.
- Auto `1.234` có thể ambiguous; vi và en là lựa chọn người vận hành kiểm tra.
  Giữ âm/ngoặc/currency/scale và original header để truy nguyên. Đơn vị cường độ
  không được rút thành đơn vị tuyệt đối; normalize chỉ khi hỗ trợ.
- ISO ngày có thể do parser rule diễn giải từ header; giữ year_basis, period type,
  nguồn và notes. Gemini yêu cầu date evidence literal và xóa ngày suy ra không đủ
  nguồn. Không đồng nhất hành vi ngày của mọi engine.

## ESG và annual payload

ESG record có pillar/topic candidate, statement/name, subject/scope/negation và
target fields tùy loại. Định nghĩa chuẩn trong config chỉ là local taxonomy;
protocol SASB còn pending. Scope 2 location/market khác nhau, actual khác target,
training hours khác money payroll. Annual dùng cùng schema ESG; không có field
“all business strategy verified”. Nội dung lặp/mâu thuẫn giữa các section chưa có
gold/dedup toàn diện. Cần review ghép cặp riêng.

## Naming và nguồn

`download_filename` dùng company/type/year/scope quan sát được nếu available,
fallback metadata đầu vào, timestamp và token; Gemini thêm GEMINI. Tên không phải
bằng chứng metadata. Native workspace/hash layout và corporate ZIP là hai loại
khác nhau. Portable pointer resolve vào `native_artifacts[artifact_id]`; PDF tải
riêng. Không thể tạo handoff có PDF chỉ từ portable JSON không còn workspace.

Không tự sửa schema/output để hợp mẫu; schemas/ chỉ bổ sung envelope suy ra cho
kiểm tài liệu. Chưa có migration tự động giữa các schema/engine khác nhau.
