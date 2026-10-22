# Gemini tự động trong ESG Tracker

Gemini là engine **tùy chọn**, bên cạnh Docling hiện có. Khi chọn Gemini, ứng dụng
gửi từng mảnh PDF trực tiếp đến Gemini API để tạo candidate BCTC/ESG: số liệu,
claim, policy, action, target, governance và ngữ cảnh tài chính. Không phải OCR
local, không phải công cụ kiểm toán hay chứng nhận báo cáo đã trích xuất đầy đủ.

## 1. Cấu hình và chạy

Cần API key cho Gemini API. Đăng ký Gemini/Google AI Pro không thay thế cấu hình
API key và quota/billing của API project. Kiểm tra quyền sử dụng, dữ liệu nhạy cảm
và chính sách lưu trữ/xử lý dữ liệu của Google trước khi gửi báo cáo.
Không gửi key vào chat, không đặt key trong PDF, JSON, Git hoặc trình duyệt.

Trong **PowerShell** ở thư mục `esg-tracker`, nhập key bằng hộp nhập ẩn:

```powershell
$geminiSecret = Read-Host "Gemini API key" -AsSecureString
$env:GEMINI_API_KEY = [System.Net.NetworkCredential]::new('', $geminiSecret).Password
Remove-Variable geminiSecret
.\.venv\Scripts\python.exe scripts\extract_gemini.py --check-config
.\.venv\Scripts\python.exe app.py
```

`--check-config` chỉ kiểm tra cấu hình/key hiện diện, **không gọi Google** và không
chứng minh key/model/quota đã hoạt động. Key nằm trong môi trường của PowerShell
và tiến trình con; đóng terminal hoặc `Remove-Item Env:GEMINI_API_KEY` để bỏ khỏi
terminal. Nếu app đã chạy, Ctrl+C trong đúng terminal chạy app, đặt biến rồi chạy
lại. Không tắt tất cả tiến trình Python.

Mặc định `config/gemini.yml`: `gemini-3.8-flash`, một trang chính/request, thêm tối
đa một trang trước/sau làm ngữ cảnh; không tự chuyển model nếu API từ chối.
Tên hiển thị trong AI Studio không đủ để chứng minh API project có quyền dùng
model ID đó. Có thể nhập API model ID khác trong form, trong phạm vi Gemini.
Không cần cài thêm Google SDK: transport dùng HTTPS từ thư viện Python chuẩn.

## 2. Chạy trên giao diện

1. Mở `http://127.0.0.1:8050`, vào màn hình tải/trích xuất báo cáo.
2. Kéo thả PDF; kiểm tra doanh nghiệp, năm, loại báo cáo và quy ước số.
3. Chọn **Gemini API** trong lựa chọn engine.
4. Kiểm tra model, đặt giới hạn request và tick xác nhận gửi PDF lên Google.
5. Bấm trích xuất. Theo dõi số request và trang đã xử lý.
6. Chọn record, mở PDF đúng trang, đối chiếu hàng/cột/đơn vị/kỳ/phạm vi.
7. Tải JSON hoặc ZIP corporate; dùng lịch sử để mở lại kết quả không gọi lại API.

Mặc định giới hạn **10 request cho toàn bộ lượt upload**, không phải mỗi file.
Đây không phải giới hạn tiền/token; mỗi request còn chứa trang ngữ cảnh và có thể
phát sinh chi phí kể cả khi timeout/lỗi hoặc JSON không hợp lệ. Retry mặc định 0;
nếu cấu hình retry, mỗi lần thử đều tính vào giới hạn. HTTP 400/401/403/404/429 dừng
gửi các batch tiếp theo trong lượt chạy; hệ thống không tự bật billing.

Để tiếp tục, tải lại đúng PDF, giữ engine/model/metadata/quy ước số/cấu hình và
xác nhận mới. Batch thành công được dùng lại; batch lỗi hoặc chưa chạy có thể gọi
API trong giới hạn lượt mới. Thay model/cấu hình/prompt/code sẽ tạo profile khác,
có thể phải chạy lại và tốn phí. Giới hạn request không phải quota trọn đời.
Lịch sử upload được lưu snapshot riêng, không bị ghi đè khi cache tiếp tục chạy.

## 3. Đọc kết quả

- Envelope tải về vẫn là `esg-upload/2.0.0`; pipeline là `gemini-pdf-v1`.
  Mỗi `documents[].output` là `gemini-report-candidates/1.0`.
