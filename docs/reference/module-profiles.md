# Hồ sơ module/symbol sinh từ source

ĐÃ XÁC MINH: tên, chữ ký, annotation, docstring và dependency đọc từ source.
Annotation/docstring không phải kiểm chứng hành vi live. Không suy kiểu trả về khi không khai báo.
Luồng nghiệp vụ, cấu hình/timeout/retry, cài đặt và giới hạn xem các chương 04/06/07/17.

## src/__init__.py

ESG Tracker MVP package.

**Dependency/import:** .

## src/database/__init__.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `db`.

## src/database/adapters.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `__future__`, `json`, `pathlib`, `re`, `src.extraction.claims`.

### infer_metric_code — dòng 30

- Đầu vào (signature): `text: str`.
- Đầu ra annotation: `str | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### pillar_for — dòng 38

- Đầu vào (signature): `dimension: str | None`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### load_phase1_records — dòng 43

- Đầu vào (signature): `workspace_root: Path`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### numeric_value — dòng 57

- Đầu vào (signature): `value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### adapt_record — dòng 75

- Đầu vào (signature): `item: dict`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/database/db.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pandas`, `pathlib`, `sqlite3`, `src.paths`.

### connect — dòng 9

- Đầu vào (signature): `path: Path | str=DATABASE_PATH`.
- Đầu ra annotation: `sqlite3.Connection`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### initialize_database — dòng 18

- Đầu vào (signature): `path: Path | str=DATABASE_PATH`.
- Đầu ra annotation: `Path`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### fetch_df — dòng 25

- Đầu vào (signature): `query: str, params=(), path: Path | str=DATABASE_PATH`.
- Đầu ra annotation: `pd.DataFrame`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/database/output_sources.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `__future__`, `dataclasses`, `hashlib`, `json`, `pathlib`, `re`, `src.extraction.claims`, `typing`, `unicodedata`.

### discover_output_documents — dòng 31

- Đầu vào (signature): `output_root: Path`.
- Đầu ra annotation: `list[OutputDocument]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### read_json — dòng 52

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### sha256 — dòng 56

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### page_rows — dòng 64

- Đầu vào (signature): `document: OutputDocument`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### artifact_rows — dòng 77

- Đầu vào (signature): `document: OutputDocument`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _ascii_key — dòng 113

- Đầu vào (signature): `value: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### infer_output_metric — dòng 118

- Đầu vào (signature): `text: str`.
- Đầu ra annotation: `str | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### infer_unit — dòng 157

- Đầu vào (signature): `key: str, explicit: Any=None`.
- Đầu ra annotation: `str | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _first_page — dòng 180

- Đầu vào (signature): `node: dict, inherited: int | None=None`.
- Đầu ra annotation: `int`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _number — dòng 193

- Đầu vào (signature): `value: Any`.
- Đầu ra annotation: `float | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _pillar — dòng 211

- Đầu vào (signature): `path: tuple[str, ...], document_type: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _topic — dòng 219

- Đầu vào (signature): `metric_code: str | None, path: tuple[str, ...], pillar: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### iter_structured_facts — dòng 232

- Đầu vào (signature): `document: OutputDocument`.
- Đầu ra annotation: `Iterator[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### summary_claim_rows — dòng 284

- Đầu vào (signature): `document: OutputDocument`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Return human-readable claims from curated summaries, excluding QA notes.

### output_manifest — dòng 328

- Đầu vào (signature): `output_root: Path`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### walk — dòng 236

- Đầu vào (signature): `node: Any, path: tuple[str, ...]=(), inherited_page: int | None=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/database/sample_data.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `__future__`, `csv`, `pathlib`.

### build_sample — dòng 499

- Đầu vào (signature): ``.
- Đầu ra annotation: `tuple[list[dict], list[dict]]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### write_sample_csv — dòng 574

- Đầu vào (signature): `sample_dir: Path, claims: list[dict], metrics: list[dict]`.
- Đầu ra annotation: `None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/__init__.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `claims`, `toolkit`.

## src/extraction/claims.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `re`.

### classify_claim — dòng 10

- Đầu vào (signature): `text: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_attributes — dòng 25

- Đầu vào (signature): `text: str`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/corporate_handoff.py

Conservative, source-bound corporate-extract-1.0 delivery adapter.

This is an export boundary, not another OCR engine or a verification engine.
Unknown fields stay unknown. Native records/checkpoints remain separate review
artifacts; no candidate alias becomes a cross-report metric identity.

**Dependency/import:** `decimal`, `importlib.util`, `json`, `jsonschema`, `pathlib`, `re`, `shutil`, `src.extraction.corporate_review`, `src.extraction.financial_context_v2`, `src.extraction.financial_v2`, `src.extraction.gemini_handoff`, `src.extraction.source_v2`, `urllib.parse`, `zipfile`.

### validator_module — dòng 37

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _meta — dòng 44

- Đầu vào (signature): `output, name`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _source_bytes_checked — dòng 49

- Đầu vào (signature): `info, digest`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _bbox — dòng 61

- Đầu vào (signature): `value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _number — dòng 71

- Đầu vào (signature): `value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Do not silently round exact decimals through an IEEE float.

### _sources — dòng 84

- Đầu vào (signature): `record`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _unit — dòng 88

- Đầu vào (signature): `raw, observed`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Return literal unit + base unit/factor only for supported, observed units.

### _value — dòng 116

- Đầu vào (signature): `record, context, uncertainties, number_format='auto'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _period — dòng 168

- Đầu vào (signature): `record, headers, quote, uncertainties, column`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### convert_document — dòng 199

- Đầu vào (signature): `document, source_info=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Return one strict handoff; unresolved document scope blocks Financial export.

### build_delivery — dòng 383

- Đầu vào (signature): `result, destination, *, source_info=None, expected_bsr=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Create a new immutable delivery directory; partial is never certified complete.

### zip_delivery — dòng 499

- Đầu vào (signature): `folder, archive=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### issue — dòng 229

- Đầu vào (signature): `code, message, pages=(), record_id=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/corporate_review.py

Source-bound enrichment and review hypotheses, never adjudicated comparisons.

Metric IDs below are a versioned local vocabulary, not GRI/IFRS identifiers.
No generic report boundary is inherited by an ESG KPI.

**Dependency/import:** `copy`, `decimal`, `re`, `src.extraction.financial_context_v2`, `src.extraction.financial_v2`, `src.extraction.source_v2`, `src.quality.dictionary`.

### identify — dòng 20

- Đầu vào (signature): `label`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### review_topics — dòng 24

- Đầu vào (signature): `record`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Currency employment accounts cannot become workforce count candidates.

### _header — dòng 39

- Đầu vào (signature): `block, role='other'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _attach — dòng 45

- Đầu vào (signature): `record, blocks`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _issue — dòng 55

- Đầu vào (signature): `h, r, code, message`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _set_metric — dòng 63

- Đầu vào (signature): `r, key`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _amount — dòng 69

- Đầu vào (signature): `r, literal, factor, unit, scale=None, number_format='vi'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### enrich_records — dòng 88

- Đầu vào (signature): `handoff, native`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Mutates a fresh handoff only. Leaves raw native/checkpoint bytes untouched.

### recover_headcounts — dòng 188

- Đầu vào (signature): `handoff, native`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Extract dated headcounts from explicit note sentences, not account balances.

### build_review_queue — dòng 226

- Đầu vào (signature): `handoffs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/docling_backend.py

Docling conversion with full native JSON and explicit table coordinates.

**Dependency/import:** `contextlib`, `docling.backend.pypdfium2_backend`, `docling.datamodel.base_models`, `docling.datamodel.pipeline_options`, `docling.document_converter`, `hashlib`, `os`, `pathlib`, `pymupdf`, `re`, `shutil`, `threading`.

### table_rows — dòng 14

- Đầu vào (signature): `table`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Keep all cells, including empty and merged cells, without guessing years.

### ocr_profile — dòng 27

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Prefer installed Vietnamese Tesseract; no downloads or silent fallback.

### ocr_environment — dòng 46

- Đầu vào (signature): `ocr`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Docling's language discovery omits options.path; scope the workaround.

Call only while holding CONVERSION_LOCK. Restore any existing user setting.

### create_converter — dòng 65

- Đầu vào (signature): `ocr=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Shared local Docling profile; importing this module does not load models.

### convert_pdf — dòng 94

- Đầu vào (signature): `source: Path, max_pages=None, progress_callback=None, start_page=1`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### all_table_claims — dòng 131

- Đầu vào (signature): `spec, full, boundary`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/esg_tables_v2.py

Source-bound ESG table candidates; never a finding or verified boundary.

**Dependency/import:** `collections`, `re`, `src.extraction.financial_context_v2`, `src.extraction.financial_v2`, `src.extraction.source_v2`.

### metric_candidates — dòng 10

- Đầu vào (signature): `text, metrics`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### explicit_unit — dòng 17

- Đầu vào (signature): `raw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Accept a complete unit label, not a substring of an intensity unit.

### extract_esg_table — dòng 26

- Đầu vào (signature): `block, bundle, work, config, metrics, number_format`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### candidate_links — dòng 153

- Đầu vào (signature): `records, evidence, metrics`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### make — dòng 58

- Đầu vào (signature): `kind, slot, raw, selected`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### field — dòng 71

- Đầu vào (signature): `record, name, value, sources, reason='Explicit source cells only; no inferred defaults.'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### classify — dòng 77

- Đầu vào (signature): `record, labels, row`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/esg_v2.py

Review-only ESG text and table candidates. Separate from financial extraction.

Unparsed tables/charts retain explicit pending coverage, not silently omitted.
Keyword classifications are provisional, not factual validation or scoring.

**Dependency/import:** `collections`, `datetime`, `json`, `jsonschema`, `pathlib`, `re`, `src.extraction.esg_tables_v2`, `src.extraction.financial_context_v2`, `src.extraction.financial_notes_v2`, `src.extraction.source_v2`, `yaml`.

### unique_year — dòng 22

- Đầu vào (signature): `text, pattern`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### explicit_fields — dòng 27

- Đầu vào (signature): `kind, raw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### build_candidates — dòng 80

- Đầu vào (signature): `block, section, report, config`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_esg — dòng 141

- Đầu vào (signature): `work, config_path=None, number_format='auto'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate_esg — dòng 229

- Đầu vào (signature): `output, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/financial_column_mapping.py

Source-only repairs for misindexed headers and combined amount cells.

Never changes native checkpoints or supplies a code/value from a dictionary.
Geometry, observed headers and body cells must agree; otherwise abstain.

**Dependency/import:** `re`, `src.extraction.financial_context_v2`.

### code_header — dòng 11

- Đầu vào (signature): `text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### resolve_code_columns — dòng 15

- Đầu vào (signature): `headers, indexed, label_column`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### split_amount_pair — dòng 50

- Đầu vào (signature): `index, cell, row, headers`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Return two virtual cells only for two explicit, aligned period columns.

Substring spans point into the unchanged native cell. The bbox remains the
whole native cell, NOT an invented token bbox. No splitting of spaced integers.

## src/extraction/financial_context_v2.py

Evidence-based statement scope and conservative adjacent-page continuation.

Never infer KPI entity boundary from financial statement scope. OCR text is not
repaired. A continuation is a reviewable rule match, not manual verification.

**Dependency/import:** `re`, `src.extraction.source_v2`, `unicodedata`.

### normalized — dòng 12

