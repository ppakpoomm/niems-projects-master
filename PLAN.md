# NIEMS Projects Master Implementation Plan

## Phase 1 – ตั้ง Repo + โครงสร้าง ✅

- [x] สร้าง repo ใหม่ชื่อ `niems-projects-master` (public)
- [x] Clone ลงเครื่อง
- [x] สร้างโฟลเดอร์ใน repo: `data/`, `schema/`, `docs/`, `docs/assets/`
- [x] เขียน README ให้ชัดเจน

## Phase 2 – GitHub Pages + Dashboard

- [ ] สร้าง `docs/index.html`
- [ ] สร้าง `docs/assets/main.js`
- [ ] เปิด GitHub Pages (Settings → Pages → Source: main, folder: /docs)
- [ ] ทดสอบเปิด `https://ppakpoomm.github.io/niems-projects-master/`

## Phase 3 – Linear Integration (Manual)

- [ ] กำหนดโครง Workspace/Teams ใน Linear
- [ ] สร้าง Custom Fields: `project_code`, `fiscal_year`, `program_code`, `owner_org_unit`, `fund_source`, `section15_main`
- [ ] ใช้ Projects Master เป็น reference เวลาเปิด issue/project ใหม่

## Phase 4 – Automation (Future)

- [ ] เขียน script (Node.js/Python) อ่าน CSV จาก GitHub
- [ ] ใช้ Linear API สร้าง/อัปเดต Issues
- [ ] ใช้ GitHub Actions trigger เมื่อมี push ในโฟลเดอร์ `data/`
