# Bộ gán nhãn tham chiếu Oil & Gas, phiên bản 1

Đây là **codebook và bộ gán nhãn nháp**, chưa phải gold đã được chuyên gia duyệt.
Không có precision thực tế khi chưa có nhãn đối chiếu PDF độc lập.
Chuẩn chỉ giúp định nghĩa chỉ tiêu; không cung cấp giá trị đúng của BSR.
Các mô tả tiếng Việt do dự án biên soạn, không thay thế văn bản chuẩn gốc.

## Các file chính

- `config/oil_gas_gold.yml`: định nghĩa khái niệm, nguồn chính thức, phiên bản,
  đơn vị, thuộc tính cần gán, cặp dễ nhầm và giới hạn áp dụng.
- `scripts/oil_gas_gold.py`: tạo gói gán nhãn mù cho hai người, kiểm tra cổng bàn giao.
- `scripts/quality_benchmark.py`: đo precision/recall/F1 theo record,
  độ đúng từng field, CER/WER khi đã có OCR reference độc lập.

Không sửa dictionary/rule trích xuất đang chạy. `concept_id` của codebook nằm
trong `standards_annotation`, tách khỏi `expected.metric_id` của hợp đồng extract.
Một ID cũ như `GHG_SCOPE_2` có thể có nhiều ứng viên: không tự chọn location/market.
Các `discovery_hints` chỉ chọn trang/ứng viên để rà soát, không dùng làm đáp án.
Nếu nhiều prediction cùng locator, mẫu chỉ tạo một chỗ gán nhãn nhưng giữ mọi
prediction để evaluator vẫn phát hiện trích xuất trùng; xem duplicate count trong plan.

## Phạm vi chuẩn và giới hạn

GRI dùng góc nhìn tác động; SASB dùng đặc thù hoạt động/ngành và nhu cầu nhà đầu tư;
IFRS ở đây là **IFRS Sustainability S1/S2**, không phải tự gán BCTC VAS thành IFRS.
Đơn vị có thể hoạt động trong nhiều ngành. EM-RM là cấu hình ứng viên cho lọc dầu/
phân phối; EM-EP, EM-MD và EM-SV hiện dùng phần GRI chung, protocol SASB riêng
chưa hoàn tất. Không khẳng định đã bao phủ mọi disclosure trong ba hệ chuẩn.

GRI 11 là khung xác định chủ đề có khả năng trọng yếu, không phải danh sách KPI
bắt buộc đồng loạt. V1 bao phủ các nhóm ưu tiên: nhân sự, GHG, năng lượng, nước,
chất thải, tràn đổ, an toàn, đào tạo, quản trị, tham nhũng, chính sách/hành động,
chiến lược/rủi ro/mục tiêu khí hậu và negative controls khoản tiền nhân sự.
Backlog: methane riêng, flaring, air pollutants, biodiversity/site, closure,
process safety, human rights/community, tax transparency, activity metrics theo
từng phân ngành và toàn bộ protocol SASB. Không biến thiếu dữ liệu mẫu thành
kết luận doanh nghiệp không công bố hoặc không tuân thủ.

Nguồn và locator ở `sources` trong codebook. Các PDF GRI người dùng đã cung cấp
được kiểm tra cùng trang chính thức. Trang IFRS xác nhận khung S1/S2; các đoạn
được lập chỉ mục của hướng dẫn ngành xác nhận một số ID EM-RM.
**Chưa lấy được toàn văn protocol SASB** từ Navigator yêu cầu đăng nhập.
`protocol_pending` và `candidate_component` không phải nhãn chuẩn đã xác minh.
Cần người dùng cung cấp bản chuẩn hợp pháp đúng phiên bản để hoàn thiện bước này;
không dùng Exposure Draft 2025 thay bản chuẩn ban hành.

## Chọn phiên bản trước khi gán nhãn

- Báo cáo 2023–2025: ưu tiên kiểm tra GRI 302:2016, 305:2016 và phiên bản được báo
  cáo tuyên bố; không mặc định dùng các số disclosure mới.
- GRI 101:2024: ngày hiệu lực dựa trên **ngày công bố** từ 01/01/2026.
- GRI 102/103:2025: dựa trên **ngày công bố** từ 01/01/2027.
- GRI 11 V1.1 công bố năm 2026 có phần lịch sử cập nhật; ngày hiệu lực 2023 của
  chuẩn ngành gốc không làm mọi sửa đổi mới có hiệu lực từ 2023.