- `coverage.pages`: `processed` = model đã trả phản hồi hoàn tất cho trang;
  `pending` = chưa gửi (ví dụ hết request); `failed` = lỗi hoặc không đọc được.
  `processed` **không** chứng minh mọi ô/đoạn đã được nhận diện.
- `model.requested` và `observed_versions` giữ tên model yêu cầu/trả về.
- `source_artifacts`: PDF gốc cùng hash và JSON batch; pointer trỏ đúng quote của
  phản hồi model. Không tạo bbox/hàng/cột giả khi chưa có tọa độ thực.
- `source_origin: gemini_visual_observation`: lời đọc của model. `quote_check`
  là `matched_native_pdf_text` nếu khớp chuỗi text có sẵn hoặc `visual_unverified`
  nếu chưa khớp; cả hai **không** xác minh quan hệ đúng hàng/năm/đơn vị.
- Giá trị gốc và đơn vị được giữ riêng; parser số chạy bằng code. Năm/ngày/entity/
  scope thiếu evidence literal được giữ `null`, kèm issue/missing_fields.
  Không đổi “Số đầu năm” thành một ngày suy luận như ngày có trong PDF.
- `semantic_status: partial`, `graph_ready: false`, `is_gold: false`;
  native record ở `needs_review`. Corporate record ở `pending_human_review`.
  Không tự tạo gold, điểm ESG, kết luận greenwashing hoặc `Contradicted`.
- ZIP corporate giữ model ID/prompt trong `quality`, issue và coverage. BCTC chưa
  xác định riêng/hợp nhất có evidence sẽ chưa được xuất thành Financial corporate.
  Corporate v1 không biểu diễn mọi loại record trong báo cáo hỗn hợp: phần không
  biểu diễn được giữ native và được ghi issue, không âm thầm bỏ khỏi native JSON.

Mục tiêu hiện tại là candidate có nguồn để rà soát, không phải cam kết “đọc hết
tất cả trường”. Mô hình có thể bỏ sót, đọc nhầm hoặc bịa quote. Validator/schema
chỉ kiểm tra cơ học; cần gold được người dùng đối chiếu PDF để đo precision,
recall/F1, accuracy theo field. Không dùng quote do model sinh làm gold OCR.

## 4. File lưu trên máy

- Cache/resume: `data/processed/gemini_v1/<input>/report_<sha>/gemini_profile_<id>/`.
- Mỗi lượt: `data/processed/uploads_v2/<run>/`; từng tài liệu có `gemini_snapshot/`
  riêng chứa PDF nguồn, batch và `gemini_records.json`.
- Worker: `data/processed/extraction_jobs/<job>/`; request không lưu API key.
- Cache giữ phản hồi thô, usage, checkpoint và consent timestamp của lượt chạy.
  Đây là dữ liệu báo cáo nhạy cảm: chỉ dùng trên máy/tài khoản được phép truy cập,
  không push `data/` lên Git. Transport không dùng Files API, không upload file lưu
  riêng trên Google; việc xử lý/lưu dữ liệu phía API vẫn theo chính sách Google.

## 5. Dòng lệnh — PowerShell hoặc CMD, một dòng

```powershell
.\.venv\Scripts\python.exe scripts\extract_gemini.py "C:\duong-dan-thuc\BSR_2025.pdf" --company BSR --year 2025 --type sustainability_report --model gemini-3.8-flash --max-requests 5 --number-format vi --allow-cloud
```

Thay đường dẫn bằng file thực tế. `--allow-cloud` là đồng ý gửi PDF/chi phí; bỏ
cờ này thì CLI không gửi. CLI trả đường dẫn native JSON; luồng UI có thêm history
snapshot và download. CLI cache tiếp tục tại cùng đường dẫn, không phải bản lưu
snapshot lịch sử như UI. Tránh sửa/xóa cache trong lúc worker chạy.

## 6. Kiểm thử và tài liệu API

`tests/test_gemini.py` dùng PDF tổng hợp và client giả lập, bao gồm luồng UI,
worker, giới hạn request, resume, provenance, history, export và corporate audit.
Không gửi tài liệu thật, không thử key thật và không gọi API tính phí trong test.
Kiểm thử thật phải do người vận hành chạy sau khi cấu hình và xác nhận.

Tài liệu Google: [GenerateContent](https://ai.google.dev/api/generate-content),
[PDF processing](https://ai.google.dev/gemini-api/docs/document-processing),
[structured output](https://ai.google.dev/gemini-api/docs/structured-output).
