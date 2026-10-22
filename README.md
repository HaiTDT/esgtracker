# ESG Tracker

Công cụ phân tích **báo cáo ESG/PTBV, báo cáo thường niên và báo cáo tài chính**,
với Oil & Gas làm ngành demo. Tải PDF, trích xuất dữ liệu có truy vết, rà soát
bằng chứng và xuất gói JSON/PDF để phân tích tiếp.

> Không phải công cụ kiểm toán hoặc kết luận greenwashing. OCR, ánh xạ chỉ tiêu
> và các cặp đối chiếu là candidate cần kiểm tra PDF. `PASS` của validator chỉ
> xác nhận điều kiện cơ học, không xác nhận nội dung đã đúng hoặc đầy đủ.

## Bộ tài liệu bàn giao và quickstart offline

Bắt đầu tại [Documentation index](docs/00-documentation-index.md): kiến trúc,
cài đặt, từng pipeline/module, hợp đồng JSON, quality, CLI, vận hành, bảo mật,
troubleshooting, packaging và checklist có dẫn chứng source/test.

Từ thư mục chứa `app.py`, sau khi cài requirements:

```powershell
.\.venv\Scripts\python.exe -B scripts/check_handover.py
.\.venv\Scripts\python.exe -B scripts/handover_smoke.py --destination outputs/first_smoke_moi
```

Đích smoke phải mới. Smoke dùng **page reader giả lập**, không kiểm OCR/LLM thật;
xem [ví dụ JSON tổng hợp](examples/README.md) và [nhật ký kiểm chứng](docs/reference/verification.md).
Gói `*-review.zip` là source snapshot kiểm nội bộ, **chưa phải release được duyệt
phân phối**; xem [distribution status](DISTRIBUTION_STATUS.md) và
[packaging](docs/15-packaging-and-release.md). `.env.example` không tự được load.

## Chức năng

Mới: [rà soát/correction và đo chất lượng](docs/QUALITY_REVIEW.md): lưu bản sửa
theo field, lịch sử/revision và phát hiện stale; tạo draft gán nhãn, đo strict
precision/recall/F1, field accuracy và CER/WER khi có gold được người dùng duyệt.
Hiện chưa có gold đã duyệt hoặc con số precision thực tế để công bố.

Mới: [Gemini API tự động](docs/GEMINI_INTEGRATION.md) trong màn hình kéo thả:
đọc PDF theo nhóm trang, lưu history/checkpoint và xuất JSON có evidence để rà
soát. Đây là tùy chọn cloud cần API key máy chủ, đồng ý gửi PDF và giới hạn request;
Docling local vẫn là mặc định. Bộ kiểm thử dùng phản hồi giả lập, chưa xác nhận
chất lượng/chi phí bằng một lượt API thật.

- Dashboard tiếng Việt, kéo thả PDF, tiến độ xử lý, trạng thái lỗi và lịch sử local.
- Docling, OCR, bảng/ô và vị trí nguồn theo trang; worker riêng để cô lập lỗi native.
- BCTC: candidate chỉ tiêu, giá trị, cột năm, đơn vị, riêng/hợp nhất và thuyết minh.
- ESG: claim, policy, action, target, governance và bảng chỉ tiêu.
- JSON nội bộ v2 hoặc ZIP `corporate-extract-1.0`: PDF gốc, JSON, manifest,
  checkpoint, hàng đợi rà soát và công cụ kiểm định.
- Từ điển metric cục bộ và cặp ESG–BCTC có ID/evidence hai phía. Khoản tiền
  liên quan nhân viên không được dùng làm số lượng nhân viên.
- Property graph tham chiếu **local**; chưa tích hợp Graph/Neo4j bên ngoài.

## 1. Cài đặt và chạy trên Windows

Môi trường đã kiểm thử: **Python 3.12 64-bit**, Windows, PowerShell. Lần đầu cần
Internet để cài thư viện và có thể tải mô hình Docling. Pipeline trích xuất hiện
tại mặc định chạy local và không cần API key. Chỉ nhánh Gemini tùy chọn cần
`GEMINI_API_KEY`; không tự gửi tài liệu lên cloud.

Mở PowerShell, chạy từng dòng:

