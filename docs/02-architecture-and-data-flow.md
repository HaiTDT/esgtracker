# 02. Kiến trúc và luồng dữ liệu

```mermaid
flowchart TD
  U[Người dùng / PDF] --> UI[Dash upload_analysis]
  UI --> W[extraction_worker / upload_worker subprocess]
  W --> R[upload_v2: validate / metadata / engine]
  R -->|Docling mặc định| C[source_v2 + page worker]
  C --> F[financial_v2 + semantics / notes / columns]
  C --> E[esg_v2 + tables: ESG và annual]
  R -->|Consent + server key| G[Gemini API / PDF fragments]
  C -->|CLI riêng| O[Ollama local / text chunks]
  F --> S[Native JSON + checkpoints + coverage]
  E --> S
  G --> S
  S --> H[History / PDF review / correction overlay]
  H --> J[Portable upload JSON / corporate ZIP]
  O --> L[local-llm-extract JSON riêng]
  DB[SQLite dashboard lưu trữ] -. import và pipeline riêng .-> D[Archive dashboard]
```

Ranh giới cloud chỉ ở Gemini được chọn rõ ràng. Local Docling có thể tải model khi
chưa có cache, nhưng không phải gọi LLM cloud để trích xuất. Ollama chỉ nhận origin
loopback và model đã cài, không tự pull hoặc fallback cloud. Không có REST service
extract công khai được triển khai; Dash callback là giao diện chính.

## Trình tự một upload

```mermaid
sequenceDiagram
  participant U as Browser
  participant D as Dash
  participant W as Upload worker
  participant P as Parser / provider
  participant FS as Local storage
  U->>D: PDF base64 + metadata + engine
  D->>FS: request/status theo job UUID
  D->>W: subprocess + môi trường máy chủ
  W->>W: kiểm file, giới hạn, nhận diện metadata
  W->>P: xử lý theo trang / batch
  P->>FS: checkpoint + hash + output
  W->>FS: run_manifest + result/status
  D->>FS: poll và mở history
  D-->>U: records, coverage, issues, download
```

`request.json` chứa nội dung báo cáo base64, là dữ liệu nhạy cảm, dù không chứa API
key. Worker log không phải JSON protocol. PDF giữ nguyên bytes; chuẩn hóa/diễn giải
nằm trong record hoặc correction layer, không ghi đè nguồn.

## Lỗi và recovery thực tế

```mermaid
flowchart LR
  X[Trang / batch] --> Q{Có checkpoint hợp lệ?}
  Q -->|thành công cùng profile| K[Dùng lại]
  Q -->|chưa có hoặc retry| A[Gọi reader / provider]
  A -->|thành công| C[Lưu processed]
  A -->|timeout / crash / invalid| F[Lưu failed hoặc partial / issue]
  F --> N[Còn trang / ngân sách thì tiếp tục theo engine]
  N --> P[Kết quả partial, không coi là đầy đủ]
  P --> R[Tải lại cùng PDF + metadata + profile]
  R --> Q
```

Docling capture có retry theo trang; OS workspace lock giải phóng khi process chết.
Gemini có request cap theo lượt, retry mặc định 0; 400/401/403/404/429 dừng batch
chưa gửi trong lượt đó. Trang pending không có nghĩa không công bố. Changing
code/profile/model/metadata có thể tạo cache mới, không chắc reuse hoặc không tốn phí.
Xem `source_v2.capture_pdf`, `gemini.extract_pdf`, `local_llm.extract_local_llm`.
