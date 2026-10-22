# Property inventory từ JSON Schema

Sinh bởi `scripts/handover_reference.py`; không thay schema runtime.
Required theo đúng object cha; `conditional` nghĩa là allOf/if/then, không phải mọi record.
Không có type/description trong schema được ghi chưa khai báo, không tự suy diễn.

## contracts/corporate_extract_v1/manifest_schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "corporate-extract-manifest-1.0"} |
| /batch_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /files | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |
| /files/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /files/*/document_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /files/*/report_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 2000, "maximum": 2100} |
| /files/*/report_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["ESG", "Financial"]} |
| /files/*/financial_scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["Separate", "Consolidated", null]} |
| /files/*/pdf_path | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /files/*/pdf_sha256 | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {"pattern": "^[0-9a-f]{64}$"} |
| /files/*/json_path | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /files/*/json_sha256 | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {"pattern": "^[0-9a-f]{64}$"} |
| /files/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["delivered", "partial", "unavailable"]} |
| /files/*/reason | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |

## contracts/corporate_extract_v1/schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "corporate-extract-1.0"} |
| /document | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /document/document_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /document/company_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /document/report_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["ESG", "Financial"]} |
| /document/source_document_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["sustainability_report", "annual_report", "financial_statement"]} |
| /document/report_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 2000, "maximum": 2100} |
| /document/financial_scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["Separate", "Consolidated", null]} |
| /document/reporting_entity | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /document/reporting_period_start | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /document/reporting_period_end | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /document/publication_date | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /document/source | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /document/source/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /document/source/file_name | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /document/source/url | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /document/source/downloaded_at_utc | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | không | trực tiếp | {} |
| /document/source/sha256 | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {"pattern": "^[0-9a-f]{64}$"} |
| /document/source/page_count | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /document/source/page_system | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "physical_pdf_page_1_based"} |
| /document | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | conditional allOf | {} |
| /document | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | conditional then | {} |
| /document/financial_scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {"enum": ["Separate", "Consolidated"]} |
| /document/source_document_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {"const": "financial_statement"} |
| /document | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | conditional allOf | {} |
| /document | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | conditional then | {} |
| /document/financial_scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {"const": null} |
| /coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /coverage/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["complete", "partial", "failed"]} |
| /coverage/scope_description | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /coverage/search_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["not_searched", "partial_search", "searched", "search_failed"]} |
| /coverage/pages_checked | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage/pages_checked/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | không | trực tiếp | {"minimum": 1} |
| /coverage/pages_unreadable | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage/pages_unreadable/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | không | trực tiếp | {"minimum": 1} |
| /coverage/topics_searched | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage/topics_searched/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp | {} |
| /coverage/search_outcomes | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage/search_outcomes/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /coverage/search_outcomes/*/topic | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /coverage/search_outcomes/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["not_searched", "searched_not_found", "parse_failure", "extraction_failure", "found"]} |
| /coverage/search_outcomes/*/pages | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage/search_outcomes/*/pages/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | không | trực tiếp | {"minimum": 1} |
| /coverage/search_outcomes/*/reason | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /records | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/record | {} |
| /records/*/record_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record | {} |
| /records/*/dimension | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["E", "S", "G", "X"]} |
| /records/*/record_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["claim", "measurement", "target", "policy", "governance_evidence", "financial_measurement"]} |
| /records/*/topic | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record | {} |
| /records/*/metric_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/metric_label | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record | {} |
| /records/*/metric_definition | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/statement | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp; #/$defs/record | {} |
| /records/*/statement/original_quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record | {} |
| /records/*/statement/interpretation | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/statement/assertion_kind | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["reported_result", "target", "plan", "policy", "context", "unknown"]} |
| /records/*/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp; #/$defs/record | {} |
| /records/*/value/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["available", "missing", "ambiguous", "unknown", "not_applicable"]} |
| /records/*/value/original_value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/value/original_unit | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/value/original_scale | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/value/normalized_value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["number", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/value/normalized_unit | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/value/normalization_factor | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["number", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/value/normalization_note | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp; #/$defs/record | {} |
| /records/*/period/observation_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period/observation_start | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period/observation_end | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period/measurement_date | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period/period_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["annual", "at_date", "quarter", "half_year", "range", "unknown"]} |
| /records/*/period/year_basis | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["explicit_quote", "table_header", "reviewed_context", "unknown"]} |
| /records/*/period/baseline_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period/target_deadline | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/boundary | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp; #/$defs/record | {} |
| /records/*/boundary/reporting_entity | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/boundary/consolidation | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["Separate", "Consolidated", "not_applicable", "unknown"]} |
| /records/*/boundary/scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/boundary/population | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/boundary/counting_method | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/boundary/calculation_method | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/boundary/verified | Chưa có description trong schema; xem dictionary nghiệp vụ. | "boolean" | có | trực tiếp; #/$defs/record | {} |
| /records/*/restatement | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp; #/$defs/record | {} |
| /records/*/restatement/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["unknown", "not_restatement_reported", "restated", "ambiguous"]} |
| /records/*/restatement/note | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/evidence | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/record | {"minItems": 1} |
| /records/*/evidence/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/evidence_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/source_sha256 | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record; #/$defs/evidence | {"pattern": "^[0-9a-f]{64}$"} |
| /records/*/evidence/*/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp; #/$defs/record; #/$defs/evidence | {"minimum": 1} |
| /records/*/evidence/*/printed_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/exact_quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/context_text | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/section | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/element_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/char_start | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {"minimum": 0} |
| /records/*/evidence/*/char_end | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {"minimum": 1} |
| /records/*/evidence/*/bbox | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["array", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/bbox | {"minItems": 4, "maxItems": 4} |
| /records/*/evidence/*/bbox/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "number" | không | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/bbox | {} |
| /records/*/evidence/*/table_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/row | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/column | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/headers | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/headers/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header | {} |
| /records/*/evidence/*/headers/*/role | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header | {"enum": ["year", "unit", "row_label", "caption", "other"]} |
| /records/*/evidence/*/headers/*/text | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header | {} |
| /records/*/evidence/*/headers/*/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header | {"minimum": 1} |
| /records/*/evidence/*/headers/*/row | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header | {} |
| /records/*/evidence/*/headers/*/column | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header | {} |
| /records/*/evidence/*/headers/*/bbox | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["array", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header; #/$defs/bbox | {"minItems": 4, "maxItems": 4} |
| /records/*/evidence/*/headers/*/bbox/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "number" | không | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/header; #/$defs/bbox | {} |
| /records/*/evidence/*/footnotes | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/record; #/$defs/evidence | {} |
| /records/*/evidence/*/footnotes/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/footnote | {} |
| /records/*/evidence/*/footnotes/*/text | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/footnote | {} |
| /records/*/evidence/*/footnotes/*/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/footnote | {"minimum": 1} |
| /records/*/evidence/*/footnotes/*/bbox | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["array", "null"] | có | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/footnote; #/$defs/bbox | {"minItems": 4, "maxItems": 4} |
| /records/*/evidence/*/footnotes/*/bbox/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "number" | không | trực tiếp; #/$defs/record; #/$defs/evidence; #/$defs/footnote; #/$defs/bbox | {} |
| /records/*/quality | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp; #/$defs/record | {} |
| /records/*/quality/extraction_method | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["manual", "rule", "cloud_llm", "chatgpt_assisted", "other"]} |
| /records/*/quality/parser_name | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/quality/model_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/quality/prompt_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/quality/uncertainty | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/record | {} |
| /records/*/quality/uncertainty/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp; #/$defs/record | {} |
| /records/*/quality/review_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["pending_human_review", "reviewed", "rejected"]} |
| /records/*/quality/reviewer | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/quality/reviewed_at_utc | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/quality/review_basis | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/comparison_group_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/record_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {"const": "financial_measurement"} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/dimension | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {"const": "X"} |
| /issue_log | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /issue_log/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /issue_log/*/issue_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /issue_log/*/code | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /issue_log/*/message | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /issue_log/*/source_pages | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /issue_log/*/source_pages/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | không | trực tiếp | {"minimum": 1} |
| /issue_log/*/record_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /issue_log/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["open", "resolved", "needs_review"]} |

