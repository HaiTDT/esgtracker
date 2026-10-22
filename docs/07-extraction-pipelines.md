# 07. Pipeline thực tế và điều kiện chuyển bước

## Nhánh UI chung

| Bước | Hàm/module | Vào → ra / cấu hình | Lỗi và phản hồi | Kiểm riêng |
| --- | --- | --- | --- | --- |
| Nhận file | upload_analysis.start | contents/names/metadata → UUID/thread | Thiếu PDF/consent/key: báo trước chạy | test_upload_v2, test_gemini |
| Validate batch | upload_v2.process_upload_v2 | extension, PDF magic, base64, path/name, size, year | Batch input sai: chưa ghi file; không phải kiểm an toàn nội dung PDF hoàn chỉnh | test_invalid_batch_has_no_writes |
| Nhận diện | toolkit.build_document_spec/infer_* | filename/folders/config + override → company/year/type | Fallback type có thể ESG; metadata origin user/filename, chưa xác minh PDF | test_extraction_toolkit |
| Persist/request | extraction_worker.run_isolated_upload | request.json + subprocess/status → result.json | Native crash có exit hex/recoverable, UI không chết theo | test_extraction_worker |
| Source local | source_v2.capture_pdf | PDF immutable/hash/profile → source.pdf/pages/canonical | Retry per page, deadline/partial/failed, coverage cả trang pending | test_source_v2 |
| Semantics | financial_v2 hoặc esg_v2 | Canonical/hash/config → typed records/issues/links | Schema/source invalid: giữ lỗi/không tự duyệt | tests parser |
| Lưu lịch sử | upload_v2 + extraction_history | Output path/run_manifest + result → reopen | Missing/tampered path/hash: từ chối hoặc báo không có | test_extraction_history |
| Export | export_result/build_delivery | Source refs + local PDF → portable JSON / corporate ZIP | Thiếu scope/unsafe/hash/schema: blocked document | test_corporate_handoff |

`source_v2.default_profile` ghi package/backend/OCR hashes. Source capture có
`batch.semantic_status=not_started`, records rỗng: không phải tool lỗi nếu chỉ mới
chạy CLI capture. Profile thay đổi tạo workspace khác; record ID ổn định trong
cùng nguồn/profile/segmentation, không bảo đảm qua mọi phiên bản.

## BCTC

`extract_financial` dùng table cells và text context, rồi `financial_semantics_v3.augment`.
`financial_column_mapping` xử lý cột mã, row label, cụm số tách/gộp; candidates vẫn
cần đối chiếu. Metadata tìm tiêu đề, currency, audit/year/scope khi có bằng chứng.
Riêng/hợp nhất không được kết luận chỉ từ tên upload.

Các bảng cân đối, kết quả kinh doanh, lưu chuyển và notes có phân loại context
trong `table_class`/notes parser. Không tuyên bố parse đủ mọi mẫu trực tiếp/gián
tiếp hay every note. Numeric row có thể tạo metric + nhiều measurement theo cột
năm. Mã dòng là `item_code_raw`, khác `metric_id` khái niệm. Scope statement-level
khác entity/population boundary của KPI.

Đơn vị table header (VND/nghìn/triệu/tỷ) có thể được dùng có nguồn; row currency/
shares có quy tắc cụ thể hơn. `parse_number` giữ blank/dash missing, ngoặc âm,
auto ambiguous; Decimal normalization tránh làm tròn nhị phân. Period role và
date mapping có thể là **rule-derived**: xem raw header/source và year_basis,
không gọi mọi ngày ISO là nguyên văn PDF. Restatement labelled khác đã xác minh.

Table continuations là rule_matched/rejected có reasons; không merge mọi bảng kế
nhau. Arithmetic chỉ chạy khi cùng code/period/unit/scope với nguồn đủ. Một số
notes/context vẫn pending và metadata có thể unknown. Xem pending/semantic_coverage.

## ESG/PTBV

`extract_esg` theo body reading order/section context; mất thứ tự thì không tùy tiện
thừa kế heading. `build_candidates` phân nhóm claim, policy, action, target,
governance theo keyword; có negation cue và issue nhưng chưa adjudicate ý nghĩa.
`extract_esg_table` tạo metric/measurement theo header/cells/đơn vị và taxonomy.
Metric config hiện có GHG Scope 1/2, energy/water/waste/headcount nếu nguồn/rule
khớp. Scope 3 có thể khớp **topic text** E_CLIMATE (`scope [123]`), nhưng chưa có
GHG_SCOPE_3 định lượng riêng trong metrics.yml; không gọi topic match là đã extract
đủ Scope 3 inventory/category/method. Không có guarantee mọi disclosure của chuẩn.

Actual measurement khác target/baseline/deadline. `payload` khác theo record_type;
không dùng câu cam kết làm achieved value. Bảng/ảnh/charts chưa parse vẫn ở
coverage pending. Boundary KPI không lấy mặc định từ materiality chung hoặc BCTC.

## Thường niên

ĐÃ XÁC MINH `report_type=annual_report` được nhận diện và **đưa vào ESG branch**.
Có thể thu được E/S/G text/table, governance/policy/action/target khi rule nhận;
chưa có unified annual ontology cho mọi hoạt động, chiến lược, rủi ro hoặc hợp nhất
phần tài chính lặp lại. Không có dedup/cross-section contradiction adjudication
toàn diện. ID trùng bị kiểm trong một output không có nghĩa đã dedup mọi phát biểu.
Muốn financial typed output hãy cấp BCTC phù hợp, không đổi JSON type bằng tay.

## Gemini và Ollama

Gemini bỏ qua capture Docling, gửi PDF fragment trực tiếp, lưu model observations
cùng quote/page và source_origin rõ. Budget chung cả batch upload; kết quả partial
cũng lưu. Corporate adapter có giới hạn domain, ghi issue phần không biểu diễn,
native vẫn giữ. Ollama chỉ đọc source text/cell đã capture, không đọc ảnh/vision và
chưa nối UI/corporate adapter. Không gọi hai nhánh này là OCR ground truth.
