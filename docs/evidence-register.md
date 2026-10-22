# Evidence register

Các locator kiểm được tự động ở [evidence.json](reference/evidence.json).
`check_handover.py` kiểm file/symbol literal tồn tại, không tự chứng minh lập luận.
Hash/symbol đầy đủ từng module trong [module-index](reference/module-index.json).
PASS theo lệnh và điều kiện cụ thể ở [verification](reference/verification.md).

| Kết luận quan trọng | Evidence ID / locator | Trạng thái |
| --- | --- | --- |
| UI app có DB initialization lúc import | E01 app.py:ensure_ready | ĐÃ XÁC MINH source; không start production đợt này |
| Upload, worker, size/type validation, local/cloud route | E02–E06 | Source + regression |
| Capture giữ PDF/hash/checkpoints/retry và empty records | E07–E08 | Source + fake-reader smoke, không live OCR |
| OCR Tesseract/RapidOCR và pypdfium2 | E09–E10 | Config/code; model accuracy chưa xác minh |
| BCTC số âm/locale/unit/kỳ/code/arithmetic | E11–E14 | Source + tests; không corpus completeness |
| ESG keyword candidate, table, annual cùng nhánh | E15–E16 và E03 | Source + three-type synthetic smoke |
| Gemini consent/model/key/header/budget/profile | E17–E18 | Code/mock; lỗi live 400 trước đó chưa rõ nguyên nhân |
| Ollama text-only loopback, installed digest, no pull/cloud | E19–E20 | Code/mock; không live inference trong đợt handover |
| Corporate/source-origin limitations, no automatic gold | E21–E24, E37 | Source + handoff tests |
| UI review là overlay/stale, không assurance/gold | E25–E27 | Source + review tests |
| Precision/recall/CER/WER cần gold độc lập | E27, docs/QUALITY_REVIEW.md | Evaluator đã có; gold/precision corpus chưa có |
| Arithmetic checker không áp dụng mọi bảng | E13/E28 | Source; tolerance/điều kiện khác nhau được ghi riêng |
| Legacy comparability có gates khác corporate | E29 | Source reading, không tuyên bố homogeneous semantics |
| Parent output/Phase1 dependency và corpus CLI khác v2 | E30/E31 | Source; source-only clone không có corpus ngoài |
| History/cache là dữ liệu local cần bảo vệ | E03/E32 | Code + reopen/resume tests |
| API tests chỉ mock | E33 | Test implementation + log đợt kiểm chứng |
| Package không cần Docker, chỉ source-only review | E34 và DISTRIBUTION_STATUS.md | Implementation + packaging tests/ZIP verification |
| Examples được tạo bằng parser thật + fake reader | E35, examples/README.md | Smoke thực thi, không model/PDF accuracy |
| Third-party license/version snapshot | E36 | Installed metadata, không legal clearance |

Không lấy tên file `final`, test PASS hoặc ghi chú mô hình làm bằng chứng đã đọc
đúng PDF. Không gọi generic error 400 là quota/billing chắc chắn. Các quyết định
kiến trúc chưa có ADR/lý do lịch sử được ghi chưa xác định, không bịa rationale.
