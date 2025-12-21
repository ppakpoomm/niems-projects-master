1) System Instructions JSON Prompts — Complete (for GitHub Copilot)
Doc ID: docs/06_copilot_instructions_prompt_pack.md
Status: Canonical (Phase 4 dependency chain)
Primary Anchors: VW01–VW10 / PM01–PM10 / Gate A–E
DB Contract: db/migrations/0001_init.sql


 Contract Anchors (copy/paste identical in all 6 docs)

DB Contract: db/migrations/0001_init.sql  
Views Contract (MVP10): VW01–VW10 VW01 vw_alignment_traceability  
VW02 vw_kpi_rag_period  
VW03 vw_budget_execution_project  
VW04 vw_evidence_coverage  
VW05 vw_data_quality_heatmap  
VW06 vw_strategic_spine_tree  
VW07 vw_activity_progress_rollup  
VW08 vw_risk_register_project  
VW09 vw_result_chain_paths  
VW10 vw_evidence_compliance_pdpa_ir    
Automation Contract (Modules): PM01–PM10 (below)  
Validation Gates: A (DDL) / B (Views) / C (ETL) / D (period_key) / E (evidence coverage)  


 6.1 Repo Layout (Canonical)
Copilot ต้องสร้าง/แก้เฉพาะใน layout นี้ (ถ้ายังไม่มีให้สร้างตามนี้ “เท่านั้น”)

db/  migrations/    0001_init.sql    0002_org_units_transition.sql    0003_evidence_assets_upgrade.sql    0004_period_key_enforcement.sql  views/    010_vw_alignment_traceability.sql    020_vw_kpi_rag_period.sql    030_vw_budget_execution_project.sql    040_vw_evidence_coverage.sql    050_vw_data_quality_heatmap.sql    060_vw_strategic_spine_tree.sql    070_vw_activity_progress_rollup.sql    080_vw_risk_register_project.sql    090_vw_result_chain_paths.sql    100_vw_evidence_compliance_pdpa_ir.sqletl/  README.md  config/    mapping_excel.yaml    mapping_forms.yaml  src/    etl_cli.py    extract_excel.py    extract_forms.py    transform_validate.py    load_upsert.py    period_key.py    evidence_policy.py    org_unit_resolver.py  tests/    test_idempotency.py    test_period_key.py    test_evidence_policy.pygraph/  README.md  schema/    projection_model.md  sync/    sync_to_neo4j.py    sync_to_pg_projection.sql  tests/    test_graph_sync.pydocs/  04_erd_mermaid.md  05_activities_database.md  06_copilot_instructions_prompt_pack.md  registry/    canonical_entity_catalog.md    ddl_naming_standards.md    copilot_prompt_pack.json.github/  workflows/    ci_contracts.yml

หมายเหตุ: ถ้าใช้ “ทางเลือก A (PostgreSQL-only)” ให้ graph/sync/sync_to_pg_projection.sql เป็นตัวหลัก และ sync_to_neo4j.py เป็น optional/disabled
ถ้าใช้ “ทางเลือก B (Hybrid PG + Graph)” เปิดใช้งาน sync_to_neo4j.py




 6.2 Naming Standard (Constraint Names) — Canonical
ต้องใช้มาตรฐานเดียวนี้ 100% และให้ Copilot ตรวจใน PM07
PK

pk_<table>  
FK

fk_<from_table>__<to_table>__<from_cols>  
ถ้าเกิน 55 chars → fk_<from>__<to>__h<8>  
UQ

uq_<table>__<cols>  
เกิน limit → uq_<table>__h<8>  
CK

ck_<table>__<rule> (เช่น ck_kpi_targets__period_key_fmt)  
IX

ix_<table>__<cols> (btree default)  
ixg_<table>__<col> (GIN), ixs_... (GiST)  
เกิน limit → ix_<table>__h<8>  
Deterministic hash rule

h<8> = sha1("type|from|to|cols|ref")[:8]
ตัวอย่าง: sha1("fk|kpi_targets|kpis|kpi_id|kpis.id")[:8]  
เอกสารกฎกลาง: docs/registry/ddl_naming_standards.md (Copilot ต้องอัปเดต/รักษา)



 6.3 Transition Rules (Deprecation-safe)
