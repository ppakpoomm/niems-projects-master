1) Databases Trees Structure — Complete
Document ID: DOC-DB-TREES-01
Version: 1.0 (Canonical)
Status: Locked to Contracts (DDL / Views / PromptPack)
System of Record (SoR): PostgreSQL
Purpose: Provide canonical data hierarchy + join spines for strategic planning, annual/5-year plans, M&E, budget execution, evidence governance, and ecosystem traceability.


 0. Contract Anchors (MUST be identical across all documents)
DB Contract (Ground truth)

db/migrations/0001_init.sql  
Views Contract (MVP10)

VW01 vw_trace__alignment_spine__mvp  
VW02 vw_budget__strategy_to_execution__mvp  
VW03 vw_budget__execution_rag__mvp  
VW04 vw_kpi__performance_vs_target__mvp  
VW05 vw_kpi__rag_dashboard__mvp  
VW06 vw_evidence__coverage_matrix__mvp  
VW07 vw_data_quality__heatmap__mvp  
VW08 vw_activity__progress_slippage__mvp  
VW09 vw_section15__coverage_by_strategy__mvp  
VW10 vw_graph__projection_edges__mvp  
Automation Contract (Prompt Modules PM01–PM10)

PM01 Migrations/DDL generator  
PM02 Views generator (VW01–VW10)  
PM03 Seed/Master data loader  
PM04 Excel ingestion ETL (staging→validate→upsert)  
PM05 Forms/Lists ingestion ETL  
PM06 Canonical upsert engine (idempotent, watermark)  
PM07 Validation gates (A–E) + CI enforcement  
PM08 Graph projection sync job (read-only)  
PM09 Data quality rules + anomaly flags  
PM10 Documentation assembler (anchors + cross-links)  
Validation Gates (Global)

Gate A: DDL compile + constraints valid  
Gate B: Views compile  
Gate C: ETL idempotency pass  
Gate D: period_key conformance ≥ 99%  
Gate E: evidence coverage increasing trend  


 1. Canonical Tree Rules (Non-negotiable)
1.1 Key Semantics

PK: id (uuid) — default primary key for all tables unless stated otherwise  
Natural Key: code (or business composite) used for ETL upsert and human traceability  
FK: *_id only; legacy strings allowed during transition (see 1.3)  
1.2 Naming Standard (Constraints/Indexes)

PK: pk_<table>  
FK: fk_<from>__<to>__<cols> or fallback ...__h<8>  
UQ: uq_<table>__<cols> or fallback ...__h<8>  
CK: ck_<table>__<rule>  
IX: ix_/ixg_/ixs_... + fallback ...__h<8>  
1.3 Transition Rules (Deprecation-safe)

Org unit: prefer *_org_unit_id → legacy *_org_unit kept until cutover  
Evidence: prefer evidence_asset_id → legacy file_url accepted until cutover  
Period: require period_key; period_label is display-only  
1.4 Output Rule for Every Node
Every node below MUST declare:

table, pk, natural key(s), parent fk(s), critical constraints, critical indexes, used_by_views  


 2. Strategic Spine Tree (Core hierarchy of plans → programs → projects)
Primary Use: planning alignment, annual/5-year plan compilation, traceability
Join Spine Views: VW01, VW02, VW09
2.1 Tree (Hierarchy)
national_policies 
 └─ ems_master_plans      
└─ strategic_goals          
└─ strategic_tactics              
└─ programs                  
└─ projects
2.2 Node Specifications (Strategic Spine)
Node: national_policies

table: national_policies  
pk: id  
natural keys: code (unique)  
parent fk: (root)  
critical constraints: uq_national_policies__code  
critical indexes: ix_national_policies__code  
used_by_views: VW01, VW02  
Node: ems_master_plans

table: ems_master_plans  
pk: id  
natural keys: code (unique), period_start/period_end  
parent fk: optional linkage via legal_basis_id → legal_frameworks.id  
critical constraints: uq_ems_master_plans__code  
critical indexes: ix_ems_master_plans__code, ix_ems_master_plans__period_start_period_end  
used_by_views: VW01  
Node: strategic_goals

