# 01. Tổng quan và phạm vi thực tế

ESG Tracker hỗ trợ người phân tích lấy dữ liệu ứng viên từ PDF BCTC, ESG/PTBV và
báo cáo thường niên, giữ nguyên văn, trang, hash/pointer để rà soát và xuất JSON.
Oil & Gas là demo/dictionary tham chiếu, không giới hạn mọi upload vào BSR.

**ĐÃ XÁC MINH trong code:** UI Dash tiếng Việt, upload PDF, worker riêng, tiến độ,
history local, source PDF, record/field review và correction overlay; Docling local;
Gemini API opt-in; Ollama text-only qua CLI; native JSON và corporate handoff;
schema/hash/source checks, quality evaluator và codebook gán nhãn nháp.

**CHƯA XÁC MINH / không cam kết:** trích xuất hết mọi field, accuracy của corpus,
toàn bộ biểu đồ/bảng nối trang, deployment đa người dùng, quy mô doanh nghiệp,
API thật chạy thành công, luật/quyền phân phối đã được duyệt. Không kiểm toán,
không kết luận buộc tội greenwashing, không tự tạo gold.

## Hai không gian dữ liệu khác nhau

1. Upload/Extract lưu local checkpoints và records để người dùng xem, sửa overlay,
   xuất JSON. `dashboard/upload_v2.py:process_upload_v2` không tự import DB hay chấm điểm.
2. Dashboard lưu trữ dùng SQLite, nguồn import riêng và legacy matching/rules/scoring.
   `app.py:ensure_ready`, `scripts/import_data.py`, `scripts/run_pipeline.py` có
   thể tạo/import/đổi DB. Không chạy lệnh import để “nạp lại UI” khi chưa sao lưu.

Legacy matching không có cùng mọi gate boundary như corporate review. Ví dụ
`src/matching/evidence.py:check_comparability` có một số điều kiện cho phép scope/
boundary thiếu; không mô tả toàn hệ thống có cùng một chuẩn so sánh chặt.

## Người dùng và sản phẩm đầu ra

Analyst kiểm tra field trên PDF; reviewer lưu quyết định; kỹ sư kiểm parser,
coverage, issue và hợp đồng. Native records là candidate. Corporate record vẫn
`pending_human_review`; `PASS files=...` chỉ là điều kiện cơ học. Quyết định đã
review trên UI là khai báo của người dùng, không phải assurance độc lập.

Annual report hiện đi qua ESG parser (`upload_v2.py`), không có cam kết bóc mọi
section doanh nghiệp/chiến lược/rủi ro và tài chính thành một ontology hoàn chỉnh.
Xem [pipeline](07-extraction-pipelines.md) và [giới hạn](17-limitations-and-known-issues.md).
