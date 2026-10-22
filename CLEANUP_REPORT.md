# Repository cleanup — đợt 1, ngày 22/10/2026

## 1. Kết quả và phạm vi

Đã khảo sát và dọn **có thể khôi phục**, không refactor, đổi tên module hoặc sửa
logic nghiệp vụ. Không commit, push, sửa Git index, thay dependency hoặc sửa
`.gitignore` trong đợt này.

- Git root: `C:\Users\THINKPAD\Documents\ChatGPT\ESG`.
- Application root: `C:\Users\THINKPAD\Documents\ChatGPT\ESG\esg-tracker`.
- Đã chuyển **36 thư mục nhóm B**, gồm **7.433 file thường**, tổng **33.540.731
  bytes (~33,54 MB / 31,99 MiB)** sang nơi cách ly ngoài Git root.
- **Không xóa vĩnh viễn thành phần dự án**. Đây là giảm dung lượng bên trong
  repository, không phải giải phóng dung lượng ổ đĩa: bản cách ly vẫn tồn tại.
- **395 file mã nguồn/cấu hình/tài liệu/test/DB được fingerprint không đổi SHA-256**.
- **7.433 file cách ly đều khớp SHA-256** trước/sau di chuyển.
- Các file còn lại trong inventory đọc được không đổi kích thước/mtime UTC.
- Kiểm thử sau dọn: **293 PASS, 0 FAIL**, 8 cảnh báo DataTable deprecated.
- Không có đủ bằng chứng để xếp thêm mã nguồn/tài liệu/dữ liệu vào nhóm C;
  không ép phân loại C chỉ nhằm làm thư mục trông gọn hơn.

Nơi cách ly và toàn bộ hồ sơ:

