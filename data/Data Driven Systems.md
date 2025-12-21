1) Data Driven Systems — Complete (Architecture + Data Flows)
Doc ID: DOC-DATA-SYSTEM-03
Version: 1.0 (Canonical)
SoR: PostgreSQL (Canonical Tables)
DB Contract: db/migrations/0001_init.sql
Views Contract: VW01–VW10
Automation Contract: PM01–PM10
Validation Gates: A–E


 0) Contract Anchors (copy/paste identical in all 6 docs)

DB Contract: db/migrations/0001_init.sql  
Views Contract (MVP10): VW01–VW10 (defined below)  
Automation Contract (Modules): PM01–PM10  
Gates: A (DDL) / B (Views) / C (ETL) / D (period_key) / E (evidence coverage)  


 1) System Purpose (Outcome ที่ระบบต้อง “ทำได้จริง”)
ระบบนี้เป็น “Data-driven operating system” สำหรับงานยุทธศาสตร์–โครงการ–งบ–KPI–หลักฐาน ของ NIEMS ที่ต้อง:

Traceability จริง (ไม่ใช่แต่งรายงาน) ผ่าน strategic_project_section15_alignment  
Reporting ที่ join ง่าย ลด bug ผ่าน period_key  
PDPA/IR คุมได้ผ่าน evidence_assets (first-class) + retention + classification + checksum  
ทำงานแบบ idempotent (ยิง ETL ซ้ำได้ ไม่พัง ไม่ซ้ำ) ผ่าน watermark/run_id/checksum  


 2) Canonical Architecture (Layered)
2.1 Layers

Sources (Raw) Excel/Sheets, Forms/SharePoint Lists, ระบบปฏิบัติการรายวัน, ไฟล์หลักฐาน 
Ingestion (Landing/Staging) รับข้อมูลเข้าแบบ “append-only” (ถ้าทำ staging schema) 
เก็บ run metadata: etl_runs    
Validation (Quality Gate) ตรวจ schema mapping, required fields, key uniqueness, period_key format, referential integrity 
Canonical Storage (SoR: PostgreSQL) ตาราง canonical ตาม DDL (40+ตารางเสริมที่จำเป็น) 
Serve (BI Contract) Views MVP10: VW01–VW10 (เป็น “Reporting contract”) 
Projection (Graph / Read-only) Sync job สร้าง projection สำหรับ graph query (impact path / trace graph) 
อ่านจาก views/canonical เท่านั้น (ห้ามเขียนกลับ) 


 3) Data Contracts (สิ่งที่ “ห้ามหลุด”)
3.1 Raw → Canonical mapping rule (แกน ETL)

Natural key to UUID resolution (เช่น code, law_code, keyword, checksum_sha256)  
Dual-field transition (ช่วงเปลี่ยนผ่าน) org_unit: *_org_unit_id preferred, *_org_unit legacy  
evidence: evidence_asset_id preferred, file_url legacy  
period: period_key required, period_label display    
3.2 Idempotency & Watermark

ทุก ETL run ต้องมี run_id (uuid) และเก็บใน etl_runs  
รองรับ watermark: time-based (updated_at watermark)  
content-based (source_checksum)    
Upsert strategy: Resolve dimension IDs ก่อน (org_units, legal_frameworks, etc.) 
Upsert fact-ish tables หลัง (kpi_performance, budget_execution_snapshots, daily_ops_logs) 


 4) Security/Compliance (PDPA/IR control points)
4.1 Evidence First-class (PDPA/IR)
evidence_assets ต้องมีขั้นต่ำ:

checksum_sha256 (dedup)  
classification (public/internal/confidential/restricted)  
retention_until + retention_note  
owner_org_unit_id  
is_personal_data + pdpa_note  
4.2 Access Pattern

Dashboard/BI อ่านผ่าน views (ลดการเปิด raw/canonical ตรง ๆ)  
Evidence access policy: metadata view ได้ (id, type, classification, retention) 
file_url อาจเป็น secure link (ภายนอก DB) 


 5) Control Flow (CI/CD + Gates)
Gate A — DDL

migrate compile ผ่าน 
constraints names pattern ถูกต้อง 
FK/CK/UQ/IX ครบตาม standard 
Gate B — Views

VW01–VW10 compile ผ่าน 
ไม่มี FK join path “วาดเกินจริง” 
Gate C — ETL