- GRI 306:2016, 306-3 = tràn đổ đáng kể; GRI 306:2020, 306-3 = chất thải phát sinh.
  Cần lưu cả mã và edition, không ghép bằng mã đơn lẻ.
- S1/S2 gốc: kỳ năm bắt đầu từ 01/01/2024, có điều kiện áp dụng sớm. Sửa đổi S2
  tháng 12/2025: kỳ bắt đầu từ 01/01/2027, cho áp dụng sớm. Khác cơ sở ngày GRI.
- Hiệu lực theo chuẩn không chứng minh nghĩa vụ pháp lý tại Việt Nam hay việc
  doanh nghiệp đã áp dụng. Ngày/edition/adoption không biết thì để null + lý do.

## 1. Tạo gói gán nhãn

Chạy PowerShell tại thư mục dự án; lệnh dưới đây viết một dòng, không có backtick:

```powershell
.\.venv\Scripts\python.exe scripts\oil_gas_gold.py build outputs\ESG_extract_V2 --destination outputs\oil_gold_bsr_v1 --pages 24 --split dev
```

Đổi thư mục đích nếu đã tồn tại; công cụ không ghi đè nhãn cũ.
BSR đã dùng phát triển rule, nên không được chọn `--split test` cho những PDF này.
Khi đổi công ty, dùng manifest delivery có PDF và JSON tương ứng.

Gói gồm:

- `reviewer_a_draft.json`, `reviewer_b_draft.json`: không chép giá trị dự đoán vào
  expected; giao riêng mỗi file cho một người, không cho xem đáp án người kia.
- `adjudication_draft.json`: người phân xử lập đáp án sau hai lượt độc lập.
- `assisted_candidates_NOT_GOLD.json`: gợi ý từ extractor, **không đưa cho người
  gán nhãn mù trước vòng độc lập**; chỉ dùng hỗ trợ sau đó.
- `coverage_plan.json`: số ứng viên theo khái niệm và các khái niệm chưa lấy mẫu.
- `source_inventory.json`: hash PDF và số trang đã xác nhận với manifest.
- `predictions.json`: giữ riêng để chấm; không sửa cho khớp gold.
- `codebook.json`: ảnh chụp codebook; mỗi draft ghi SHA-256 cấu hình gốc.

Chọn trang ưu tiên chỉ tiêu và cân bằng nguồn, **không phải mẫu ngẫu nhiên**.
Phải thêm trang scan, biểu đồ, trang không có KPI và chỉ tiêu bị bỏ sót; thêm
PDF công ty khác giữ kín để đo khả năng tổng quát. Chia theo PDF/công ty trước
khi chỉnh rule, không chia hai bản của cùng PDF vào dev và test.

## 2. Người gán nhãn điền gì?

Mở PDF gốc bằng đường dẫn trong inventory và manifest. `physical_page` tính từ 1,
không nhầm số in trên trang. Kiểm tra toàn trang, tiêu đề bảng, cột năm, footnote,
trang tiếp nối và phần phương pháp/phạm vi liên quan. Thêm record bị bỏ sót,
xóa ứng viên không phải record trong phạm vi loại record đang gán nhãn.

Trong mỗi item:

1. `expected`: giá trị thực sự đọc từ PDF theo field hiện có. Measurement cần
   metric_id, value, unit, observation_year, period_type, reporting_entity,
   consolidation, scope. Narrative cần text. Có thể bổ sung field khác trong
   `src/quality/records.py:FIELDS`.
2. `reviewed_fields`: những field expected đã đối chiếu, không tick hàng loạt.
3. `field_evidence`: mỗi field có giá trị cần danh sách evidence cùng PDF với
   source_sha256, physical_page, anchor, quote nguyên văn. Trang phương pháp có
   thể khác trang bảng. Với số liệu bảng, quote giữ tên hàng + cột + nội dung ô;
   lưu scale/đơn vị ở evidence phù hợp, không chép câu diễn giải thành nguyên văn.
4. `unknown_reasons`: null không phải 0. Nêu rõ chưa thấy/không áp dụng/không đọc
   được, kèm vùng đã tìm trong ghi chú; không lấy scope từ BCTC lấp cho ESG.