Copilot ต้องถือกฎนี้เป็น “กฎหมายสูงสุด” ใน ETL/Views
Org Unit Transition

Preferred: *_org_unit_id (FK -> org_units.id)  
Legacy tolerated: *_org_unit (string)  
Dual-write (ช่วงเปลี่ยนผ่าน): เขียนทั้งคู่ได้ แต่ อ่านด้วย id ก่อน  
Evidence First-class

Preferred: evidence_asset_id ใน evidence_chain และ FK ที่เกี่ยวข้อง  
Legacy tolerated: file_url (รับได้ชั่วคราว) แต่ต้อง backfill → asset และผูก checksum  
Period Canonical Join Key

Required: period_key format (เช่น 2569-Q1, 2569-01, 2569-H1, 2569-Y)  
period_label เป็น display-only (optional)  
บังคับด้วย CHECK constraint + validator (Gate D)  


 6.4 PM01–PM10 (Automation Modules Catalog)
นี่คือรายชื่อโมดูลมาตรฐาน (anchor) ที่ต้องใช้ชื่อเดิมทุกที่

PM01 pm01_generate_migrations  
PM02 pm02_generate_views_mvp10  
PM03 pm03_generate_tests_contracts  
PM04 pm04_generate_etl_excel  
PM05 pm05_generate_etl_forms  
PM06 pm06_transform_validate_upsert  
PM07 pm07_enforce_ddl_naming_and_gateA  
PM08 pm08_graph_sync_job  
PM09 pm09_ci_pipeline_gates  
PM10 pm10_release_docs_and_runbooks  


 3) Copilot JSON Prompt Pack — Complete
ให้ Copilot ใช้ไฟล์นี้เป็น “แผนที่จักรวาล” แบบ deterministic
บันทึกเป็น: docs/registry/copilot_prompt_pack.json

