# 11. Triển khai và vận hành

**ĐÃ XÁC MINH:** ứng dụng local Windows, single Dash process + worker subprocess,
SQLite/disk local. **CHƯA XÁC MINH:** production multi-user, container, Windows
service, horizontal scaling, Linux/macOS. Không có auth/RBAC/TLS/multi-tenant storage
isolation được triển khai. Không đổi host sang 0.0.0.0 hoặc public reverse proxy chỉ
để demo khi chưa có thiết kế bảo mật.

`WORKER_SLOT` trong extraction_worker là semaphore **trong process**, không phải
distributed queue; nhiều server process có thể vượt ý định concurrency. Capture
có OS workspace lock; Docling legacy có CONVERSION_LOCK. Không mô tả chúng như
scheduler nhiều máy. UI đóng không bảo đảm worker bị hủy; chưa có cancel API hỗ trợ.

## Dữ liệu và secret

- `data/uploads/<batch>`: PDF nhận; `data/processed/extraction_jobs/<uuid>`:
  request/status/result/worker.log; request có base64 PDF.
- `data/processed/uploads_v2/<run>`: run_manifest; Gemini có immutable snapshot
  riêng. `capture_v2`, `gemini_v1`, source_v2/local_llm tùy UI/CLI/profile.
- `data/processed/human_review/reviews.sqlite3` khi review được dùng: overlay/event
  riêng; không nằm trong DB archive.
- `database/esg_tracker.db`: archive SQLite; `data/models` và model cache hệ thống
  khác không tự đi kèm source package.
- API key nằm trong môi trường terminal khởi chạy app/worker, không trong UI/job
  JSON. Đổi terminal có thể mất key. `.env.example` không tự load.

## Backup, update và rollback

Trước update: dừng đúng app/worker, bảo đảm không có SQLite writer; sao lưu cả
data/processed, uploads, review DB, archive DB và các source artifacts mà history
trỏ tới. Copy SQLite đang ghi không được bảo đảm nhất quán; dùng SQLite backup
API hoặc dừng writer có kiểm chứng. Chưa có nút backup tích hợp.

Giữ code/config/version và environment manifest cùng backup; schema/ID/profile
thay đổi có thể làm review stale. Update source trên bản sao rồi chạy tests/smoke,
không ghi đè runtime directories. Rollback code **và** config/DB snapshot tương ứng;
không hứa schema tự downgrade. Helper import_data/run_pipeline có thể thay DB:
không dùng chúng như lệnh reload web.

History/checkpoint mất file hoặc hash đổi sẽ bị từ chối; không “sửa hash cho khớp”
để qua gate. Resume cùng PDF/metadata/profile; Docling retry pages failed/partial,
Gemini cap mới có thể phát sinh thêm phí. Profile version thay → xử lý mới.

## Log/giám sát và retention

Theo dõi status/error/coverage/issue, worker exit hex, API usageMetadata và disk
free. Chưa có Prometheus/alert/budget USD hay log redaction toàn hệ thống. Lỗi API
HTTP hiện bị giữ thông báo chung, chưa chi tiết Google an toàn. Không bật debug
public hoặc gửi log/request nguyên bản lên chat. Timeout/cost control xem chương 06.

Không có retention scheduler tự động. **ĐỀ XUẤT** policy theo quyền khách hàng:
giữ source + artifacts + review + manifest đủ để tái lập; dọn cache có inventory/
quarantine như CLEANUP_REPORT tại Git root. Không xóa cả outputs/tmp/data theo tên.
Độ nghẽn chính có căn cứ là Docling memory/latency theo trang và Gemini request cap;
throughput/RAM/cost thật chưa benchmark trong đợt này.