- Đầu vào (signature): `text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### scope_candidate — dòng 17

- Đầu vào (signature): `block`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### resolve_scope — dòng 40

- Đầu vào (signature): `block, bundle`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### title_context — dòng 52

- Đầu vào (signature): `context`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### column_count — dòng 66

- Đầu vào (signature): `block`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### header_signature — dòng 70

- Đầu vào (signature): `headers`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### continuation_decision — dòng 79

- Đầu vào (signature): `previous, current, page_statuses, first_on_page, last_on_previous, unit_reader`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Require explicit continuation + same title/columns, reject conflicts/gaps.

## src/extraction/financial_layout_recovery.py

Conservative recovery of missed statement tables from searchable OCR words.

Only pages with an explicit primary-statement title and explicit metric/code/
current/comparative headers qualify. Coordinates are PDF points, TOPLEFT.
No company-specific names, values, row counts or page numbers are configured.
Docling's texts remain unchanged. Derived tables are labelled for review.

**Dependency/import:** `re`, `src.extraction.financial_context_v2`.

### recover_statement_table — dòng 13

- Đầu vào (signature): `document, words, page_height`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add — dòng 55

- Đầu vào (signature): `text, row, col, box, header=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/financial_notes_v2.py

Source-preserving note paragraphs with deterministic, review-only tags.

No financial/ESG judgment, no inferred periods or KPI entities, no OCR repair.
Paragraphs remain separate records; section context can cross processed pages.

**Dependency/import:** `json`, `re`, `src.extraction.financial_context_v2`, `src.extraction.source_v2`.

### ordered_blocks — dòng 25

- Đầu vào (signature): `bundle, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Native body ordering, including nested groups; flag unreachable text blocks.

### extract_notes — dòng 56

- Đầu vào (signature): `bundle, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### disposition — dòng 63

- Đầu vào (signature): `block, status, record_id=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### visit — dòng 36

- Đầu vào (signature): `ref`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/financial_semantics_v3.py

Evidence-backed report metadata, periods, semantic coverage and checks.

This layer never overwrites raw OCR cells or equates source coverage with
semantic completeness. Rules are candidates; no automated audit verdict.

**Dependency/import:** `ast`, `collections`, `datetime`, `decimal`, `re`, `src.extraction.financial_context_v2`, `src.extraction.financial_notes_v2`, `src.extraction.source_v2`.

### source_evidence — dòng 17

- Đầu vào (signature): `block`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### dates_in — dòng 21

- Đầu vào (signature): `raw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### metadata — dòng 33

- Đầu vào (signature): `bundle`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### table_class — dòng 104

- Đầu vào (signature): `block, context`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### relative_role — dòng 122

- Đầu vào (signature): `raw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### resolved_period — dòng 139

- Đầu vào (signature): `header, row_label, section_type, meta, existing=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Relative columns resolve from PDF period evidence, never supplied year.

### augment — dòng 189

- Đầu vào (signature): `output, bundle, contexts, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### section_contexts — dòng 325

- Đầu vào (signature): `bundle, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### arithmetic_checks — dòng 352

- Đầu vào (signature): `records`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### compatible_check_period — dòng 408

- Đầu vào (signature): `total, operand`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### formula_terms — dòng 427

- Đầu vào (signature): `expression`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Parse only item-code additions/subtractions; never execute source text.

### semantic_coverage — dòng 448

- Đầu vào (signature): `bundle, output, contexts`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### esg_search — dòng 481

- Đầu vào (signature): `output, bundle`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### put — dòng 38

- Đầu vào (signature): `name, candidates, method='explicit_source'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### walk — dòng 434

- Đầu vào (signature): `item, sign=1`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/financial_v2.py

Conservative financial table candidates from the immutable v2 source ledger.

No metric whitelist, no guessed years, no boundary verification, no OCR repair.
Qualitative notes remain pending; explicit continuations are reviewable rules.

**Dependency/import:** `collections`, `datetime`, `decimal`, `json`, `jsonschema`, `pathlib`, `re`, `src.extraction.financial_column_mapping`, `src.extraction.financial_context_v2`, `src.extraction.financial_notes_v2`, `src.extraction.financial_semantics_v3`, `src.extraction.source_v2`, `unicodedata`.

### fold — dòng 24

- Đầu vào (signature): `text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### parse_number — dòng 29

- Đầu vào (signature): `raw, number_format='auto'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Return decimal string and status. Blank/dash are never converted to zero.

### parse_period — dòng 73

- Đầu vào (signature): `header`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Only parse explicit header dates/years; never default to report year.

### period_role — dòng 92

- Đầu vào (signature): `header`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _cell_source — dòng 105

- Đầu vào (signature): `block, index, cell`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _preceding_texts — dòng 116

- Đầu vào (signature): `block, bundle, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Read table context by native body order, not texts/tables array order.

### unit_context — dòng 149

- Đầu vào (signature): `context, headers`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### normalized_decimal — dòng 173

- Đầu vào (signature): `value, scale`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_table — dòng 179

- Đầu vào (signature): `block, context, inventory, number_format='auto', inherited_headers=None, scope=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _table_contexts — dòng 365

- Đầu vào (signature): `bundle, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_financial — dòng 403

- Đầu vào (signature): `work, *, number_format='auto'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate_financial — dòng 465

- Đầu vào (signature): `output, work=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### visit — dòng 123

- Đầu vào (signature): `ref`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### header_source — dòng 191

- Đầu vào (signature): `index, cell`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### issue — dòng 227

- Đầu vào (signature): `record, field, code, reason`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/gemini.py

Explicit-consent Gemini PDF pipeline; no OCR dependency, no automatic billing.

Visual observations are model output, never disguised as verified PDF text.
The API key never enters job JSON, profiles, exports, exceptions or URLs.

**Dependency/import:** `base64`, `collections`, `copy`, `datetime`, `decimal`, `hashlib`, `json`, `jsonschema`, `os`, `pathlib`, `pymupdf`, `re`, `shutil`, `src.extraction.financial_context_v2`, `src.extraction.financial_semantics_v3`, `src.extraction.financial_v2`, `src.extraction.local_llm`, `src.extraction.source_v2`, `time`, `urllib.error`, `urllib.request`, `uuid`, `yaml`.

### read_json — dòng 68

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### canonical_hash — dòng 72

- Đầu vào (signature): `value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### settings — dòng 76

- Đầu vào (signature): `root=ROOT, **overrides`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### api_key — dòng 90

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### decode_response — dòng 153

- Đầu vào (signature): `envelope`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### scope_value — dòng 166

- Đầu vào (signature): `text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### check_batch — dòng 173

- Đầu vào (signature): `response, primary, supplied`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### native_match — dòng 187

- Đầu vào (signature): `quote, native_text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### make_records — dòng 191

- Đầu vào (signature): `checkpoint, report, profile_id, artifact, native_texts`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Model quotes remain visibly model-origin, even with a substring match.

### extract_pdf — dòng 278

- Đầu vào (signature): `source, output_root, config, *, company_id, report_type, report_year, consent=False, budget=None, number_format='auto', client=None, progress_callback=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __init__ — dòng 102

- Đầu vào (signature): `self, limit`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reserve — dòng 107

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __init__ — dòng 114

- Đầu vào (signature): `self, status`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __init__ — dòng 120

- Đầu vào (signature): `self, config, *, consent=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### generate — dòng 126

- Đầu vào (signature): `self, pdf_bytes, request_info, schema`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### proven — dòng 222

- Đầu vào (signature): `value, roles, *, year=False, iso=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### persist — dòng 322

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/gemini_handoff.py

Corporate adapter for explicit cloud-LLM candidates, not native text proof.

**Dependency/import:** `decimal`, `jsonschema`, `pathlib`, `src.extraction.corporate_handoff`, `src.extraction.corporate_review`, `src.extraction.gemini`, `src.extraction.source_v2`.

### convert — dòng 11

- Đầu vào (signature): `document, source_info=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### issue — dòng 30

- Đầu vào (signature): `code, message, pages=(), record_id=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/isolated_page_reader.py

A persistent Docling subprocess with an enforceable per-page deadline.

Control/results are atomic JSON files; library stdout is only a private log.
Timeout terminates only this reader's owned process tree, never other apps.

**Dependency/import:** `json`, `os`, `pathlib`, `src.extraction.source_v2`, `subprocess`, `sys`, `time`, `uuid`.

### __init__ — dòng 20

- Đầu vào (signature): `self, folder, ocr, timeout=120, *, worker_script=None, startup_timeout=180, mode='configured'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _read — dòng 33

- Đầu vào (signature): `self, name`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _start — dòng 39

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __call__ — dòng 57

- Đầu vào (signature): `self, path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### close — dòng 80

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/local_llm.py

Opt-in Ollama text extraction. No cloud, tools, downloads, or factual verdict.

Separate output contract: do not silently substitute this for typed/corporate V2.
Model-suggested fields require literal citations; association remains unverified.

**Dependency/import:** `collections`, `hashlib`, `json`, `jsonschema`, `pathlib`, `re`, `src.extraction.financial_v2`, `src.extraction.source_v2`, `time`, `urllib.error`, `urllib.parse`, `urllib.request`, `yaml`.

### read_json — dòng 52

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### digest — dòng 56

- Đầu vào (signature): `value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate_url — dòng 65

- Đầu vào (signature): `url`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### load_settings — dòng 75

- Đầu vào (signature): `path=None, **overrides`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### build_chunks — dòng 150

- Đầu vào (signature): `bundle, max_chars`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: All nonempty text/cells get a span; no silent clipping; no inherited year.

Cell coordinates and IDs remain source-bound even when Docling missed headers.
One primary block per chunk; repeated table headers are context-only.
This first backend does not perform cross-page semantic joining.

### prompt_source — dòng 218

- Đầu vào (signature): `source`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### source_proof — dòng 227

- Đầu vào (signature): `citation, sources, allowed`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate_candidates — dòng 239

- Đầu vào (signature): `response, schema, sources, chunk, report, number_format`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### standards_label_only — dòng 300

- Đầu vào (signature): `text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_local_llm — dòng 308

- Đầu vào (signature): `workspace, output_dir, settings, *, start_page=1, max_pages=None, max_chunks=None, client=None, progress_callback=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Process all retained text/cells by default; per-chunk resume; honest gaps.

### redirect_request — dòng 61

- Đầu vào (signature): `self, req, fp, code, msg, headers, newurl`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __init__ — dòng 100

- Đầu vào (signature): `self, settings`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### request — dòng 106

- Đầu vào (signature): `self, path, body=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### preflight — dòng 123

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### generate — dòng 134

- Đầu vào (signature): `self, payload, schema`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### persist — dòng 350

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/native_pdf_fallback.py

Literal native-PDF fallback; never certifies layout/semantic completeness.

PyMuPDF supplies text, table cells and bounding boxes. No value, header or
coordinate is generated from a language model or guessed from adjacent years.

**Dependency/import:** `pymupdf`.

### read_native_page — dòng 9

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _prov — dòng 78

- Đầu vào (signature): `box, length`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _cell — dòng 83

- Đầu vào (signature): `text, box, row, col, header`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/source_v2.py

Versioned source capture, not semantic ESG/financial extraction.

Checkpoints preserve successful pages and make failures resumable. IDs are stable
within the same PDF and extraction profile, not across segmentation changes.

**Dependency/import:** `collections`, `contextlib`, `datetime`, `fcntl`, `hashlib`, `importlib.metadata`, `json`, `jsonschema`, `msvcrt`, `os`, `pathlib`, `pymupdf`, `shutil`, `src.extraction.docling_backend`, `src.extraction.financial_layout_recovery`, `src.extraction.isolated_page_reader`, `subprocess`, `tempfile`, `time`.

### now — dòng 25

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### stable_id — dòng 29

- Đầu vào (signature): `kind, *parts`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### file_hash — dòng 34

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### atomic_json — dòng 42

- Đầu vào (signature): `path, data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### default_profile — dòng 64

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _docling_page — dòng 79

- Đầu vào (signature): `path, number, converter`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _ocr_docling_page — dòng 90

- Đầu vào (signature): `path, number, converter, ocr`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Tesseract language OCR -> searchable page -> Docling layout/tables.

No blind OSD rotation. Render orientation follows the PDF. The searchable
page is fitted back to the exact original page size before table inference.
Original PDF/checkpoints from other profiles remain untouched.

### source_blocks — dòng 125

- Đầu vào (signature): `report_id, profile_id, page_number, native, artifact_id, artifact_hash`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### new_record — dòng 143

- Đầu vào (signature): `report_id, anchor_id, record_type='unknown', slot='0'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Foundation envelope; semantic parsers populate fields in a later phase.