`C:\Users\THINKPAD\Documents\ChatGPT\ESG_cleanup_20261022_a\`

Manifest: `ESG_cleanup_20261022_a\manifest.json`.
Đường dẫn lưu đúng cấu trúc tương đối:

```text
ESG_cleanup_20261022_a/
├── quarantine/esg-tracker/...    Các thư mục đã chuyển, nguyên đường dẫn tương đối
├── manifest.json                Nguồn/đích, lý do, nhóm, UTC, hash từng file
├── plan.json                    Danh sách phạm vi đã kiểm tra trước khi chuyển
├── inventory_before.json        Metadata cây trước dọn
├── inventory_after.json         Metadata cây sau dọn, trước khi thêm báo cáo này
├── protected_hashes_before.json SHA-256 395 file được bảo vệ
├── verification.json            Kết quả đối chiếu cuối cùng
├── git_before.txt / git_after.txt
├── source_checks.json / pip_check.log
├── pytest.xml / pytest.log
├── restore.ps1 / restore_dry_run.log
├── cleanup.ps1 / metadata_recheck.ps1 / check_repository.py
└── test_run/                    Workspace kiểm thử mới, ngoài repository
```

Hồ sơ ngoài repository có thể chứa fixture sao chép từ dữ liệu báo cáo và đường
dẫn máy tác giả. Không tự công bố/push hồ sơ này. Không lưu giá trị API key hoặc
dump biến môi trường vào báo cáo.

## 2. Bằng chứng xác định hệ thống hiện tại

Không chọn phiên bản theo ngày sửa file hoặc chữ `final`:

1. `README.md` chỉ dẫn chạy `esg-tracker/app.py`; `app.py` import
   `dashboard.upload_analysis` và `dashboard.components.workspace`, bind
   `127.0.0.1:8050` khi chạy trực tiếp.
2. UI gọi `dashboard/extraction_worker.py`, worker chạy
   `scripts/upload_worker.py` và `dashboard/upload_v2.py`.
3. Docling là engine mặc định. Upload routing vẫn gọi `source_v2.py`,
   `financial_v2.py` hoặc `esg_v2.py`; Gemini là nhánh tùy chọn có consent/API key.
4. Financial output hiện là `esg-financial-candidates/2.3.0`, parser 6; ESG là
   `esg-candidates/2.1.0`, parser 3. Gemini dùng `gemini-report-candidates/1.0`.
   Đây là các hợp đồng cùng tồn tại, không phải các thư mục để chọn một rồi xóa phần còn lại.
5. CLI `extract_corpus.py`, `extract_source_v2.py`, `extract_financial_v2.py`,
   `extract_esg_v2.py`, `extract_gemini.py`, `extract_local_llm.py`, export/audit/
   quality/gold/review vẫn là các entry point được tài liệu hoặc tests sử dụng.
6. Có dynamic import: corporate handoff load
   `contracts/corporate_extract_v1/validate.py`; delivery load
   `scripts/validate_corporate_review.py`; tests load một số CLI bằng file path.
   Không dùng “không có import trực tiếp” để loại script/schema.
7. `src/paths.py` dùng application root cho config/schema/DB nhưng dùng parent
   workspace cho nguồn Phase 1 và `output/`. `scripts/import_data.py` vẫn đọc hai
   JSON Phase 1 tại Git root và dữ liệu trong `output/`.
8. Thư viện hiện tại được kiểm tra trong `.venv`: Dash 3.4.0, Docling 2.135.0,
   PyMuPDF 1.28.2, pytest 8.4.2; chi tiết toàn bộ ở `source_checks.json`.

Không có AGENTS.md áp dụng được tìm thấy ở các ancestor đã kiểm tra hoặc cây
mã nguồn đã khảo sát. Không tìm thấy Dockerfile, Compose, CI/CD workflow hoặc
package.json trong ứng dụng chính. Không suy ra deployment ngoài máy từ sự vắng
mặt đó; không đánh giá CI của repository lồng riêng.

Lúc bắt đầu khảo sát và trước mỗi bước di chuyển không phát hiện Python process
hoặc listener 8050. Vì vậy đây là xác định **cây mã đang được người dùng sử dụng
theo entry point/tài liệu**, không phải chứng minh phiên bản của server live.
Không dừng tiến trình hay dịch vụ nào. Không đụng `.venv` hoặc các Node process
của Codex và runtime ngoài workspace.

## 3. Cấu trúc trước / sau

Đường dẫn dưới đây tương đối với Git root, không phải application root.

```text
ESG/                                  TRƯỚC                  SAU
├── .git/                             giữ nguyên             giữ nguyên
├── .pytest_cache/                    không đọc được         giữ nguyên, BLOCKED
├── esg-tracker/
│   ├── app.py, README.md,
│   │   requirements.txt, pytest.ini  mã đang dùng            giữ nguyên
│   ├── src/, dashboard/, scripts/    nguồn + __pycache__     nguồn giữ; cache cách ly
│   ├── config/, contracts/, tests/   nguồn/schema/tests      giữ; bytecode cách ly
│   ├── docs/, database/              tài liệu + DB thực      giữ nguyên
│   ├── .venv/, data/, .superdesign/  môi trường/tài nguyên   giữ nguyên
│   ├── .pytest_cache/                không đọc được         giữ nguyên, BLOCKED
│   ├── outputs/                      42 thư mục con          30 thư mục con
│   │   ├── các delivery/AI/gold       dữ liệu có giá trị      giữ nguyên
│   │   ├── LOCAL_LLM_SMOKE_*          kết quả thực có ref     giữ nguyên
│   │   └── 12 basetemp đã xác minh   test-generated          cách ly
│   └── tmp/                          nhiều loại nội dung     giữ phần chưa xác minh
│       ├── 4 basetemp đã xác minh    test-generated          cách ly
│       └── .pytest_cache/            cache đọc được          cách ly
├── output/                           Git gitlink + dữ liệu   giữ nguyên
├── outputs/                          workbook + Git lồng     giữ nguyên
├── tmp/, gri document/, scripts/     tài liệu/ảnh/chưa rõ     giữ nguyên
├── node_modules/                     junction ra runtime     giữ nguyên, không đi theo
├── Phase1 JSON/DOCX, generator, ZIP   nguồn/di sản/chưa rõ     giữ nguyên
└── CLEANUP_REPORT.md                 chưa có                 thêm báo cáo này
```

Inventory trước: **82.501 mục / 47.420 file / 12.857.356.905 bytes**.
Inventory sau dọn, trước khi thêm báo cáo: **68.626 mục / 39.987 file /
12.823.816.174 bytes**.

Đây là metadata đọc được, **không phải dung lượng đầy đủ trên đĩa**: không duyệt
nội dung `.git`, `.venv`, `node_modules`, không follow junction/symlink, hai cache
bị từ chối quyền đọc không được tính đầy đủ. Vì vậy số file thường khác số mục
bao gồm thư mục/reparse point.

## 4. Phân loại A / C / D — thành phần được giữ

| Đường dẫn | Vai trò | Bằng chứng sử dụng / điều chưa xác minh | Nhóm | Hành động |
| --- | --- | --- | --- | --- |
| `.git/`, Git lồng và Git index | Lịch sử/versioning | Git root thực tế; không được di chuyển theo yêu cầu | A | Giữ |
| `esg-tracker/app.py` | UI entry point | README, imports UI, main bind 8050; import có `ensure_ready()` | A | Giữ, không import app production khi test |
| `esg-tracker/src/`, `dashboard/` | Xử lý, DB, UI, review | Imports hiện tại; 43 module local được kiểm tra đường dẫn | A | Giữ toàn bộ nguồn/assets |
| `esg-tracker/config/` | Metrics/rules/engine/quality | YAML/JSON được parser, mapper, benchmark và CLI đọc | A | Giữ |
| `esg-tracker/contracts/` | Schema/prompt contract/validator | Runtime path và dynamic import; schema v1 vẫn phục vụ handoff | A | Giữ |
| `esg-tracker/scripts/` | CLI, workers, audit, build tài liệu, QA | 32 file có dấu `__main__` trong tập kiểm tra; subprocess/dynamic calls | A | Giữ, không loại CLI vì ít import |
| `esg-tracker/tests/`, `pytest.ini` | Regression/fixtures | Suite sau dọn chạy 293 tests | A | Giữ nguồn/fixture |
| `esg-tracker/requirements.txt`, `.venv/` | Dependencies/runtime local | Interpreter dùng để chạy suite; pip check PASS | A | Giữ, không tái cài/xóa môi trường |
| `esg-tracker/database/` | Schema và DB làm việc | `src/paths.py`, app và import pipeline; DB có thay đổi từ trước | A | Giữ, fingerprint không đổi |
| `esg-tracker/data/` | PDF upload, history, checkpoints, models | Upload/history/worker và OCR đọc đường dẫn này | A | Giữ toàn bộ |
| `esg-tracker/docs/`, `.superdesign/` | Hướng dẫn và design handoff | README links, UI design-system; không phải code của dự án khác | A | Giữ |
| `esg-tracker/outputs/ESG_extract_V2*`, `BSR_*`, `quality_*`, `oil_gold_*`, `SA_AUDIT_*`, `ui_qa_*`, `corporate_qa_*` | Delivery, dữ liệu review, bằng chứng QA | JSON/PDF/ảnh/log có giá trị; một số đường dẫn dùng bởi docs/CLI/tests | A | Giữ, chỉ lấy bytecode đã xác minh |
| `esg-tracker/outputs/LOCAL_LLM_SMOKE_20261021` | Kết quả Ollama thực | `docs/LOCAL_LLM.md` chỉ rõ smoke_report và fingerprint | A | Giữ, không nhầm với pytest basetemp |
| `BSR_Phase1_Extract_Batch_v1.json`, `BSR_Phase1_Extract_Financial_Crosscheck_v1.json` | Nguồn import legacy | `src/database/adapters.py:load_phase1_records`, `scripts/import_data.py` | A | Giữ dù tên v1 |
| JSON schema/manifest và DOCX Phase 1 tại root | Tài liệu/nguồn người dùng | Bản gốc/đặc tả/hồ sơ bàn giao, chưa được phép bỏ | A | Giữ |
| `build_phase1_qa_workbook.mjs`, `node_modules/` | Tạo workbook QA | Generator import `@oai/artifact-tool`; node_modules là junction ra Codex runtime | A | Giữ junction, không recurse hoặc xóa target |
| `outputs/01a06a5f-28ba-7073-b533-668fa5ec761d` | Workbook người dùng | Output path được generator khai báo | A | Giữ |
| `output/` | Nguồn import/test, Git lồng | Git mode 160000; dirty từ trước; importer đọc JSON ở đây | A | Giữ, cần chốt chiến lược Git trước release |
| `gri document/`, ảnh/JSON/PDF trong `tmp/` | Nguồn chuẩn và rà PDF | Tài liệu/ảnh đối chiếu có thể có giá trị; tên tmp không đủ để bỏ | A | Giữ |
| `outputs/github_source_20261019/` | Bản source publication riêng | Chứa `.git`; chưa xác minh ownership/commit so với bản chính | D | Giữ; cần xác nhận đây là checkout bàn giao nào |
| `ESG_Generic_Extraction_Toolkit_v1_20260913_structured.zip`, `tmp.zip` | Archive | Chưa xác minh là backup duy nhất hay bundle được bàn giao | D | Giữ; cần inventory nội dung và owner xác nhận trước dọn tiếp |
| `esg-tracker/tmp/lo-profile-*`, `pdf*`, `extraction_smoke_20260913` | Profile/render/thử nghiệm lịch sử | Một số profile được Git theo dõi; không có reference runtime hiện tại nhưng chưa đủ để bỏ | D | Giữ; xác minh quy trình render ngoài repo/giá trị dữ liệu |
| `esg-tracker/tmp/pytest/` và các tmp/QA khác ngoài danh sách đã duyệt | Workspace hỗn hợp lịch sử | Chưa kiểm tra từng run, có thể chứa kết quả/DB/ảnh cần giữ | D | Giữ, không chuyển cả cây theo tên |
| `.pytest_cache/`, `esg-tracker/.pytest_cache/` | Có vẻ cache nhưng không đọc được | UnauthorizedAccessException; chưa xác minh nội dung | D | Giữ, BLOCKED; không đổi ACL/take ownership |
| `scripts/` tại Git root | Thư mục ngoài app | Chưa có bằng chứng có thể loại vì không có import | D | Giữ |

**Nhóm C:** chưa có thành phần được xác nhận đủ điều kiện trong đợt 1. Không có
source, ZIP, tài liệu, model hoặc dataset nào bị kết luận không liên quan chỉ từ tên,
trạng thái untracked, độ giống nhau hoặc việc thiếu import.

## 5. Nhóm B — từng phạm vi đã chuyển

Mọi đường dẫn tương đối dưới đây được giữ nguyên dưới `quarantine/`. Tất cả có
trạng thái `moved` trong manifest; không có bước di chuyển bị lỗi.

Bằng chứng **T**: thư mục chỉ chứa top-level fixture `test_...<số>`/pytest-current
link/lock, khớp tests hiện có; không có file Git theo dõi; không có reference
runtime hoặc history tới run này. Có thể tái tạo bằng pytest với basetemp mới.

Bằng chứng **P**: chỉ `.pyc`, có source `.py` tương ứng còn tồn tại, không có file
tracked; Python có thể tạo lại. Không lấy cache trong nested publication checkout.

Bằng chứng **K**: chỉ cache chuẩn pytest (`CACHEDIR.TAG`, README, nodeids,
lastfailed/stepwise và .gitignore); không có tracked file.

| Đường dẫn | Vai trò / bằng chứng | Nhóm | Hành động đã làm |
| --- | --- | --- | --- |
| `esg-tracker/outputs/GEMINI_FULL_20261021_a` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/GEMINI_FULL_20261021_b` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/GEMINI_NEW_20261021_a` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/GEMINI_NEW_20261021_b` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/GEMINI_SMOKE_20261021_a` | Basetemp giả lập, T | B | Cách ly |
| `esg-tracker/outputs/LOCAL_LLM_REGRESSION_20261021` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/LOCAL_LLM_REGRESSION_20261021_FINAL` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/LOCAL_LLM_REGRESSION_20261021_R2` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/LOCAL_LLM_TEST_20261021` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/LOCAL_LLM_TEST_20261021_R2` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/LOCAL_LLM_TEST_20261021_R3` | Basetemp, T | B | Cách ly |
| `esg-tracker/outputs/LOCAL_LLM_TEST_20261021_R4` | Basetemp, T | B | Cách ly |
| `esg-tracker/tmp/pytest_bsr_ai_reference_20261021_full` | Basetemp, T | B | Cách ly |
| `esg-tracker/tmp/pytest_oil_gold_20261021_run1` | Basetemp, T | B | Cách ly |
| `esg-tracker/tmp/pytest_oil_gold_20261021_run2` | Basetemp, T | B | Cách ly |
| `esg-tracker/tmp/pytest_oil_gold_20261021_run3` | Basetemp, T | B | Cách ly |
| `esg-tracker/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/tests/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/scoring/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/rules/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/quality/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/preprocessing/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/normalization/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/matching/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/extraction/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/src/database/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/scripts/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/dashboard/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/dashboard/pages/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/dashboard/components/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/contracts/corporate_extract_v1/__pycache__` | Bytecode, P | B | Cách ly |
| `esg-tracker/outputs/ESG_extract_V2_preflight_20261017/validation/__pycache__` | Bytecode validator, P | B | Cách ly |
| `esg-tracker/outputs/ESG_extract_V2/validation/__pycache__` | Bytecode validator, P | B | Cách ly |
| `esg-tracker/outputs/BSR_2023_2025_HANDOFF_REVIEW_READY_20261016_v2/validation/__pycache__` | Bytecode validator, P | B | Cách ly |
| `esg-tracker/tmp/.pytest_cache` | Cache pytest, K | B | Cách ly |

