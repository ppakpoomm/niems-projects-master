1) Activities Database — Complete (WBS/Schedule/Progress/Risk)
Doc ID: docs/05_activities_database.md
Status: Canonical (Phase 4 dependency chain)
Primary Views: VW07 / VW08 / VW04
Primary Modules: PM06 / PM04 (ingest + validate + upsert)
Related Gates: B (Views) / C (ETL) / E (Evidence coverage)


 Contract Anchors (copy/paste identical in all 6 docs)

DB Contract: db/migrations/0001_init.sql  
Views Contract (MVP10): VW01–VW10 VW07 vw_activity_progress_rollup (Activities backbone)  
VW08 vw_risk_register_project (Risk backbone)  
VW04 vw_evidence_coverage (Evidence backbone)    
Automation Contract (Modules): PM01–PM10  
Validation Gates: A (DDL) / B (Views) / C (ETL) / D (period_key) / E (evidence coverage)  


 5.1 Purpose and Scope
This document defines the operational activity data model that enables:

WBS (Work Breakdown Structure) planning at project level  
Schedule control (planned vs actual, slippage)  
Progress roll-up (activity → project → program)  
Risk monitoring with evidence-backed mitigation updates  
Non-goals:

ไม่สร้างตารางใหม่แบบ “ใหญ่ไฟลุก” ในเฟสนี้ 
ไม่ทำระบบ PM เต็มรูปแบบ (dependency graph, critical path) ตอนนี้—แต่เตรียม upgrade path ไว้  


 5.2 Canonical Entities (FK-aligned with DDL)
5.2.1 Core tables (as-is)

activity_types — catalog ของประเภทกิจกรรม (template)  
activity_instances — แผนกิจกรรมรายโครงการ (Plan layer)  
daily_ops_logs — บันทึกปฏิบัติการรายวัน/รายเหตุการณ์ (Execute layer)  
risks — ทะเบียนความเสี่ยง (Risk layer)  
evidence_assets + evidence_chain — หลักฐานแบบ first-class + linkage (Evidence layer)  
projects — ขอบเขตแผนงาน/เจ้าของ/ปีงบ  
locations — พื้นที่/สถานที่จัดกิจกรรม  
5.2.2 Relationships (join spines)

projects (1) -> activity_instances (*) via activity_instances.project_id  
activity_types (1) -> activity_instances (*) via activity_instances.activity_type_id  
daily_ops_logs (*) -> activity_instances (optional) via activity_instances.daily_id (pointer)

หมายเหตุ: โครงสร้าง DDL ปัจจุบันให้ activity_instances.daily_id ชี้กลับไป log ได้ 1 ตัว (optional)


  

Evidence linkage (golden operational trace): evidence_chain.activity_id -> activity_instances.id  
evidence_chain.daily_id -> daily_ops_logs.id  
evidence_chain.project_id -> projects.id    
Risk linkage: risks.project_id -> projects.id  
risks.related_daily_id -> daily_ops_logs.id    


 5.3 Operational Model (How it actually works)
5.3.1 Plan layer: activity_instances
Objective: เก็บ “แผนกิจกรรม” ที่ต้องใช้ทำ WBS+Schedule baseline
Must-have fields (already in schema):

project_id, activity_type_id, name_th  
planned_start, planned_end  
actual_start, actual_end (optional until executed)  
location_id (optional)  
Operational rule (canonical):

Activity plan is valid only if: planned_start <= planned_end (when both exist)  
name_th follows WBS naming convention (defined below)    
5.3.2 Execute layer: daily_ops_logs
Objective: บันทึก “สิ่งที่เกิดขึ้นจริง” แบบถี่และจับต้องได้ (progress events)
Recommended usage pattern:

1 log = 1 event (meeting / training day / site visit / deliverable submission / schedule change) 
Link to project whenever possible: daily_ops_logs.project_id  
Link to activity type when relevant: daily_ops_logs.activity_type_id  
Link to location when relevant: daily_ops_logs.location_id  
5.3.3 Evidence layer: evidence_assets + evidence_chain
Objective: ทำให้ progress/risk “มีหลักฐาน” ตรวจสอบย้อนกลับได้
Canonical rule:

ทุก log ที่อ้างว่า “เสร็จ/ส่งมอบ/ประชุมแล้ว” ต้องมีอย่างน้อย 1 evidence link ภายในรอบเวลาเดียวกัน 
Evidence must be linked through evidence_chain (not “free URL in text”)  
5.3.4 Risk layer: risks
Objective: เชื่อมความเสี่ยงกับงานจริงและเหตุการณ์จริง (related_daily_id)
Rule:

