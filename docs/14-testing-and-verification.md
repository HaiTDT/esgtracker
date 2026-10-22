# 14. Kiểm chứng bàn giao

Kết quả lệnh cụ thể nằm ở [verification.md](reference/verification.md). Chỉ dùng
PASS khi đã chạy và có log; code reading được ghi riêng. Không coi số test là accuracy.

## Tầng kiểm tra

1. Inventory/symbol/schema field generation: đọc source/config, ghi hash/metadata,
   không start app hoặc tải model. Link/evidence/schema checker không fetch website.
2. Offline smoke ba loại báo cáo: parser thật, **FAKE page reader** cung cấp source
   có kiểm soát. Validate native JSON và upload envelope. Không kiểm OCR của PDF.
3. Regression: existing suite + handover packaging/link/smoke tests, isolated tmp;
   Gemini/Ollama được mock, không gọi provider thật.
4. Source-only review archive: allowlist, hashes từng file và ZIP; scan nội dung
   các entry, không chỉ filename. Thử path traversal/symlink/secret/missing input.
5. Staging sạch từ ZIP: không .git/.venv/DB/corpus gốc. Dùng **interpreter/package
   đã cài của máy hiện tại**, không được gọi là pip install máy mới. Tests cần PDF
   BSR ngoài gói có thể SKIP đúng lý do; ghi số lượng thực.
6. Fresh online/offline install, OCR/model và API thật: CHƯA XÁC MINH nếu không
   chạy; không test tính phí chỉ để chứng minh quickstart.

## Lệnh tái kiểm

```powershell
.\.venv\Scripts\python.exe -B scripts/check_handover.py
.\.venv\Scripts\python.exe -B scripts/handover_smoke.py --destination outputs/handover_smoke_moi
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider --basetemp outputs/handover_tests_moi
.\.venv\Scripts\python.exe -B -m pip check
```

Đích phải mới; pytest có thể tự dọn basetemp, đừng trỏ vào thư mục chứa dữ liệu thật.
Trong đợt bàn giao, dùng đường dẫn ngoài repository cho mọi workspace/log/test.
PYTHONDONTWRITEBYTECODE=1 giúp không sinh lại cache đã dọn. Không import app.py trên
DB làm việc; isolated Dash layout smoke không chạy ensure_ready.

New scripts có test: secret scan fail không in secret, .env.example rỗng, reject
existing/inside-app destination, archive hashes, known banned suffixes/dirs, documentation
links/evidence, example schemas, three synthetic report paths. Đây là contract của
tool bàn giao, không chỉnh parser đang chạy.

Logs/report chỉ là bằng chứng thực thi từng scope. Nếu schema sai, fixes chỉ vào
tài liệu/tool mới; không sửa runtime output để “làm test xanh”. Nếu model thật chưa
chạy hoặc Gemini 400 chưa có safe detail, ghi BLOCKED, không gộp vào PASS khác.
