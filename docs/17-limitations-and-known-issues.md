# 17. Giới hạn và vấn đề đang mở

| Vấn đề | Trạng thái / bằng chứng | Ảnh hưởng và hướng xử lý |
| --- | --- | --- |
| Gemini HTTP 400 trong lượt thật trước đó | CHƯA GIẢI QUYẾT; screenshot người dùng, client bỏ error body | Không kết luận quota/billing; cần safe diagnostics và acceptance có ngân sách |
| Chưa có gold đã được người dùng duyệt | ĐÃ XÁC MINH evaluator/templates/reference flags | Không công bố precision/recall/accuracy corpus; gán nhãn độc lập |
| Annual route ESG | ĐÃ XÁC MINH upload_v2/extract_esg | Không phải extract mọi finance/business/governance field; cần parser/ontology bổ sung |
| Scan/chart/cross-page còn thiếu | ĐÃ XÁC MINH pending/coverage trong outputs | Không dùng page processed = đầy đủ; review source và add missing gold |
| Generic boundary chưa xác minh | ĐÃ XÁC MINH new_record/missing_fields/adapter | Giữ null, không lấy từ BCTC/general materiality |
| Local LLM text-only/CLI | ĐÃ XÁC MINH local_llm, README | Chưa vision/UI/corporate integration; không tự thay model download |
| Corporate contract domain limitations | ĐÃ XÁC MINH gemini_handoff và corporate adapter | Một số record mixed không biểu diễn, giữ native+issue; không khẳng định lossless mọi engine |
| Legacy archive vs corporate review khác gates | ĐÃ XÁC MINH matching/evidence và corporate_review | Không gọi toàn bộ matching là đã chứng minh comparability |
| Metadata/financial period có rule inference | ĐÃ XÁC MINH financial_semantics | Giữ raw/source/year_basis; không nói mọi ngày ISO là literal |
| Human reviewer tự khai báo | ĐÃ XÁC MINH UI/review_store | Không authenticated adjudication; reviewed không thành gold tự động |
| Auth/retention/backup/cancel/distributed queue | CHƯA có cơ chế đầy đủ trong app | Chỉ local trusted operator; deployment cần thiết kế riêng |
| Fresh install / offline OCR weights | CHƯA XÁC MINH trong đợt này | Existing environment PASS không bảo đảm máy mới chạy được |
| LICENSE dự án/PyMuPDF/model rights | CHƯA XÁC MINH pháp lý; metadata đã đọc | Review ZIP không phải public/customer release |
| DB/Phase1/output ngoài app | ĐÃ XÁC MINH paths/importer | Source-only package không kèm lịch sử/corpus; app có demo/fallback, test corpus có thể skip |
| Git root/nested gitlink và publication copy | ĐÃ XÁC MINH cleanup report | Không zip/push cả workspace; owner chốt version/source-of-truth |
| Dependency tooling phụ | ĐÃ XÁC MINH imports Node/docx/Pillow | Chưa npm/setup manifest đầy đủ cho workbook/browser QA/manual build |
| Dash DataTable deprecated | Cảnh báo tests, chưa bị lỗi hiện tại | Kế hoạch migrate UI riêng, không đổi thư viện trong handover |

Không sửa nghiệp vụ để che các giới hạn. Các ghi chú `review_ui`/`graph_adapter`
trong một số native pending list phản ánh lịch sử parser, không là inventory khả
năng toàn ứng dụng: review UI/corporate adapter hiện có, nhưng không áp dụng mọi
schema/backend. Khi xung đột, đối chiếu symbol/route/version và test scope.