### sync_missing_fields — dòng 164

- Đầu vào (signature): `record`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Derive both lists from field statuses and values; never coerce null to zero.

### workspace_lock — dòng 180

- Đầu vào (signature): `work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: OS-held lock releases on native crash; legacy ownerless locks stay intact.

### capture_pdf — dòng 226

- Đầu vào (signature): `source, output_root, *, company_id=None, report_type=None, report_year=None, max_pages=None, start_page=1, retries=1, progress_callback=None, page_reader=None, profile=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Capture selected pages; default full PDF. Reuse successful checkpoints.

page_reader/profile injection is for deterministic tests. Never mark semantic
extraction complete here. This is a single-writer workspace guarded by a lock.

### _capture — dòng 249

- Đầu vào (signature): `source, work, digest, report_id, profile, profile_id, company_id, report_type, report_year, max_pages, start_page, retries, callback, reader, cleanup`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate_source_bundle — dòng 374

- Đầu vào (signature): `bundle, work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Checks JSON Schema cannot express: references, counts and source hashes.

### persist — dòng 284

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/extraction/toolkit.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `__future__`, `collections`, `csv`, `dataclasses`, `datetime`, `hashlib`, `json`, `math`, `numpy`, `pathlib`, `pymupdf`, `rapidfuzz.fuzz`, `rapidocr_onnxruntime`, `re`, `src.extraction.claims`, `src.extraction.docling_backend`, `typing`, `unicodedata`, `yaml`.

### load_yaml — dòng 92

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _ascii_key — dòng 99

- Đầu vào (signature): `value: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _normal_text — dòng 105

- Đầu vào (signature): `value: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _clean_page_text — dòng 109

- Đầu vào (signature): `value: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _aliases — dòng 114

- Đầu vào (signature): `config: dict`.
- Đầu ra annotation: `list[tuple[str, str]]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### infer_company_id — dòng 122

- Đầu vào (signature): `path: Path, config: dict`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### infer_year — dòng 141

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `int`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### infer_report_type — dòng 148

- Đầu vào (signature): `path: Path, config: dict`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### build_document_spec — dòng 172

- Đầu vào (signature): `path: Path, config: dict, company_override: str | None=None, year_override: int | None=None, report_type_override: str | None=None`.
- Đầu ra annotation: `DocumentSpec`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### discover_pdfs — dòng 198

- Đầu vào (signature): `input_path: Path, config: dict | None=None`.
- Đầu ra annotation: `list[Path]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### sha256 — dòng 214

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _line_key — dòng 222

- Đầu vào (signature): `line: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### repeated_lines — dòng 226

- Đầu vào (signature): `page_texts: list[str], ratio: float, minimum_pages: int`.
- Đầu ra annotation: `set[str]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### strip_repeated_lines — dòng 235

- Đầu vào (signature): `text: str, repeated: set[str]`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _sidecar_candidates — dòng 240

