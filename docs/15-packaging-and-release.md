# 15. Đóng gói và phát hành

Chọn **source-only ZIP + manifest + SHA-256** phù hợp Python/Dash local. Không tự
thêm Docker/Compose hoặc installer binary khi chưa kiểm được native OCR/models.
Version handover đề xuất `0.1.0-handover.1`, chỉ snapshot tài liệu/review; không đổi
schema version/parser ID hay tự tuyên bố semantic v1.0 production.

**Public/customer release đang BLOCKED** bởi quyền sở hữu/LICENSE dự án chưa chốt,
licensing PyMuPDF/transitive/model weights và cài máy mới/model/API chưa kiểm. Không
tự cấp MIT/Apache. Xem [distribution status](../DISTRIBUTION_STATUS.md). Gói review
chỉ phục vụ chủ dự án kiểm nội bộ, không phải quyền phân phối mã hoặc dữ liệu.

## Thành phần vào/ra gói

| Vào gói review | Không vào |
| --- | --- |
| app.py, source/config/contracts/dashboard assets dạng text | .git, .venv, node_modules/junction |
| scripts/tests/fixtures code + requirements/pytest.ini | data/, models, uploads, history và DB |
| docs Markdown/JSON reference, schemas, JSON synthetic examples | PDF/DOCX/XLSX báo cáo, ZIP cũ, ảnh render review |
| database/schema.sql, .env.example rỗng, DISTRIBUTION_STATUS | .env thật, credential/service-account file, cache/log/tmp/output |

Config/test chứa tham chiếu/ví dụ doanh nghiệp hiện có được giữ để code/CLI/tests
không mất dependency. Không coi chúng đã được legal clearance vì là file source;
chủ dự án phải rà nội dung trước chia sẻ ngoài. Heuristic scanner không nhận diện
mọi PII/copyright/secrets. Không include dữ liệu ngoài application root dù Git root
có Phase1/output được legacy importer tìm tùy chọn.

## Tạo và kiểm gói

Từ thư mục app, chọn đích **mới, ngoài application và Git root** để không lẫn với
nguồn. Ví dụ đường dẫn thực tế trên máy tác giả:

```powershell
.\.venv\Scripts\python.exe -B scripts/package_handover.py --version 0.1.0-handover.1 --destination "C:\Users\THINKPAD\Documents\ChatGPT\ESG_handover_review_moi" --dry-run
.\.venv\Scripts\python.exe -B scripts/package_handover.py --version 0.1.0-handover.1 --destination "C:\Users\THINKPAD\Documents\ChatGPT\ESG_handover_review_moi"
```

Dry-run không ghi thư mục/gọi API. Bản tạo thật ghi ZIP, manifest.json,
SHA256SUMS.txt; manifest trong ZIP có file paths/hash/bytes, exclusions, scan scope
và release blockers. Zip metadata/order cố định cho cùng bytes; timestamps trong
JSON nguồn thay thì checksum khác là bình thường. Không package trực tiếp từ toàn
Git root; tool không đọc request/upload/secret files và không deploy/push Git.

Người nhận kiểm checksum bằng PowerShell, thay đường dẫn ZIP thật:

```powershell
Get-FileHash -LiteralPath "C:\goi-nhan\esg-tracker-0.1.0-handover.1-review.zip" -Algorithm SHA256
```

So sánh toàn bộ hash với SHA256SUMS.txt do kênh tin cậy cung cấp; checksum không phải
chữ ký số hoặc xác minh danh tính nhà phát hành.

Sau build: verify entry hashes + re-scan từng nội dung text ZIP; giải nén vào
staging mới, chạy check_handover/offline smoke/tests bằng đúng interpreter được ghi
nhận. Không dùng đường dẫn archive không tin cậy để extractall không kiểm path.
Các tests BSR cần external corpus không thể được chứng minh chỉ bằng source ZIP.

Chưa có signed release, reproducible wheel lock có hashes, SBOM transitive/model
license inventory hoặc installer độc lập. `dependency-constraints.txt` ghi observed
versions, không bù việc đó. Khi owner chốt license và scope distribution, tạo ADR,
review clean Git/source snapshot, chạy acceptance có ngân sách và tag version
được owner cho phép. Không thực hiện publish trong đợt tài liệu này.