table: strategic_goals  
pk: id  
natural keys: code (unique within master_plan recommended)  
parent fk: master_plan_id → ems_master_plans.id, optional national_policy_id → national_policies.id  
critical constraints: uq_strategic_goals__master_plan_id_code (recommended)  
critical indexes: ix_strategic_goals__master_plan_id, ix_strategic_goals__national_policy_id, ix_strategic_goals__code  
used_by_views: VW01, VW02, VW09  
Node: strategic_tactics

table: strategic_tactics  
pk: id  
natural keys: code (unique within goal recommended)  
parent fk: strategic_goal_id → strategic_goals.id  
critical constraints: ck_strategic_tactics__priority_level_enum (if enum), uq_strategic_tactics__strategic_goal_id_code (recommended)  
critical indexes: ix_strategic_tactics__strategic_goal_id, ix_strategic_tactics__code  
used_by_views: VW01, VW02, VW09  
Node: programs

table: programs  
pk: id  
natural keys: code (unique), optional budget_program_id  
parent fk: strategic_tactic_id → strategic_tactics.id, optional budget_program_id → budget_programs.id  
critical constraints: uq_programs__code  
critical indexes: ix_programs__strategic_tactic_id, ix_programs__budget_program_id  
used_by_views: VW02  
Node: projects

table: projects  
pk: id  
natural keys: code (unique), fiscal_year  
parent fk: program_id → programs.id, optional strategic_tactic_id → strategic_tactics.id  
org unit transition: owner_org_unit_id preferred; owner_org_unit legacy string allowed  
critical constraints: ck_projects__fiscal_year_valid, uq_projects__code (or uq_projects__fiscal_year_code)  
critical indexes: ix_projects__program_id, ix_projects__fiscal_year, ix_projects__owner_org_unit_id  
used_by_views: VW01, VW02, VW06, VW08, VW09  


 3. Performance Tree (KPI → targets → performance)
Primary Use: KPI tracking, RAG dashboards, quarterly/annual reporting
Join Spine Views: VW04, VW05 (plus VW01 for alignment context)
3.1 Tree (Hierarchy)
kpis  
├─ kpi_targets (period_key)  
└─ kpi_performance (period_key, evidence_set_id)
3.2 Node Specifications
Node: kpis

table: kpis  
pk: id  
natural keys: code (unique)  
parent fk: optional law_link_id → legal_frameworks.id  
org unit transition: owner_org_unit_id preferred; owner_org_unit legacy allowed  
critical constraints: uq_kpis__code, ck_kpis__kpi_type_enum  
critical indexes: ix_kpis__code, ix_kpis__owner_org_unit_id, ix_kpis__kpi_type  
used_by_views: VW04, VW05, VW01, VW06  
Node: kpi_targets

table: kpi_targets  
pk: id  
natural keys: (kpi_id, fiscal_year, period_key) unique  
parent fk: kpi_id → kpis.id  
period standard: period_key required (e.g., 2569-Q1, 2569-01, 2569-H1, 2569-Y)  
critical constraints: uq_kpi_targets__kpi_id_fiscal_year_period_key, ck_kpi_targets__period_key_fmt  
critical indexes: ix_kpi_targets__kpi_id_period_key, ix_kpi_targets__fiscal_year  
used_by_views: VW04, VW05  
Node: kpi_performance

table: kpi_performance  
pk: id  
natural keys: (kpi_id, period_key, period_start, period_end) recommended unique  
parent fk: kpi_id → kpis.id, optional evidence_set_id → evidence_chain.id  
period standard: period_key required; period_start/end canonical for timebox truth  
critical constraints: ck_kpi_performance__period_key_fmt, ck_kpi_performance__period_range_valid  
critical indexes: ix_kpi_performance__kpi_id_period_key, ix_kpi_performance__period_start_period_end  
used_by_views: VW04, VW05, VW06  


 4. Budget Tree (Budget program → allocation → lines → transactions → snapshots)
Primary Use: budget planning, execution monitoring, fiscal reporting
Join Spine Views: VW02, VW03
4.1 Tree (Hierarchy)
budget_programs  
└─ budget_allocations (fiscal_year, org_unit)      
└─ project_budget_lines          
├─ financial_transactions          
├─ budget_revisions          
└─ budget_execution_snapshots
4.2 Node Specifications
Node: budget_programs

table: budget_programs  
pk: id  
natural keys: code (unique)  
parent fk: optional law_basis_id → legal_frameworks.id  
critical constraints: uq_budget_programs__code  
critical indexes: ix_budget_programs__code  
used_by_views: VW02, VW03  
Node: budget_allocations

