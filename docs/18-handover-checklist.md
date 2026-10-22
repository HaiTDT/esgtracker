# 18. Checklist bàn giao

## Đã thực hiện trong phạm vi kỹ thuật

- [x] Xác định app.py, UI/worker/CLI, local/cloud và side-effect DB.
- [x] Inventory module/symbol/import, schema fields và dependencies quan sát.
- [x] Tài liệu hóa ba report types đúng route hiện tại, không giả annual full parser.
- [x] Giữ code/thuật toán/schema runtime, raw PDF/data/DB và lịch sử cũ.
- [x] Quickstart/offline fixture samples tách khỏi gold/report thật.
- [x] Script packaging source-only, checksum/manifest và heuristic secret checks.
- [x] .env.example không secret và chỉ rõ không auto-load.
- [x] Ghi test scope/PASS/FAIL/BLOCKED và evidence, không công bố accuracy chưa đo.

Kết quả thực thi cuối cùng và giới hạn: [verification](reference/verification.md).

## Cần chủ dự án ký xác nhận trước release

- [ ] Chủ sở hữu/code license và phạm vi chia sẻ nội bộ/khách hàng/công khai.
- [ ] Điều kiện PyMuPDF AGPL/commercial, các dependency/model/standard rights.
- [ ] Config/test reference excerpts và dữ liệu báo cáo được phép phân phối gì.
- [ ] Chọn Git source-of-truth; giải quyết output gitlink/copy repository, tag/version.
- [ ] Máy đích, network/offline, OS, storage/backup, auth/privacy và reviewer roles.
- [ ] Ngân sách và consent cho API thật; model API được cấp quyền, quota/retention.
- [ ] Acceptance trên PDF thật có phạm vi/coverage/expected values đã duyệt.
- [ ] Gold độc lập, đối chiếu PDF, adjudication và benchmark theo engine/type/field.
- [ ] Cài máy sạch và model cache/offline; acceptance rollback/restore.
- [ ] SLA/concurrency/cost/retention nếu cần server nhiều người dùng.

Không đánh dấu hoàn tất bằng PASS schema/tests. Không tự publish, bật billing,
chuyển dữ liệu thật sang cloud hoặc cấp giấy phép khi chưa có quyết định.

## Hướng dẫn người nhận

1. Đọc README → documentation index → install.
2. Verify checksum ZIP, giải nén vào thư mục mới, không chép đè runtime data.
3. Chạy check_handover/offline smoke rồi cài/kiểm Docling OCR theo quyền.
4. Chạy một PDF được phép, đọc coverage/issues, đối chiếu vài record với PDF.
5. Tập lưu review/correction và mở history, export native/corporate có nguồn.
6. Thử backup/restore trên workspace riêng trước update môi trường thật.
7. Chốt các checkbox chưa hoàn tất bằng bằng chứng, không lời cam kết chung.