idempotency pass (ยิงซ้ำแล้ว row count/keys stable) 
upsert correctness (ไม่มี duplicate natural keys) 
Gate D — period_key

conformance ≥ 99% (regex pass) 
period_key join สำเร็จระหว่าง target/performance 
Gate E — evidence coverage

coverage trend เพิ่มขึ้น (อย่างน้อยไม่ถอยหลังแบบไร้เหตุผล) 
evidence ที่เป็น personal data ถูกจัด classification/retention ครบ 


 6) Reference Architecture Diagrams (Mermaid — ใช้ใน docs ได้ทันที)
6.1 System Context

flowchart LR  
U1[Executives/Committees] --> BI[Dashboards/Reports] 
U2[M&E/Strategy Team] --> BI  
U3[Finance Team] --> BI  
U4[Ops Team] --> BI  
S1[Excel/Sheets] --> ING[Ingestion/ETL]  
S2[Forms/Lists] --> ING  
S3[Daily Logs] --> ING  
S4[Evidence Files] --> ING  
ING --> VAL[Validation Rules + Gates]  
VAL --> DB[(PostgreSQL SoR)]  
DB --> VW[(VW01–VW10 Views)]  
VW --> BI  VW --> GSYNC[Graph Sync (Read-only Projection)]  
GSYNC --> G[(Graph Store/Projection)]
6.2 Data Flow (Raw → Canonical → Serve)

flowchart TB  
RAW[Raw Inputs] --> STG[Landing/Staging (optional)]  
STG --> MAP[Map + Normalize + Resolve IDs]  
MAP --> VQ[Validate: keys/period_key/FK]  
VQ --> UPS[Upsert Canonical Tables]  
UPS --> VW[VW01–VW10]  
VW --> OUT[Dashboards + Exports]  
VW --> GP[Graph Projection Sync]
6.3 CI Pipeline (Contracts enforcement)

flowchart LR  
PR[Pull Request] --> A[Gate A: DDL compile]  
A --> B[Gate B: Views compile]  
B --> C[Gate C: ETL idempotency tests]  
C --> D[Gate D: period_key conformance]  
D --> E[Gate E: evidence coverage checks]  
E --> DEPLOY[Deploy]


 2) Analytics Views MVP 10 วิว (VW01–VW10) — Reporting Contract
0) Views Contract Anchors (ชื่อจริงชุดเดียว)
ทุกเอกสารต้องอ้าง “รหัส+ชื่อ view” นี้เท่านั้น

 

VW01: vw_alignment_traceability  
VW02: vw_kpi_rag_period  
VW03: vw_budget_execution_project  
VW04: vw_evidence_coverage  
VW05: vw_data_quality_heatmap  
VW06: vw_strategic_spine_tree  
VW07: vw_activity_progress_rollup  
VW08: vw_risk_register_project  
VW09: vw_result_chain_paths  
VW10: vw_evidence_compliance_pdpa_ir  
ไฟล์แนะนำ: db/views/010_vw_mvp10.sql (หรือแยกเป็น 10 ไฟล์ก็ได้ แต่ชื่อ view ต้องตามนี้)



 1) View Specs (อ่านง่ายแบบ “BI contract”)
VW01 — Alignment & Traceability (the gold made usable)

Purpose: บอกว่า “โครงการนี้โยงยุทธศาสตร์/มาตรา 15/KPI อะไร” แบบ query ได้  
Join spine: strategic_goals → strategic_tactics → programs → projects + section15_master + kpis  
Primary consumers: Trees/ERD/Architecture, Dashboard alignment  
Key columns: goal_code, tactic_code, program_code, project_code, section15_number, kpi_code, weight  
VW02 — KPI RAG by period_key

Purpose: RAG = target vs reported โดยใช้ period_key มาตรฐานเดียว  
Rule (MVP): GREEN: reported ≥ target 
AMBER: reported ≥ 0.9*target 
RED: reported < 0.9*target 
GRAY: missing target or missing performance 
VW03 — Budget Execution rollup (project-level)

Purpose: สรุป approved/disbursed/remaining และ %disbursed แบบ canonical  
VW04 — Evidence Coverage

Purpose: coverage ของ evidence ต่อ project/kpi/budget/section15 + classification mix  
VW05 — Data Quality Heatmap

Purpose: heatmap issues ตาม system/issue_type/month (+kpi optional)  
VW06 — Strategic Spine Tree