score = likelihood * impact (ถ้าจะคำนวณใน ETL / view)  
ทุกการอัปเดต mitigation ควรถูกบันทึกเป็น daily_ops_logs + evidence  


 5.4 WBS Specification (works now, upgrades later)
5.4.1 WBS coding standard (Phase-0 compatible, no schema change)
เนื่องจาก DDL ปัจจุบันยังไม่มี wbs_code เป็น field แยก เราบังคับผ่าน canonical naming convention ใน activity_instances.name_th:
Format (strict):

WBS:<wbs_code> | <title>  
Example: WBS:1.2.3 | จัดประชุมทบทวนแนวทาง  
WBS:2.1 | ออกแบบแบบฟอร์มรายงานผล    
Parsing rule (ETL PM06):

Extract wbs_code = substring after WBS: before |  
Extract title = substring after |  
Validation rule:

wbs_code regex (recommended): ^[0-9]+(\.[0-9]+)*$  
5.4.2 Optional upgrade (vNext, not required now)
เมื่อระบบนิ่ง ค่อยเพิ่ม field ใน activity_instances:

wbs_code text null  
parent_activity_id uuid null (self FK)  
แต่ตอนนี้ “ห้ามใช้เป็นข้ออ้างให้ระบบไม่เดิน”—เราเดินด้วย convention ก่อน



 5.5 Schedule Specification (Planned vs Actual)
5.5.1 Baseline schedule (in-table, audit-friendly)

Baseline uses planned_start, planned_end  
Actual uses actual_start, actual_end  
5.5.2 Derived schedule metrics (computed in VW07)
Definitions:

planned_duration_days = planned_end - planned_start + 1  
actual_duration_days = actual_end - actual_start + 1  
start_variance_days = actual_start - planned_start  
end_variance_days = actual_end - planned_end  
slippage_days = GREATEST(0, end_variance_days)  
Schedule status (canonical):

ON_TRACK: slippage_days <= 0  
AT_RISK: 1–7 days  
DELAYED: >7 days  
ปรับ threshold ได้ใน view logic แต่ชื่อสถานะควรคงที่เพื่อรายงาน

 5.5.3 Schedule change control (no new tables)
หากต้องปรับแผน:

บันทึกเหตุผลเป็น daily_ops_logs event type “SCHEDULE_CHANGE”  
แนบหลักฐาน (หนังสือ/อีเมล/บันทึกอนุมัติ) ผ่าน evidence_assets + evidence_chain  
เปลี่ยน planned_start/end ได้ แต่ต้องมี audit fields (created/updated) ทำงานจริง  


 5.6 Progress Specification (event-driven, evidence-backed)
5.6.1 Progress event taxonomy (stored in daily_ops_logs.description)
เพื่อให้ดึง progress ได้สม่ำเสมอ ให้ใช้ tag แบบ machine-readable ใน daily_ops_logs.description:
Canonical tags (minimal set):

#PROGRESS:<0-100> (e.g., #PROGRESS:40)  
#MILESTONE:<code> (e.g., #MILESTONE:D1_SUBMITTED)  
#DELIVERABLE:<name> (e.g., #DELIVERABLE:TOR_FINAL)  
#BLOCKER:<text> (optional)  
Example log description:

ประชุมทีมงานสรุป TOR รอบสุดท้าย #PROGRESS:70 #DELIVERABLE:TOR_FINAL  
5.6.2 Progress computation (VW07)

If latest #PROGRESS:x exists within activity window → percent_complete = x  
Else derive proxy from milestone completion count (optional) 
status derived from: percent_complete 
schedule status 
presence of evidence links (VW04) 
Progress status (canonical):

NOT_STARTED (0)  
IN_PROGRESS (1–99)  
COMPLETED (100 + evidence present)  
COMPLETED_NO_EVIDENCE (100 but evidence missing) → นี่คือ “red flag” ที่ระบบต้องโชว์  


 5.7 Risk Specification (project-linked, log-linked)
5.7.1 Scoring and thresholds

risk_score = likelihood * impact (1–25)  
Risk level: LOW 1–5  
MEDIUM 6–12  
HIGH 13–19  
CRITICAL 20–25    
5.7.2 Risk lifecycle (VW08)

