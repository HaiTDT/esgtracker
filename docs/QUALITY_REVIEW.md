# Rà soát, correction và đo chất lượng

## Trạng thái thực tế

Đã có phần mềm lưu bản sửa và tính chỉ số; **chưa có bộ gold do người có nghiệp vụ
duyệt và chưa có precision thực tế của corpus**. Không được dùng số bài test, PASS
schema hoặc mức độ khớp checkpoint OCR để thay cho accuracy so với PDF.

## 1. Rà soát trên giao diện

Khởi động lại app, Ctrl + F5, mở kết quả cũ trong Lịch sử hoặc upload báo cáo mới.
Chọn record ở bảng, đến **Rà soát bằng chứng → Rà soát & bản sửa của người dùng**:

1. Mở/đọc PDF ở khung nguồn; kiểm tra đúng hàng/cột và năm.
2. Nhập tên reviewer và lý do. Đây là tên tự khai báo, chưa có xác thực tài khoản.
3. Chỉ tick các field đã kiểm tra. Chọn Xác nhận, Sửa, Từ chối hoặc Mở lại.
4. Nếu Sửa, nhập JSON object theo field cho phép. Ví dụ minh họa cú pháp:

```json
{"value": "1594", "unit": "people", "observation_year": 2025}
```

Ví dụ này **không phải đáp án chuẩn cho record bạn đang chọn**. Không tự điền năm,
đơn vị hoặc boundary nếu PDF không đủ căn cứ. Native `value` là giá trị parser;
corporate `normalized_value` là giá trị đã quy đổi, không được nhầm hai lớp.

5. Tick xác nhận đã đối chiếu PDF và Lưu. Chọn record khác rồi quay lại/mở app lại
để xem bản sửa và lịch sử. Sửa một field chỉ tạo `partially_reviewed`; record đo
lường chỉ được `reviewed` khi tất cả field bắt buộc đã được người dùng chọn kiểm tra.
`reviewed` ở đây là trạng thái con người khai báo, không phải assurance độc lập.

Các field: metric_id, value, unit, observation_year, period_type, measurement_date,
reporting_entity, consolidation, scope, counting_method, calculation_method, text.
`text` sửa trong lớp reviewer; không thay original_text/exact_quote OCR của nguồn.

### Lưu trữ và xuất

- SQLite riêng: `data/processed/human_review/reviews.sqlite3`, tách DB dashboard.
- Mỗi lần Lưu tạo event/revision; Mở lại cũng là event, không xóa lịch sử.
- JSON v2 tải về có `human_review`; ZIP corporate có `notes/human_review.json`.
- JSON/OCR/PDF gốc không bị sửa. Bản sửa có hiệu lực nằm ở `current.effective_fields`.
- Chỉ trạng thái reviewed/partially_reviewed không stale mới hiển thị bản sửa.
- Một record bị sửa không tự cập nhật các tổng, scoring hoặc Graph. ZIP có
  `notes/dependency_invalidations.json` ghi những cặp phụ thuộc cần kiểm tra lại.
- Thay đổi source snapshot, parser hoặc từ điển làm bản duyệt thành `stale`; không
  tiếp tục áp dụng correction cũ. Chưa có hệ thống người dùng/chống sửa DB bởi chủ máy.
- `reviewed` không tự biến thành gold. Không tự đưa correction vào tập test.

## 2. Từ điển chung

Điểm vào mới: `config/metric_dictionary.yml`. Corporate mapper đọc definition,
pattern, điều kiện loại trừ và đơn vị từ file này, không giữ một CATALOG riêng viết tay.
File tham chiếu `config/metrics.yml` qua `legacy_esg_source` để không nhân đôi cấu
hình ESG cũ. Các parser/luồng legacy vẫn dùng cấu hình đó; chưa ép chúng đổi metric ID.

Mọi local metric vẫn `pending_expert_validation`; `source_references` để trống nếu
chưa có nguồn xác nhận, không tự bịa tham chiếu chuẩn. Từ khóa khớp không chứng minh
metric/kỳ/phạm vi tương đương. Khởi động lại app sau khi sửa từ điển.

Xuất toàn bộ dictionary đang dùng:

```powershell
.\.venv\Scripts\python.exe scripts/quality_benchmark.py dictionary --output outputs/metric_dictionary_review.json
```

## 3. Chuẩn bị bộ gold — không tự gán nhãn thật

Từ thư mục project, dùng gói corporate đã có để tạo draft và predictions riêng:

```powershell
.\.venv\Scripts\python.exe scripts/quality_benchmark.py template outputs/ESG_extract_V2 --destination outputs/quality_bsr_draft --limit-pages 12 --split dev
```

Đích phải mới. Nhận `gold_draft.json`, `predictions.json`, `sampling.json`.
Draft có `expected={}`, chưa có reviewer và chưa xác nhận PDF. `suggested_prediction`
chỉ để tham khảo, không phải nhãn chuẩn. Predictions có hash phiên bản code/config.