## contracts/esg_v2.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "esg-candidates/2.1.0"} |
| /parser_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": [2, 3]} |
| /graph_ready | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /semantic_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "partial"} |
| /evidence | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /evidence/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /evidence/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "candidate"} |
| /evidence/*/boundary_verified | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /links | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /links/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /links/*/relation | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "candidate_context"} |
| /links/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "needs_review"} |
| /links/*/comparability | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /links/*/comparability/eligible | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /records | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /records/*/record_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["claim", "policy", "action", "target", "governance", "unknown", "metric", "measurement"]} |
| /records/*/original_text | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /records/*/source_refs | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |
| /records/*/domain | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | trực tiếp | {"const": "esg"} |
| /records/*/content_period | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["null", "object"] | có | trực tiếp | {} |
| /records/*/classification | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /records/*/classification/pillar | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["E", "S", "G", "unknown"]} |
| /records/*/classification/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "candidate"} |
| /records/*/review | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /records/*/review/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "needs_review"} |
| /records/*/review/verified_fields | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"maxItems": 0} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | conditional then | {} |
| /records/*/payload/unit | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | conditional then | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload/target_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | conditional then | {} |
| /records/*/payload/baseline_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | conditional then | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /issues | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /pending | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |

## contracts/financial_v2.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "esg-financial-candidates/2.3.0"} |
| /parser_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": [4, 5, 6]} |
| /graph_ready | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /semantic_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "partial"} |
| /records | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /records/*/record_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /records/*/record_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["metric", "measurement", "financial_context"]} |
| /records/*/domain | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | trực tiếp | {"const": "financial"} |
| /records/*/original_text | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /records/*/original_cells | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /records/*/source_refs | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |
| /records/*/source_refs/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp | {} |
| /records/*/data_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["available", "missing", "ambiguous", "unknown"]} |
| /records/*/review | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /records/*/review/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | trực tiếp | {"const": "needs_review"} |
| /records/*/review/verified_fields | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | không | trực tiếp | {"maxItems": 0} |
| /records/*/missing_fields | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /records/*/classification | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /records/*/classification/pillar | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | trực tiếp | {"const": "unknown"} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | conditional then | {} |
| /records/*/payload/raw_value | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | conditional then | {} |
| /records/*/payload/parsed_value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | conditional then | {"pattern": "^-?[0-9]+(?:\\.[0-9]+)?$"} |
| /records/*/payload/normalized_value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | conditional then | {} |
| /records/*/payload/unit | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | conditional then | {} |
| /records/*/payload/currency | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | conditional then | {} |
| /records/*/payload/scale | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | conditional then | {"enum": [null, "1", "1000", "1000000", "1000000000"]} |
| /records/*/payload/statement_scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | conditional then | {"enum": [null, "separate", "consolidated"]} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional allOf | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /records/*/payload | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | conditional then | {} |
| /links | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /links/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /links/*/relation_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "metric_measurement"} |
| /links/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "candidate"} |
| /table_continuations | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /table_continuations/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /table_continuations/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["rule_matched", "rejected"]} |
| /table_continuations/*/review_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "needs_review"} |
| /table_continuations/*/reasons | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /table_continuations/*/reasons/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp | {} |
| /table_continuations/*/sources | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /notes_coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /notes_coverage/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /metadata | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /semantic_coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /semantic_coverage/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "partial"} |
| /semantic_coverage/pages | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /semantic_coverage/tables | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /arithmetic_checks | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /arithmetic_checks/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /arithmetic_checks/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["pass", "mismatch", "not_checked"]} |
| /hierarchy_relationships | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /esg_relevant_disclosures | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /issues | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /issues/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /pending | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |

## contracts/gemini_extract.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "gemini-report-candidates/1.0"} |
| /provider | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "gemini_api"} |
| /graph_ready | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /semantic_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "partial"} |
| /profile_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /model | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /reports | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1, "maxItems": 1} |
| /source_artifacts | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |
| /issues | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /coverage/total_pages | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /coverage/pages | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage/pages/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /coverage/pages/*/pdf_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /coverage/pages/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["pending", "processed", "failed"]} |
| /records | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /records/*/review | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /records/*/review/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | trực tiếp | {"const": "needs_review"} |
| /records/*/review/verified_fields | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | trực tiếp | {"const": []} |
| /records/*/extraction_provenance | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /records/*/extraction_provenance/provider | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "gemini_api"} |
| /records/*/extraction_provenance/is_gold | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /records/*/extraction_provenance/factual_accuracy_verified | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |

## contracts/gemini_response.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /records | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"maxItems": 200} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/record | {} |
| /records/*/record_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["measurement", "claim", "policy", "action", "target", "governance", "financial_context"]} |
| /records/*/domain | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["financial", "esg", "context"]} |
| /records/*/pillar | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["E", "S", "G", "unknown"]} |
| /records/*/label_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record | {} |
| /records/*/value_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/unit_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["integer", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/measurement_date | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period_start | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/period_end | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/reporting_entity | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/consolidation_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/scope_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp; #/$defs/record | {} |
| /records/*/interpretation_notes | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/record | {} |
| /records/*/interpretation_notes/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp; #/$defs/record | {} |
| /records/*/evidence | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/record | {"minItems": 1, "maxItems": 30} |
| /records/*/evidence/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/record | {} |
| /records/*/evidence/*/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp; #/$defs/record | {} |
| /records/*/evidence/*/role | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/record | {"enum": ["label", "value", "column_header", "unit", "narrative", "date", "boundary"]} |
| /records/*/evidence/*/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/record | {} |
| /page_reviews | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /page_reviews/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /page_reviews/*/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {} |
| /page_reviews/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["read", "unreadable", "no_relevant_data"]} |
| /page_reviews/*/note | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /metadata | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /metadata/company_name | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | có | trực tiếp; #/$defs/meta | {} |
| /metadata/company_name/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/company_name/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/company_name/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/reporting_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | có | trực tiếp; #/$defs/meta | {} |
| /metadata/reporting_year/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/reporting_year/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/reporting_year/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/statement_scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | có | trực tiếp; #/$defs/meta | {} |
| /metadata/statement_scope/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/statement_scope/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/meta | {} |
| /metadata/statement_scope/physical_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp; #/$defs/meta | {} |
| /warnings | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /warnings/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp | {} |

## contracts/local_llm_extract.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "local-llm-extract/1.0"} |
| /graph_ready | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /is_gold | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /semantic_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "partial"} |
| /records | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /records/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /records/*/record_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /records/*/record_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["measurement", "claim", "policy", "action", "target", "governance", "financial_context"]} |
| /records/*/domain | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["financial", "esg", "context"]} |
| /records/*/parsed_value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /records/*/evidence | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |
| /records/*/evidence/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /records/*/quality | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /records/*/quality/review_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "pending_human_review"} |
| /records/*/quality/boundary_verified | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /records/*/quality/is_gold | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /records/*/quality/verdict | Chưa có description trong schema; xem dictionary nghiệp vụ. | "null" | có | trực tiếp | {} |
| /coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /coverage/semantic_completeness_verified | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /validation | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /validation/factual_accuracy_verified | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | không | trực tiếp | {"const": false} |