Purpose: ข้อมูลทำ Trees แบบไม่เพ้อ (ใช้ join จริง)  
VW07 — Activity Progress Rollup

Purpose: schedule slippage + completion status จาก planned/actual + daily logs linkage  
VW08 — Risk Register Project

Purpose: risk score + linkage กับ daily log / project เพื่อเอาไปทำ correlation กับ schedule/budget/kpi  
VW09 — Result Chain Paths (impact path)

Purpose: เดิน graph ของ result_chain_edges เพื่อใช้ทำ impact route จริง  
VW10 — Evidence Compliance (PDPA/IR)

Purpose: ตรวจ personal data / classification / retention / dedup / orphan usage  


 2) SQL: MVP10 Views (PostgreSQL)

หมายเหตุ: ใช้ schema public ตามค่าเริ่มต้น, ถ้าคุณใช้ schema อื่นให้ prefix เอง
แนะนำให้รันหลัง Gate A ผ่านแล้ว (DDL compile)


 
-- db/views/010_vw_mvp10.sqlBEGIN;
-- =========================
-- VW01: Alignment Traceability
-- =========================
CREATE OR REPLACE VIEW vw_alignment_traceability ASSELECT  
a.id AS alignment_id,  sg.id AS strategic_goal_id,  sg.code AS strategic_goal_code,  sg.name_th AS strategic_goal_name_th,  st.id AS tactic_id,  st.code AS tactic_code,  st.name_th AS tactic_name_th,  p.id AS program_id,  p.code AS program_code,  p.name_th AS program_name_th,  prj.id AS project_id,  prj.code AS project_code,  prj.name_th AS project_name_th,  prj.fiscal_year,  s15.id AS section15_id,  s15.number AS section15_number,  s15.name_th AS section15_name_th,  k.id AS kpi_id,  k.code AS kpi_code,  k.name_th AS kpi_name_th,  a.weight,  a.noteFROM strategic_project_section15_alignment aJOIN strategic_goals sg ON sg.id = a.strategic_goal_idLEFT JOIN strategic_tactics st ON st.id = a.tactic_idJOIN projects prj ON prj.id = a.project_idLEFT JOIN programs p ON p.id = prj.program_idJOIN section15_master s15 ON s15.id = a.section15_idLEFT JOIN kpis k ON k.id = a.kpi_idWHERE a.status = 'active';
-- =========================
-- VW06: Strategic Spine Tree-- (used heavily by Trees docs)-- =========================
CREATE OR REPLACE VIEW vw_strategic_spine_tree ASSELECT  
np.id AS national_policy_id,  np.code AS national_policy_code,  np.name_th AS national_policy_name_th,  mp.id AS master_plan_id,  mp.code AS master_plan_code,  mp.name_th AS master_plan_name_th,  sg.id AS strategic_goal_id,  sg.code AS strategic_goal_code,  sg.name_th AS strategic_goal_name_th,  st.id AS tactic_id,  st.code AS tactic_code,  st.name_th AS tactic_name_th,  pg.id AS program_id,  pg.code AS program_code,  pg.name_th AS program_name_th,  prj.id AS project_id,  prj.code AS project_code,  prj.name_th AS project_name_th,  prj.fiscal_yearFROM ems_master_plans mpLEFT JOIN strategic_goals sg ON sg.master_plan_id = mp.idLEFT JOIN national_policies np ON np.id = sg.national_policy_idLEFT JOIN strategic_tactics st ON st.strategic_goal_id = sg.idLEFT JOIN programs pg ON pg.strategic_tactic_id = st.idLEFT JOIN projects prj ON prj.program_id = pg.idWHERE mp.status = 'active';
-- =========================
-- VW02: KPI RAG by period_key
-- =========================
CREATE OR REPLACE VIEW vw_kpi_rag_period ASWITH 
perf AS (  SELECT    kp.kpi_id,    kp.period_key,    MIN(kp.period_start) AS period_start,    MAX(kp.period_end) AS period_end,    SUM(kp.reported_value) AS reported_value,    MIN(kp.unit) AS unit  FROM kpi_performance kp  WHERE kp.status = 'active'  GROUP BY kp.kpi_id, kp.period_key),tgt AS (  SELECT    kt.kpi_id,    kt.fiscal_year,    kt.period_type,    kt.period_label,    kt.period_key,    kt.target_value,    kt.unit  FROM kpi_targets kt  WHERE kt.status = 'active')SELECT  k.id AS kpi_id,  k.code AS kpi_code,  k.name_th AS kpi_name_th,  COALESCE(tgt.period_key, perf.period_key) AS period_key,  tgt.fiscal_year,  tgt.period_type,  tgt.period_label,  perf.period_start,  perf.period_end,  tgt.target_value,  perf.reported_value,  COALESCE(tgt.unit, perf.unit) AS unit,  CASE    WHEN tgt.target_value IS NULL OR perf.reported_value IS NULL THEN 'GRAY'    WHEN perf.reported_value >= tgt.target_value THEN 'GREEN'    WHEN perf.reported_value >= (tgt.target_value * 0.9) THEN 'AMBER'    ELSE 'RED'  END AS rag_statusFROM kpis kLEFT JOIN tgt ON tgt.kpi_id = k.idLEFT JOIN perf ON perf.kpi_id = k.id AND perf.period_key = tgt.period_keyWHERE k.status = 'active';
-- =========================
-- VW03: Budget Execution Project
-- =========================
CREATE OR REPLACE VIEW vw_budget_execution_project ASSELECT  
prj.id AS project_id,  prj.code AS project_code,  prj.name_th AS project_name_th,  prj.fiscal_year,  s.snapshot_date,  SUM(s.approved_amount) AS approved_amount,  SUM(s.disbursed_amount) AS disbursed_amount,  SUM(COALESCE(s.commitment_amount,0)) AS commitment_amount,  SUM(COALESCE(s.remaining_amount,0)) AS remaining_amount,  CASE    WHEN SUM(s.approved_amount) > 0 THEN ROUND((SUM(s.disbursed_amount) / SUM(s.approved_amount)) * 100.0, 2)    ELSE NULL  END AS percent_disbursedFROM budget_execution_snapshots sJOIN projects prj ON prj.id = s.project_idWHERE s.status = 'active' AND prj.status = 'active'GROUP BY prj.id, prj.code, prj.name_th, prj.fiscal_year, s.snapshot_date;
-- =========================
-- VW04: Evidence Coverage
-- =========================
CREATE OR REPLACE VIEW vw_evidence_coverage ASSELECT  
prj.id AS project_id,  prj.code AS project_code,  prj.name_th AS project_name_th,  prj.fiscal_year,  ec.kpi_id,  k.code AS kpi_code,  ec.budget_line_id,  ec.section15_id,  s15.number AS section15_number,  COUNT(ec.id) AS evidence_link_count,  COUNT(DISTINCT ec.evidence_asset_id) AS distinct_asset_count,  COUNT(*) FILTER (WHERE ea.is_personal_data = true) AS personal_data_count,  COUNT(*) FILTER (WHERE ea.classification IN ('confidential','restricted')) AS high_class_countFROM evidence_chain ecLEFT JOIN evidence_assets ea ON ea.id = ec.evidence_asset_idLEFT JOIN projects prj ON prj.id = ec.project_idLEFT JOIN kpis k ON k.id = ec.kpi_idLEFT JOIN section15_master s15 ON s15.id = ec.section15_idWHERE ec.status = 'active'GROUP BY  prj.id, prj.code, prj.name_th, prj.fiscal_year,  ec.kpi_id, k.code,  ec.budget_line_id,  ec.section15_id, s15.number;
-- =========================
-- VW05: Data Quality Heatmap (monthly)
-- =========================
CREATE OR REPLACE VIEW vw_data_quality_heatmap ASSELECT  
dqi.system_name,  dqi.issue_type,  date_trunc('month', dqi.created_at)::date AS month_bucket,  dqi.kpi_id,  k.code AS kpi_code,  COUNT(*) AS issue_countFROM data_quality_issues dqiLEFT JOIN kpis k ON k.id = dqi.kpi_idWHERE dqi.status = 'active'GROUP BY dqi.system_name, dqi.issue_type, month_bucket, dqi.kpi_id, k.code;
-- =========================
-- VW07: Activity Progress Rollup
-- =========================
CREATE OR REPLACE VIEW vw_activity_progress_rollup ASSELECT  
ai.id AS activity_id,  ai.project_id,  prj.code AS project_code,  prj.name_th AS project_name_th,  ai.activity_type_id,  at.code AS activity_type_code,  at.name_th AS activity_type_name_th,  ai.name_th AS activity_name_th,  ai.planned_start,  ai.planned_end,  ai.actual_start,  ai.actual_end,  CASE    WHEN ai.actual_end IS NOT NULL THEN 'COMPLETED'    WHEN ai.actual_start IS NOT NULL THEN 'IN_PROGRESS'    ELSE 'NOT_STARTED'  END AS activity_status,  CASE    WHEN ai.planned_end IS NOT NULL AND ai.actual_end IS NULL AND current_date > ai.planned_end THEN (current_date - ai.planned_end)    WHEN ai.planned_end IS NOT NULL AND ai.actual_end IS NOT NULL AND ai.actual_end > ai.planned_end THEN (ai.actual_end - ai.planned_end)    ELSE 0  END AS schedule_slip_days,  COUNT(d.id) AS linked_daily_logsFROM activity_instances aiJOIN projects prj ON prj.id = ai.project_idJOIN activity_types at ON at.id = ai.activity_type_idLEFT JOIN daily_ops_logs d ON d.id = ai.daily_idWHERE ai.status = 'active' AND prj.status = 'active'GROUP BY  ai.id, ai.project_id, prj.code, prj.name_th,  ai.activity_type_id, at.code, at.name_th,  ai.name_th, ai.planned_start, ai.planned_end, ai.actual_start, ai.actual_end;
-- =========================
-- VW08: Risk Register Project
-- =========================
CREATE OR REPLACE VIEW vw_risk_register_project ASSELECT  
r.id AS risk_id,  r.project_id,  prj.code AS project_code,  prj.name_th AS project_name_th,  prj.fiscal_year,  r.description,  r.likelihood,  r.impact,  COALESCE(r.score, (r.likelihood * r.impact)) AS computed_score,  r.mitigation_plan,  r.related_daily_id,  d.log_date AS related_log_date,  d.title AS related_log_titleFROM risks rLEFT JOIN projects prj ON prj.id = r.project_idLEFT JOIN daily_ops_logs d ON d.id = r.related_daily_idWHERE r.status = 'active';
-- =========================
-- VW09: Result Chain Paths (recursive)
-- =========================
CREATE OR REPLACE VIEW vw_result_chain_paths ASWITH RECURSIVE 
paths AS (  SELECT    r.id AS root_node_id,    r.id AS current_node_id,    r.name_th AS current_node_name_th,    r.level AS current_level,    ARRAY[r.id] AS path_ids,    0 AS depth  FROM result_chains r  WHERE r.status = 'active'  UNION ALL  SELECT    p.root_node_id,    e.child_node_id AS current_node_id,    rc.name_th AS current_node_name_th,    rc.level AS current_level,    p.path_ids || e.child_node_id,    p.depth + 1  FROM paths p  JOIN result_chain_edges e ON e.parent_node_id = p.current_node_id AND e.status = 'active'  JOIN result_chains rc ON rc.id = e.child_node_id AND rc.status = 'active'  WHERE p.depth < 20)SELECT  root_node_id,  current_node_id,  current_node_name_th,  current_level,  depth,  path_idsFROM paths;
-- =========================
-- VW10: Evidence Compliance (PDPA/IR)
-- =========================
CREATE OR REPLACE VIEW vw_evidence_compliance_pdpa_ir ASSELECT  
ea.id AS evidence_asset_id,  ea.checksum_sha256,  ea.file_url,  ea.mime_type,  ea.bytes_size,  ea.classification,  ea.retention_until,  ea.is_personal_data,  ea.owner_org_unit_id,  ou.code AS owner_org_unit_code,  ou.name_th AS owner_org_unit_name_th,  COUNT(ec.id) AS usage_links,  COUNT(ec.id) FILTER (WHERE ec.project_id IS NULL AND ec.kpi_id IS NULL AND ec.budget_line_id IS NULL AND ec.section15_id IS NULL) AS orphan_linksFROM evidence_assets eaLEFT JOIN org_units ou ON ou.id = ea.owner_org_unit_idLEFT JOIN evidence_chain ec ON ec.evidence_asset_id = ea.id AND ec.status = 'active'WHERE ea.status = 'active'GROUP BY  ea.id, ea.checksum_sha256, ea.file_url, ea.mime_type, ea.bytes_size, ea.classification,  ea.retention_until, ea.is_personal_data, ea.owner_org_unit_id, ou.code, ou.name_th;COMMIT;


