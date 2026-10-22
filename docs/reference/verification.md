# Nhật ký kiểm chứng bộ bàn giao

Ngày: 22/10/2026. Windows/Python 3.12; không gửi báo cáo ra ngoài, không gọi API
thật/tải model hoặc bật billing. Mã nghiệp vụ/schema runtime không đổi; bổ sung
tài liệu, schema envelope suy ra, tool đóng gói/smoke/reference/check và tests riêng.

| Kiểm tra | Điều kiện / mong đợi | Kết quả thực tế | Trạng thái | Giới hạn |
| --- | --- | --- | --- | --- |
| Cleanup regression trước bộ tài liệu | Existing .venv, tmp riêng | 293 passed, 8 warnings | PASS | Không fresh install/accuracy |
| handover_reference.py | Đọc source/schema/package metadata | Index 162 file, module signatures, schema fields; 20 dependency observations | PASS | Installed metadata, không fresh resolver/SBOM đầy đủ |
| handover_smoke.py | Parser thật + FAKE page reader | BCTC 3, ESG 5, annual 5 records; schema valid; 0 API | PASS | Không OCR/PDF accuracy; số này chỉ của fixture |
| Documentation links/evidence/examples | check_handover.py | 24 trang/entry docs, 73 link local, 37 evidence locator; 5 example schemas hợp lệ | PASS | Không fetch external URLs; không quét mọi link tài liệu lịch sử |
| New handover tests | tests/test_handover.py, gồm missing-entry/junction tests | 11 passed ở lượt riêng và trong full suite | PASS | Junction traversal test dùng mock classification, không OS symlink thật |
| Full regression hiện tại | regression_final, workspace ngoài repo, fake providers | 304 passed, 8 warnings, 43,10s | PASS | Không live model hoặc corpus accuracy |
| Staging preflight lần 1 | Gói source-only đầu, không corpus | 1 failed, 299 passed, 3 skipped; thiếu app.py/CSV do allowlist mới | FAIL ĐÃ KHẮC PHỤC | Giữ log, sửa packager và thêm tests bắt lỗi, không sửa parser |
| Review archive R2 | Hash/SHA256/path/entry allowlist check | 232 file entries khớp manifest, re-scan nội dung không phát hiện pattern secret đã biết | PASS | Heuristic, không legal clearance/guarantee không PII |
| Staging R2 full suite | Không DB/corpus/venv, interpreter hiện có | 301 passed, 3 skipped, 8 warnings, 43,12s | PASS TRONG PHẠM VI | 3 tests nguồn BSR ../output bị SKIP đúng điều kiện; không fresh install |
| Staging R2 doc/smoke | check_handover + handover_smoke | Link/evidence/schema PASS; BCTC/ESG/annual 3/5/5 records + corporate fixture | PASS | FAKE page reader, không OCR thật |
| Helpers PowerShell và dependencies | Parser::ParseFile; setup preview; run -CheckOnly; pip check | 2 script syntax PASS, preview/check-only PASS; No broken requirements found | PASS | -Install và production app chưa chạy |
| CLI help | 9 entry point chính --help | 9 PASS, không extraction/network/model check | PASS | Cú pháp, không chứng minh chạy báo cáo thật |
| Giữ nguyên nghiệp vụ | So 395 SHA-256 baseline cleanup | Chỉ README.md thay đổi có chủ ý; 0 thay đổi ngoài dự kiến | PASS | File mới là docs/tool/test/example, không thuộc baseline |
| Fresh install/offline OCR/live API/deploy | Cần môi trường/quyền/ngân sách | Không chạy | BLOCKED | Không suy từ mock |
| Public/customer distribution | Owner/LICENSE/third-party/model/data rights | Chưa quyết định | BLOCKED | Review snapshot không phải release |

## Lệnh và hồ sơ thực thi

Workspace log ngoài repository:
`C:\Users\THINKPAD\Documents\ChatGPT\ESG_handover_checks_20261022_a`.

- `regression_final.log/.xml`: suite trên cây nguồn hiện tại.
- `staging_tests.log/.xml`: lỗi preflight lần đầu, giữ để truy vết.
- `staging_r2_tests.log/.xml`: suite trên source-only staging R2.
- `staging_r2/archive_verification.json`: archive hash + từng entry trước giải nén.
- `smoke_corporate/`, `staging_r2_smoke/`: controlled fixtures, schema/gates; không gold.
- `package_dry_run.json`: danh sách allowlist trước build.

```powershell
# App root, đích test mới ngoài source; PYTHONDONTWRITEBYTECODE=1
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider --basetemp "C:\Users\THINKPAD\Documents\ChatGPT\ESG_handover_checks_20261022_a\regression_final" --junitxml="C:\Users\THINKPAD\Documents\ChatGPT\ESG_handover_checks_20261022_a\regression_final.xml"
.\.venv\Scripts\python.exe -B scripts/handover_reference.py
.\.venv\Scripts\python.exe -B scripts/check_handover.py
.\.venv\Scripts\python.exe -B scripts/handover_smoke.py --destination "C:\Users\THINKPAD\Documents\ChatGPT\ESG_handover_checks_20261022_a\smoke_corporate"
```

Các thư mục trên đã tồn tại; lệnh tái kiểm phải dùng tên mới. Staging dùng đường
dẫn tuyệt đối tới **interpreter của .venv gốc**, cwd là bản giải nén, không có
dependency environment mới. Không gọi việc đó là cài máy sạch thành công.

Sau R2, cập nhật tài liệu/nhật ký và refresh hồ sơ app signature của reference
generator (đã chạy), không sửa nghiệp vụ. Gói cuối sẽ được verify lại entry hashes,
link/schema và targeted handover tests; không cần chạy lại expensive OCR hoặc mọi
test không liên quan. Checksum gói nằm bên ngoài ZIP để tránh self-reference hash.
