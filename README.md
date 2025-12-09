# \# NIEMS Projects Master – FY2569

# 

# Repository นี้ใช้เก็บข้อมูล \*\*Projects Master\*\* ปีงบประมาณ 2569 ของสถาบันการแพทย์ฉุกเฉินแห่งชาติ (สพฉ.) โดยมีเป้าหมายเพื่อใช้เป็น \*\*Single Source of Truth\*\* สำหรับ:

# 

# \- ระบบติดตามและประเมินผล (M\&E)

# \- Dashboard บน GitHub Pages

# \- Linear app (Project / Issue Management)

# 

# \## 📂 โครงสร้างข้อมูลหลัก

# 

# \- `data/projects\_master\_2569.csv` – ทะเบียนโครงการพร้อม mapping SECTION 15

# \- `schema/DATA\_SCHEMA\_3\_0.md` – Data Schema กลาง (40 Lists)

# \- `schema/projects\_master\_dictionary.md` – Data dictionary เฉพาะ Projects Master

# \- `docs/` – GitHub Pages Dashboard (HTML + JavaScript)

# 

# \## 🌐 Dashboard

# 

# Dashboard สามารถเข้าถึงได้ที่: \[https://ppakpoomm.github.io/niems-projects-master/](https://ppakpoomm.github.io/niems-projects-master/)

# 

# \## 📊 Data Schema

# 

# ดูรายละเอียด Data Schema 3.0 ได้ที่:

# \- \[DATA\_SCHEMA\_3\_0.md](schema/DATA\_SCHEMA\_3\_0.md) - Schema กลางทั้งระบบ (40 lists)

# \- \[projects\_master\_dictionary.md](schema/projects\_master\_dictionary.md) - Dictionary เฉพาะ Projects Master

# 

# \## 🔗 Integration

# 

# \- \*\*GitHub\*\* – Version control และ GitHub Pages

# \- \*\*Linear\*\* – Project management และ issue tracking  

# \- \*\*M\&E System\*\* – Data source สำหรับการติดตามและประเมินผล


## 📚 วิธีการใช้งาน (How to Use)

### 1️⃣ สร้าง Project ใหม่ใน Linear

1. เข้า Linear app ที่ [https://linear.app/mande-niems/team/STR](https://linear.app/mande-niems/team/STR)
2. คลิก **"Create new issue"** หรือกด `C`
3. คลิก **"Template"** และเลือก **"NIEMS Project"**
4. ตั้งชื่อ Project ตามรูปแบบ: `[Type] [Region] [2569] ชื่อโครงการ`
   - **Type**: Research, Development, Training, Policy
   - **Region**: Bangkok, Central, North, Northeast, South, All
   - **ตัวอย่าง**: `[Research] [Bangkok] [2569] การศึกษาผลกระทบสภาพภูมิอากาศ`
5. กรอกข้อมูลใน template ตามความเหมาะสม
6. คลิก **"Create issue"**

### 2️⃣ การ Sync ข้อมูลอัตโนมัติ

ระบบจะ **sync อัตโนมัติทุกวันเวลา 08:00 น. (เวลาไทย)** ผ่าน GitHub Actions

- ข้อมูลจะถูกดึงจาก Linear API และบันทึกลงใน `data/projects_master_2569.csv`
- Dashboard บน GitHub Pages จะอัพเดตอัตโนมัติ

**หากต้องการ sync ทันที:**
1. เข้า [GitHub Actions](https://github.com/ppakpoomm/niems-projects-master/actions/workflows/linear-sync.yml)
2. คลิก **"Run workflow"** > **"Run workflow"**
3. รอ workflow ทำงานเสร็จ (~15-20 วินาที)

### 3️⃣ ดู Dashboard

เข้าชม Dashboard ที่: [https://ppakpoomm.github.io/niems-projects-master/](https://ppakpoomm.github.io/niems-projects-master/)

**Features:**
- ตารางแสดงข้อมูลโครงการทั้งหมด
- กรองและค้นหาตามประเภท/ภูมิภาค/ปีงบประมาณ
- Export ข้อมูลเป็น CSV/Excel
- แสดงกราฟสถิติต่างๆ


# 

# \## 📝 License

# 

# ข้อมูลใน repository นี้เป็นของสถาบันการแพทย์ฉุกเฉินแห่งชาติ (สพฉ.)



