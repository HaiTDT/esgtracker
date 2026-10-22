# 12. Troubleshooting

Không bật billing, đổi model hoặc sửa dữ liệu chỉ từ một thông báo chung. Giữ
PDF/hash/profile và các evidence trước khi chạy lại; không gửi secret/log nguyên bản.

| Triệu chứng | Nguyên nhân có thể | Cách kiểm tra | Cách xử lý hiện có / đề nghị | Bằng chứng thành công |
| --- | --- | --- | --- | --- |
| Input does not exist | Placeholder, sai đường dẫn, CMD nhận backtick | Test-Path file thật; nhìn shell PS hay CMD | Dùng một dòng, đúng script extract_corpus.py, không `_corpus.py` | Inventory tìm đúng PDF |
| Không mở app/8050 bận | App khác đang nghe, sai venv/cwd | Terminal log, Get-NetTCPConnection -LocalPort 8050 | Ctrl+C đúng terminal; chạy lại app.py; không kill mọi Python | Local page phục vụ, không chỉ process còn sống |
| Thiếu module/model | Cài sai venv, chưa có Docling weights | python.exe path, pip check, worker.log | Cài requirements trong đúng .venv; tải model chỉ khi được phép | Import + trang OCR thật xử lý thành công (smoke fake không đủ) |
| PDF scan/empty OCR | Scan, thiếu tiếng Việt, xoay, chất lượng kém | coverage/page checkpoint/ảnh PDF | Cài Tesseract/data hoặc xem OCR profile; giữ source, profile mới nếu cần | Đối chiếu chữ/bảng trên PDF thật, không chỉ processed |
| PDF mật khẩu/hỏng | Encryption/xref/truncated download | Lỗi khi mở, xác minh bytes từ nguồn hợp pháp | Nhận bản đọc được/giải mã được chủ sở hữu cho phép; không bypass trái phép | Mở và đọc trang được, hash/source version ghi lại |
| Crash 0xc0000005 | Native library/memory access | exit_code_hex/Windows event/worker.log | Worker cô lập, backend profile pypdfium2 đang dùng; xem OCR_CRASH_RECOVERY | App còn sống + resume saved pages; không khẳng định hết mọi crash |
| Timeout trang | OCR/model chậm, tài nguyên | PAGE_DEADLINE_EXCEEDED, owned page worker log | Capture giữ failed/partial, thử profile/cấu hình sau kiểm RAM; không tăng timeout vô hạn | Trang được xử lý + source review |
| Hết RAM/disk | Weights, scan ảnh lớn, nhiều copy/history | OS metrics/disk, exception/log | Dừng đúng task, thêm tài nguyên hoặc giảm scope thử; chưa có auto cleanup an toàn | Ghi JSON/checkpoint đầy đủ, không chỉ còn disk |
| Sai cột/năm/scale | Header lệch, OCR gộp, sai locale | raw cells/header/field_sources, content_period | Dùng locale có căn cứ; reviewer correction; parser change cần tests riêng | Đúng row/column/PDF; không chỉ arithmetic pass |
| Bảng nối trang/header lặp | Continuation ambiguous/mất order | table_continuations/coverage/reasons | Review thủ công; không merge mọi bảng liền nhau | Cùng unit/kỳ/scope được chứng minh |
| Thiếu field/schema fail | Unsupported layout, metadata unknown, output sửa tay | validation.errors, missing_fields, schema version | Giữ null/issue; xử lý branch đúng; đừng ép required bằng số đoán | Schema PASS + nguồn vẫn resolve; semantic review riêng |
| Corporate blocked | Chưa biết riêng/hợp nhất, missing source/hash | notes/blocked_documents.json | Giữ native, bổ sung evidence thật; không thay report khác | Validator + manifest path/hash đúng |
| Gemini HTTP 400 | Request/schema/key/precondition có thể không hợp lệ | Hiện chỉ có generic HTTP code, chưa giữ safe detail | Không retry liên tục/bật billing. ĐỀ XUẤT safe provider diagnostics rồi sửa nguyên nhân | API trả STOP + accepted JSON và PDF review; chưa có đợt này |
| Gemini 401/403/404 | Key/quyền/model/config | Status + API project/model quyền trên Google | Tạo/rotate key trên máy chủ; dùng API model ID được phép, không gửi key vào chat | Request được chấp nhận; presence check không đủ |
| Gemini 429/pending | Quota hoặc request cap nội bộ | Budget.used/limit, stop_reason và coverage | Chờ quota/đổi phạm vi được phép, re-consent run mới; không tự billing | Số request/coverage tăng đúng, không bỏ pending |
| Timeout API | Network/provider, request có thể đã xử lý | Batch attempt/duration/log | Giữ failed; cân nhắc chi phí trước retry | Accepted response, usage nếu có; không khẳng định failed miễn phí |
| JSON LLM bị cắt | Token budget/schema/layout | finishReason/done_reason/validation | Checkpoint failed; điều chỉnh cấu hình có giới hạn sau review | Schema và page/literal gates PASS, vẫn needs_review |
| Kết quả đổi giữa lần chạy | Model/profile/header/OCR/package đổi | Model digest/version, profile hash/config | Giữ snapshot, version constraints; rerun independent benchmark | Có provenance so sánh; không cam kết deterministic |
| Review stale/history mất | Source/profile/dictionary đổi, artifact bị xóa | review state/fingerprint, hash/path | Khôi phục backup đúng bộ, re-review; không sửa hash | PDF/record/source resolve + review không stale |

Thông báo trích xuất kết thúc không có nghĩa đủ dữ liệu. Ưu tiên issue log và
coverage trước dùng các con số làm báo cáo. Các giá trị confidence cố định trong
legacy code không phải precision đã được hiệu chuẩn.
