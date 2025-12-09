A. Data Dictionary (Markdown)

A0. ฟิลด์มาตรฐาน (ใช้กับทุก List)
Field	Type	Description
id	string	Primary key (UUID หรือรหัสภายใน)
created_at	datetime	วันที่–เวลาที่สร้าง
created_by	string	ผู้สร้าง (user id / system)
updated_at	datetime	วันที่–เวลาที่แก้ไขล่าสุด
updated_by	string	ผู้แก้ไขล่าสุด
status	enum	สถานะ (active/inactive/draft/archived ฯลฯ)
กลุ่ม A – Policy / Strategy / Law (Lists 1–8)
1. national_policies

นโยบาย/ยุทธศาสตร์ระดับชาติที่เกี่ยวข้องกับ EMS

Field	Type	Description
code	string	รหัสนโยบาย/ยุทธศาสตร์
name_th	string	ชื่อนโยบาย (ไทย)
name_en	string	ชื่อนโยบาย (อังกฤษ)
description	text	คำอธิบายโดยสรุป
issuing_agency	string	หน่วยงานเจ้าของนโยบาย (เช่น รัฐบาล, สธ., ฯลฯ)
start_year	integer	ปีเริ่มต้น
end_year	integer	ปีสิ้นสุด (ถ้ามี)
2. ems_master_plans

แผนหลักการแพทย์ฉุกเฉินระดับประเทศ (เช่น ฉบับที่ 4 พ.ศ. 2566–2570)

Field	Type	Description
code	string	รหัสแผน (เช่น EMSMP4)
name_th	string	ชื่อแผน
period_start	integer	ปีเริ่มต้น
period_end	integer	ปีสิ้นสุด
legal_basis_id	fk(legal_frameworks)	อ้างอิงฐานกฎหมาย
document_url	string	ลิงก์เอกสารฉบับเต็ม
3. strategic_goals

เป้าหมายเชิงยุทธศาสตร์ของ EMS/NIEMS

Field	Type	Description
code	string	รหัสเป้าหมาย
name_th	string	ชื่อเป้าหมาย
description	text	รายละเอียด
master_plan_id	fk(ems_master_plans)	อยู่ภายใต้แผนหลักใด
national_policy_id	fk(national_policies)	เชื่อมกับยุทธศาสตร์ชาติข้อใด
4. strategic_tactics

กลยุทธ์/ยุทธศาสตร์ย่อย/โปรแกรมหลัก

Field	Type	Description
code	string	รหัสกลยุทธ์/โปรแกรม
name_th	string	ชื่อกลยุทธ์
description	text	รายละเอียด
strategic_goal_id	fk(strategic_goals)	อยู่ภายใต้เป้าหมายใด
priority_level	enum	สูง/กลาง/ต่ำ
5. legal_frameworks

กฎหมาย/ระเบียบ/ประกาศที่เกี่ยวข้อง

Field	Type	Description
law_code	string	รหัสกฎหมาย/มาตรา
name_th	string	ชื่อกฎหมาย
section	string	มาตรา (เช่น ม.15, ม.16)
description	text	สาระสำคัญ
effective_date	date	มีผลใช้บังคับตั้งแต่
reference_url	string	ลิงก์เอกสารกฎหมาย
6. section15_master

ภารกิจตามมาตรา 15 ทั้ง 9 วงเล็บ

Field	Type	Description
number	integer	เลขวงเล็บ (1–9)
name_th	string	ชื่อภารกิจ
description	text	คำอธิบายภารกิจ
law_id	fk(legal_frameworks)	อ้างอิงมาตราที่เกี่ยวข้อง
7. external_strategies

ยุทธศาสตร์/นโยบายของหน่วยงานภายนอก (เช่น UN, WHO, NESDC ฯลฯ)

Field	Type	Description
code	string	รหัสยุทธศาสตร์
name_th	string	ชื่อ (ไทย ถ้ามี)
name_en	string	ชื่อ (อังกฤษ)
organization	string	เจ้าของยุทธศาสตร์
description	text	รายละเอียด
8. governance_bodies

คณะกรรมการ/อนุกรรมการ/คณะทำงาน