```powershell
git clone https://github.com/HaiTDT/esgtracker.git
cd esgtracker
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Nếu không có `py`, dùng `python -m venv .venv` với Python 3.12 đã cài.
Không cần activate môi trường ảo, tránh lỗi execution policy của PowerShell.

Mở **[http://127.0.0.1:8050](http://127.0.0.1:8050)**. Giữ cửa sổ chạy app mở.

- Tắt app: **Ctrl + C** trong cửa sổ PowerShell đó.
- Chạy lại: `.\.venv\Scripts\python.exe app.py`.
- Sau khi cập nhật mã: dừng app, cài lại requirements nếu cần, chạy lại và
  nhấn **Ctrl + F5** trên trình duyệt.
- App mặc định chỉ lắng nghe `127.0.0.1`. Chưa có đăng nhập/phân quyền để mở
  công khai ra Internet.

Linux/macOS chưa được kiểm thử đầy đủ. Cách gọi Python tương ứng:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

## 2. Dữ liệu của bản clone mới

Repository gồm mã nguồn, cấu hình, schema, tài liệu và kiểm thử; **không chứa PDF
đã upload, DB làm việc, mô hình OCR hoặc ZIP bàn giao**. Lịch sử trên máy tác giả
không tự chuyển sang máy khác.

Khi chưa có database, app tự tạo SQLite, thử nhập bộ nguồn local nếu có và khởi
tạo dữ liệu Demo có nhãn riêng. Nếu chưa có báo cáo thật, vào **Tải báo cáo / Extract**
để bắt đầu; không hiểu số Demo là dữ liệu đã được xác minh.

Các batch BSR trước đây không phải dependency bắt buộc để upload PDF mới. Những
tài liệu `docs/` có ngày tháng ghi nhận trạng thái tại thời điểm viết; đường dẫn
trên máy tác giả trong ví dụ cần thay bằng đường dẫn trên máy bạn.

## 3. Sử dụng giao diện

1. Vào **Tải báo cáo / Extract**, kéo PDF vào hoặc chọn từ máy tính.
2. Điền mã doanh nghiệp, năm và loại báo cáo.
3. Giữ **Quy ước số: Tự động** nếu chưa kiểm tra PDF. Chỉ chọn Việt Nam khi
   `1.594` có nghĩa `1594`, còn `1,5` là `1.5`.
4. Nhấn **Trích xuất và phân tích**, theo dõi tiến độ toàn bộ trang.
5. Tìm/lọc dữ liệu, chọn một dòng và đối chiếu bằng chứng với trang PDF.
6. Tải **JSON v2** cho định dạng nội bộ, hoặc **Tải gói bàn giao chuẩn (ZIP)**
   để nhận đầy đủ nguồn và JSON theo hợp đồng.
7. Lần sau: **Lịch sử trích xuất → Làm mới danh sách → Mở kết quả đã lưu**.

Upload **không tự nhập vào Dashboard lưu trữ hoặc chạy scoring**. Dashboard lưu
trữ là luồng SQLite riêng. `scripts/import_data.py` thay nội dung đã nhập trong
database; không chạy trên dữ liệu làm việc khi chưa sao lưu.

Tên file gợi ý: `ESG_BSR_2025.pdf`, `BCTC_BSR_2024.pdf`, `BCTN_PLX_2025.pdf`.
Tên có ngày ở đầu vẫn có thể nhận diện; tên file không đủ để xác nhận phạm vi
riêng/hợp nhất. Kéo thả không yêu cầu đặt PDF sẵn trong thư mục cố định.

## 4. Cấu trúc gói bàn giao

```text
delivery/
├── manifest.json
├── pdf/                         PDF gốc giữ nguyên bytes
├── json/                        Một corporate-extract-1.0 JSON/PDF
├── notes/
│   ├── native/                  Parser output + checkpoint truy vết
│   ├── demo_review_queue.json   priority_records + candidate_pairs + exclusions
│   └── graph_review.json        Property graph tham chiếu local
└── validation/                  Schema, validator và báo cáo
```

| Trường/trạng thái | Cách hiểu |
| --- | --- |
| `record_id`, `evidence_id` | ID record/bằng chứng, không phải mã chỉ tiêu chung |
| `metric_id = local:*:v1` | Từ điển cục bộ, không phải mã GRI/IFRS được xác nhận |
| `physical_page` | Trang vật lý bắt đầu từ 1, có thể khác số in trên trang |
| `original_quote`, `exact_quote` | Nội dung quan sát ở nguồn; OCR có thể sai |
| `normalized_value` | Giá trị đã áp dụng scale một lần; không nhân lại |
| `unknown` / `null` | Chưa có căn cứ xác định, không thay bằng 0 |
| `NOT_REVIEWED` | Chưa rà soát trên giao diện |
| `pending_human_review` | Record bàn giao chưa được người dùng duyệt |
| `NeedsReview` | Cặp candidate còn cần kiểm tra kỳ/định nghĩa/phạm vi |
| `partial` | Chưa xác nhận đã trích xuất đầy đủ nội dung báo cáo |
| `unavailable` | Slot chưa có nguồn/kết quả phù hợp; manifest ghi lý do |

Không suy boundary KPI ESG từ BCTC hoặc bìa báo cáo. Không ghép tổng doanh thu
với doanh thu thuần, tiền thuế với chi phí thuế, khoản phải trả người lao động
với số nhân viên. Cặp còn blocker giữ `eligible_for_numeric_comparison=false`,
không tự tạo gold hoặc kết luận `Contradicted`. Kiểm tra nội bộ ESG không được
tính vào số claim đã đối chiếu tài chính.

## 5. Dùng dòng lệnh

Chạy từ thư mục chứa `app.py`. Mỗi ví dụ dưới là một dòng hoàn chỉnh. Thay đường
dẫn ví dụ bằng file thật, không nhập nguyên `C:\bao-cao` nếu nó không tồn tại.

### Chụp nguồn PDF có checkpoint

```powershell
.\.venv\Scripts\python.exe scripts/extract_source_v2.py "C:\bao-cao\BCTC_BSR_2024.pdf" --company BSR --report-type financial_statements --report-year 2024
```

Lệnh trả workspace có `canonical.json`. Dùng đường dẫn đó để chạy parser BCTC:

```powershell
.\.venv\Scripts\python.exe scripts/extract_financial_v2.py "C:\workspace-duoc-tra-ve" --number-format auto
.\.venv\Scripts\python.exe scripts/extract_esg_v2.py --help
```

`--max-pages 3` chỉ thử cài đặt; bỏ tham số để đọc toàn bộ. Source CLI có thể trả
exit code 2 khi kết quả partial; phải xem coverage, không coi là thành công đầy đủ.

### Xuất ZIP từ lịch sử local

```powershell
.\.venv\Scripts\python.exe scripts/export_corporate_handoff.py --saved-id JOB_ID --destination outputs/delivery_moi --zip
```

Thay `JOB_ID` bằng ID lịch sử; run cũ dùng `run:<id>`. Thư mục đích phải mới,
không ghi đè gói đã bàn giao. JSON portable không đủ tạo lại ZIP nếu thiếu PDF
và checkpoint local.

### Xuất ma trận BSR 2023–2025

```powershell
.\.venv\Scripts\python.exe scripts/export_corporate_handoff.py --bsr-history --destination outputs/BSR_delivery_moi --zip
```

Lệnh chọn kết quả sẵn trong lịch sử, không tự tải báo cáo hoặc chạy OCR. Slot
thiếu giữ `unavailable`, không thay bằng năm/phạm vi khác.

### Kiểm định gói

```powershell
.\.venv\Scripts\python.exe outputs/delivery_moi/validation/validate.py --manifest outputs/delivery_moi/manifest.json --pdf-dir outputs/delivery_moi/pdf
```

Gói bổ sung V2 còn có audit quote/checkpoint/normalization và kiểm tra cặp + Graph.
Xem [hướng dẫn V2](docs/ESG_EXTRACT_V2.md). `missing_expected_reports=0` của Graph
tham chiếu local không chứng minh đã nạp vào dịch vụ Graph bên ngoài.

## 6. OCR và xử lý lỗi thường gặp

- Lần đầu Docling có thể phải tải model; cần kết nối mạng và dung lượng đĩa.
- Có thể cài Tesseract rồi chạy
  `.\.venv\Scripts\python.exe scripts/setup_vietnamese_ocr.py` để tải `vie`/`eng`.
  Script chỉ lấy language data, **không cài Tesseract executable**.
- Nếu Tesseract không sẵn sàng, backend dùng RapidOCR; không bảo đảm chính xác
  tiếng Việt tương đương và vẫn phải kiểm tra nguyên văn.
- Worker riêng có deadline theo trang để cô lập crash native. Lỗi/quá hạn phải
  giữ trong coverage và issue log; không tự coi trang đó là đã đọc.
- Không nhấn trích xuất nhiều lần khi job đang chạy. Nếu lỗi, xem thông báo và
  lịch sử trước khi thử lại.
- Cổng 8050 đang bận: dừng app cũ bằng Ctrl + C. Không tắt các tiến trình Python
  khác nếu chưa xác định chúng thuộc ứng dụng.
- PowerShell và CMD khác cú pháp xuống dòng. Các ví dụ dùng một dòng để tránh
  lỗi backtick bị hiểu thành tên file.

Xem [OCR/crash recovery](docs/OCR_CRASH_RECOVERY.md),
[source capture](docs/SOURCE_V2_USAGE.md) và [upload](docs/UPLOAD_V2_USAGE.md).

## 7. Kiểm thử

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

Test kiểm tra schema, truy vết, normalization, cột năm, khác biệt phạm vi, worker,
lịch sử và cặp candidate. Một số test tích hợp cần corpus BSR riêng tại `../output`;
nếu không có thì ghi **SKIPPED**, không thay bằng nguồn giả. Kết quả test không
phải thước đo accuracy của toàn bộ corpus.

## 8. Cấu trúc mã nguồn

```text
esgtracker/
├── app.py
├── requirements.txt
├── config/                  Doanh nghiệp, metrics, luật và cấu hình
├── contracts/               JSON schemas và hợp đồng bàn giao
├── dashboard/               UI, upload, tiến độ, lịch sử
├── src/
│   ├── extraction/          Capture, OCR, BCTC/ESG, corporate export/review
│   ├── normalization/
│   ├── matching/
│   ├── rules/
│   ├── scoring/
│   └── database/
├── scripts/                 CLI và kiểm định
├── database/schema.sql      DB làm việc được tạo lúc chạy, không commit
├── tests/
└── docs/
```

Runtime data ở `data/uploads`, `data/processed`, `data/models`, `outputs` và
`database/*.db`. Sao lưu nếu muốn giữ lịch sử; không xóa các thư mục này chỉ để
cập nhật mã nguồn. `.gitignore` loại chúng khỏi những commit mới.

## Giới hạn

- Chưa bảo đảm đọc hết mọi bảng, biểu đồ, footnote hoặc bảng nối trang.
- Thiếu chứng cứ về boundary/population/phương pháp/restatement thì giữ null/unknown.
- Cần parser/profile mới khi sửa một số lỗi OCR/mapping; không sửa PDF gốc.
- Chưa có workflow duyệt ngữ nghĩa đầy đủ để tự chuyển mọi record thành reviewed.
- Không bundle PDF, DB, model hoặc ZIP BSR trong Git. Bàn giao dữ liệu riêng qua
  kênh phù hợp; tài liệu báo cáo vẫn thuộc quyền của đơn vị phát hành.
- Không đưa secrets/token vào source, README, URL remote hoặc cấu hình.

Tài liệu thêm: [BCTC](docs/FINANCIAL_V2_USAGE.md), [ESG](docs/ESG_V2_USAGE.md),
[lịch sử](docs/EXTRACTION_HISTORY.md), [corporate handoff](docs/CORPORATE_HANDOFF_USAGE.md).

## Bộ gán nhãn tham chiếu Oil & Gas

[Hướng dẫn gold GRI/SASB/IFRS S1–S2](docs/OIL_GAS_GOLD.md) mô tả codebook 32 khái niệm,
hai lượt gán nhãn PDF độc lập, phân xử và đo độ chính xác. Tạo gói nháp:

```powershell
.\.venv\Scripts\python.exe scripts\oil_gas_gold.py build outputs\ESG_extract_V2 --destination outputs\oil_gold_bsr_v1 --pages 24 --split dev
```

Gói tạo ra là `DRAFT_NOT_GOLD`, không tự điền đáp án hoặc tính precision.
Protocol SASB đầy đủ còn cần bản chuẩn hợp pháp đúng edition; ánh xạ pending không
được coi là tương đương chuẩn. Không thay đổi rule trích xuất hay kết luận ESG.

[Bản tham chiếu BSR do AI đối chiếu PDF](docs/BSR_AI_REFERENCE.md) là sidecar riêng,
không tự chuyển thành human gold hoặc ghi đè dữ liệu extract.

## LLM local qua Ollama - opt-in CLI

Đã có [backend trích xuất bằng LLM local](docs/LOCAL_LLM.md): source-v2 →
Ollama đã cài local → JSON Schema → kiểm trích dẫn từng field → candidate chờ duyệt.
Không tự tải model, không fallback cloud; giữ checkpoint/resume, model digest và
cảnh báo phần nguồn chưa đọc. Kiểm cấu hình bằng:

```powershell
.\.venv\Scripts\python.exe scripts/extract_local_llm.py --check
```

Đây là backend text-only đầu tiên, **chưa thay engine UI kéo thả, chưa có vision
hoặc cam kết trích xuất đầy đủ báo cáo**. Output `local-llm-extract/1.0` riêng,
không tự nạp corporate adapter/Graph và không tạo kết luận greenwashing.
