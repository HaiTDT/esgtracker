# 05. Hướng dẫn người sử dụng

## Bắt đầu không dùng tài liệu thật

Chạy quickstart offline trong [cài đặt](04-installation-and-configuration.md).
Kết quả gồm `example_financial_statements.json`, `example_ESG.json`,
`example_annual_report.json`, `example_upload.json` và `smoke_report.json`.
Nguồn được giả lập; PASS không chứng minh OCR hoạt động. Xem thêm
[ví dụ tổng hợp](../examples/README.md).

## Chạy báo cáo thật trên UI

1. Vào **Tải báo cáo / Extract**, kéo thả PDF. Tối đa 20 file/lượt, 100 MB/file,
   250 MB/lượt. Không yêu cầu chép PDF vào thư mục cố định.
2. Kiểm tra mã doanh nghiệp, năm, loại báo cáo. Tên gợi ý: `BCTC_BSR_2024.pdf`,
   `ESG_PLX_2025.pdf`, `BCTN_BSR_2025.pdf`. Tên có ngày ở đầu có thể nhận diện;
   khi chưa chắc hãy override. Không coi tên là bằng chứng riêng/hợp nhất/kỳ KPI.
3. Chọn quy ước số. Auto có thể giữ `1.594` ambiguous; chỉ chọn vi/en sau khi xem
   dấu phân cách trong nguồn. Sai locale có thể làm sai 1.000 lần.
4. Giữ Docling local cho luồng mặc định. Chỉ chọn Gemini khi được phép gửi PDF
   lên Google, đã có key/quota, tick consent và đặt request cap nhỏ để thử.
5. Bấm trích xuất, theo dõi trang/coverage. UI còn hoạt động không có nghĩa worker
   chưa lỗi. “Kết thúc” không có nghĩa đã đọc hết mọi nội dung.
6. Chọn record, xem nguyên văn, field sources, PDF đúng trang vật lý. So đúng
   hàng, cột năm, đơn vị/scale, kỳ và pháp nhân. Màu xanh không phải xác minh.
7. Trong phần review, nhập reviewer/lý do, chọn field đã kiểm và xác nhận đã đối
   chiếu PDF. Sửa tạo overlay; PDF/native JSON không bị thay. Reviewer tự khai báo.
8. Download native JSON hoặc ZIP corporate. Nếu corporate bị chặn scope/schema,
   giữ native và xem blocked_documents; không ép chuyển bằng giả định.

## Mở lại và tiếp tục

History → Làm mới → chọn kết quả → Mở. Việc mở không chạy OCR lại. Muốn tiếp tục
trang pending/failed: tải lại đúng PDF, giữ metadata/engine/profile. Gemini cần
consent mới, request cap mới; các request thất bại vẫn có thể có chi phí. Cache
khác model/config có thể không dùng lại. Các snapshot Gemini từng lượt không bị
resume ghi đè. Không xóa `.writer.lock`/OS guard khi chưa rõ owner.

PDF nguồn có nút tải riêng; portable upload JSON không nhúng PDF. ZIP corporate
cần local workspace còn nguyên và hash khớp. Không dùng bản JSON sửa tay để tạo
“nguồn gốc đã xác minh”. Review và correction cũng không tự cập nhật score hoặc
mọi cặp downstream; kiểm dependency invalidations trước dùng kết quả.

Dashboard lưu trữ là luồng khác; upload không tự nạp vào đó. Lệnh import có thể
thay DB; xem [vận hành](11-deployment-and-operations.md) trước chạy.
