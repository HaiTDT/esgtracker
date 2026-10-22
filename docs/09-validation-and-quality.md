# 09. Validation khác accuracy và completeness

| Lớp kiểm tra | Đã triển khai | Chưa chứng minh |
| --- | --- | --- |
| JSON syntax | JSON parser/atomic_json allow_nan=False | Nội dung đúng |
| Schema | contracts + Draft202012Validator | Field nhìn đúng trong PDF |
| Source/reference | Path boundary, SHA256, block/pointer/ID/count checks | OCR hay model không bịa/đọc nhầm |
| Nghiệp vụ | Parse số/scale/kỳ candidates, scope/metric exclusions, một số công thức | Mọi chuẩn kế toán/ESG đều được bao phủ |
| Accuracy | Evaluator đã có | Chưa có human gold corpus được duyệt, chưa có precision thật |
| Completeness | Coverage page/block/table, pending/issue | processed hết trang không chứng minh không bỏ sót KPI |

`source_v2.validate_source_bundle`, `financial_v2`/`esg_v2` validation, corporate
contract validator và `scripts/audit_corporate_handoff.py` kiểm nhiều điều kiện khác
nhau. Audit Gemini chỉ resolve **model observation quote**, đếm riêng native quote;
không gọi đây là đối chiếu PDF độc lập. Không dùng cùng output model làm gold OCR.

## Công thức và mức sai số

`financial_semantics_v3.arithmetic_checks` dựa trên công thức explicit trong row và
operand/kỳ tương thích; code có tolerance ở đơn vị trình bày `(số operand + 1)/2`.
Không áp dụng công thức vào hàng không đủ code/kỳ/nguồn. Kết quả mismatch tạo issue.
`src/quality/checks.py:financial_formula_checks` là checker khác: chỉ same-table,
same-column, same-year/unit/scale/scope, code duy nhất, so residual Decimal chính
xác và đề nghị review rounding. Không khẳng định hai checker có cùng tolerance.

Phân loại metric có exclusions cho khoản tiền nhân sự; chưa phải ontology chuẩn
được chuyên gia xác nhận. Duplicate IDs/references được kiểm trong output; semantic
duplicate giữa sections/PDF khác chưa được giải quyết toàn diện. Bảng nhiều trang,
header lặp, chart còn cần review coverage, không tự suy dữ liệu không công bố.

## Đo bằng gold độc lập

Workflow hiện có ở [QUALITY_REVIEW](QUALITY_REVIEW.md) và [OIL_GAS_GOLD](OIL_GAS_GOLD.md).
Template chứa expected rỗng, gợi ý không phải nhãn chuẩn. Người gán phải đọc PDF,
thêm nội dung bị bỏ sót, loại candidate sai, chọn field, ghi reviewer/scope/split.
BSR đã dùng phát triển rule nên là dev, không phải holdout test độc lập.

`quality_benchmark.py evaluate` từ chối draft và leakage cùng PDF dev/test. Strict
TP yêu cầu tất cả expected field đúng; sai số/năm/unit có thể FP + FN. Có precision,
recall/F1, field accuracy với support, CER/WER nếu có bản chép độc lập. Mẫu số rỗng
trả null. Đơn vị chỉ gán một số anchor không cho phép suy recall toàn corpus.
Quality cặp ESG–BCTC cần gold riêng về definition/kỳ/boundary, chưa được benchmark.

**ĐỀ XUẤT lấy mẫu:** holdout theo doanh nghiệp/PDF, phân tầng text/scan/chart/table
nối trang, ba loại báo cáo và cả trang không có candidate. Hai annotator độc lập,
adjudication, khoá prediction trước khi chấm. Không tuyên bố cỡ mẫu đại diện khi
chưa có thiết kế thống kê.

| Nhóm lỗi | Mức vận hành đề nghị (chưa engine severity mới) | Cách review |
| --- | --- | --- |
| Sai số, dấu, scale, currency, kỳ/phạm vi | Critical cho so sánh | Tạm chặn numeric comparison, đọc row/header/PDF |
| Bỏ sót/trích thừa/double-count | High | Gán đủ scope trang, audit cả candidate lẫn phần không thấy |
| Đọc nhầm nguyên văn/quote/page | High | Đối chiếu PDF/ảnh độc lập, không sửa original để che lỗi |
| Topic/metric mapping, actual vs target | High | So definition/exclusions và temporal semantics |
| Typo không đổi nghĩa | Theo ngữ cảnh | Ghi correction có nguồn; không tự hạ mức nếu ảnh hưởng chỉ tiêu |

293 tests của đợt cleanup và các tests mới chỉ là regression phần mềm, không phải
“accuracy 100%”. Hệ thống chưa đủ cơ sở công bố bất kỳ phần trăm corpus accuracy nào.
