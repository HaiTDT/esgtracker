# Ví dụ tổng hợp — không phải dữ liệu doanh nghiệp, không phải gold

Các JSON ở đây do `scripts/handover_smoke.py` tạo bằng **parser thật và page reader
giả lập**. Mã doanh nghiệp `SYNTH`, số 100/90 và câu chính sách là fixture do dự án
tạo để kiểm tra cấu trúc. Không dùng chúng để đo OCR, LLM hay accuracy của BSR.
Không có PDF báo cáo thật trong thư mục này.

- `example_financial_statements.json`: native financial, không phải corporate handoff.
- `example_ESG.json`: native ESG.
- `example_annual_report.json`: annual được xử lý bởi nhánh ESG hiện tại.
- `example_upload.json`: envelope portable với ba tài liệu, source checkpoints giả lập.
- `example_corporate_financial.json`: adapter corporate từ fixture BCTC, vẫn pending_human_review.

Các quote/pointer/hash trong ví dụ là của fixture tương ứng. PDF fixture và local
workspace không được bundle vào đây, nên kiểm schema được nhưng không kiểm bytes
PDF hoặc tạo ZIP corporate chỉ từ các JSON này. Chạy smoke với thư mục đích mới
để tái tạo cả workspace khi cần. Các timestamp/ID có thể khác giữa các lần chạy.

```powershell
.\.venv\Scripts\python.exe scripts/handover_smoke.py --destination outputs/synthetic_smoke_moi
```