{  "prompt_pack_name": "niems_strategy_platform_contract_pack",  "version": "1.0.0",  "language": "en-US",  "style": {    "tone": "technical",    "rules": [      "Do NOT invent new tables beyond the Canonical Entity Catalog (40+ core + required auxiliary).",      "All FK relationships in SQL must match the ERD and declared FK targets.",      "Use deterministic constraint names per ddl_naming_standards.md.",      "Never rename VW01–VW10 or PM01–PM10 anchors.",      "Gate A–E are mandatory acceptance criteria."    ]  },  "contracts": {    "db_contract": "db/migrations/0001_init.sql",    "views_contract_mvp10": {      "VW01": "vw_alignment_traceability",      "VW02": "vw_kpi_rag_period",      "VW03": "vw_budget_execution_project",      "VW04": "vw_evidence_coverage",      "VW05": "vw_data_quality_heatmap",      "VW06": "vw_strategic_spine_tree",      "VW07": "vw_activity_progress_rollup",      "VW08": "vw_risk_register_project",      "VW09": "vw_result_chain_paths",      "VW10": "vw_evidence_compliance_pdpa_ir"    },    "validation_gates": {      "A": "DDL compiles; constraints valid; naming pattern enforced; no missing FK/CK/UQ/IX names.",      "B": "All MVP10 views compile and run on sample fixtures.",      "C": "ETL is idempotent (re-run produces zero duplicates) and supports Excel+Forms.",      "D": "period_key conformance >= 99% (validator + CHECK constraint).",      "E": "evidence coverage trend is measurable and increasing (VW04 + policy checks)."    }  },  "feature_flags": {    "use_graph": true,    "graph_engine": "neo4j",    "pg_projection_fallback": true  },  "registry_files": {    "canonical_entity_catalog": "docs/registry/canonical_entity_catalog.md",    "ddl_naming_standards": "docs/registry/ddl_naming_standards.md"  },  "modules": [    {      "id": "PM01",      "name": "pm01_generate_migrations",      "goal": "Generate ordered PostgreSQL migration SQL files aligned with the DB contract and transition roadmap.",      "inputs": [        "db/migrations/0001_init.sql (ground truth target)",        "docs/registry/ddl_naming_standards.md",        "Transition rules: org_units, evidence_assets, period_key"      ],      "outputs": [        "db/migrations/0001_init.sql",        "db/migrations/0002_org_units_transition.sql",        "db/migrations/0003_evidence_assets_upgrade.sql",        "db/migrations/0004_period_key_enforcement.sql"      ],      "prompt": [        "You are implementing PostgreSQL migrations for a strategy/M&E platform.",        "Create 0001_init.sql that defines all canonical tables (40+ core) + required auxiliary (org_units, evidence_assets, result_chain_edges).",        "Use UUID PKs, audit columns, record_status, and deterministic constraint naming.",        "0002 adds org_units + *_org_unit_id columns (nullable), keeps legacy *_org_unit strings, adds resolver indexes.",        "0003 introduces evidence_assets as first-class (checksum_sha256, classification, retention_until, owner_org_unit_id, is_personal_data), and updates evidence_chain to prefer evidence_asset_id while tolerating legacy file_url until cutover.",        "0004 enforces period_key: add column where needed, CHECK constraint for format, and backfill helper function stubs if required.",        "Do not rename existing columns unless explicitly marked deprecated; prefer additive migrations."      ],      "acceptance_criteria": [        "All constraints (PK/FK/UQ/CK/IX) have deterministic names (per naming standard).",        "SQL compiles on PostgreSQL 14+.",        "No FK points to non-existent target."      ],      "gates": ["A"]    },    {      "id": "PM02",      "name": "pm02_generate_views_mvp10",      "goal": "Generate MVP10 analytics views as the BI contract (VW01–VW10) with stable join paths.",      "inputs": [        "db/migrations/*.sql",        "View list VW01–VW10",        "ERD join spines (Strategy, KPI, Budget/Evidence/Ops)"      ],      "outputs": [        "db/views/010_vw_alignment_traceability.sql",        "db/views/020_vw_kpi_rag_period.sql",        "db/views/030_vw_budget_execution_project.sql",        "db/views/040_vw_evidence_coverage.sql",        "db/views/050_vw_data_quality_heatmap.sql",        "db/views/060_vw_strategic_spine_tree.sql",        "db/views/070_vw_activity_progress_rollup.sql",        "db/views/080_vw_risk_register_project.sql",        "db/views/090_vw_result_chain_paths.sql",        "db/views/100_vw_evidence_compliance_pdpa_ir.sql"      ],      "prompt": [        "Implement each view as CREATE OR REPLACE VIEW in its own file.",        "VW01 must trace national_policies -> master_plans -> goals -> tactics -> programs -> projects, and join strategic_project_section15_alignment with section15_master and optionally kpis.",        "VW02 must join kpis + kpi_targets(period_key) + kpi_performance(period_key) and compute RAG.",        "VW03 must provide project-level budget execution using budget_allocations, project_budget_lines, financial_transactions, and budget_execution_snapshots.",        "VW04 must compute evidence coverage by project/activity/kpi/budget_line using evidence_assets + evidence_chain.",        "VW05 must summarize data_quality_issues by system and kpi with severity proxies.",        "VW06 must output the strategic spine tree with canonical keys and parent refs.",        "VW07 must compute activity schedule status, slippage_days, parsed WBS code from activity_instances.name_th convention, and progress proxy from daily logs.",        "VW08 must produce risk register roll-up with risk_level thresholds and last mitigation log date.",        "VW09 must expose result chain paths using result_chain_edges (parent-child) and optionally join to goals/programs.",        "VW10 must report evidence policy compliance (checksum present, classification present, retention set, personal data flag)."      ],      "acceptance_criteria": [        "All views compile (Gate B).",        "Join paths use canonical keys (UUID FKs + period_key).",        "Views do not reference columns/tables outside the DB contract."      ],      "gates": ["B"]    },    {      "id": "PM03",      "name": "pm03_generate_tests_contracts",      "goal": "Generate contract tests for DDL, views, and ETL idempotency.",      "inputs": [        "db/migrations/*.sql",        "db/views/*.sql",        "etl/src/*"      ],      "outputs": [        "etl/tests/test_idempotency.py",        "etl/tests/test_period_key.py",        "etl/tests/test_evidence_policy.py"      ],      "prompt": [        "Create pytest-based tests that validate:",        "(1) DDL runs in a clean Postgres container,",        "(2) all views compile after migrations,",        "(3) ETL re-run is idempotent (no duplicate natural keys),",        "(4) period_key validator passes >= 99% on fixtures,",        "(5) evidence policy compliance metrics exist for VW10."      ],      "acceptance_criteria": ["All tests pass in CI pipeline."],      "gates": ["A", "B", "C", "D", "E"]    },    {      "id": "PM04",      "name": "pm04_generate_etl_excel",      "goal": "Implement Excel ingestion ETL (extract -> validate -> upsert canonical).",      "inputs": [        "SMART4MyBook.xlsx (source)",        "etl/config/mapping_excel.yaml"      ],      "outputs": [        "etl/src/extract_excel.py",        "etl/src/etl_cli.py"      ],      "prompt": [        "Build an Excel ETL that reads configured sheets and columns, normalizes types, and outputs canonical records.",        "Implement WBS parsing from activity_instances.name_th convention: 'WBS:<code> | <title>'.",        "Implement safe upsert keys: use code-based natural keys where defined; otherwise deterministic UUID mapping from stable fields.",        "Log run_id, row_hash, and watermark timestamps for idempotency."      ],      "acceptance_criteria": ["Re-running ETL produces no duplicates; upsert keys are stable."],      "gates": ["C"]    },    {      "id": "PM05",      "name": "pm05_generate_etl_forms",      "goal": "Implement Forms/Lists ingestion (API payload -> validate -> upsert).",      "inputs": [        "etl/config/mapping_forms.yaml"      ],      "outputs": [        "etl/src/extract_forms.py"      ],      "prompt": [        "Implement a generic JSON payload ingestion (forms/lists) with schema validation.",        "Resolve org_unit to org_units.id using org_unit_resolver; keep legacy strings during transition."      ],      "acceptance_criteria": ["Payload validation rejects malformed period_key and missing required fields."],      "gates": ["C", "D"]    },    {      "id": "PM06",      "name": "pm06_transform_validate_upsert",      "goal": "Central transform/validate/load layer for Excel + Forms with policy enforcement.",      "inputs": [        "etl/src/period_key.py",        "etl/src/evidence_policy.py",        "etl/src/org_unit_resolver.py"      ],      "outputs": [        "etl/src/transform_validate.py",        "etl/src/load_upsert.py",        "etl/src/period_key.py",        "etl/src/evidence_policy.py",        "etl/src/org_unit_resolver.py"      ],      "prompt": [        "Implement period_key generator and validator. Enforce canonical formats: YYYY-Qn, YYYY-MM, YYYY-H1/H2, YYYY-Y.",        "Implement evidence policy checks: checksum_sha256 required for new evidence assets; classification and retention_until required for restricted classes.",        "Implement org_unit resolver: map incoming strings/codes to org_units.id; create placeholder org_units only if explicitly allowed."      ],      "acceptance_criteria": [        "period_key conformance >= 99% (Gate D).",        "Evidence assets for new uploads must have checksum and classification (Gate E trend measurable)."      ],      "gates": ["C", "D", "E"]    },    {      "id": "PM07",      "name": "pm07_enforce_ddl_naming_and_gateA",      "goal": "Enforce deterministic naming for PK/FK/UQ/CK/IX and fail Gate A if any mismatch.",      "inputs": [        "docs/registry/ddl_naming_standards.md",        "PostgreSQL catalog (pg_constraint, pg_indexes)"      ],      "outputs": [        "etl/src/ddl_naming_validator.py",        ".github/workflows/ci_contracts.yml (Gate A hook)"      ],      "prompt": [        "Write a validator that connects to Postgres and checks every constraint/index name matches the naming pattern.",        "If any constraint/index is unnamed or mismatched, fail with actionable messages including expected deterministic name.",        "Integrate into CI as Gate A."      ],      "acceptance_criteria": ["Gate A fails if a single constraint/index name violates the standard."],      "gates": ["A"]    },    {      "id": "PM08",      "name": "pm08_graph_sync_job",      "goal": "Sync a read-only graph projection for stakeholder/traceability queries (Hybrid option).",      "inputs": [        "VW01, VW06 (strategy spine)",        "VW04 (evidence coverage)",        "Feature flag use_graph"      ],      "outputs": [        "graph/sync/sync_to_neo4j.py",        "graph/sync/sync_to_pg_projection.sql",        "graph/schema/projection_model.md"      ],      "prompt": [        "Create a read-only projection graph model:",        "Nodes: Policy, MasterPlan, Goal, Tactic, Program, Project, Section15, KPI, EvidenceAsset, OrgUnit.",        "Edges: ALIGNS_TO, IMPLEMENTS, COVERS, MEASURES, HAS_EVIDENCE, OWNS.",        "Use watermarks (updated_at) and idempotent MERGE semantics.",        "If use_graph is false, create PG projection tables or materialized views instead."      ],      "acceptance_criteria": ["Graph sync is idempotent and uses canonical IDs as node keys."],      "gates": ["C"]    },    {      "id": "PM09",      "name": "pm09_ci_pipeline_gates",      "goal": "Create CI pipeline that enforces Gate A–E in order.",      "inputs": [        "db/migrations/*.sql",        "db/views/*.sql",        "etl/tests/*",        "graph/tests/*"      ],      "outputs": [        ".github/workflows/ci_contracts.yml"      ],      "prompt": [        "Implement CI steps:",        "Gate A: run migrations + ddl naming validator.",        "Gate B: compile all views.",        "Gate C: run ETL idempotency tests.",        "Gate D: run period_key tests (>=99%).",        "Gate E: run evidence policy tests + compute baseline coverage metrics."      ],      "acceptance_criteria": ["CI fails fast on earliest gate violation with clear logs."],      "gates": ["A", "B", "C", "D", "E"]    },    {      "id": "PM10",      "name": "pm10_release_docs_and_runbooks",      "goal": "Generate runbooks and docs alignment outputs for maintainers.",      "inputs": [        "docs/04_erd_mermaid.md",        "docs/05_activities_database.md",        "docs/registry/*",        "CI logs"      ],      "outputs": [        "docs/registry/single_source_map.md",        "docs/registry/deprecation_roadmap.md",        "docs/registry/validation_runbook.md"      ],      "prompt": [        "Create operational runbooks for Gates and deprecation milestones (M1–M4).",        "Ensure all docs reference the same anchors and file paths."      ],      "acceptance_criteria": ["Docs contain no conflicting names; anchors are consistent across files."],      "gates": ["A", "B", "C", "D", "E"]    }  ]}


 6.5 “Copilot Manual” (How to run the pack without chaos)
