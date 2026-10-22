# 13. Bảo mật và xử lý dữ liệu

Ứng dụng local chưa có auth/RBAC/multi-tenant isolation. Job UUID/PDF route và
filesystem path/hash checks không thay cho xác thực, antivirus hoặc PDF sandbox.
Không public app hoặc mở port qua LAN/Internet mà không có thiết kế bổ sung.

Input giữ nguyên PDF, request có base64; source text, model response, prompt,
checkpoints, logs và corrections có thể chứa thông tin nhạy cảm. Phân quyền thư
mục/ổ đĩa/backup theo người dùng, mã hoá nếu policy yêu cầu; các cơ chế OS này chưa
được ứng dụng tự cấu hình. Không gửi log/PDF đi dịch vụ ngoài trong bước kiểm thử.

Browser UI có Google Fonts imports trong `dashboard/assets/style.css` và
`zz_workspace.css`; app dùng external Bootstrap theme. “Xử lý báo cáo local” không
có nghĩa mọi request browser đều offline. Chưa kiểm air-gap UI; muốn offline hoàn
toàn cần đóng gói/kiểm license font/theme riêng.

Gemini cần consent UI và key server, gửi PDF fragment (cả trang context), không
chỉ một KPI. Code không dùng Files API lưu tệp riêng nhưng chính sách xử lý/lưu
phía Google vẫn áp dụng; retention/training policy tài khoản **chưa được thẩm định**.
Không suy free tier an toàn cho dữ liệu mật. Ollama loopback giới hạn origin/cloud
aliases; không bảo đảm endpoint local không bị process khác giả mạo.

Key đã từng lộ trong chat phải revoke/rotate, không chỉ xoá khỏi terminal. Không
ghi key vào .env.example/source/docs/downloads. App không tự load .env. Không dump
environment hoặc đưa key vào command URL. Hai biến GEMINI_API_KEY/GOOGLE_API_KEY
khác nhau bị từ chối; không set cả hai tùy tiện. Worker kế thừa env máy chủ.

Packager chỉ chọn UTF-8 source extensions/roots, không recurse symlink/junction,
không include .git/.venv/data/DB/PDF/office documents/output/log/cache. Heuristic
scan chặn một số Google key/private-key patterns, không chứng minh không còn mọi
secret hoặc dữ liệu nhạy cảm. Seed config/test/reference quotes cần review quyền
phân phối riêng. Có cả licensing gate về trạng thái, không có quyền tự cấp LICENSE.

**ĐỀ XUẤT chưa triển khai:** authenticated users, encrypted storage, audited secret
manager, malware scanning/true PDF sandbox, retention automation, provider error
redaction theo allowlist, quotas/token-cost ledger và access audit. Không ghi chúng
như chức năng hiện tại chỉ vì có subprocess/UUID/SQLite.