Create risk (risks) with mitigation plan  
Every mitigation action: log as daily_ops_logs with #RISK:<risk_id or code>  
attach evidence via evidence_chain    
Risk “active monitoring” if: No mitigation log within N days (policy parameter) 


 5.8 Analytics Views (how reporting binds to reality)
5.8.1 VW07 — vw_activity_progress_rollup (must cover)
Minimum columns (contract-level expectation):

project_id, project_code, activity_id, activity_name  
wbs_code (parsed), planned_start, planned_end, actual_start, actual_end  
percent_complete, progress_status  
schedule_status, slippage_days  
last_log_date, last_progress_value  
5.8.2 VW08 — vw_risk_register_project (must cover)
Minimum columns:

project_id, project_code  
risk_id, description  
likelihood, impact, risk_score, risk_level  
last_related_log_date (from related_daily_id)  
mitigation_evidence_count (from evidence_chain)  
5.8.3 VW04 — vw_evidence_coverage (must cover)
Minimum columns (activity focus):

activity_id, project_id  
evidence_count_total, evidence_count_by_classification  
coverage_status (OK / MISSING / PARTIAL)  


 5.9 Data Capture Interfaces (Forms/Lists that don’t suck)
5.9.1 Minimal Forms (MVP)

Activity Type Catalog Form → activity_types  
Activity Planning Form → activity_instances  
Daily Ops Log Capture → daily_ops_logs  
Risk Register Form → risks  
Validation at input (recommended):

WBS naming format enforced in UI (regex) 
planned_start/end required for planned activities 
progress tags helper buttons (ลดงานพิมพ์) 
5.9.2 Excel ingestion (supports your workbook “Activities” sheet)
จากไฟล์ SMART4MyBook.xlsx แผ่น Activities พบโครงสร้างคอลัมน์หลักใช้งานได้ดี:

WBS  
กิจกรรม/งาน  
ระยะเวลา (วัน)  
วันเริ่ม (แผน) / วันเสร็จ (แผน)  
ผู้รับผิดชอบ  
ความก้าวหน้า (%)  
สถานะ
และมีคอลัมน์ timeline จำนวนมากเพื่อทำ Gantt 
ETL mapping (PM06):

WBS + กิจกรรม/งาน → activity_instances.name_th ด้วย format WBS:<code> | <title>  
วันเริ่ม (แผน) → activity_instances.planned_start  
วันเสร็จ (แผน) → activity_instances.planned_end  
ความก้าวหน้า (%) → เขียนเป็น daily log event ล่าสุด: #PROGRESS:x (ถ้าไม่มี log จริง)  
สถานะ → derive เป็น progress_status ใน VW07 (ไม่ต้องเก็บซ้ำ)  
ข้อดี: ทำให้ Excel เป็น “staging input” ได้โดยไม่ทำลาย canonical model



 5.10 Security / Compliance (PDPA/IR-ready by design)

Evidence เป็นจุดเสี่ยงหลัก: ต้องมี classification, retention_until, checksum_sha256  
daily_ops_logs.description ห้ามใส่ PII แบบไม่จำเป็น (ให้แนบเป็น evidence แล้วกำกับสิทธิ์แทน)  
สิทธิ์เข้าถึง: Ops: เขียน daily logs 
M&E: อ่านทั้งหมด + เขียน lessons/flags 
IR/Legal: อ่าน evidence classified + audit records 


 5.11 Validation and Gates (Definition of Done)
Gate B (Views compile):

VW07/VW08/VW04 compile ผ่าน และให้ผลลัพธ์ตาม contract columns 
Gate C (ETL idempotency):

รัน ETL ซ้ำแล้วไม่สร้าง activity_instances ซ้ำ (ต้องมี upsert key) 
Parsing WBS format ผ่าน ≥ 99% 
Gate E (Evidence coverage trend):

สัดส่วน activities ที่มี evidence_chain ≥ baseline และแนวโน้มเพิ่มขึ้นรายเดือน 


 5.12 Roadmap (no drama, no downtime)
M1 (Now): Convention-first

ใช้ WBS naming convention + progress tags + evidence linkage 
M2: Backfill + tighten rules

ทำ backfill wbs_code (ถ้ามี field แยกใน vNext) 
เพิ่ม CHECK rules ใน ingestion layer 
M3: Enforce “completed requires evidence”

COMPLETED แต่ไม่มีหลักฐาน = red flag ใน dashboard 
M4: Optional schema upgrade (if needed)

เพิ่ม wbs_code, parent_activity_id, percent_complete (ถ้าต้องการเก็บค่าสแน็ปช็อตใน DB)  