table: budget_allocations  
pk: id  
natural keys: (fiscal_year, org_unit_id, budget_program_id) recommended unique  
parent fk: budget_program_id → budget_programs.id, optional project_id → projects.id  
org unit transition: org_unit_id preferred; legacy org_unit string allowed  
critical constraints: ck_budget_allocations__fiscal_year_valid  
critical indexes: ix_budget_allocations__fiscal_year, ix_budget_allocations__budget_program_id, ix_budget_allocations__org_unit_id  
used_by_views: VW02, VW03  
Node: project_budget_lines

table: project_budget_lines  
pk: id  
natural keys: (project_id, line_name) or (project_id, line_code) recommended unique  
parent fk: project_id → projects.id, optional fund_source_id → fund_sources.id  
critical constraints: ck_project_budget_lines__budget_type_enum  
critical indexes: ix_project_budget_lines__project_id, ix_project_budget_lines__fund_source_id  
used_by_views: VW02, VW03, VW06  
Node: financial_transactions

table: financial_transactions  
pk: id  
natural keys: (project_budget_line_id, transaction_date, amount, transaction_type) recommended unique (or document_ref)  
parent fk: project_budget_line_id → project_budget_lines.id, optional evidence_id → evidence_chain.id  
critical constraints: ck_financial_transactions__transaction_type_enum  
critical indexes: ix_financial_transactions__project_budget_line_id, ix_financial_transactions__transaction_date  
used_by_views: VW03, VW06  
Node: budget_execution_snapshots

table: budget_execution_snapshots  
pk: id  
natural keys: (snapshot_date, project_id, budget_line_id) recommended unique  
parent fk: project_id → projects.id, optional budget_line_id → project_budget_lines.id  
critical indexes: ix_budget_execution_snapshots__project_id_snapshot_date, ix_budget_execution_snapshots__snapshot_date  
used_by_views: VW02, VW03  


 5. Evidence Tree (First-class evidence assets → evidence chain)
Primary Use: PDPA/IR compliance, auditability, evidence coverage, dedup/retention
Join Spine Views: VW06, VW07, VW03 (where transactions link evidence)
5.1 Tree (Hierarchy)
evidence_assets (first-class)  
└─ evidence_chain (linkage hub)       
├─ (project_id)       
├─ (kpi_id)       
├─ (activity_id / daily_id)       
├─ (budget_line_id)       
└─ (section15_id)
5.2 Node Specifications
Node: evidence_assets

table: evidence_assets  
pk: id  
natural keys: checksum_sha256 (unique recommended)  
parent fk: optional owner_org_unit_id → org_units.id  
critical constraints: uq_evidence_assets__checksum_sha256, ck_evidence_assets__classification_enum, ck_evidence_assets__retention_valid  
critical indexes: ix_evidence_assets__checksum_sha256, ix_evidence_assets__classification, ix_evidence_assets__owner_org_unit_id  
used_by_views: VW06, VW07, VW03  
Node: evidence_chain

table: evidence_chain  
pk: id  
natural keys: (evidence_asset_id, project_id, kpi_id, activity_id, daily_id, budget_line_id, section15_id) (composite uniqueness optional)  
parent fk: evidence_asset_id → evidence_assets.id (preferred)  
legacy: file_url accepted until cutover  
plus links: project_id, kpi_id, activity_id, daily_id, budget_line_id, section15_id    
critical constraints: ck_evidence_chain__confidence_level_enum  
critical indexes: ix_evidence_chain__project_id, ix_evidence_chain__kpi_id, ix_evidence_chain__activity_id, ix_evidence_chain__daily_id, ix_evidence_chain__budget_line_id, ix_evidence_chain__section15_id  
ix_evidence_chain__evidence_asset_id    
used_by_views: VW06, VW03, VW04/VW05 (via kpi_performance.evidence_set_id)  


 6. Ops & Activities Tree (Types → instances → daily logs; with risks)
Primary Use: WBS/Schedule/Progress/Risk operationalization
Join Spine Views: VW08, VW06 (evidence), VW07 (quality)
6.1 Tree (Hierarchy)
activity_types  
└─ activity_instances (project_id, schedule)        
└─ daily_ops_logs (log_date, link to project/kpi/section15)risks (project_id, related_daily_id)
6.2 Node Specifications
Node: activity_types