Field	Type	Description
name_th	string	ชื่อคณะกรรมการ/คณะทำงาน
role	string	บทบาทหน้าที่หลัก
legal_basis_id	fk(legal_frameworks)	อ้างอิงกฎหมาย/ระเบียบ
scope	text	ขอบเขตอำนาจหน้าที่
secretariat_org	string	หน่วยงานเลขานุการ
กลุ่ม B – Program / Project / Activity (Lists 9–16)
9. programs

แผนงาน/โปรแกรมหลัก (เช่น แผนงานบุคลากร, แผนงานท่องเที่ยว ฯลฯ)

Field	Type	Description
code	string	รหัสโปรแกรม/แผนงาน
name_th	string	ชื่อแผนงาน
description	text	รายละเอียด
strategic_tactic_id	fk(strategic_tactics)	อยู่ภายใต้กลยุทธ์ใด
budget_program_id	fk(budget_programs)	mapping กับโครงสร้างงบประมาณราชการ
10. result_chains

Result chain / Logic model (input→process→output→outcome→impact)

Field	Type	Description
name_th	string	ชื่อ chain/โมดูล
level	enum	input/process/output/outcome/impact
description	text	คำอธิบาย
strategic_goal_id	fk(strategic_goals)	ผูกกับเป้าหมาย
program_id	fk(programs)	อยู่ภายใต้แผนงานใด
11. projects

โครงการ (F-/I-/EC-)

Field	Type	Description
code	string	รหัสโครงการ (F-/I-/EC-)
name_th	string	ชื่อโครงการ
description	text	รายละเอียดโครงการ
fiscal_year	integer	ปีงบประมาณ
program_id	fk(programs)	อยู่ภายใต้แผนงานใด
strategic_tactic_id	fk(strategic_tactics)	เชื่อมกลยุทธ์
owner_org_unit	string	สำนัก/กลุ่มเจ้าภาพหลัก
section15_coverage_note	text	ข้อสังเกตภารกิจ ม.15 ที่เกี่ยวข้อง (เสริมจาก table 40)
12. project_budget_lines

รายการงบประมาณต่อโครงการ/หมวดรายจ่าย

Field	Type	Description
project_id	fk(projects)	โครงการแม่
line_code	string	รหัสบรรทัดงบ (ถ้ามี)
line_name	string	ชื่อรายการ (เช่น ค่าใช้จ่ายบุคลากร, ค่าเดินทาง)
budget_type	enum	personnel/operating/investment/other
approved_amount	decimal	วงเงินอนุมัติทั้งปี
fund_source_id	fk(fund_sources)	แหล่งงบ
13. activity_types

ชนิดกิจกรรมมาตรฐาน (ใช้เป็น codebook)

Field	Type	Description
code	string	รหัสชนิดกิจกรรม
name_th	string	ชื่อ เช่น ประชุม, ฝึกอบรม, ฝึกซ้อม, ลงพื้นที่
description	text	รายละเอียด/ตัวอย่าง
default_section15_ids	text	ภารกิจ ม.15 ที่มักจะเกี่ยวข้อง (เก็บเป็น list/JSON)
14. activity_instances

กิจกรรมที่เกิดขึ้นตามแผน (ระดับ “กิจกรรมโครงการ”)

Field	Type	Description
project_id	fk(projects)	โครงการที่สังกัด
activity_type_id	fk(activity_types)	ชนิดกิจกรรม
name_th	string	ชื่อกิจกรรม
description	text	รายละเอียด
planned_start	date	วันที่เริ่มตามแผน
planned_end	date	วันที่สิ้นสุดตามแผน
actual_start	date	วันที่เริ่มจริง
actual_end	date	วันที่สิ้นสุดจริง
location_id	fk(locations)	สถานที่
daily_id	fk(daily_ops_logs)	ลิงก์ไปยังเหตุการณ์รายวันที่สำคัญที่สุด (ถ้ามี)
15. stakeholders

ผู้มีส่วนได้ส่วนเสีย

Field	Type	Description
name_th	string	ชื่อหน่วยงาน/กลุ่ม
stakeholder_type	enum	internal/external/community/etc.
role	string	บทบาทในระบบ EMS
section15_role	string	บทบาทต่อ ม.15 ข้อใดบ้าง (ข้อความสรุป)
contact_info	text	ช่องทางติดต่อ
16. locations

