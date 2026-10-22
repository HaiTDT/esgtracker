# Trích xuất bằng LLM local - backend đầu tiên

Ngày triển khai: 21/10/2026. **Đã có backend/CLI chạy Ollama thật, chưa thay engine
trên giao diện kéo thả và chưa phải cam kết trích xuất toàn bộ báo cáo.** Giữ nhánh
rule và dữ liệu cũ để đối chiếu; không đổi schema native/corporate hiện hành.

## Đã triển khai

- Đọc workspace Source v2 đã có `canonical.json`, kiểm PDF/checkpoint/hash/pointer
  trước khi gửi phần chữ/ô bảng tới mô hình **đã cài trên máy**.
- Chạy qua Ollama loopback, không dùng SDK/API cloud, không pull model tự động;
  bỏ proxy và chặn redirect/host ngoài loopback, chặn model có dấu hiệu remote/cloud.
- Prompt chống coi nội dung tài liệu là lệnh; không cấp tool/function execution.
- Tạo kế hoạch chunk cho mọi text/cell được giữ trong source; giữ pending cho phần
  chưa chọn, retry lỗi từng chunk, lưu checkpoint để resume.
- JSON Schema cho model response và output; không chấp nhận JSON bị truncate.
- Kiểm trích dẫn từng field bằng substring literal trong source span. Sai year,
  số bị model chuẩn hóa không có literal, nguồn/quote bịa: giữ field null hoặc
  quarantine candidate. Bản model trả nguyên giữ trong checkpoint để kiểm tra.
- Loại candidate chỉ dựa vào tiêu đề/header/caption hoặc nhãn GRI/SASB thuần túy.
- Số raw được parse bằng code/Decimal string, **chưa tự áp scale**. `13 tỷ đồng`
  không tự xuất normalized_value=13 VND. Giữ đơn vị và scope raw để review.
- Lưu model digest, prompt/schema/code hash, thời gian/token từ Ollama;
  review_status luôn pending_human_review, boundary_verified=false, verdict=null.
- Resume kiểm hash checkpoint đã ghi trong ledger; không âm thầm tin file đã sửa.

Các kiểm tra literal chỉ xác nhận chữ có trong source, **không chứng minh model
ghép đúng hàng/cột/năm hoặc hiểu đúng định nghĩa**. Domain/pillar/type vẫn candidate.

## Máy đang có gì?

Đã kiểm tra: khoảng 32 GB RAM, NVIDIA RTX A2000 Laptop 8 GB VRAM. Ollama đang hoạt
động trên `http://127.0.0.1:11434`, có `llama3:8b` (Q4_0), digest
`365c0bd3c000a25d28ddbf732fe1c6add414de7275464c4e4d1c3b5fcb5d8ad1`.
Đây là model có sẵn để kiểm thử, **không phải model đã được chứng minh đạt accuracy
tài chính/tiếng Việt**. Model này không có vision. Không tải thêm model trong lần làm này.

## Cách chạy trên PowerShell

Chạy từ:

```powershell
cd "C:\Users\THINKPAD\Documents\ChatGPT\ESG\esg-tracker"
```

Kiểm runtime/model, không sinh nội dung:

```powershell
.\.venv\Scripts\python.exe scripts/extract_local_llm.py --check
```

Cấu hình tại `config/local_llm.yml`: provider/model, loopback URL, timeout, retry,
context/output limit, chunk budget và number_format. Không cần API key hay pip
dependency mới. Không đổi biến môi trường hệ thống, không khởi động lại Ollama/app.

### Chạy thử nguồn ESG đã có trên máy

```powershell
$llmSource = "outputs/SA_AUDIT_20261021_01/smoke_capture/report_595d7503b899fc513541b5bb1572a3c2f2a58f68f07cd33da77ef846e8aad2bf/profile_18599d2b44a4308b2470bdb4ee7bc29c60737c6413b8aef90b4b8acca9f564bb"
.\.venv\Scripts\python.exe scripts/extract_local_llm.py "$llmSource" --output-dir outputs/LOCAL_LLM_SMOKE_20261021 --start-page 39 --max-pages 1 --max-chunks 5
$LASTEXITCODE
```

Đã chạy thật lệnh này. Nó chỉ gửi 5 chunk, không phải cả PDF. Những chunk khác
vẫn pending. Chạy lại cùng lệnh/source/model/code dùng checkpoint, không gọi model
lại cho chunk đã thành công. Nếu đổi code/schema/model digest/source capture thì
profile mới tách kết quả; không ghi đè kết quả profile cũ.

Với nguồn khác: chạy `scripts/extract_source_v2.py` như hướng dẫn Source v2 trước,
rồi truyền **workspace mà CLI trả về** vào `extract_local_llm.py`. BCTC, ESG và annual
đều được backend đọc theo từng nội dung, không dùng tên file làm bằng chứng scope.

### Xử lý toàn bộ nguồn text/cells của workspace

```powershell
.\.venv\Scripts\python.exe scripts/extract_local_llm.py "$llmSource" --output-dir outputs/LOCAL_LLM_FULL_TEXT_20261021
```

Không có page/chunk limit thì lập kế hoạch cho toàn bộ text/cell đang có trong
workspace. **Nếu Source v2 chỉ đọc một trang thì bỏ limit LLM cũng không tạo ra 67
trang còn thiếu.** Cần chạy source capture đủ trang trước. Không đưa whole PDF vào
một prompt. Chunking v1 theo block, budget ký tự JSON, chưa tokenizer-exact hoặc
context joining xuyên trang; paragraph/cell dài được tách span chứ không cắt bỏ.

### Exit code