- Đầu vào (signature): `ocr_root: Path | None, stem: str, page_number: int`.
- Đầu ra annotation: `list[Path]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _read_sidecar — dòng 251

- Đầu vào (signature): `ocr_root: Path | None, stem: str, page_number: int`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _automatic_ocr — dòng 258

- Đầu vào (signature): `page: pymupdf.Page, scale: float`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_pages — dòng 275

- Đầu vào (signature): `spec: DocumentSpec, extraction_config: dict, ocr_root: Path | None=None, max_pages: int | None=None, progress_callback=None`.
- Đầu ra annotation: `tuple[list[dict], dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _metric_catalog — dòng 349

- Đầu vào (signature): `metrics_config: dict, toolkit_config: dict`.
- Đầu ra annotation: `dict[str, dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### infer_metrics — dòng 370

- Đầu vào (signature): `text: str, catalog: dict[str, dict]`.
- Đầu ra annotation: `list[str]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _parse_number — dòng 387

- Đầu vào (signature): `token: str`.
- Đầu ra annotation: `float | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_measurements — dòng 416

- Đầu vào (signature): `text: str`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _compact_ascii — dòng 427

- Đầu vào (signature): `value: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### infer_financial_statement_scope — dòng 433

- Đầu vào (signature): `pages: list[dict], source_name: str=''`.
- Đầu ra annotation: `str | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _financial_number — dòng 446

- Đầu vào (signature): `value: str`.
- Đầu ra annotation: `int | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_financial_table_claims — dòng 458

- Đầu vào (signature): `spec: DocumentSpec, pages: list[dict], catalog: dict[str, dict], financial_scope: str | None`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### split_candidates — dòng 568

- Đầu vào (signature): `text: str, minimum: int, maximum: int`.
- Đầu ra annotation: `list[str]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### is_claim_candidate — dòng 585

- Đầu vào (signature): `text: str, report_type: str, keywords: list[str], measurements: list[dict], metric_codes: list[str]`.
- Đầu ra annotation: `bool`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### build_claim_records — dòng 599

- Đầu vào (signature): `spec: DocumentSpec, pages: list[dict], toolkit_config: dict, metrics_config: dict`.
- Đầu ra annotation: `tuple[list[dict], list[dict]]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _json_ready — dòng 710

- Đầu vào (signature): `value: Any`.
- Đầu ra annotation: `Any`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### write_json — dòng 720

- Đầu vào (signature): `path: Path, payload: Any`.
- Đầu ra annotation: `None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### write_csv — dòng 725

- Đầu vào (signature): `path: Path, rows: list[dict]`.
- Đầu ra annotation: `None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract_document — dòng 742

- Đầu vào (signature): `spec: DocumentSpec, output_dir: Path, toolkit_config: dict, metrics_config: dict, ocr_root: Path | None=None, max_pages: int | None=None, progress_callback=None`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### company_summary — dòng 818

- Đầu vào (signature): `specs: list[DocumentSpec], claims: list[dict], review: list[dict]`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### run_extraction — dòng 842

- Đầu vào (signature): `specs: list[DocumentSpec], output_root: Path, run_id: str, toolkit_config: dict, metrics_config: dict, ocr_root: Path | None=None, max_pages: int | None=None, progress_callback=None`.
- Đầu ra annotation: `Path`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### document_key — dòng 88

- Đầu vào (signature): `self`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### begins — dòng 153

- Đầu vào (signature): `prefixes: Iterable[str]`.
- Đầu ra annotation: `bool`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### contains — dòng 156

- Đầu vào (signature): `prefixes: Iterable[str]`.
- Đầu ra annotation: `bool`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### in_folder — dòng 160

- Đầu vào (signature): `folders: Iterable[str]`.
- Đầu ra annotation: `bool`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### report_progress — dòng 862

- Đầu vào (signature): `event`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/matching/__init__.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `evidence`.

## src/matching/evidence.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `rapidfuzz.fuzz`, `src.normalization.units`.

### candidate_score — dòng 8

- Đầu vào (signature): `claim: dict, metric: dict`.
- Đầu ra annotation: `float`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### check_comparability — dòng 17

- Đầu vào (signature): `claim: dict, metric: dict`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### relationship_for — dòng 35

- Đầu vào (signature): `claim: dict, metric: dict | None, tolerance: float=0.02`.
- Đầu ra annotation: `tuple[str, dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### checks_json — dòng 62

- Đầu vào (signature): `checks: dict`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/normalization/__init__.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `units`.

## src/normalization/units.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `re`, `unicodedata`.

### canonical_unit — dòng 31

- Đầu vào (signature): `unit: str | None`.
- Đầu ra annotation: `str | None`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### units_convertible — dòng 39

- Đầu vào (signature): `from_unit: str | None, to_unit: str | None`.
- Đầu ra annotation: `bool`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### normalize_value — dòng 44

- Đầu vào (signature): `value: float | int | None, raw_unit: str | None, standard_unit: str | None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/paths.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pathlib`.

## src/preprocessing/__init__.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `text`.

## src/preprocessing/text.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `re`, `spacy`.

### clean_text — dòng 4

- Đầu vào (signature): `text: str`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### sentence_split — dòng 8

- Đầu vào (signature): `text: str`.
- Đầu ra annotation: `list[str]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/quality/__init__.py

Human review and independent quality evaluation, not automatic assurance.

**Dependency/import:** .

## src/quality/checks.py

Deterministic issue detectors, not truth labels or greenwashing verdicts.

**Dependency/import:** `ast`, `collections`, `decimal`, `re`, `src.quality.dictionary`.

### record_checks — dòng 10

- Đầu vào (signature): `snapshot`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _sum_expression — dòng 34

- Đầu vào (signature): `expression, values`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### financial_formula_checks — dòng 48

- Đầu vào (signature): `native`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### flag — dòng 14

- Đầu vào (signature): `code, message`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### walk — dòng 39

- Đầu vào (signature): `node`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/quality/dictionary.py

Versioned dictionary entry point; legacy ESG config remains an explicit import.

**Dependency/import:** `functools`, `hashlib`, `pathlib`, `re`, `src.extraction.financial_context_v2`, `yaml`.

### load_dictionary — dòng 14

- Đầu vào (signature): `root=ROOT`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### identify_metric — dòng 35

- Đầu vào (signature): `label, dictionary=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/quality/evaluation.py

Independent field/record scoring and OCR edit distance. Never manufactures gold.

**Dependency/import:** `collections`, `decimal`, `rapidfuzz.distance`, `src.quality.records`, `unicodedata`.

### location — dòng 10

- Đầu vào (signature): `row`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### edit_distance — dòng 14

- Đầu vào (signature): `a, b`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### ocr_errors — dòng 18

- Đầu vào (signature): `reference, prediction`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### equal — dòng 30

- Đầu vào (signature): `field, a, b`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### prf — dòng 39

- Đầu vào (signature): `tp, fp, fn`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### make_template — dòng 44

- Đầu vào (signature): `predictions, split='test'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### evaluate — dòng 63

- Đầu vào (signature): `predictions, gold, *, split='test', development_sources=(), ocr_predictions=()`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/quality/oil_gold.py

Standards-assisted, deliberately non-gold annotation packs and release gates.

The codebook never changes production extraction rules or fills reference values.
Reviewer identities are declarations; these gates are not authentication.

**Dependency/import:** `collections`, `copy`, `datetime`, `hashlib`, `json`, `math`, `pathlib`, `pymupdf`, `re`, `src.quality.evaluation`, `src.quality.records`, `yaml`.

### load_codebook — dòng 21

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### concept_candidates — dòng 34

- Đầu vào (signature): `row, book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: ID links/text hints for discovery ONLY, never reference answers.

### applicability_dates — dòng 46

- Đầu vào (signature): `*, publication_date=None, period_start=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Date eligibility is NOT legal adoption, materiality, or declared compliance.

### build_pack — dòng 60

- Đầu vào (signature): `prediction_data, book, *, pages=24, split='dev', development_sources=()`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _items — dòng 131

- Đầu vào (signature): `gold, book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### verify_source_delivery — dòng 207

- Đầu vào (signature): `path, golds=()`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Read-only original-PDF hashes and page-range gate, including footnote pages.

### release_check — dòng 234

- Đầu vào (signature): `final, reviewer_a, reviewer_b, book, *, a_sha256, b_sha256, development_sources=()`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Validate independent declarations; never promote a draft or write gold.

### eligible — dòng 50

- Đầu vào (signature): `value, threshold`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### evidence_valid — dòng 135

- Đầu vào (signature): `evidence, source`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/quality/records.py

Small common projection for native and corporate records; source stays immutable.

**Dependency/import:** `copy`, `datetime`, `decimal`, `hashlib`, `json`, `pathlib`, `src.quality.dictionary`.

### digest — dòng 16

- Đầu vào (signature): `value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### versions — dòng 20

- Đầu vào (signature): `root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### required_fields — dòng 31

- Đầu vào (signature): `record`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### project — dòng 35

- Đầu vào (signature): `record, document, *, linked_metric=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### native_snapshots — dòng 78

- Đầu vào (signature): `result`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### valid_corrections — dòng 93

- Đầu vào (signature): `patch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/quality/review_store.py

Append-only, optimistic-concurrency human corrections stored separately from OCR.

**Dependency/import:** `contextlib`, `copy`, `datetime`, `json`, `pathlib`, `sqlite3`, `src.quality.records`, `uuid`.

### __init__ — dòng 18

- Đầu vào (signature): `self, root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### connect — dòng 22

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### history — dòng 34

- Đầu vào (signature): `self, key`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### latest — dòng 40

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### current — dòng 45

- Đầu vào (signature): `self, snapshot, versions, events=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### save — dòng 59

- Đầu vào (signature): `self, snapshot, *, action, corrections, reviewed_fields, reviewer, reason, source_confirmed, versions, expected_revision`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### export — dòng 110

- Đầu vào (signature): `self, snapshots, versions`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/rules/__init__.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `engine`.

## src/rules/engine.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `__future__`, `pathlib`, `src.paths`, `yaml`.

### __init__ — dòng 15

- Đầu vào (signature): `self, rules_path: Path | None=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### _result — dòng 19

- Đầu vào (signature): `self, rule_id: str, explanation: str, relationship: str | None=None`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### evaluate — dòng 24

- Đầu vào (signature): `self, claim: dict, link: dict | None=None, context: dict | None=None`.
- Đầu ra annotation: `list[dict]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## src/scoring/__init__.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `risk`.

## src/scoring/risk.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pathlib`, `src.paths`, `yaml`.

### load_scoring — dòng 16

- Đầu vào (signature): `path: Path | None=None`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### risk_level — dòng 20

- Đầu vào (signature): `score: float`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### claim_score — dòng 30

- Đầu vào (signature): `rule_results: list[dict], evidence_coverage: float, claim_confidence: float, config: dict | None=None`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## dashboard/__init__.py

Dashboard package.

**Dependency/import:** .

## dashboard/assets/extract.css

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## dashboard/assets/human_review.css

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## dashboard/assets/style.css

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## dashboard/assets/workspace.js

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## dashboard/assets/zz_workspace.css

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## dashboard/components/__init__.py

Reusable component namespace.

**Dependency/import:** .

## dashboard/components/presentation.py

Display adapters only: never mutate extraction outputs or evidence states.

**Dependency/import:** `dashboard.upload_v2`, `json`.

### review_label — dòng 7

- Đầu vào (signature): `record`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### display_rows — dòng 17

- Đầu vào (signature): `result`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### session_summary — dòng 40

- Đầu vào (signature): `result`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### table_filter — dòng 49

- Đầu vào (signature): `search=None, company=None, year=None, pillar=None, review=None, kind=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## dashboard/components/workspace.py

Reusable, presentation-only Dash components for the analysis workspace.

**Dependency/import:** `dash`.

### icon — dòng 5

- Đầu vào (signature): `name`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### badge — dòng 12

- Đầu vào (signature): `label, tone='neutral', code=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### section_heading — dòng 18

- Đầu vào (signature): `step, title, description, action=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### stat_card — dòng 23

- Đầu vào (signature): `label, component_id, help_text, symbol`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### empty_state — dòng 29

- Đầu vào (signature): `title, description, action=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### workspace_shell — dòng 34

- Đầu vào (signature): `content, archive`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## dashboard/extraction_history.py

Discover durable local extraction results, including pre-history upload runs.

**Dependency/import:** `dashboard.extraction_worker`, `functools`, `pathlib`, `re`, `src.extraction.source_v2`.

### _job_summary — dòng 11

- Đầu vào (signature): `path, modified, size`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### load_saved_result — dòng 29

- Đầu vào (signature): `root, saved_id`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### history_options — dòng 57

- Đầu vào (signature): `root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## dashboard/extraction_worker.py

Isolated OCR worker supervision, durable status, and crash diagnostics.

Only the child imports/runs conversion. The Dash process keeps serving if a
native PDF/OCR library terminates the child. Worker stdout is a private log,
never a JSON protocol (third-party libraries may print arbitrary messages).

**Dependency/import:** `ctypes`, `json`, `os`, `pathlib`, `re`, `src.extraction.source_v2`, `subprocess`, `sys`, `threading`, `time`.

### job_folder — dòng 23

- Đầu vào (signature): `root, job_id`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### read_json — dòng 29

- Đầu vào (signature): `path, default=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### pid_alive — dòng 36

- Đầu vào (signature): `pid`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### load_job — dòng 62

- Đầu vào (signature): `root, job_id`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### run_isolated_upload — dòng 82

- Đầu vào (signature): `root, job_id, contents, filenames, company=None, year=None, report_type=None, progress_callback=None, number_format='auto', *, worker_script=None, engine='docling', cloud_consent=False, gemini_model=None, max_api_requests=10`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## dashboard/human_review.py

Local review controls reusing the current UI; original extraction is immutable.

**Dependency/import:** `copy`, `dash`, `dashboard.components.presentation`, `json`, `src.extraction.source_v2`, `src.quality.checks`, `src.quality.records`, `src.quality.review_store`.

### review_controls — dòng 13

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reviewed_result — dòng 43

- Đầu vào (signature): `result, root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### review_export — dòng 62

- Đầu vào (signature): `result, root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### register_review_callbacks — dòng 66

- Đầu vào (signature): `app, root, result_loader, source_loader, pdf_loader`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### bind — dòng 71

- Đầu vào (signature): `selected, job, refresh`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### save — dòng 101

- Đầu vào (signature): `clicks, selected, job, selection, action, patch, fields, reviewer, reason, confirm, refresh`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### refresh_table — dòng 124

- Đầu vào (signature): `refresh, job`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## dashboard/pages/__init__.py

Five presentation tabs are composed in app.py for a compact MVP.

**Dependency/import:** .

## dashboard/upload_analysis.py

Session-isolated PDF uploads and background extraction for Dash.

**Dependency/import:** `dash`, `dashboard.components.presentation`, `dashboard.components.workspace`, `dashboard.extraction_history`, `dashboard.extraction_worker`, `dashboard.human_review`, `dashboard.upload_v2`, `flask`, `json`, `pathlib`, `src.extraction.corporate_handoff`, `src.extraction.gemini`, `src.extraction.source_v2`, `threading`, `uuid`.

### upload_panel — dòng 22

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### process_upload — dòng 190

- Đầu vào (signature): `root, contents, filenames, company=None, year=None, report_type=None, progress_callback=None, number_format='auto'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### job_result — dòng 194

- Đầu vào (signature): `job, root=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### source_pdf — dòng 202

- Đầu vào (signature): `result, document_index`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### render_source — dòng 216

- Đầu vào (signature): `selection`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### register_upload_callbacks — dòng 257

- Đầu vào (signature): `app, root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### refresh_history — dòng 261

- Đầu vào (signature): `clicks, job, tick`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### view_pdf — dòng 268

- Đầu vào (signature): `job_id, document_index`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### filenames — dòng 281

- Đầu vào (signature): `names`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### start — dòng 291

- Đầu vào (signature): `clicks, contents, names, company, year, kind, number_format, engine='docling', consent=None, gemini_model=None, request_limit=10`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### engine_settings — dòng 325

- Đầu vào (signature): `engine`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### open_history — dòng 332

- Đầu vào (signature): `clicks, saved_id, current`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### poll — dòng 348

- Đầu vào (signature): `tick, job`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### source_detail — dòng 392

- Đầu vào (signature): `selected, job`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### source_link — dòng 402

- Đầu vào (signature): `index, job, selected`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### download_pdf — dòng 417

- Đầu vào (signature): `clicks, index, job`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### download — dòng 426

- Đầu vào (signature): `clicks, job`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### handoff_enabled — dòng 442

- Đầu vào (signature): `job, tick`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### download_handoff — dòng 448

- Đầu vào (signature): `clicks, job`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### presentation — dòng 478

- Đầu vào (signature): `job, rows, tick`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### filter_records — dòng 493

- Đầu vào (signature): `search, company, year, pillar, review, kind`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### table_state — dòng 498

- Đầu vào (signature): `rows, visible`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### work — dòng 309

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### progress — dòng 310

- Đầu vào (signature): `event`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## dashboard/upload_v2.py

Isolated upload orchestration for source capture + typed v2 parsers.

No database import, scoring, cross-run matching or verification is performed.

**Dependency/import:** `base64`, `binascii`, `datetime`, `json`, `pathlib`, `re`, `shutil`, `src.extraction.esg_v2`, `src.extraction.financial_v2`, `src.extraction.gemini`, `src.extraction.source_v2`, `src.extraction.toolkit`, `unicodedata`, `uuid`.

### read_json — dòng 21

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### download_filename — dòng 25

- Đầu vào (signature): `result, *, timestamp=None, token=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Windows-safe descriptive name; naming never establishes verified metadata.

### process_upload_v2 — dòng 61

- Đầu vào (signature): `root, contents, filenames, company=None, year=None, report_type=None, progress_callback=None, number_format='auto', *, engine='docling', cloud_consent=False, gemini_model=None, max_api_requests=10`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### export_result — dòng 189

- Đầu vào (signature): `result`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Portable native checkpoints keyed by artifact ID; source PDFs separately.

### record_rows — dòng 212

- Đầu vào (signature): `result`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### selected_source — dòng 233

- Đầu vào (signature): `result, row_id`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### slug — dòng 27

- Đầu vào (signature): `value, fallback='UNKNOWN'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### source_value — dòng 32

- Đầu vào (signature): `output, field, fallback=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### one — dòng 46

- Đầu vào (signature): `values, mixed`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### emit — dòng 119

- Đầu vào (signature): `event`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/audit_corporate_handoff.py

Extra delivery checks: nine-slot matrix, exact numeric product, native quotes.

Runs the supplied validator first. Does not adjudicate PDF/OCR semantics.

**Dependency/import:** `argparse`, `datetime`, `decimal`, `importlib.util`, `json`, `pathlib`, `re`, `sys`.

### main — dòng 16

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/audit_financial_upload.py

Inspect a v2 upload without dumping native checkpoints to the console.

**Dependency/import:** `argparse`, `collections`, `hashlib`, `json`, `pathlib`, `pymupdf`, `sys`.

### main — dòng 13

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/build_bsr_ai_reference.py

Assemble an auditable AI transcription sidecar, NEVER a human gold benchmark.

Curated values live in a separate seed file authored after visual PDF review.
Predictions are read only AFTER reference creation to attach old IDs/pointers.
No production record, source PDF, human annotation or approval is modified.

**Dependency/import:** `argparse`, `collections`, `copy`, `decimal`, `hashlib`, `json`, `pathlib`, `re`, `shutil`, `src.extraction.source_v2`, `src.quality.evaluation`, `src.quality.records`, `sys`, `unicodedata`, `yaml`.

### normal_text — dòng 30

- Đầu vào (signature): `text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### number — dòng 34

- Đầu vào (signature): `raw, unit, ambiguity=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### make_reference — dòng 56

- Đầu vào (signature): `source, page, label, raw, unit, column, box, *, table, year=None, concept=None, expected_extra=None, notes=None, ambiguity=None, quote=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### build_references — dòng 93

- Đầu vào (signature): `seeds, pages`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### attach_bindings — dòng 242

- Đầu vào (signature): `refs, predictions`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Link by source/row/column metadata only, NEVER by predicted numeric value.

### validate_reference — dòng 271

- Đầu vào (signature): `data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### comparison_proposals — dòng 312

- Đầu vào (signature): `refs, predictions`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Disagreements for human review, not precision or automatic corrections.

### main — dòng 340

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/build_review_delivery_v2.py

Revise a corporate delivery non-destructively; never overwrite its source.

**Dependency/import:** `argparse`, `copy`, `json`, `pathlib`, `shutil`, `src.extraction.corporate_handoff`, `src.extraction.corporate_review`, `src.extraction.source_v2`, `sys`.

### build — dòng 16

- Đầu vào (signature): `source, destination`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/build_user_manual.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `PIL`, `__future__`, `datetime`, `docx`, `docx.enum.section`, `docx.enum.style`, `docx.enum.table`, `docx.enum.text`, `docx.oxml`, `docx.oxml.ns`, `docx.shared`, `os`, `pathlib`, `sys`, `textwrap`, `yaml`.

### set_cell_shading — dòng 43

- Đầu vào (signature): `cell, fill: str`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### set_cell_border — dòng 52

- Đầu vào (signature): `cell, color='D9D9D9', size='4'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### set_repeat_table_header — dòng 69

- Đầu vào (signature): `row`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_field — dòng 76

- Đầu vào (signature): `run, instruction: str`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### keep_with_next — dòng 89

- Đầu vào (signature): `paragraph`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### configure_document — dòng 95

- Đầu vào (signature): `doc: Document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_part — dòng 142

- Đầu vào (signature): `doc: Document, roman: str, title: str`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_chapter — dòng 158

- Đầu vào (signature): `doc: Document, number: int, title: str, lead: str=''`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_h2 — dòng 169

- Đầu vào (signature): `doc: Document, text: str`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_h3 — dòng 175

- Đầu vào (signature): `doc: Document, text: str`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_bullets — dòng 181

- Đầu vào (signature): `doc: Document, items, numbered=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_code — dòng 188

- Đầu vào (signature): `doc: Document, code: str`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_callout — dòng 197

- Đầu vào (signature): `doc: Document, kind: str, text: str`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_table — dòng 220

- Đầu vào (signature): `doc: Document, title: str, headers, rows, widths=None, font_size=8.2`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_figure — dòng 252

- Đầu vào (signature): `doc: Document, path: Path, caption: str, width_cm=16.0`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### add_summary — dòng 263

- Đầu vào (signature): `doc: Document, items`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### get_font — dòng 268

- Đầu vào (signature): `size=30, bold=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### diagram_pipeline — dòng 278

- Đầu vào (signature): `path: Path, technical=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### diagram_gri — dòng 316

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### diagram_reading — dòng 336

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### diagram_ui — dòng 352

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### load_configs — dòng 380

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### front_matter — dòng 387

- Đầu vào (signature): `doc: Document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### part_i_ii — dòng 477

- Đầu vào (signature): `doc: Document, assets: dict`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### part_iii — dòng 608

- Đầu vào (signature): `doc: Document, assets: dict, rules, scoring`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### part_iv — dòng 787

- Đầu vào (signature): `doc: Document, assets: dict`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### part_v — dòng 909

- Đầu vào (signature): `doc: Document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### appendices — dòng 1004

- Đầu vào (signature): `doc: Document, metrics, rules`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### build — dòng 1111

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/capture_bsr_esg_handoff.py

Capture three supplied BSR ESG PDFs with Docling, native text/OCR fallback.

No legacy generated ESG JSON is used as evidence. New page checkpoints and
results are durable and discoverable in extraction history.

**Dependency/import:** `argparse`, `json`, `os`, `pathlib`, `src.extraction.esg_v2`, `src.extraction.isolated_page_reader`, `src.extraction.source_v2`, `sys`, `uuid`.

### main — dòng 21

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### progress — dòng 42

- Đầu vào (signature): `event`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/check_handover.py

Check new documentation links, source locators and published synthetic schemas.

**Dependency/import:** `argparse`, `json`, `jsonschema`, `pathlib`, `re`, `sys`, `urllib.parse`.

### check — dòng 14

- Đầu vào (signature): `root=ROOT`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/docling_page_worker.py

Private persistent page reader; never writes a source capture checkpoint.

**Dependency/import:** `json`, `pathlib`, `pymupdf`, `src.extraction.docling_backend`, `src.extraction.source_v2`, `sys`, `tempfile`, `time`.

### main — dòng 15

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/export_corporate_handoff.py

Export saved extraction results to a strict, partial corporate handoff.

**Dependency/import:** `argparse`, `dashboard.extraction_history`, `json`, `pathlib`, `src.extraction.corporate_handoff`, `src.extraction.financial_context_v2`, `sys`.

### bsr_slot — dòng 15

- Đầu vào (signature): `doc`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 30

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### pdf_value — dòng 18

- Đầu vào (signature): `name, fallback`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/export_financial_handoff.py

Portable one-JSON-per-BCTC handoff with source checkpoints and batch manifest.

**Dependency/import:** `argparse`, `collections`, `json`, `pathlib`, `shutil`, `src.extraction.financial_v2`, `src.extraction.source_v2`, `sys`.

### summary — dòng 15

- Đầu vào (signature): `output`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### export — dòng 27

- Đầu vào (signature): `workspaces, destination, number_format='auto', baseline=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 139

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/export_full_financial_json.py

Export full page text, every OCR numeric occurrence and monetary groups.

This is a lossless OCR coverage export, not a claim that all table cells have
been verified. Missing spatial information is represented explicitly.

**Dependency/import:** `argparse`, `datetime`, `hashlib`, `json`, `pathlib`, `re`.

### parse_money — dòng 17

- Đầu vào (signature): `text`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 22

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/extract_corpus.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `__future__`, `argparse`, `datetime`, `json`, `pathlib`, `src.extraction.toolkit`, `sys`.

### parser — dòng 26

- Đầu vào (signature): ``.
- Đầu ra annotation: `argparse.ArgumentParser`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 66

- Đầu vào (signature): ``.
- Đầu ra annotation: `int`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/extract_esg_v2.py

Extract review-only ESG text/table records from a v2 source workspace.

**Dependency/import:** `argparse`, `json`, `pathlib`, `src.extraction.esg_v2`, `sys`.

### main — dòng 12

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/extract_financial_v2.py

Parse existing v2 source captures without running OCR again.

**Dependency/import:** `argparse`, `json`, `pathlib`, `src.extraction.financial_v2`, `sys`.

### main — dòng 12

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/extract_gemini.py

Explicit-consent Gemini PDF extraction. Configuration checks never call API.

**Dependency/import:** `argparse`, `json`, `pathlib`, `src.extraction.gemini`, `sys`.

### main — dòng 12

- Đầu vào (signature): `argv=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/extract_local_llm.py

Opt-in source-v2 -> local Ollama candidates; never downloads models.

**Dependency/import:** `argparse`, `json`, `pathlib`, `src.extraction.local_llm`, `sys`.

### main — dòng 12

- Đầu vào (signature): `argv=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/extract_source_v2.py

P0/P1 source capture CLI. Semantic parsers are not implemented here.

**Dependency/import:** `argparse`, `json`, `pathlib`, `src.extraction.source_v2`, `sys`.

### main — dòng 12

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/finalize_review_delivery.py

Re-run all mechanical gates and publish a NEW validation/report.json for V2.

**Dependency/import:** `argparse`, `datetime`, `hashlib`, `json`, `pathlib`, `src.extraction.corporate_review`, `subprocess`, `sys`.

### finalize — dòng 15

- Đầu vào (signature): `folder`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### read — dòng 16

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/finish_bsr_esg_with_native_fallback.py

Finish supplied BSR ESG sources, preserving successful Docling captures.

New hybrid profile, new anchors; original checkpoints/JSON are not overwritten.
Every fallback page remains partial, not successful Docling extraction.

**Dependency/import:** `argparse`, `copy`, `json`, `pathlib`, `src.extraction.esg_v2`, `src.extraction.native_pdf_fallback`, `src.extraction.source_v2`, `sys`, `uuid`.

### main — dòng 20

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### progress — dòng 57

- Đầu vào (signature): `event`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/handover_reference.py

Generate source/schema/dependency references without running app/OCR/API.

**Dependency/import:** `argparse`, `ast`, `csv`, `hashlib`, `importlib`, `json`, `pathlib`, `re`.

### write — dòng 15

- Đầu vào (signature): `path, value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### run — dòng 20

- Đầu vào (signature): `destination`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### walk — dòng 76

- Đầu vào (signature): `node, root, pointer='', required=False, condition='trực tiếp', refs=()`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/handover_smoke.py

OFFLINE controlled fixture smoke: real parsers, FAKE PDF page reader, no OCR/API.

**Dependency/import:** `argparse`, `copy`, `dashboard.upload_v2`, `json`, `jsonschema`, `pathlib`, `pymupdf`, `src.extraction.corporate_handoff`, `src.extraction.esg_v2`, `src.extraction.financial_v2`, `src.extraction.source_v2`, `sys`.

### run — dòng 19

- Đầu vào (signature): `destination`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 38

- Đầu vào (signature): `*_, data=native`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/import_data.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pathlib`, `src.database`, `src.database.adapters`, `src.database.output_sources`, `src.database.sample_data`, `src.extraction.claims`, `src.normalization.units`, `src.paths`, `sys`, `yaml`.

### execute — dòng 24

- Đầu vào (signature): `connection, table: str, row: dict`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reset_content — dòng 30

- Đầu vào (signature): `connection`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### import_demo — dòng 35

- Đầu vào (signature): `connection`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### import_phase1_fallback — dòng 85

- Đầu vào (signature): `connection`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### import_output_sources — dòng 128

- Đầu vào (signature): `connection`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Import the six BSR 2023-2025 output bundles as the primary real corpus.

### main — dòng 279

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/initialize_database.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pathlib`, `src.database`, `sys`.

## scripts/oil_gas_gold.py

Build a blind Oil & Gas annotation pack; check independent gold release gates.

**Dependency/import:** `argparse`, `hashlib`, `json`, `pathlib`, `scripts.quality_benchmark`, `src.quality.oil_gold`, `sys`.

### main — dòng 14

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/package_handover.py

Source-only internal review archive; no deployment, upload, secrets or datasets.

**Dependency/import:** `argparse`, `hashlib`, `json`, `pathlib`, `re`, `sys`, `zipfile`.

### digest — dòng 19

- Đầu vào (signature): `raw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### source_files — dòng 22

- Đầu vào (signature): `root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### scan — dòng 49

- Đầu vào (signature): `raw, relative`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### package — dòng 59

- Đầu vào (signature): `root, destination, version, *, dry_run=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 108

- Đầu vào (signature): `argv=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/prepare_ai_reference_pages.py

Render selected source pages for AI inspection; no gold/approval is created.

**Dependency/import:** `hashlib`, `json`, `pathlib`, `pymupdf`, `src.extraction.source_v2`, `subprocess`, `sys`.

### main — dòng 13

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/quality_benchmark.py

Prepare human gold drafts, measure independent predictions, inspect rule checks.

**Dependency/import:** `argparse`, `hashlib`, `json`, `pathlib`, `src.extraction.source_v2`, `src.quality.checks`, `src.quality.dictionary`, `src.quality.evaluation`, `src.quality.records`, `sys`, `yaml`.

### benchmark_versions — dòng 18

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### known_development_sources — dòng 23

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### read — dòng 28

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### predictions — dòng 32

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### write_new — dòng 80

- Đầu vào (signature): `path, data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 87

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/refresh_esg_handoff.py

Reparse retained ESG checkpoints with the current parser, without OCR.

Creates a new history job. Old result.json and parser-version outputs stay intact.

**Dependency/import:** `argparse`, `copy`, `dashboard.extraction_history`, `json`, `pathlib`, `src.extraction.esg_v2`, `src.extraction.source_v2`, `sys`, `uuid`.

### main — dòng 19

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/run_pipeline.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pathlib`, `src.database`, `src.matching.evidence`, `src.paths`, `src.rules`, `src.scoring`, `sys`, `uuid`, `yaml`.

### as_dict — dòng 17

- Đầu vào (signature): `row`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### demo_context — dòng 21

- Đầu vào (signature): `claim: dict`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 47

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/serve_quality_qa.py

Isolated browser QA server using SYNTHETIC data; never user report history.

**Dependency/import:** `argparse`, `dash`, `dashboard`, `dashboard.components.workspace`, `flask`, `json`, `os`, `pathlib`, `pymupdf`, `src.extraction.source_v2`, `sys`.

### serve — dòng 17

- Đầu vào (signature): `root, port`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### seed — dòng 41

- Đầu vào (signature): `node`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### css — dòng 50

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/setup_vietnamese_ocr.py

Fetch official Tesseract language data into this project, not system folders.

**Dependency/import:** `hashlib`, `json`, `pathlib`, `shutil`, `urllib.request`.

### main — dòng 11

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/upload_worker.py

Child process entry point. Native crashes cannot terminate the Dash parent.

**Dependency/import:** `dashboard.upload_v2`, `json`, `os`, `pathlib`, `src.extraction.source_v2`, `sys`.

### main — dòng 13

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### progress — dòng 18

- Đầu vào (signature): `event`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/validate_corporate_review.py

Standalone review-pair and reference property-graph importer/validator.

Does not write to an external Graph service or produce a verification verdict.
Run the supplied validate.py first for schema/PDF/manifest integrity.

**Dependency/import:** `argparse`, `collections`, `datetime`, `hashlib`, `json`, `pathlib`.

### load — dòng 14

- Đầu vào (signature): `path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### write — dòng 18

- Đầu vào (signature): `path, value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### graph_import — dòng 22

- Đầu vào (signature): `graph`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Materialize nodes/edges into a local reference graph and check all FKs.

### validate — dòng 43

- Đầu vào (signature): `folder, *, require_complete=True, require_pairs=True`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/verify_archive_ui.cjs

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## scripts/verify_bsr2024_handoff.py

Source-reviewed sample oracle, NOT a repair/extraction rule for BSR reports.

Expected values were read visually from the supplied PDF. This script only
compares parser output and writes a separate QA report; it never fills cells.

**Dependency/import:** `argparse`, `json`, `pathlib`, `src.extraction.financial_semantics_v3`, `src.extraction.financial_v2`, `src.extraction.source_v2`, `sys`.

### verify — dòng 42

- Đầu vào (signature): `package`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## scripts/verify_corporate_ui.cjs

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## scripts/verify_filter_ui.cjs

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## scripts/verify_history_ui.cjs

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## scripts/verify_human_review_ui.cjs

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## scripts/verify_workspace_ui.cjs

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## tests/conftest.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pathlib`, `sys`.

## tests/fixtures/capture_crash_worker.py

Test OS lock recovery after a process dies during page 2.

**Dependency/import:** `os`, `pathlib`, `src.extraction.source_v2`, `sys`.

### read — dòng 10

- Đầu vào (signature): `path, page`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/fixtures/isolated_worker_stub.py

Test-only process: simulate hard native exit without loading OCR models.

**Dependency/import:** `ctypes`, `json`, `os`, `pathlib`, `src.extraction.source_v2`, `sys`.

## tests/fixtures/page_worker_stub.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pathlib`, `src.extraction.source_v2`, `sys`, `time`.

## tests/test_bsr_ai_reference.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `importlib.util`, `pathlib`, `pytest`, `src.quality.evaluation`.

### module — dòng 8

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_numeric_transcription_preserves_scale_and_does_not_guess_separator — dòng 15

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### record — dòng 26

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ai_sidecar_is_not_human_gold_and_null_lists_are_synchronised — dòng 31

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_links_do_not_copy_wrong_prediction_values_or_mutate_ids — dòng 48

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_existing_gold_evaluator_refuses_ai_reference — dòng 66

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_corporate_handoff.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `json`, `pathlib`, `pymupdf`, `pytest`, `scripts.export_corporate_handoff`, `src.extraction.corporate_handoff`, `src.extraction.financial_context_v2`, `src.extraction.source_v2`.

### document — dòng 13

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_contract_comparative_year_unit_and_pending_review — dòng 44

- Đầu vào (signature): `document, tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_missing_scope_is_blocked_not_invented — dòng 65

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_attachment_lists_do_not_conflict_with_actual_pdf_scope — dòng 71

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unknown_units_missing_values_and_precision_are_not_faked — dòng 84

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_context_year_is_not_marked_human_reviewed_and_no_restatement_assumption — dòng 104

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_interpretation_cannot_be_laundered_into_source_quote — dòng 113

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_parsed_amount_must_match_literal_source_before_normalization — dòng 120

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_adjustment_column_is_not_automatically_restatement — dòng 127

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_dividend_reference_year_and_wrong_column_do_not_become_observation_header — dòng 135

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_esg_units_types_unknown_dimensions_and_no_metric_alias_join — dòng 146

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_delivery_checks_pdf_hash_manifest_nine_slots_and_zip — dòng 162

- Đầu vào (signature): `document, tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_blocked_documents_are_not_falsely_delivered — dòng 180

- Đầu vào (signature): `document, tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_official_source_flag_requires_https_host_and_recomputed_file_hash — dòng 187

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_delivery_slot_uses_pdf_year_not_old_supplied_report_year — dòng 199

- Đầu vào (signature): `document`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### ref — dòng 20

- Đầu vào (signature): `text, col`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_corporate_review.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `importlib.util`, `pathlib`, `pytest`, `src.extraction.corporate_review`.

### test_monetary_accounts_are_not_employee_counts — dòng 9

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### record — dòng 19

- Đầu vào (signature): `rid, unit='person', scope='unknown', year=2024`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_pairs_are_hypotheses_not_numeric_verdicts — dòng 27

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_different_year_or_known_scope_cannot_pair — dòng 42

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_headcount_recovery_has_explicit_date_and_source_and_is_idempotent — dòng 52

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_graph_loader_rejects_dangling_nodes — dòng 64

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_normalization_is_once_and_keeps_exact_large_integer — dòng 73

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_new_priority_queue_does_not_promote_keyword_only_narrative — dòng 83

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_database.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pathlib`, `sqlite3`, `src.database`.

### test_schema_has_required_tables — dòng 7

- Đầu vào (signature): `tmp_path: Path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_docling_backend.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `src.extraction.docling_backend`.

### test_table_rows_preserve_empty_and_merged_cells — dòng 4

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_esg_v2.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `json`, `pymupdf`, `pytest`, `src.extraction.esg_v2`, `src.extraction.source_v2`.

### page — dòng 11

- Đầu vào (signature): `*items`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### run_esg — dòng 16

- Đầu vào (signature): `tmp_path, pages, kind='ESG', failure=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### records_of — dòng 32

- Đầu vào (signature): `output, kind`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### table_page — dòng 36

- Đầu vào (signature): `values, claim=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_esg_table_periods_units_and_candidate_links — dòng 49

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_workforce_table_stt_group_dvt_and_indicator_headers — dòng 68

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_table_unknown_metric_and_no_period_guess — dòng 80

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_table_explicit_locale_and_intensity_not_defaulted — dòng 92

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_top_unit_and_merged_value_remain_reviewable — dòng 102

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_same_topic_different_metric_does_not_link — dòng 112

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_table_tampered_source_evidence_and_links_detected — dòng 119

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_policy_without_number_keeps_original_and_unknown_date — dòng 133

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_multi_type_paragraph_with_explicit_target_year_baseline_not_guessed — dòng 150

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_explicit_baseline_and_ambiguous_deadline — dòng 164

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_policy_effective_date_only_explicit_source_phrase — dòng 173

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_governance_body_named_but_other_roles_remain_unknown — dòng 180

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_mixed_pillars_not_forced_into_single_pillar — dòng 189

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unknown_retained_and_tables_explicitly_pending — dòng 196

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_heading_inherited_but_not_across_failed_page — dòng 209

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_heading_inherited_on_adjacent_processed_pages_and_stable_ids — dòng 220

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unreachable_heading_not_inherited — dòng 229

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_negated_target_is_only_candidate_not_positive_assertion — dòng 237

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_direct_target_percentage_not_actual_number_elsewhere — dòng 247

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_governance_report_frequency_not_meeting_frequency — dòng 257

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_annual_report_allowed_without_forcing_financial_paragraph_as_esg — dòng 264

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_report_requires_own_branch — dòng 270

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_tamper_missing_list_source_text_and_coverage_detected — dòng 275

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 22

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_extraction_history.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `dash`, `dashboard`, `dashboard.extraction_history`, `dashboard.upload_v2`, `json`, `src.extraction.source_v2`, `uuid`.

### save_run — dòng 12

- Đầu vào (signature): `root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_old_runs_are_discovered_reopened_and_exported_without_ocr — dòng 30

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_jobs_survive_restart_and_do_not_duplicate_underlying_run — dòng 40

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_small_history_index_survives_restart_and_invalidates_on_result_change — dòng 51

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_invalid_corrupt_or_missing_history_does_not_open — dòng 74

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_history_callback_restores_after_memory_loss_and_blocks_switch_while_running — dòng 86

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### track — dòng 62

- Đầu vào (signature): `path, *args`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_extraction_toolkit.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pathlib`, `pymupdf`, `src.extraction.toolkit`.

### test_filename_metadata_supports_multiple_oil_and_gas_companies — dòng 23

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_report_type_can_appear_after_a_date — dòng 38

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unknown_company_is_not_mislabeled_as_oil_and_gas — dòng 46

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_discovery_excludes_reference_standard_folders — dòng 54

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_measurement_parser_handles_vietnamese_and_english_units — dòng 64

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_metric_inference_prefers_specific_variant — dòng 72

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_reports_reject_generic_commitment_language — dòng 80

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_scope_is_taken_from_report_title — dòng 85

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_table_inherits_vnd_and_links_current_comparative_values — dòng 92

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_end_to_end_run_emits_claims_and_ocr_review — dòng 126

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ocr_sidecar_recovers_scanned_page — dòng 157

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_document_without_claims_is_sent_to_review — dòng 189

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### load_yaml_json — dòng 214

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_extraction_worker.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `dash`, `dashboard`, `dashboard.extraction_worker`, `json`, `os`, `pathlib`, `pymupdf`, `pytest`, `src.extraction.source_v2`, `subprocess`, `sys`, `time`, `uuid`.

### test_worker_hard_crash_is_reported_and_parent_survives — dòng 19

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_result_survives_memory_loss_and_invalid_ids_are_rejected — dòng 30

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_os_lock_and_saved_pages_survive_hard_exit — dòng 42

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ui_remains_usable_after_child_native_failure — dòng 64

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_profile_records_alternative_backend — dòng 87

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_active_os_lock_cannot_be_reclaimed — dòng 93

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_atomic_json_retries_transient_sharing_violation — dòng 101

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 54

- Đầu vào (signature): `path, page`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### callback — dòng 70

- Đầu vào (signature): `fragment`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### replace — dòng 105

- Đầu vào (signature): `before, after`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_financial_column_mapping.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `json`, `pymupdf`, `pytest`, `src.extraction.financial_v2`, `src.extraction.source_v2`, `tests.test_financial_v2`.

### box — dòng 12

- Đầu vào (signature): `left, right`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### merged_header_fixture — dòng 16

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_misindexed_merged_code_header_and_amount_pair_are_source_grounded — dòng 34

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ambiguous_code_mapping_abstains — dòng 55

- Đầu vào (signature): `change`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_spaced_integer_or_multiple_tokens_not_guessed — dòng 73

- Đầu vào (signature): `raw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_same_column_vertical_contamination_not_split — dòng 82

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_reversed_period_columns_follow_headers_not_assumed_order — dòng 93

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_separate_current_year_cell_is_not_excluded_as_metadata — dòng 103

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_substring_sources_validate_and_tampering_is_rejected — dòng 111

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_financial_context_v2.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pymupdf`, `pytest`, `src.extraction.financial_context_v2`, `src.extraction.financial_v2`, `src.extraction.source_v2`.

### cell — dòng 11

- Đầu vào (signature): `text, row, col, header=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### native_page — dòng 17

- Đầu vào (signature): `title, *, headers=True, unit=None, scope=None, years=('2025', '2024')`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### run_pages — dòng 31

- Đầu vào (signature): `tmp_path, pages, failed_page=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### measurements — dòng 47

- Đầu vào (signature): `result, page`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_explicit_continuation_inherits_headers_unit_and_scope_with_sources — dòng 52

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_reject_continuation_conflicts_without_inheriting — dòng 82

- Đầu vào (signature): `tmp_path, change, reason`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_do_not_inherit_across_failed_page — dòng 102

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_three_page_chain_keeps_original_header_provenance — dòng 112

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_conflicting_scope_stays_null_and_missing — dòng 122

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_filename_and_general_reference_do_not_establish_scope — dòng 132

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_scope_labels — dòng 146

- Đầu vào (signature): `text, value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 37

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_financial_handoff.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pymupdf`, `pytest`, `scripts.export_financial_handoff`, `src.extraction.financial_v2`, `src.extraction.source_v2`, `tests.test_financial_v2`.

### test_portable_package_has_resolvable_sources_and_refuses_overwrite — dòng 12

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_financial_notes_v2.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pymupdf`, `src.extraction.financial_v2`, `src.extraction.source_v2`.

### page — dòng 9

- Đầu vào (signature): `*paragraphs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### run_notes — dòng 14

- Đầu vào (signature): `tmp_path, pages, fail_page=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_policy_without_numbers_keeps_exact_text_and_missing_fields — dòng 32

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_notes_context_continues_across_pages_with_heading_source — dòng 52

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_gap_blocks_heading_inheritance_but_retains_keyword_candidate — dòng 68

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_statement_footer_and_unit_not_falsely_extracted_as_notes — dòng 79

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_financial_esg_mentions_stay_candidates_not_esg_verdict — dòng 88

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unreachable_text_retained_and_flagged — dòng 102

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_statement_heading_stops_notes_context — dòng 111

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_nested_reading_order_and_numeric_leading_paragraph — dòng 120

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_notes_coverage_missing_entry_rejected — dòng 129

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 20

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_financial_semantics_v3.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `src.extraction.financial_layout_recovery`, `src.extraction.financial_semantics_v3`, `src.extraction.financial_v2`, `tests.test_financial_v2`.

### meta — dòng 7

- Đầu vào (signature): `start='2024-01-01', end='2024-12-31'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_contents_page_numbers_are_not_measurements — dòng 11

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_relative_columns_use_pdf_period_not_input_year — dòng 20

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_opening_cash_in_flow_table_is_instant — dòng 31

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_multiple_year_headers_are_not_collapsed — dòng 37

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_nested_formula_and_unsafe_formula — dòng 45

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_metadata_start_excludes_subsidiary_control_dates — dòng 52

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_layout_recovery_is_not_generic_numeric_text_table — dòng 68

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_asset_class_headers_are_values_not_row_labels — dòng 73

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_damaged_code_header_still_excludes_code_values — dòng 84

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_missing_statement_table_recovered_from_word_alignment — dòng 92

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_missing_note_number_never_inherits_previous_number — dòng 111

- Đầu vào (signature): `monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### block — dòng 53

- Đầu vào (signature): `text, page`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_financial_v2.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pymupdf`, `pytest`, `src.extraction.financial_v2`, `src.extraction.source_v2`.

### cell — dòng 10

- Đầu vào (signature): `text, row, col, header=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### fixture — dòng 16

- Đầu vào (signature): `headers=('2025', '2024'), values=('85.004.418.533.771', '88.352.140.328.065')`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_two_columns_are_two_measurements_not_code_or_note — dòng 29

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_numeric_parser_preserves_ambiguity — dòng 52

- Đầu vào (signature): `raw, expected, status`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_explicit_formats_and_exact_large_integer_normalization — dòng 56

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unknown_period_not_report_year_and_missing_lists — dòng 66

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_missing_unit_and_blank_zero_distinct — dòng 77

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_merged_value_not_silently_assigned — dòng 87

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_absent_source_cell_is_logged_not_synthesized — dòng 97

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_english_currency_scale_and_unrelated_context_not_inherited — dòng 105

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_date_and_quarter_not_guessed — dòng 115

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_end_to_end_source_context_export_and_stable_ids — dòng 122

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_esg_rejected_by_financial_parser — dòng 148

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_gemini.py

No live Google calls: synthetic PDFs + controlled model responses only.

**Dependency/import:** `base64`, `dash`, `dashboard`, `dashboard.extraction_history`, `dashboard.extraction_worker`, `json`, `pathlib`, `pymupdf`, `pytest`, `scripts.extract_gemini`, `scripts.quality_benchmark`, `src.extraction`, `src.extraction.corporate_handoff`, `src.extraction.gemini_handoff`, `src.quality.records`, `subprocess`, `sys`, `urllib.error`, `uuid`.

### no_live_google — dòng 19

- Đầu vào (signature): `monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### pdf_file — dòng 25

- Đầu vào (signature): `tmp_path, pages=1`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### response — dòng 34

- Đầu vào (signature): `page=1, financial=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### envelope — dòng 47

- Đầu vào (signature): `data, finish='STOP'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### extract — dòng 65

- Đầu vào (signature): `tmp_path, pages=1, client=None, budget=None, financial=False, **kwargs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_consent_key_and_config_guards — dòng 74

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_partial_response_never_success — dòng 89

- Đầu vào (signature): `finish`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_tool_safety_and_page_guards — dòng 93

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_pdf_mapping_provenance_budget_and_resume — dòng 104

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_dates_years_without_literal_evidence_stay_null — dòng 133

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_explicit_dates_and_visual_unverified — dòng 146

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_error_caps_stop_and_failures_saved — dòng 158

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_request_reserved_before_api_call — dòng 168

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_cloud_upload_export_history_review_and_corporate — dòng 178

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_corporate_scope_unknown_blocks_but_native_survives — dòng 214

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_http_body_and_key_not_in_error_or_url — dòng 223

- Đầu vào (signature): `monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ui_consent_controls_and_request_settings — dòng 242

- Đầu vào (signature): `monkeypatch, tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_worker_job_does_not_persist_key — dòng 276

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_history_immutable_when_cache_resumed — dòng 289

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_context_only_and_unreadable_do_not_create_records — dòng 309

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_cli_check_config_never_calls_api — dòng 318

- Đầu vào (signature): `monkeypatch, capsys`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_stray_scope_word_does_not_establish_statement_scope — dòng 328

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __init__ — dòng 53

- Đầu vào (signature): `self, financial=False, transform=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### generate — dòng 56

- Đầu vào (signature): `self, pdf, info, schema`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### transform — dòng 134

- Đầu vào (signature): `data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### transform — dòng 147

- Đầu vào (signature): `data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### transform — dòng 216

- Đầu vào (signature): `data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### fake_open — dòng 227

- Đầu vào (signature): `request, **kwargs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### callback — dòng 248

- Đầu vào (signature): `fragment`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### fake_worker — dòng 257

- Đầu vào (signature): `*a, **kw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### transform — dòng 310

- Đầu vào (signature): `data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### transform — dòng 329

- Đầu vào (signature): `data`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### generate — dòng 160

- Đầu vào (signature): `self, *_`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### generate — dòng 170

- Đầu vào (signature): `self, *args`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __init__ — dòng 261

- Đầu vào (signature): `self, target, **kw`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### start — dòng 262

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_handover.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `importlib.util`, `json`, `pathlib`, `pytest`, `zipfile`.

### load — dòng 11

- Đầu vào (signature): `name`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_handover_local_links_evidence_examples — dòng 18

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_three_type_offline_smoke_and_no_overwrite — dòng 23

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### fixture_source — dòng 33

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_packaging_allowlist_hash_manifest_and_reproducibility — dòng 46

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_packaging_secret_error_does_not_echo_value — dòng 63

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_packaging_bad_versions_rejected — dòng 74

- Đầu vào (signature): `tmp_path, version`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_packaging_destinations_empty_env_and_dry_run — dòng 79

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_packager_does_not_traverse_junction_classified_directory — dòng 92

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_packager_rejects_missing_entrypoint — dòng 104

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_human_review_store.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `json`, `pytest`, `src.quality.records`, `src.quality.review_store`.

### snapshot — dòng 9

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### save — dòng 14

- Đầu vào (signature): `store, s, **kwargs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_corrections_persist_separately_and_do_not_overwrite_snapshot — dòng 21

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_concurrent_stale_write_and_wrong_types_rejected — dòng 33

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_source_or_dictionary_change_invalidates_without_applying_old_values — dòng 42

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_incremental_edits_accumulate_and_reset_is_a_new_event — dòng 51

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_full_review_requires_all_fields_and_still_has_no_financial_verdict — dòng 63

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_human_review_ui.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `dash`, `dashboard`, `dashboard.components.presentation`, `dashboard.human_review`, `json`, `pathlib`, `pymupdf`, `src.extraction.source_v2`, `src.quality.records`, `src.quality.review_store`.

### result_fixture — dòng 15

- Đầu vào (signature): `root`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### callback — dòng 31

- Đầu vào (signature): `app, name`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ui_save_requires_pdf_confirmation_survives_reopen_and_exports_overlay — dòng 35

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_changed_source_or_missing_pdf_cannot_keep_review_effective — dòng 60

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_isolated_page_reader.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pathlib`, `pytest`, `src.extraction.isolated_page_reader`, `time`.

### test_persistent_worker_reuses_process_for_multiple_pages — dòng 11

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_hard_deadline_stops_owned_worker_and_later_page_can_continue — dòng 23

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_local_llm.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `json`, `pathlib`, `pymupdf`, `pytest`, `src.extraction`, `src.extraction.source_v2`.

### settings — dòng 12

- Đầu vào (signature): `**changes`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_remote_credentials_and_unsafe_origins_rejected — dòng 19

- Đầu vào (signature): `url`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_loopback_origins_allowed — dòng 24

- Đầu vào (signature): `url`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_model_not_installed_is_not_downloaded — dòng 28

- Đầu vào (signature): `monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_cloud_alias_with_local_endpoint_rejected — dòng 39

- Đầu vào (signature): `monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_bad_settings_rejected — dòng 48

- Đầu vào (signature): `change`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### source_catalog — dòng 52

- Đầu vào (signature): `text='Tổng số lao động năm 2025: 1.594 người'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### response — dòng 58

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate — dòng 68

- Đầu vào (signature): `value`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_source_bound_measurement_and_unknown_boundary — dòng 74

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_hallucinated_year_is_cleared_not_report_year — dòng 86

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_hallucinated_numeric_value_cannot_be_measurement — dòng 95

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_invented_quote_and_source_are_quarantined — dòng 102

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_extra_verdict_or_tools_fields_schema_rejected — dòng 110

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_headings_and_standard_labels_are_not_claims — dòng 116

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_standards_mention_in_actual_narrative_is_not_blanket_excluded — dòng 132

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_standards_label_with_trailing_ocr_icon_noise_is_rejected — dòng 137

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_generation_truncation_is_failure — dòng 148

- Đầu vào (signature): `monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_redirect_is_blocked — dòng 154

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_long_text_no_silent_clipping_and_stable_chunk_ids — dòng 159

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### fixture_workspace — dòng 178

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_limit_keeps_pending_then_resume_no_duplicate_calls — dòng 190

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_checkpoint_tamper_blocks_resume — dòng 207

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_failed_chunks_retry_without_discarding_plan — dòng 217

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_smoke_limit_does_not_hide_previous_unselected_failure — dòng 229

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### request — dòng 31

- Đầu vào (signature): `path, body=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### __init__ — dòng 170

- Đầu vào (signature): `self, fail=False`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### preflight — dòng 171

- Đầu vào (signature): `self`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### generate — dòng 172

- Đầu vào (signature): `self, payload, schema`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 184

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_matching.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `src.matching.evidence`.

### base_claim — dòng 4

- Đầu vào (signature): `**overrides`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### base_metric — dòng 10

- Đầu vào (signature): `**overrides`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_supports_within_tolerance — dòng 16

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_contradiction_only_when_comparable — dòng 21

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_capex_is_not_compared_with_opex — dòng 26

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_consolidated_not_compared_with_separate — dòng 31

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_absolute_not_compared_with_intensity — dòng 36

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unconvertible_unit_is_not_contradiction — dòng 41

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_scope_mismatch_is_not_contradiction — dòng 46

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_missing_is_not_contradiction — dòng 51

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_values_are_compared_after_unit_conversion — dòng 56

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_native_pdf_fallback.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pymupdf`, `pytest`, `src.extraction.corporate_handoff`, `src.extraction.esg_v2`, `src.extraction.native_pdf_fallback`, `src.extraction.source_v2`.

### test_literal_fallback_table_is_partial_and_reaches_contract_with_source — dòng 11

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_blank_or_image_only_native_page_is_not_claimed_read — dòng 40

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_normalization.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pytest`, `src.normalization.units`.

### test_unit_conversion — dòng 14

- Đầu vào (signature): `value, unit, target, expected`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unknown_unit_is_ambiguous — dòng 21

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_convertibility_is_explicit — dòng 27

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_oil_gold.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `pathlib`, `pytest`, `src.quality.oil_gold`.

### book — dòng 14

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### record — dòng 18

- Đầu vào (signature): `metric='GHG_SCOPE_2'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reviewed — dòng 23

- Đầu vào (signature): `name`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### final — dòng 34

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### check — dòng 41

- Đầu vào (signature): `f, a, b, book, **kwargs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_codebook_refs_and_no_money_headcount_equivalence — dòng 45

- Đầu vào (signature): `book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_date_basis_not_reporting_year_and_not_adoption — dòng 57

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_blind_drafts_do_not_inherit_prediction_or_promote — dòng 65

- Đầu vào (signature): `book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_release_requires_independent_review_and_hashes — dòng 79

- Đầu vào (signature): `book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_disagreement_and_added_or_removed_items_need_reason — dòng 91

- Đầu vào (signature): `book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_release_blocks_incomplete_annotations — dòng 101

- Đầu vào (signature): `book, change`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_leakage_gate_and_full_scope_match — dòng 114

- Đầu vào (signature): `book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_pending_sasb_cannot_be_declared_equivalent — dòng 124

- Đầu vào (signature): `book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_duplicate_predictions_are_not_duplicate_reference_items — dòng 133

- Đầu vào (signature): `book`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_output_sources.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `pathlib`, `pytest`, `src.database.output_sources`.

### test_discovers_only_six_bsr_2023_2025_documents — dòng 21

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_output_bundle_inventory_is_complete — dòng 28

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_metric_inference_does_not_treat_eii_as_total_energy — dòng 37

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_summary_claims_exclude_data_quality_checklists — dòng 48

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_quality_checks.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `src.quality.checks`, `src.quality.dictionary`.

### test_dictionary_is_provisional_and_ambiguous_mapping_is_not_forced — dòng 5

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### native_row — dòng 15

- Đầu vào (signature): `code, value, label, year=2024, scope='separate'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_formula_residual_is_review_signal_not_contradiction — dòng 21

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_headcount_unit_and_value_review — dòng 31

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_quality_cli.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `importlib.util`, `json`, `pathlib`.

### module — dòng 6

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_known_development_pdfs_cannot_be_templated_as_independent_test — dòng 12

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_prediction_metadata_does_not_claim_current_code_produced_old_extraction — dòng 28

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_quality_evaluation.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `pytest`, `src.quality.evaluation`, `src.quality.records`.

### prediction — dòng 8

- Đầu vào (signature): `rid='a', anchor='/tables/0/cells/1', value=10, year=2024`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### gold_for — dòng 14

- Đầu vào (signature): `rows`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_draft_cannot_report_precision_or_auto_gold — dòng 25

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_wrong_year_is_not_a_correct_record_even_when_value_matches — dòng 33

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_missing_extra_duplicate_and_partial_scope — dòng 45

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_null_is_not_zero_and_no_predictions_is_not_100_percent — dòng 56

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_document_level_development_leakage_and_incomplete_gold_rejected — dòng 66

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ocr_uses_accents_and_separate_prediction_not_gold_suggestions — dòng 76

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_rules.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `src.rules`.

### claim — dòng 4

- Đầu vào (signature): `**overrides`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_vague_claim — dòng 11

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_evidence_gap_not_contradiction — dòng 16

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_weak_target — dòng 22

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_scope_shift_is_explained_without_contradiction — dòng 27

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_unit_mismatch_is_ambiguous — dòng 33

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_all_15_rules_configured — dòng 39

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_scoring.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `src.scoring`.

### test_default_formula_for_maximum_components — dòng 4

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_risk_bands — dòng 12

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_source_v2.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `json`, `pymupdf`, `pytest`, `src.extraction.source_v2`.

### sample_pdf — dòng 11

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### page_ok — dòng 21

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### read_bundle — dòng 27

- Đầu vào (signature): `work`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_failure_keeps_other_pages_and_resume_only_failed — dòng 31

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_limited_range_is_not_full_and_empty_is_not_blank — dòng 64

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_profile_isolation_and_identical_rerun_ids — dòng 76

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_field_missing_lists_sync_without_coercion — dòng 89

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_metadata_conflict_and_writer_lock — dòng 103

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_source_tamper_and_unresolved_pointer_are_detected — dòng 115

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_partial_source_survives_failed_retry — dòng 123

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### broken — dòng 34

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### repaired — dòng 47

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### empty — dòng 66

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### no_call — dòng 80

- Đầu vào (signature): `*args`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 126

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_upload_v2.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `base64`, `copy`, `dash`, `dashboard`, `pathlib`, `pymupdf`, `pytest`, `src.extraction.source_v2`.

### test_download_filename_uses_pdf_metadata_and_scope_not_source_filename — dòng 14

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_download_filename_handles_batch_partial_and_unsafe_components — dòng 26

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_download_filename_does_not_invent_missing_company_or_year — dòng 39

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### pdf_upload — dòng 45

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### workspace — dòng 53

- Đầu vào (signature): `tmp_path, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_upload_v2_routes_mixed_batch_and_exports_portable_sources — dòng 74

- Đầu vào (signature): `workspace`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_invalid_batch_has_no_writes — dòng 98

- Đầu vào (signature): `workspace, contents, names`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_partial_batch_keeps_success_and_explicit_failure — dòng 104

- Đầu vào (signature): `workspace, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_export_rejects_tampered_artifact_and_unsafe_path — dòng 117

- Đầu vào (signature): `workspace`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_same_company_year_type_isolated_and_path_sanitized — dòng 130

- Đầu vào (signature): `workspace`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### make_ui — dòng 139

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### callback — dòng 148

- Đầu vào (signature): `app, fragment`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_ui_callbacks_progress_source_and_json_download — dòng 152

- Đầu vào (signature): `workspace`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_pdf_route_has_no_filesystem_input_and_checks_hash — dòng 181

- Đầu vào (signature): `workspace`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_upload_exposes_partial_page_capture — dòng 201

- Đầu vào (signature): `workspace, monkeypatch`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_annual_report_with_date_prefix_uses_annual_metadata — dòng 213

- Đầu vào (signature): `workspace`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_reupload_same_pdf_reuses_checkpoint_across_jobs — dòng 218

- Đầu vào (signature): `workspace`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### doc — dòng 27

- Đầu vào (signature): `company, kind, year`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### capture — dòng 58

- Đầu vào (signature): `source, output_root, **kwargs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### sometimes — dòng 106

- Đầu vào (signature): `source, output_root, **kwargs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### partial — dòng 202

- Đầu vào (signature): `source, output_root, **kwargs`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reader — dòng 65

- Đầu vào (signature): `path, number`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## tests/test_workspace_presentation.py

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** `copy`, `dash`, `dashboard`, `dashboard.components.presentation`, `dashboard.components.workspace`, `json`.

### result_fixture — dòng 11

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_counts_only_claims_and_explicit_review_not_candidate_links — dòng 22

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_no_data_not_invented_as_zero_or_score — dòng 34

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_filter_input_is_quoted_and_all_dimensions_are_supported — dòng 40

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_layout_ids_are_unique_and_workflow_and_disclaimers_are_present — dòng 51

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### test_error_state_exposes_retry_without_changing_worker_result — dòng 76

- Đầu vào (signature): `tmp_path`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### record — dòng 12

- Đầu vào (signature): `kind, rid, review='needs_review'`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### walk — dòng 56

- Đầu vào (signature): `node`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## config/ai_reference_bsr_20261021.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/bsr_source_candidates_20261016.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/bsr_verified_sources_20261016.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/esg_v2.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/extraction_toolkit.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/extraction_v2_contract_draft.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/gemini.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/local_llm.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/metric_dictionary.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/metrics.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/oil_gas_gold.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/quality_development_sources.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/rules.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## config/scoring.yml

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/corporate_extract_v1/manifest_schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/corporate_extract_v1/schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/corporate_extract_v1/validate.py

Standalone mechanical validator for corporate-extract-1.0 deliveries.

Requires only packages in requirements.txt; imports no project modules.
Semantic accuracy and human adjudication remain separate.

**Dependency/import:** `__future__`, `argparse`, `glob`, `hashlib`, `json`, `jsonschema`, `pathlib`, `pypdf`, `sys`.

### load_json — dòng 22

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `dict`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### sha256 — dòng 27

- Đầu vào (signature): `path: Path`.
- Đầu ra annotation: `str`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### schema_errors — dòng 35

- Đầu vào (signature): `document: dict, schema: dict`.
- Đầu ra annotation: `list[str]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate_handoff — dòng 41

- Đầu vào (signature): `path: Path, schema: dict, pdf_dir: Path | None=None`.
- Đầu ra annotation: `tuple[dict | None, list[str]]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### validate_manifest — dòng 162

- Đầu vào (signature): `path: Path, schema: dict`.
- Đầu ra annotation: `tuple[dict | None, list[str]]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### expand_paths — dòng 195

- Đầu vào (signature): `patterns: list[str]`.
- Đầu ra annotation: `list[Path]`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### main — dòng 203

- Đầu vào (signature): `argv: list[str] | None=None`.
- Đầu ra annotation: `int`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

## contracts/esg_v2.schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/financial_v2.schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/gemini_extract.schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/gemini_response.schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/local_llm_extract.schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/local_llm_response.schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## contracts/source_v2.schema.json

Không có module docstring; xem source và inventory kiến trúc.

**Dependency/import:** .

## app.py

Production entry point; import has DB initialization side effects.

**Dependency/import:** `__future__`, `dash`, `dash_bootstrap_components`, `dashboard.components.workspace`, `dashboard.upload_analysis`, `pandas`, `pathlib`, `plotly.express`, `plotly.graph_objects`, `src.database`, `src.paths`, `subprocess`, `sys`.

### ensure_ready — dòng 167

- Đầu vào (signature): ``.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### options — dòng 179

- Đầu vào (signature): `series, mapping=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### dropdown — dòng 199

- Đầu vào (signature): `label, component_id, opts, value=None, multi=True`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### card — dòng 206

- Đầu vào (signature): `label, component_id, icon, accent='navy', subtext=None`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### table — dòng 217

- Đầu vào (signature): `component_id, columns, page_size=10`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### filtered — dòng 511

- Đầu vào (signature): `mode, years, docs, pillars, topics, metric_codes, relationships`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### reset_filters — dòng 541

- Đầu vào (signature): `_`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### heatmap_drilldown — dòng 550

- Đầu vào (signature): `click_data, _reset_clicks`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### top_claim_drilldown — dòng 573

- Đầu vào (signature): `active_cell, rows`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### update — dòng 610

- Đầu vào (signature): `mode, years, docs, pillars, topics, metric_codes, risk_types, severities, relationships, trend_metrics, trend_kinds`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.

### viewer — dòng 797

- Đầu vào (signature): `claim_id`.
- Đầu ra annotation: `chưa khai báo`.
- Contract ghi trong source: Chưa có docstring; không tự suy từ tên hàm.