Manifest ghi UTC từng lần di chuyển và SHA-256 từng file; khoảng di chuyển
15:26:49–15:28:23 UTC ngày 22/10/2026 (22:26:49–22:28:23 UTC+7).

## 6. Kiểm tra thực tế sau dọn

| Kiểm tra | Trạng thái | Kết quả và giới hạn |
| --- | --- | --- |
| SHA-256 file được bảo vệ | PASS | 395 file, 0 thay đổi; gồm source/config/contracts/test/docs/DB, không phải hash mọi file của toàn workspace |
| Hash file cách ly | PASS | 7.433 file, 0 mismatch |
| Metadata file giữ lại | PASS | 39.987 file thường, 0 khác biệt bytes/mtime UTC trong inventory đọc được |
| Syntax/import local/runtime path | PASS | 123 Python file parse/compile không ghi pyc, 43 import local; 20 đường dẫn runtime kiểm tra tồn tại |
| Isolated UI smoke | PASS | Dash layout HTTP 200; không khởi động app production |
| Dependencies | PASS | `python -B -m pip check`: No broken requirements found |
| Regression + extraction smoke giả lập | PASS | 293 passed / 0 failed, 31,73 giây; 8 cảnh báo DataTable deprecated |
| Upload/export/history smoke | PASS | Tests mixed BCTC/ESG và Gemini fake PDF → records → history → corporate/schema/audit; không phải kiểm chứng model thật |
| Restore dry run | PASS | Kiểm tra manifest, hash, đường dẫn; 36 WOULD RESTORE; chưa thực hiện restore vì không phát sinh lỗi do dọn |
| Hai `.pytest_cache` không có quyền đọc | BLOCKED | Giữ nguyên; không nâng quyền/đổi ACL |
| Server production + DB initialization | BLOCKED / chưa chạy có chủ ý | `app.py` gọi `ensure_ready()` lúc import, có thể initialize/import/run pipeline lên DB thật; không dùng để smoke |
| OCR/model thật, Ollama server và Google API thật | BLOCKED / ngoài phạm vi | Không chạy OCR hàng loạt, tải model hoặc gọi API trả phí; lỗi Gemini HTTP 400 trước đó chưa được xử lý trong đợt cleanup |
| Clone sạch / Docker / deploy | BLOCKED / chưa xác minh | Không tạo environment/clone mới hoặc deploy; không có cấu hình Docker/CI trong app chính |