## contracts/local_llm_response.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /candidates | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"maxItems": 20} |
| /candidates/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/candidate | {} |
| /candidates/*/record_type | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/candidate | {"enum": ["measurement", "claim", "policy", "action", "target", "governance", "financial_context"]} |
| /candidates/*/domain | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/candidate | {"enum": ["financial", "esg", "context"]} |
| /candidates/*/pillar | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp; #/$defs/candidate | {"enum": ["E", "S", "G", "unknown"]} |
| /candidates/*/label | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate | {} |
| /candidates/*/evidence | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/candidate | {"minItems": 1, "maxItems": 20} |
| /candidates/*/evidence/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp; #/$defs/candidate; #/$defs/citation | {} |
| /candidates/*/evidence/*/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/citation | {} |
| /candidates/*/evidence/*/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/citation | {} |
| /candidates/*/fields | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp; #/$defs/candidate | {} |
| /candidates/*/fields/value_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/value_raw/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/value_raw/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/value_raw/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/unit_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/unit_raw/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/unit_raw/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/unit_raw/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/year/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/year/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/year/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_start_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_start_raw/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_start_raw/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_start_raw/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_end_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_end_raw/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_end_raw/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/period_end_raw/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/measurement_date_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/measurement_date_raw/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/measurement_date_raw/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/measurement_date_raw/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/reporting_entity | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/reporting_entity/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/reporting_entity/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/reporting_entity/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/consolidation_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/consolidation_raw/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/consolidation_raw/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/consolidation_raw/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/scope_raw | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/scope_raw/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/scope_raw/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/scope_raw/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/baseline_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/baseline_year/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/baseline_year/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/baseline_year/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/target_year | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["object", "null"] | không | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/target_year/value | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "integer"] | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/target_year/source_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/fields/target_year/quote | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp; #/$defs/candidate; #/$defs/field | {} |
| /candidates/*/notes | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp; #/$defs/candidate | {"maxItems": 20} |
| /candidates/*/notes/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp; #/$defs/candidate | {} |
| /warnings | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"maxItems": 30} |
| /warnings/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | không | trực tiếp | {} |

