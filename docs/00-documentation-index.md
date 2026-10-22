# Bộ tài liệu bàn giao ESG Tracker

Ngày kiểm tra: **22/10/2026**, Windows/Python 3.12. Đây là tài liệu của cây mã
hiện tại, không phải tuyên bố release đã đủ điều kiện phân phối.

Nhãn thống nhất: **ĐÃ XÁC MINH** = đọc implementation hoặc chạy kiểm tra được nêu;
**CHƯA XÁC MINH** = thiếu môi trường/nhãn/quyền hoặc chưa chạy;
**ĐỀ XUẤT** = chưa triển khai. “Đã xác minh code có chức năng” khác “đã chạy live”.

## Lộ trình đọc

| Người đọc | Bắt đầu | Đọc tiếp |
| --- | --- | --- |
| Người dùng mới | [Tổng quan](01-system-overview.md), [cài đặt](04-installation-and-configuration.md) | [Sử dụng](05-user-guide.md), [đọc JSON](08-json-contract-and-data-dictionary.md) |
| Kỹ sư tiếp quản | [Kiến trúc](02-architecture-and-data-flow.md), [cấu trúc](03-project-structure.md) | [pipeline](07-extraction-pipelines.md), [CLI](10-api-cli-reference.md) |
| Người kiểm tra dữ liệu | [Validation](09-validation-and-quality.md) | [quality workflow hiện có](QUALITY_REVIEW.md), [gold Oil & Gas](OIL_GAS_GOLD.md) |
| Người vận hành | [Vận hành](11-deployment-and-operations.md) | [troubleshooting](12-troubleshooting.md), [bảo mật](13-security-and-data-handling.md) |
| Người phát hành | [Kiểm chứng](14-testing-and-verification.md) | [đóng gói](15-packaging-and-release.md), [checklist](18-handover-checklist.md) |

Các chương còn lại: [tools/dependencies](06-tools-and-dependencies.md),
[bảo trì](16-maintenance-and-extension.md), [giới hạn](17-limitations-and-known-issues.md),
[evidence register](evidence-register.md).

## Tham chiếu sinh từ source, không phải tài liệu viết đoán

- [Module/symbol index](reference/module-index.json): source hash, class/function, imports.
- [Hồ sơ signature/docstring của từng module](reference/module-profiles.md).
- [Kiểm kê từng file](reference/component-inventory.csv).
- [Mọi property tìm được trong schema](reference/schema-fields.md).
- [Dependency/license metadata](reference/dependencies.json).
- [Constraints quan sát được](reference/dependency-constraints.txt): **không phải lockfile portable**.
- [Kết quả kiểm tra bàn giao](reference/verification.md).
- [Ví dụ JSON tổng hợp](../examples/README.md), [schema catalog](../schemas/README.md).

## Tài liệu cũ và tài liệu này

Giữ nguyên hướng dẫn chuyên sâu: SOURCE_V2_USAGE, FINANCIAL_V2_USAGE, ESG_V2_USAGE,
CORPORATE_HANDOFF_USAGE, EXTRACTION_HISTORY, OCR_CRASH_RECOVERY, LOCAL_LLM,
GEMINI_INTEGRATION. Các IMPLEMENTATION_REPORT/INPUT_ANALYSIS/tài liệu có ngày là
lịch sử; khi khác nhau, đối chiếu **code + evidence + phiên bản output**, không mặc
định văn bản mới hơn luôn đúng. Không thay thế code bằng đặc tả tương lai
EXTRACTION_REQUIREMENTS_DESIGN_V2.

Quickstart offline nhỏ nhất:

```powershell
# Từ thư mục chứa app.py, với .venv đã cài requirements
.\.venv\Scripts\python.exe -B scripts/handover_smoke.py --destination outputs/first_smoke_moi
.\.venv\Scripts\python.exe -B scripts/check_handover.py
```

Lệnh đầu dùng page reader giả lập, không kiểm OCR/API. Không dùng lại thư mục đích.
