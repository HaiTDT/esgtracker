# 03. Cấu trúc và điểm vào

Ứng dụng là thư mục chứa `app.py`, không nhất thiết là Git root. Trên máy tác giả,
Git root nằm một cấp trên `esg-tracker`. Giữ phân biệt này khi bàn giao.

| Thành phần | Vai trò | Vào → ra | Dependency / bằng chứng | Xác minh |
| --- | --- | --- | --- | --- |
| `app.py` | UI/server và archive dashboard | HTTP → layout/callback | Dash; `ensure_ready` có DB side effect | Source + isolated UI, không start production |
| `dashboard/upload_analysis.py` | Form/job/poll/source/download | PDF + input → UI/job | upload_v2, worker, history, human_review | Tests |
| `dashboard/extraction_worker.py`, `scripts/upload_worker.py` | Cô lập OCR/native crash | request.json → result/status/log | Python subprocess, semaphore | Tests worker crash |
| `src/extraction/source_v2.py` | Source ledger/checkpoint | PDF → canonical/native page JSON | PyMuPDF, isolated Docling reader | Fake-reader tests; không xác minh OCR thật đợt này |
| `financial_*` | Bảng, cột, kỳ, note, semantic candidate | canonical → financial JSON | config/schema, Decimal, nguồn layout | Tests |
| `esg_v2.py`, `esg_tables_v2.py` | Text/table E/S/G, policy/action/target | canonical → ESG/annual JSON | esg_v2.yml, metrics.yml | Tests |
| `gemini.py`, `gemini_handoff.py` | PDF cloud / adapter | fragment → candidate → corporate | server key, HTTPS, schemas | Mock tests, live chưa xác minh |
| `local_llm.py` | Text-only LLM local | canonical → LLM JSON riêng | Ollama loopback, local_llm.yml | Mock tests; xem smoke lịch sử riêng |
| `corporate_handoff.py`, `corporate_review.py` | Export/metric/pair candidate | native + PDF → ZIP/queue | dictionary, contract validator dynamic import | Tests + schema, không assurance |
| `src/quality/` | Review store, dictionary, evaluator, checks | prediction + human gold → metrics | SQLite riêng, rapidfuzz | Unit/CLI tests; gold thật chưa có |
| `src/database`, matching/rules/scoring | Archive/legacy workflow | import → DB/rules/score | schema.sql, YAML | Tests; không tự chạy từ upload |
| `config/`, `contracts/` | Cấu hình và schema runtime | YAML/JSON → parser/gates | Paths relative ROOT | Source/path checks |
| `schemas/` | Catalog + inferred upload schema | mẫu → doc validation | Không tham gia runtime hiện tại | New handover tests |
| `examples/` | Fixture JSON minh họa | fake source → parser thật | Không dùng dữ liệu khách hàng | Schema tests |
| `data/uploads`, `data/processed`, `data/models` | Báo cáo/history/model/log | runtime disk → resume/review | Không bundle source package | Giữ nguyên dữ liệu |
| `database/esg_tracker.db` | DB làm việc | archive queries | Tạo khi chạy, không ship DB thật | Không sửa trong bàn giao |
| `scripts/prepare_github_publication.ps1` | Publisher cũ | source → thư mục mới | allowlist cũ; không thay bằng tool mới tự động | Đọc code; không chạy đợt này |
| `scripts/package_handover.py` | Packager review mới | allowlist → ZIP/hash/manifest | Standard library, secret heuristic | Tests / verify archive |

Kiểm kê theo file và symbol nằm trong [CSV](reference/component-inventory.csv) và
[module index](reference/module-index.json). CSV không giả định docstring là bằng
chứng đã chạy. Các công cụ chuyên biệt BSR vẫn được giữ, không đồng nhất chúng
với tính năng generic áp dụng mọi công ty.

Không có migration service/ORM upgrade tool độc lập đã xác minh. `database/schema.sql`
và initialization của `src/database` là cơ chế hiện có; thay schema cần backup,
đọc kỹ code khởi tạo và kế hoạch nâng cấp riêng. Không có notebook/Compose/CI chính
được tìm thấy trong cây app được khảo sát.
