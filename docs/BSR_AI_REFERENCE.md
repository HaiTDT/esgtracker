# AI-assisted PDF reference

`scripts/prepare_ai_reference_pages.py` tạo ảnh từ PDF nguyên gốc theo mẫu BSR
đã chọn. Nó không tự kiểm tra nội dung ảnh hoặc tạo gold.

`config/ai_reference_bsr_20261021.yml` lưu các bản chép do AI thực hiện sau khi
xem trang PDF. Không sinh giá trị tham chiếu từ predictions.

`scripts/build_bsr_ai_reference.py --destination <thư-mục-mới>` đóng gói các bản
chép, liên kết record_id/JSON pointer cũ bằng metadata hàng/cột, ghi đề xuất
thay đổi chưa áp dụng, ảnh nguồn, độ phủ và danh sách chưa rà.

Đây là workflow **BSR cố định**, không phải một model tự động gán nhãn chuẩn cho
mọi doanh nghiệp. Muốn thêm tài liệu phải render, xem trực tiếp, biên soạn seed
và kiểm tra bằng chứng; không chỉ đổi tên công ty trong config.

Trạng thái bắt buộc: AI_reviewed_pending_human_review, is_gold=false,
review_status=pending_human_review. Không có bước tự phê duyệt; evaluator human
gold từ chối schema này. Không chép sidecar vào bản nhãn độc lập trước khi hai
người gán nhãn đã làm vòng đầu, để tránh rò đáp án/gợi ý.

Null là chưa xác định; cả boundary.missing_fields và missing_fields bên ngoài
được tính lại theo field thực tế. Phạm vi nguồn/giá trị chưa đủ để khẳng định
entity list hoặc consolidation method đã xác minh. Không sửa PDF/corporate JSON.

Gói hiện có: `outputs/BSR_AI_reference_20261021/START_HERE.md`.