Chọn trang round-robin theo PDF, có giới hạn số trang. Đây chỉ là **mẫu bắt đầu
từ các trang có candidate**, không phải mẫu thống kê đại diện. Phải bổ sung trang
scan, biểu đồ, bảng nối trang, trang không có record và trang parser bỏ sót. Không
bỏ các trang khó chỉ để làm precision cao hơn. Nên có thêm doanh nghiệp chưa dùng
để chỉnh quy tắc; chia tập theo PDF/doanh nghiệp, không theo từng dòng ngẫu nhiên.

Người rà soát phải đọc PDF độc lập rồi:

- Thêm item bị bỏ sót; xóa candidate sai khỏi danh sách item đúng.
- Giữ locator gồm SHA-256 PDF, physical_page, anchor và record_type. Nếu nội dung
  bị bỏ sót không có pointer native, ghi anchor thủ công nhất quán để tính missing.
- Điền expected và reviewed_fields. Record đo lường cần tối thiểu metric_id, value,
  unit, observation_year, period_type, reporting_entity, consolidation và scope.
  Claim/policy dạng chữ cần text. Chỉ điền null nếu người rà soát đã xác nhận là
  không xác định/không được công bố, không dùng null để che thiếu nhãn.
- Điền annotator, reviewed_against_pdf=true và split=train/dev/test.
- fully_annotated=true chỉ khi đã kiểm tra TẤT CẢ record trong scope trang + loại
  record khai báo. Nếu false chỉ đánh giá các anchor đã gán nhãn, không suy corpus recall.
- Chỉ sau khi duyệt thật mới đổi annotation_status thành human_reviewed.
- Nếu đo OCR, chép ocr_reference theo cùng scope/thứ tự đọc của trang dự đoán.
  OCR prediction lấy từ predictions.json, không lấy bản chép chuẩn làm dự đoán.

BSR đã được dùng chỉnh quy tắc trước đây nên bộ mẫu này là `dev`, không phải
test độc lập. Danh sách đã biết ở `config/quality_development_sources.yml` được
tự áp dụng để chặn đưa các PDF đó vào tập test.

Giữ test độc lập. Ghi SHA của các PDF khác đã dùng chỉnh quy tắc vào
development_source_sha256 hoặc truyền --development-source; evaluator chặn cùng PDF
ở development và test. Không thể tự chứng minh một PDF chưa từng dùng tinh chỉnh
nếu lịch sử development không được khai báo trung thực.

## 4. Đo precision/recall và OCR

```powershell
.\.venv\Scripts\python.exe scripts/quality_benchmark.py evaluate --predictions outputs/quality_bsr_draft/predictions.json --gold outputs/quality_bsr_draft/gold_draft.json --split dev --output outputs/quality_bsr_report.json
```

Lệnh từ chối draft/chưa đủ field, unit chưa duyệt và trùng nguồn dev/test.

- Match theo source/page/anchor/record_type, không dùng giá trị để tìm đáp án gần nhất.
- Strict TP: tất cả field expected đều đúng. Sai năm dù đúng số vẫn FP + FN.
- Candidate thừa/lặp là FP; record gold không tìm thấy là FN trong phạm vi gán nhãn.
- Tính precision, recall, F1 và field accuracy có support; mẫu số rỗng trả null.
- CER/WER dùng edit distance, giữ dấu tiếng Việt, NFC normalization; không bỏ dấu
  để che lỗi OCR. Không có reference thì CER/WER=null, không báo 0% lỗi.
- Báo lỗi theo record/field và theo nguồn PDF; báo rõ unit fully annotated/partial.
- Đây chưa phải benchmark precision/recall của cặp ESG–BCTC. Cặp vẫn cần gold
  riêng về khả năng so sánh, kỳ và phạm vi trước khi đo chất lượng pairing.

Gold cho phần extraction khác nguồn chuẩn để đo OCR. Đánh giá khớp OCR checkpoint
chỉ kiểm tra truy vết. Không gọi đó là accuracy so với PDF.

## 5. Kiểm tra số liệu tự động

```powershell
.\.venv\Scripts\python.exe scripts/quality_benchmark.py check outputs/ESG_extract_V2 --output outputs/quality_bsr_rule_checks.json
```

Kiểm tra nguồn, năm thiếu, đơn vị/headcount âm/lẻ và công thức BCTC dạng mã dòng
(ví dụ 60=50-51-52). Công thức chỉ chạy khi đủ code duy nhất, cùng bảng, cột, năm,
đơn vị/scale và riêng/hợp nhất. Không ghép tùy tiện khác trang. Sai số dư là
`NeedsReview` để kiểm tra OCR/rounding, không tạo Contradicted. Các phép kiểm tra
tổng biểu đồ/bảng nối trang và mọi phương trình kế toán chưa được bao phủ đầy đủ.

## 6. Giới hạn triển khai

Đã có workflow local và evaluator. Chưa có gold đã duyệt, precision corpus,
xác thực reviewer, benchmark pair, adjudication hai annotator hoặc tự tái tính
mọi kết quả downstream từ correction. Các phần này cần dữ liệu/duyệt nghiệp vụ
thật; không thay bằng PASS test hay kết quả máy tự gán.