พื้นที่/สถานที่/เขตบริการ

Field	Type	Description
code	string	รหัสพื้นที่
name_th	string	ชื่อ เช่น จังหวัด, เขตสุขภาพ, สนามบิน
loc_type	enum	province/health_region/airport/hospital/other
parent_location_id	fk(locations)	hierarchical (เช่น จังหวัดอยู่ในเขตสุขภาพ)
latitude	decimal	พิกัด (ถ้ามี)
longitude	decimal	พิกัด (ถ้ามี)
กลุ่ม C – KPI / Evaluation (Lists 17–24)
17. kpis

ตัวชี้วัด (28 ตัว + Joint KPIs ฯลฯ)

Field	Type	Description
code	string	รหัส KPI
name_th	string	ชื่อตัวชี้วัด
description	text	คำอธิบาย/นิยาม
kpi_type	enum	input/process/output/outcome/impact
primary_process_step	enum	S/I/P/O/C
data_source_type	enum	system/daily_log/survey/mixed
owner_org_unit	string	หน่วยงานเจ้าภาพ
law_link_id	fk(legal_frameworks)	ถ้ามีฐานกฎหมายรองรับ
18. kpi_targets

เป้าหมายตัวชี้วัดรายปี/รายช่วงเวลา

Field	Type	Description
kpi_id	fk(kpis)	ตัวชี้วัด
fiscal_year	integer	ปีงบประมาณ
period_type	enum	annual/quarterly/monthly
period_label	string	Q1, Q2, M1, H1 ฯลฯ
target_value	decimal	ค่าเป้าหมาย
unit	string	หน่วย เช่น %, คน, ครั้ง
19. kpi_performance

ผลการดำเนินงานของตัวชี้วัด

Field	Type	Description
kpi_id	fk(kpis)	ตัวชี้วัด
period_start	date	วันที่เริ่มช่วงประเมิน
period_end	date	วันที่สิ้นสุดช่วงประเมิน
reported_value	decimal	ค่าจริงที่วัดได้
unit	string	หน่วย
evidence_set_id	fk(evidence_chain)	หลักฐานชุดที่ใช้ยืนยัน
comment	text	หมายเหตุ/วิเคราะห์ผล
20. sipoc_processes

ตาราง SIPOC มาตรฐาน

Field	Type	Description
name_th	string	ชื่อขั้นตอนหรือ process
category	enum	S/I/P/O/C
description	text	คำอธิบาย
system_source	string	ระบบข้อมูลที่เกี่ยวข้อง (NDEMS/ePCR/LINE ฯลฯ)
21. evaluation_frameworks

กรอบการประเมิน (CIPP, ECS-R-I, RE-AIM ฯลฯ)

Field	Type	Description
name	string	ชื่อกรอบ เช่น CIPP
dimension	string	เช่น Context/Input/Process/Product
description	text	รายละเอียดมิติ
usage_note	text	ใช้อย่างไรใน NIEMS
22. risks

Risk Register

Field	Type	Description
project_id	fk(projects)	โครงการที่เกี่ยวข้อง (ถ้ามี)
description	text	คำอธิบายความเสี่ยง
likelihood	integer	ความน่าจะเป็น (1–5)
impact	integer	ผลกระทบ (1–5)
score	integer	ค่ารวม (คำนวณ)
mitigation_plan	text	แผนรองรับ
related_daily_id	fk(daily_ops_logs)	กรณีเกิดเหตุการณ์รายวัน
23. lessons_learned

บทเรียนจากการดำเนินงาน

Field	Type	Description
project_id	fk(projects)	โครงการ
kpi_id	fk(kpis)	ตัวชี้วัด (ถ้ามี)
description	text	สิ่งที่ได้เรียนรู้
recommendation	text	ข้อเสนอแนะต่อไป
evidence_id	fk(evidence_chain)	หลักฐานอ้างอิง
24. recommendations

ข้อเสนอแนะเชิงระบบ

Field	Type	Description
title	string	หัวข้อข้อเสนอแนะ
description	text	รายละเอียด
alignment_id	fk(strategic_project_section15_alignment)	เชื่อมกับระดับใดใน value chain
priority	enum	high/medium/low
responsible_org	string	ผู้รับผิดชอบนำไปปฏิบัติ
กลุ่ม D – Finance / Budget (Lists 25–34)
25. budget_programs