table: activity_types  
pk: id  
natural keys: code (unique)  
critical constraints: uq_activity_types__code  
critical indexes: ix_activity_types__code  
used_by_views: VW08  
Node: activity_instances

table: activity_instances  
pk: id  
natural keys: (project_id, activity_type_id, name_th) recommended  
parent fk: project_id → projects.id, activity_type_id → activity_types.id, optional location_id → locations.id, optional daily_id → daily_ops_logs.id  
critical indexes: ix_activity_instances__project_id, ix_activity_instances__planned_start_planned_end, ix_activity_instances__actual_start_actual_end  
used_by_views: VW08, VW06  
Node: daily_ops_logs

table: daily_ops_logs  
pk: id  
natural keys: (log_date, org_unit_id, title) recommended  
parent fk: optional project_id, kpi_id, location_id, activity_type_id, section15_primary_id, and external refs (Linear/GitHub)  
org unit transition: org_unit_id preferred; legacy org_unit string allowed  
critical indexes: ix_daily_ops_logs__log_date, ix_daily_ops_logs__project_id, ix_daily_ops_logs__kpi_id, ix_daily_ops_logs__org_unit_id, ix_daily_ops_logs__section15_primary_id  
used_by_views: VW08, VW06, VW07  
Node: risks

table: risks  
pk: id  
natural keys: (project_id, description) recommended  
parent fk: project_id → projects.id, optional related_daily_id → daily_ops_logs.id  
critical constraints: ck_risks__likelihood_1_5, ck_risks__impact_1_5  
critical indexes: ix_risks__project_id, ix_risks__related_daily_id, ix_risks__score  
used_by_views: VW08  


 7. Traceability Tree (The “Gold” alignment hub)
Primary Use: real traceability (not decorative reporting), Section 15 compliance mapping
Join Spine Views: VW01, VW09, (and feeds VW10 edges)
7.1 Tree (Conceptual)
strategic_goals / strategic_tactics / projects / section15_master / kpis  
└─ strategic_project_section15_alignment (weight, note)
7.2 Node Specifications
Node: strategic_project_section15_alignment

table: strategic_project_section15_alignment  
pk: id  
natural keys: (strategic_goal_id, project_id, section15_id, tactic_id?, kpi_id?) unique recommended  
parent fk: strategic_goal_id → strategic_goals.id  
project_id → projects.id  
section15_id → section15_master.id  
optional tactic_id → strategic_tactics.id, optional kpi_id → kpis.id    
critical constraints: ck_alignment__weight_1_10  
critical indexes: ix_alignment__project_id, ix_alignment__strategic_goal_id, ix_alignment__section15_id, ix_alignment__kpi_id  
used_by_views: VW01, VW09, VW10  


 8. Governance & Legal Tree (Law → Section 15 → Governance bodies)
Primary Use: mandate traceability, legal basis reporting
Join Spine Views: VW01, VW09 (context), and compliance narratives
8.1 Tree (Hierarchy)
legal_frameworks  
├─ section15_master  
└─ governance_bodies (optional legal_basis_id)
8.2 Node Specifications
Node: legal_frameworks

table: legal_frameworks  
pk: id  
natural keys: law_code (unique)  
critical indexes: ix_legal_frameworks__law_code  
used_by_views: VW01, VW09  
Node: section15_master

table: section15_master  
pk: id  
natural keys: (law_id, number) unique  
parent fk: law_id → legal_frameworks.id  
critical indexes: ix_section15_master__law_id_number  
used_by_views: VW01, VW09, VW06  
Node: governance_bodies

table: governance_bodies  
pk: id  
natural keys: name_th (unique recommended)  
parent fk: optional legal_basis_id → legal_frameworks.id  
critical indexes: ix_governance_bodies__legal_basis_id  
used_by_views: (contextual; optional)  


 9. Org Units Tree (Master org units with hierarchy; cross-cutting)
Primary Use: cleanup string sprawl, reporting by org, access control owner semantics
Join Spine Views: touches VW01/VW02/VW04/VW06/VW07/VW08 depending on table ownership
9.1 Tree (Hierarchy)
org_units  
└─ org_units (self parent)
9.2 Node Specifications
Node: org_units