## contracts/source_v2.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /batch | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /batch/schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "esg-source/2.0.0"} |
| /batch/capture_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["completed", "partial"]} |
| /batch/semantic_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "not_started"} |
| /batch/graph_ready | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /batch/profile_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /batch/record_count | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": 0} |
| /batch/block_count | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 0} |
| /batch/issue_count | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 0} |
| /companies | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"maxItems": 0} |
| /reports | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1, "maxItems": 1} |
| /reports/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /reports/*/report_version_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /reports/*/source_sha256 | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {"pattern": "^[a-f0-9]{64}$"} |
| /reports/*/source_access | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "source.pdf"} |
| /reports/*/company_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /reports/*/report_scope | Chưa có description trong schema; xem dictionary nghiệp vụ. | "null" | có | trực tiếp | {} |
| /reports/*/publication_date | Chưa có description trong schema; xem dictionary nghiệp vụ. | "null" | có | trực tiếp | {} |
| /reports/*/pdf_page_count | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /source_artifacts | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"minItems": 1} |
| /source_artifacts/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /source_blocks | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /source_blocks/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /source_blocks/*/block_id | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /source_blocks/*/original_text | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["string", "null"] | có | trực tiếp | {} |
| /source_blocks/*/original_cells | Chưa có description trong schema; xem dictionary nghiệp vụ. | ["array", "null"] | có | trực tiếp | {} |
| /source_blocks/*/disposition | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "pending_semantic_extraction"} |
| /source_blocks/*/source | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /source_blocks/*/source/pdf_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /source_blocks/*/source/printed_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "null" | có | trực tiếp | {} |
| /records | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"maxItems": 0} |
| /evidence | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"maxItems": 0} |
| /links | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {"maxItems": 0} |
| /coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /coverage/total_pages | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /coverage/counts | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /coverage/pages | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /coverage/pages/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /coverage/pages/*/pdf_page | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /coverage/pages/*/status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["pending", "processed", "partial", "failed", "confirmed_blank"]} |
| /coverage/pages/*/attempts | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 0} |
| /issues | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /issues/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |

## schemas/upload-export.inferred.schema.json

| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |
| --- | --- | --- | --- | --- | --- |
| /schema_version | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "esg-upload/2.0.0"} |
| /pipeline | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"enum": ["source-typed-v2", "gemini-pdf-v1"]} |
| /document_count | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 1} |
| /documents | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /documents/* | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | không | trực tiếp | {} |
| /documents/*/document_index | Chưa có description trong schema; xem dictionary nghiệp vụ. | "integer" | có | trực tiếp | {"minimum": 0} |
| /documents/*/filename | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /documents/*/capture_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
| /documents/*/coverage | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /documents/*/output | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /documents/*/native_artifacts | Chưa có description trong schema; xem dictionary nghiệp vụ. | "object" | có | trực tiếp | {} |
| /failures | Chưa có description trong schema; xem dictionary nghiệp vụ. | "array" | có | trực tiếp | {} |
| /graph_ready | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": false} |
| /semantic_status | Chưa có description trong schema; xem dictionary nghiệp vụ. | "chưa khai báo" | có | trực tiếp | {"const": "partial"} |
| /source_note | Chưa có description trong schema; xem dictionary nghiệp vụ. | "string" | có | trực tiếp | {} |