Copilot Chat / Copilot Agent ให้ทำงานทีละโมดูลตามลำดับ dependency นี้:

PM01 → สร้าง migrations + transition scripts  
PM07 → ใส่ naming validator + บังคับ Gate A  
PM02 → สร้าง VW01–VW10 ตามสัญญา → Gate B  
PM04 + PM05 + PM06 → ETL Excel/Forms + idempotent upsert → Gate C/D/E  
PM08 → graph sync (เปิด/ปิดด้วย feature flag)  
PM03 + PM09 → tests + CI pipeline บังคับ Gate A–E  
PM10 → runbooks + single source map + deprecation roadmap docs  
หลักการ: “ถ้า Gate A ยังไม่ผ่าน ห้ามไปต่อ” เพราะทุกอย่างถัดไปจะหลุดทั้งกอง



 6.6 Guardrails Prompts (3 trade-offs ที่ต้องเคร่ง)
ใช้เป็น prompt ติดไว้ใน Copilot Chat เวลาเริ่มงานแต่ละส่วน

GUARDRAIL: Org Units Transition- Always prefer *_org_unit_id FK to org_units.id- Keep legacy *_org_unit strings during transition (do NOT delete)- Ensure resolvers + indexes exist for backfill and dual-read- Migration must be additive and backward compatible

GUARDRAIL: Evidence Assets Policy- Evidence must be a first-class asset (evidence_assets)- For new assets, checksum_sha256 + classification + retention_until are mandatory- evidence_chain must prefer evidence_asset_id; tolerate legacy file_url only until cutover- Add tests that enforce policy and enable Gate E trending

GUARDRAIL: period_key Standard- period_key formats allowed: YYYY-Qn, YYYY-MM, YYYY-H1/H2, YYYY-Y- Add CHECK constraints + validator- Any ETL record missing period_key must be rejected or deterministically generated- Gate D requires >=99% conformance