table: org_units  
pk: id  
natural keys: code (unique), name_th  
parent fk: parent_org_unit_id → org_units.id (nullable)  
critical constraints: uq_org_units__code, ck_org_units__no_self_parent  
critical indexes: ix_org_units__parent_org_unit_id, ix_org_units__code  
used_by_views: all (as dimension)  


 10. Data Quality Tree (Issues by system/KPI/daily; supports heatmap)
Primary Use: data governance, remediation loop, confidence in reporting
Join Spine Views: VW07
10.1 Tree (Hierarchy)
ata_quality_issues  
├─ (kpi_id)  
└─ (daily_id)
10.2 Node Specifications
Node: data_quality_issues

table: data_quality_issues  
pk: id  
natural keys: (system_name, issue_type, kpi_id?, daily_id?, created_at) recommended  
parent fk: optional kpi_id → kpis.id, optional daily_id → daily_ops_logs.id  
critical indexes: ix_dqi__system_name, ix_dqi__kpi_id, ix_dqi__daily_id, ix_dqi__issue_type  
used_by_views: VW07  


 11. Join Spines (Canonical join paths tied to Views Contract)
JS-01 Strategic Trace Spine (VW01)
Goal: “จากนโยบาย → โครงการ → KPI/Section15” แบบ traceable
Canonical path:

strategic_goals.id → strategic_tactics.strategic_goal_id → programs.strategic_tactic_id → projects.program_id  
projects.id ↔ strategic_project_section15_alignment.project_id  
alignment.section15_id → section15_master.id → legal_frameworks.id  
(optional) alignment.kpi_id → kpis.id  
JS-02 Evidence Coverage Spine (VW06)
Goal: “กิจกรรม/ผลลัพธ์มีหลักฐานจริงไหม”
Canonical path:

evidence_assets.id → evidence_chain.evidence_asset_id  
evidence_chain.project_id → projects.id  
evidence_chain.kpi_id → kpis.id  
kpi_performance.evidence_set_id → evidence_chain.id (กรณี evidence set ต่อ performance)  
JS-03 Budget-to-Strategy Spine (VW02)
Goal: “งบไหลจาก program → project → execution และโยงยุทธศาสตร์”
Canonical path:

budget_programs.id → budget_allocations.budget_program_id  
budget_allocations.project_id → projects.id  
projects.program_id → programs.id → strategic_tactics.id → strategic_goals.id  
projects.id → project_budget_lines.project_id → financial_transactions.project_budget_line_id  
budget_execution_snapshots.project_id → projects.id  


 12. Critical Index Map (MVP-level, view-driven)
These are “must have” indexes because Views depend on them:

projects(program_id), projects(fiscal_year), projects(owner_org_unit_id)  
strategic_project_section15_alignment(project_id, strategic_goal_id, section15_id, kpi_id)  
kpi_targets(kpi_id, period_key, fiscal_year)  
kpi_performance(kpi_id, period_key, period_start)  
project_budget_lines(project_id)  
financial_transactions(project_budget_line_id, transaction_date)  
budget_execution_snapshots(project_id, snapshot_date)  
evidence_chain(project_id), evidence_chain(kpi_id), evidence_chain(evidence_asset_id)  
daily_ops_logs(log_date, org_unit_id, project_id, kpi_id)  
risks(project_id, related_daily_id)  
org_units(code, parent_org_unit_id)  
data_quality_issues(system_name, kpi_id, daily_id)  


 13. “Graph-ready” Tree Projection (Hybrid option)
Graph Projection Contract: VW10

Input: canonical tables (no schema rewrite) 
Output: edge_list (from_id, to_id, edge_type, weight?, meta?)  
Seed edges (minimum): strategic_goal → tactic → program → project 
project → kpi (via alignment / evidence / performance) 
project → section15 
project → evidence_asset (via evidence_chain) 


 14. Quality & Consistency Checks (Trees must not drift)

Gate A: FK/CK/UQ/IX naming conforms + DDL compiles  
Gate B: VW01–VW10 compile without missing indexes/fks  
Gate D: period_key matches canonical regex forms  
Gate E: evidence coverage (VW06) shows non-decreasing trend over time  


 End of Document
This Trees spec is “contract-derived”: it MUST NOT invent new tables/fields beyond DDL.