แผนงานงบประมาณราชการ (เช่น 1.1, 1.2, 1.3 ฯลฯ)

Field	Type	Description
code	string	รหัสแผนงานงบประมาณ
name_th	string	ชื่อแผนงาน
description	text	รายละเอียด
law_basis_id	fk(legal_frameworks)	ถ้ามี
26. budget_allocations

การจัดสรรงบตามหน่วยงาน/แผน/โครงการ

Field	Type	Description
fiscal_year	integer	ปีงบประมาณ
org_unit	string	สำนัก/กลุ่ม
budget_program_id	fk(budget_programs)	แผนงานงบ
project_id	fk(projects)	โครงการ
approved_amount	decimal	วงเงินจัดสรร
27. financial_transactions

รายการเบิกจ่าย/ผูกพัน

Field	Type	Description
project_budget_line_id	fk(project_budget_lines)	ผูกกับบรรทัดงบ
transaction_date	date	วันที่ทำรายการ
amount	decimal	จำนวนเงิน
transaction_type	enum	disbursement/commitment/adjustment
document_ref	string	เลขที่เอกสาร (ใบสำคัญ/PO ฯลฯ)
evidence_id	fk(evidence_chain)	หลักฐานประกอบ
28. budget_revisions

ข้อมูลการปรับแผนงบ (ต้นปี/กลางปี/ปลายปี)

Field	Type	Description
project_budget_line_id	fk(project_budget_lines)	
revision_round	enum	initial/mid-year/end-year
old_amount	decimal	จำนวนเดิม
new_amount	decimal	จำนวนใหม่
reason	text	เหตุผล
29. fund_sources

แหล่งงบประมาณ

Field	Type	Description
code	string	รหัสแหล่งงบ
name_th	string	ชื่อ เช่น งบสถาบัน, กองทุนการแพทย์ฉุกเฉิน
description	text	รายละเอียด
30. unit_cost_models

แบบจำลองต้นทุนหน่วยบริการ

Field	Type	Description
name_th	string	ชื่อ model
description	text	รายละเอียด
unit_definition	string	หน่วย เช่น ต่อ case, ต่อคน, ต่อครั้ง
formula	text	สูตรคำนวณ (pseudo-code)
31. financial_kpis

ตัวชี้วัดด้านการเงิน

Field	Type	Description
code	string	รหัส
name_th	string	ชื่อตัวชี้วัด
description	text	รายละเอียด
calculation	text	วิธีคำนวณ
32. audit_records

บันทึกการตรวจสอบ/สอบทาน

Field	Type	Description
project_id	fk(projects)	โครงการ
audit_date	date	วันที่ตรวจ
auditor_org	string	หน่วยงานตรวจ
findings	text	ข้อค้นพบ
recommendations	text	ข้อเสนอแนะ
evidence_id	fk(evidence_chain)	เอกสารประกอบ
33. data_quality_issues

ประเด็นคุณภาพข้อมูล

Field	Type	Description
system_name	string	ระบบที่พบ (NDEMS/ePCR/LINE ฯลฯ)
kpi_id	fk(kpis)	ตัวชี้วัดที่ได้รับผลกระทบ
issue_type	string	ประเภทปัญหา (missing, inconsistent, delay ฯลฯ)
description	text	รายละเอียด
daily_id	fk(daily_ops_logs)	ถ้าเกิดจากเหตุการณ์รายวัน
resolution_note	text	วิธีแก้ไข
34. system_lookups

ตาราง code/lookup อื่น ๆ

Field	Type	Description
category	string	ประเภท lookup เช่น org_unit, project_type ฯลฯ
code	string	รหัส
label_th	string	ป้ายภาษาไทย
label_en	string	ป้ายอังกฤษ
กลุ่ม E – Operations & Evidence (Lists 35–40 – ใหม่)
35. daily_ops_logs

บันทึกการดำเนินงาน/กิจกรรมรายวัน