Lệnh test đã chạy từ `esg-tracker`, với output nằm ngoài repository:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider --basetemp "C:\Users\THINKPAD\Documents\ChatGPT\ESG_cleanup_20261022_a\test_run" --junitxml="C:\Users\THINKPAD\Documents\ChatGPT\ESG_cleanup_20261022_a\pytest.xml"
.\.venv\Scripts\python.exe -B -m pip check
```

Không dùng lại basetemp đã có cho lần test kế tiếp: chọn thư mục mới. Tests dùng
client/page reader giả lập hoặc workspace riêng; không đo precision/recall thực.
Metadata checker ban đầu so sánh chuỗi ISO với DateTime do PowerShell tự chuyển
kiểu, gây false positive. Đã kiểm tra lại bằng UTC timestamp ticks; bản kết quả
ban đầu giữ ở `verification_initial_timestamp_comparison.json`, kết quả đúng ở
`verification.json`. Không sửa mtime file nguồn để làm phép kiểm tra đạt.

## 7. Git và an toàn thay đổi

Trước cleanup đã có **15 tracked file sửa** trong ứng dụng và **dirty gitlink
`output`**, cùng **8.688 dòng untracked** trong chế độ `--untracked-files=all`.
Đây là trạng thái có sẵn, không phải thay đổi do dọn. Không mặc định untracked là rác.

Các thay đổi có sẵn được giữ nguyên. Các thư mục di chuyển đều không chứa tracked
file. Không stage/commit/reset/checkout. Báo cáo này là một file mới tại Git root.
`git_before.txt`/`git_after.txt` ghi trạng thái trước khi thêm báo cáo.

Không sửa `.gitignore`: app đã có ignore phù hợp cho bytecode/cache/uploads/
models/outputs/tmp/secrets. Nó không khiến DB, profile hay dữ liệu đã tracked
tự ngừng được theo dõi; không dùng ignore mới để che các mục chưa hiểu rõ.

## 8. Khôi phục

Dừng hoặc kiểm tra các Python process trước khi restore. Mặc định script chỉ
dry-run, không di chuyển dữ liệu:

```powershell
& "C:\Users\THINKPAD\Documents\ChatGPT\ESG_cleanup_20261022_a\restore.ps1"
```

Thực hiện khôi phục khi cần:

```powershell
& "C:\Users\THINKPAD\Documents\ChatGPT\ESG_cleanup_20261022_a\restore.ps1" -Apply
```

Script kiểm tra root, relative path và SHA-256; không follow đường dẫn ra ngoài
phạm vi dự kiến, không ghi đè nếu đường dẫn gốc đã tồn tại. Nếu app đã tạo lại
cache, script báo SKIP; không tự xóa cache mới để ép restore. Mỗi lần Apply có log
restore riêng. Manifest cleanup gốc được giữ nguyên.

## 9. Những việc còn phải chốt trước khi đóng gói

1. **Chốt release từ cây đang dirty.** Review/stage có chọn lọc phần source cần
   giao; không commit toàn workspace vì có dữ liệu/DB/ảnh/ZIP và Git lồng.
2. **Chốt xử lý `output` gitlink và publication checkout riêng.** `output` có
   mode 160000 nhưng không thấy `.gitmodules` ở root; clone sạch có thể không
   mang theo nguồn này. App có demo/fallback nhưng test/import dữ liệu thật là
   chuyện khác. Không tự sửa Git topology trong cleanup.
3. **Đóng gói source và dữ liệu thành hai phần rõ ràng.** Bảo toàn quyền sử dụng
   PDF/GRI; không ship DB/review/upload/API credentials tùy tiện. Publisher hiện
   tại là `scripts/prepare_github_publication.ps1`, nhưng đợt này chưa chạy nó và
   chưa xác nhận output clone sạch; cần đính kèm CLEANUP_REPORT riêng vì ở Git root.
4. **Bổ sung quy trình cài các công cụ phụ khi cần bàn giao chúng.** Node QA dùng
   Playwright, workbook dùng `@oai/artifact-tool` từ junction ngoài repo; chưa có
   npm manifest cài độc lập. `build_user_manual.py` dùng python-docx/Pillow nhưng
   chúng không được khai báo trực tiếp trong requirements. Không sửa dependency
   hoặc loại các script này để che thiếu sót.
5. **Tái lập môi trường.** Ghi lock/version/model requirements và kiểm thử máy sạch;
   suite trên `.venv` hiện tại không chứng minh cài mới/offline hoạt động.
6. **Giải quyết lỗi Gemini HTTP 400 bằng thông báo đã che secret** trước khi công
   bố tích hợp live đã hoạt động. Test mock hiện tại không thay cho API smoke thật.
7. **Gold/accuracy và human review vẫn là giới hạn nghiệp vụ có sẵn.** PASS tests,
   schema và cleanup không chứng nhận extract đủ trường hay chính xác toàn corpus.
8. Với nhóm D, xác nhận owner/provenance/quy trình gọi ngoài repo trước một đợt
   dọn sâu hơn. Giữ nguyên các mục đó trong đợt này.

Kết luận: đợt dọn an toàn và regression **đã được kiểm tra thực tế** trong phạm vi
trên. Không tuyên bố toàn hệ thống, deployment hoặc model/API thật đã hoạt động
bình thường chỉ dựa vào các kiểm tra đó.