5. `standards_annotation.concept_id`: chọn khái niệm đã kiểm tra, hoặc null + lý do.
   `references` chép đúng object source/disclosure/relationship từ codebook.
   `relationship`: component_of / conditional_overlap / related_not_equivalent /
   not_equivalent / unresolved. Không đồng nghĩa một giá trị đã thỏa toàn bộ chuẩn.
6. `qualifiers`: điền common_qualifiers + thuộc tính riêng của concept.
   Mỗi thuộc tính có giá trị cần evidence dưới khóa `qualifier:<tên>`;
   null cần unknown_reasons riêng, kể cả khi không áp dụng.
   Raw scale và phép đổi giữ riêng, không đổi số trong quote.
7. Ghi edition/adoption evidence khi có; không biết thì giữ null. Năm cột khác
   năm báo cáo phải giữ đúng năm quan sát và year_basis; restatement không rõ
   không tự khẳng định có/không điều chỉnh.

Sau khi kiểm tra đủ mọi record trong phạm vi trang/loại record, đặt
`fully_annotated: true`, `reviewed_against_pdf: true`, `annotator` là tên người làm.
Chỉ khi hoàn tất mới đổi `annotation_status` sang `human_reviewed`.
Đây là tuyên bố trách nhiệm của người dùng, không phải xác thực danh tính tự động.

## 3. Phân xử và kiểm tra bàn giao

Người phân xử kiểm tra mọi khác biệt, cả record được thêm/xóa. Bản final ghi
`adjudication.reviewer`, `reviewed_against_pdf`, hash hai file reviewer đã hoàn tất.
Dùng `Get-FileHash -Algorithm SHA256 <file>` và chuyển chữ hash về chữ thường.
Mỗi khác biệt/thay đổi đáp án có một `decisions` entry:

```json
{"locator":["<PDF_SHA256>",39,"<anchor>","measurement"],"reason":"Lý do phân xử sau đối chiếu PDF"}
```

```powershell
.\.venv\Scripts\python.exe scripts\oil_gas_gold.py release-check --final outputs\oil_gold_bsr_v1\adjudication_draft.json --reviewer-a outputs\oil_gold_bsr_v1\reviewer_a_draft.json --reviewer-b outputs\oil_gold_bsr_v1\reviewer_b_draft.json --source-delivery outputs\ESG_extract_V2 --output outputs\oil_gold_bsr_v1\release_report.json
```

Draft sẽ bị từ chối, không tự đổi thành gold. Kiểm tra cổng gồm hai người khác
nhau, cùng scope, field bắt buộc, evidence, lý do null, tham chiếu chuẩn, protocol
pending, hash nhãn/codebook/PDF, phạm vi trang và leakage.
`PASS_MECHANICAL_GATES` không chứng minh người gán nhãn trung thực hoặc giá trị
thực sự đúng; người có nghiệp vụ vẫn phải ký duyệt ngoài hệ thống nếu cần.

## 4. Chấm bộ đã duyệt

```powershell
.\.venv\Scripts\python.exe scripts\quality_benchmark.py evaluate --predictions outputs\oil_gold_bsr_v1\predictions.json --gold outputs\oil_gold_bsr_v1\adjudication_draft.json --split dev --output outputs\oil_gold_bsr_v1\accuracy_report.json
```

Đo extraction-field/record bằng evaluator hiện có. `standards_annotation` là
metadata gán nhãn chuyên môn, **chưa có bộ chấm semantic alignment độc lập**;
không trộn nó vào precision extract. CER/WER chỉ có khi người dùng chép OCR
reference độc lập và predictions chứa text OCR tương ứng. Đúng số nhưng sai năm,
phạm vi hay metric vẫn sai strict record. Báo cáo theo nhóm chỉ tiêu, scan/text,
doanh nghiệp và năm khi đủ mẫu; báo cả mẫu số, phần chưa lấy mẫu và giới hạn.

Không dùng ngưỡng precision chung do GRI/SASB/IFRS quy định: các chuẩn này không
ấn định ngưỡng pass cho extractor. Ngưỡng nghiệm thu do dự án thống nhất, theo
rủi ro sai số tiền, đơn vị/scale, kỳ và boundary. Không tạo gold hoặc kết luận
Contradicted/greenwashing tự động.