Field	Type	Description
log_date	date	วันที่เกิดเหตุการณ์
time_from	time	เวลาเริ่ม
time_to	time	เวลาสิ้นสุด (ถ้ามี)
title	string	หัวข้อกิจกรรม (หัวข้อโพสต์ LINE)
description	text	เนื้อหาจาก LINE Note / สรุปกิจกรรม
activity_type_id	fk(activity_types)	ชนิดกิจกรรม
org_unit	string	สำนัก/กลุ่ม/ทีมที่เกี่ยวข้อง
location_id	fk(locations)	พื้นที่
project_id	fk(projects)	โครงการที่เกี่ยวข้อง (ถ้ามี)
kpi_id	fk(kpis)	ตัวชี้วัดที่เกี่ยวข้อง (ถ้ามี)
section15_primary_id	fk(section15_master)	ภารกิจหลักที่เกี่ยวข้อง
section15_secondary_note	text	ภารกิจอื่นๆ ที่เกี่ยวข้อง (ข้อความเสริม)
linear_issue_id	string	ID จาก Linear (ถ้าเชื่อมแล้ว)
github_event_id	string	ID ของ event ใน GitHub Data Lake
36. evidence_chain

เชื่อมหลักฐานกับกิจกรรม/KPI/ภารกิจ/งบ

Field	Type	Description
daily_id	fk(daily_ops_logs)	หลักฐานเชื่อมกับ event วันใด
activity_id	fk(activity_instances)	กิจกรรมแผนงานที่เกี่ยวข้อง
project_id	fk(projects)	โครงการ
kpi_id	fk(kpis)	ตัวชี้วัด
budget_line_id	fk(project_budget_lines)	บรรทัดงบประมาณ
section15_id	fk(section15_master)	ภารกิจ ม.15
file_url	string	ที่อยู่ไฟล์ (GitHub/Drive/SharePoint ฯลฯ)
file_type	string	ชนิดไฟล์ (image/pdf/docx ฯลฯ)
evidence_type	string	เช่น รูปถ่าย, รายงาน, บันทึกประชุม
confidence_level	enum	low/medium/high
37. section15_keyword_mapping

แมปคำสำคัญ → ภารกิจ ม.15

Field	Type	Description
keyword	string	คำ/วลีที่พบในข้อความ
section15_id	fk(section15_master)	ภารกิจที่เกี่ยวข้อง
weight	integer	น้ำหนัก (เช่น 1–10)
note	text	หมายเหตุการใช้งาน/ข้อจำกัด
38. budget_execution_snapshots

Snapshot สถานะการใช้จ่ายงบ ณ เวลาใดเวลาหนึ่ง

Field	Type	Description
snapshot_date	date	วันที่ของ snapshot (เช่น 2568-11-30)
project_id	fk(projects)	โครงการ
budget_line_id	fk(project_budget_lines)	รายการงบ
approved_amount	decimal	อนุมัติทั้งปี
disbursed_amount	decimal	เบิกจ่ายแล้ว
commitment_amount	decimal	PO/PR
remaining_amount	decimal	คงเหลือ
percent_disbursed	decimal	ร้อยละเบิกจ่าย
39. kpi_sipoc_linkages

เชื่อม KPI ↔ SIPOC

Field	Type	Description
kpi_id	fk(kpis)	ตัวชี้วัด
sipoc_id	fk(sipoc_processes)	ขั้นตอนในกระบวนการ
process_step	enum	S/I/P/O/C
data_source	string	แหล่งข้อมูล (เช่น NDEMS, ePCR, DailyOps)
frequency	enum	monthly/quarterly/annual
owner_org_unit	string	หน่วยงานเจ้าภาพ collecting data
40. strategic_project_section15_alignment

เมทริกซ์เชื่อมยุทธศาสตร์ ↔ โครงการ ↔ ม.15 ↔ KPI

Field	Type	Description
strategic_goal_id	fk(strategic_goals)	เป้าหมายยุทธศาสตร์
tactic_id	fk(strategic_tactics)	กลยุทธ์/โปรแกรมย่อย
project_id	fk(projects)	โครงการ
section15_id	fk(section15_master)	ภารกิจตาม ม.15
kpi_id	fk(kpis)	ตัวชี้วัด
weight	integer	น้ำหนักความสำคัญ (1–10)
note	text	คำอธิบาย/ข้อสมมติ