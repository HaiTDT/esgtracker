# 16. Bảo trì và mở rộng

Không chỉnh trực tiếp PDF/native JSON/history để sửa parser. Giữ raw + correction
overlay, ghi lý do/ticket, tạo fixture nhỏ, sửa code có regression tests và parser/
profile version đúng. Sửa config/từ điển cũng có thể làm review stale.

| Thay đổi muốn làm | Điểm cần đọc trước | Kiểm bắt buộc |
| --- | --- | --- |
| Công ty/tên file mới | toolkit.build_document_spec, extraction_toolkit.yml | Company/year/type override, date prefix, unknown company |
| Chỉ tiêu/đơn vị mới | metric_dictionary.yml, metrics.yml, quality.dictionary, corporate_review | Definition/exclusions, unit/scale, money vs headcount, period/boundary |
| Layout BCTC mới | financial_column_mapping, financial_context_v2, financial_semantics_v3, notes_v2 | Header/code/value match, comparative/opening/restated, continuation, raw/source invariant |
| ESG policy/target mới | esg_v2.build_candidates, esg_tables_v2, esg_v2.yml | Negation, actual vs target, missing boundary, scope2 method distinction |
| Annual unified parser | upload_v2 routing, ESG contract/corporate adapter | ĐỀ XUẤT mới, không đổi route cũ âm thầm; contract + migration + duplicate semantics |
| Model/provider mới | gemini/local_llm settings/client/PROMPT/contracts | Consent/key/data route, truncation/schema, request budget, provenance, cost; live acceptance riêng |
| UI review | human_review.py, quality.review_store/records | Required fields, partial review, stale/dependency invalidation, no automatic gold |
| Schema mới | contracts + writers + exports + schema dictionary generator | Backward compatibility policy, version/migration, replay fixture; chưa có converter chung |
| Packaging mới | package_handover.py + tests/test_handover.py | No secret/data/link leakage, repeatable paths/hash, no overwrite |

Không tự cập nhật score/cặp dựa trên một field correction mà bỏ qua scope/dependency.
Các extension cần ADR nêu input/output, compatibility, provenance, review gates và
chi phí. Không dùng BSR dev làm holdout test sau khi chỉnh rule; bổ sung doanh nghiệp
độc lập và gold có provenance.

Sau thay source/config/schema: chạy `handover_reference.py` để refresh chỉ mục/hash,
`check_handover.py`, tests cần thiết, regenerate examples nếu implementation thực
sự đổi và ghi là fixture mới. Không regenerate prediction để khớp gold đã xem.

Các backlog ưu tiên có căn cứ: safe Gemini error diagnostics (400), clean-install
acceptance, complete license review, gold evaluation và annual ontology/dedup.
Chúng là **ĐỀ XUẤT**, không được ghi đã triển khai bởi bộ tài liệu này.
