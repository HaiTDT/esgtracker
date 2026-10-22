# Danh mục schema

Schema runtime duy nhất nằm trong [contracts/](../contracts/); không sao chép sang
thư mục này để tránh drift. [Data dictionary sinh từ schema](../docs/reference/schema-fields.md)
liệt kê mọi property/required/conditional tìm được. Ý nghĩa nghiệp vụ và giới hạn
nằm trong [hợp đồng JSON](../docs/08-json-contract-and-data-dictionary.md).

`upload-export.inferred.schema.json` là schema **suy ra từ implementation**
`dashboard/upload_v2.py:export_result`, dùng kiểm tra tài liệu/mẫu, không được
gắn thêm vào runtime và không thay đổi output hiện tại. Nó không chứng minh
schema/semantics của từng `documents[].output`.