- `0`: chỉ dùng cho `--check` thành công.
- `1`: lỗi input/runtime/checkpoint hoặc có chunk thất bại.
- `2`: đã lưu kết quả ứng viên, nhưng semantic vẫn partial; không phải lỗi chắc
  chắn của runtime, không phải chứng nhận full report hoặc factual accuracy.

Trong PowerShell xem `$LASTEXITCODE` ngay sau Python; exit code của shell wrapper
có thể không giữ nguyên số 2 của process Python.

## Đọc kết quả

Mặc định:

```text
data/processed/local_llm/report_<PDF-SHA>/llm_profile_<hash>/
  profile.json
  source_catalog.json
  chunks/chunk_<hash>.json
  llm_records.json
```

`llm_records.json` có schema `local-llm-extract/1.0`, **không phải**
`corporate-extract-1.0` hoặc `esg-upload/2.0.0`. Không import thẳng vào adapter cũ.

| Trường | Ý nghĩa |
|---|---|
| records[].label_raw / original_text | Chữ nguồn, không phải câu model tự tóm tắt |
| records[].record_type/domain/pillar | Phân loại do model đề xuất, chưa xác minh |
| fields.value_raw / parsed_value | Số gốc và Decimal string được code parse; locale ambiguous giữ null |
| fields.year / baseline_year / target_year | Chỉ giữ năm có literal 4 chữ số trong quote riêng |
| fields.*_raw | Chưa chuẩn hóa/ngầm diễn giải ngày, đơn vị, consolidation hay scope |
| field_sources | Bằng chứng của từng field, native pointer, span, page, ô/bbox nếu có |
| normalization | Chưa áp đơn vị/scale; normalized_value giữ null |
| company_id_input | Metadata nhập, không chứng minh reporting entity của record |
| quality | Pending review, không gold, không verdict |
| coverage.source_pages | Source đã đọc/failed/pending những trang nào |
| coverage.counts/chunks | Chunk LLM processed/failed/pending |
| coverage.text_pass_complete | Mọi source span đã được model xử lý; không phải recall/đủ KPI |
| coverage.uninterpreted_blocks | Hình/biểu đồ/form chưa hiểu bằng text model |
| issues / records[].issues | Lỗi chunk, candidate/field bị từ chối, cảnh báo model |

`source_catalog.json` giải source_id ngắn về block ID, checkpoint SHA, JSON pointer,
text span và tọa độ nguồn. Output tiếp tục phụ thuộc source workspace: giữ PDF và
checkpoint nếu muốn truy vết; đây chưa phải gói portable PDF/JSON bàn giao.

## Giới hạn và các bước tiếp theo

1. **Vision**: cần model local hỗ trợ hình ảnh để đọc scan/biểu đồ/header mất trong
   OCR. Chưa tải/chọn model mới. Không thể dùng text model để khôi phục chắc chắn
   chữ không còn trong checkpoint.
2. **Ngữ cảnh**: cần thêm section router, parent/subsidiary attribution, header/unit
   context xuyên trang và table-aware row grouping. V1 mới lặp header đã quan sát,
   không tự suy header mất.
3. **Tích hợp UI và corporate adapter**: cần hợp đồng adapter riêng và regression
   test; giao diện upload hiện tại vẫn gọi rule parser. Chưa bật LLM âm thầm bằng
   cấu hình global và chưa sửa dữ liệu review cũ.
4. **Đo chất lượng**: benchmark model local với gold độc lập, không lấy model tự
   chấm câu trả lời. Citation/schema pass không phải precision/recall.
5. **Số học/normalization**: kết hợp business validators hiện có sau khi map có
   evidence; không để LLM tự sửa số hoặc tự tính lại báo cáo.

Không mở Ollama/app ra Internet. Các kiểm tra loopback/model ở client không thay
thế cấu hình server/kiểm toán network; nếu cần chế độ local-only chặt hơn, xem
`OLLAMA_NO_CLOUD=1` trong FAQ chính thức. Thay đổi đó cần restart server, chưa thực
hiện trên máy của bạn.

## Tài liệu API chính thức đã đối chiếu

- [Chat API](https://docs.ollama.com/api/chat): format JSON Schema, done_reason và usage.
- [Structured outputs](https://docs.ollama.com/capabilities/structured-outputs).
- [Vision](https://docs.ollama.com/capabilities/vision): model phải hỗ trợ images; không có trong model đang thử.
- [Local/cloud và cấu hình](https://docs.ollama.com/faq).

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_local_llm.py -q -p no:cacheprovider
```

Test dùng mock cho network và source fixture; smoke trên model thật là phép thử
riêng. Xem `outputs/LOCAL_LLM_SMOKE_20261021/` trên máy này. Không công bố precision
hoặc full-report accuracy từ vài chunk thử nghiệm.

Kết quả cuối ngày 21/10/2026: **273 test passed**, 7 cảnh báo deprecation Dash;
trong đó 35 test mới cho local LLM. Smoke code cuối chạy 5/16 chunk trên nguồn một
trang: 29,547 giây, resume 0,578 giây, 1 candidate được giữ sau kiểm literal, 9
issues, 11 chunk pending. Candidate còn pending_human_review; không có phép đo
accuracy. Mô hình đã từng gán nhầm header/nhãn GRI thành claim; guard loại các
trường hợp đó đã được thêm và kiểm bằng regression test.

Log và fingerprint code/model/output: `outputs/LOCAL_LLM_SMOKE_20261021/smoke_report.json`.
Đường dẫn output chính xác được ghi trong `output_path` của report này. Các profile
thử trước đó vẫn được giữ; không lấy kết quả profile cũ làm kết quả code mới.
