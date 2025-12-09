async function loadCSV(url) {
  const res = await fetch(url);
  const text = await res.text();
  const lines = text.trim().split("\n");
  const headers = lines[0].split(",");
  
  const rows = lines.slice(1).map((line) => {
    const cols = line.split(",");
    const obj = {};
    headers.forEach((h, i) => (obj[h.trim()] = (cols[i] || "").trim()));
    return obj;
  });
  
  return rows;
}

function unique(values, key) {
  return [...new Set(values.map((v) => v[key]).filter(Boolean))].sort();
}

function fillSelect(selectId, items) {
  const sel = document.getElementById(selectId);
  sel.innerHTML = '<option value="">-- ทั้งหมด --</option>';
  items.forEach((val) => {
    const opt = document.createElement("option");
    opt.value = val;
    opt.textContent = val;
    sel.appendChild(opt);
  });
}

function renderTable(data) {
  const tbody = document.getElementById("projectsBody");
  tbody.innerHTML = "";
  
  if (data.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 40px; color: #7f8c8d;">ไม่พบข้อมูลโครงการ</td></tr>';
    return;
  }
  
  data.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.project_code || "-"}</td>
      <td>${row.project_name_th || "-"}</td>
      <td>${row.fiscal_year || "-"}</td>
      <td>${row.program_code || "-"}</td>
      <td>${row.owner_org_unit || "-"}</td>
      <td>${row.deputy_owner || "-"}</td>
      <td>${row.section15_main || "-"}</td>
      <td>${row.fund_source_code || "-"}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderSummary(data) {
  const summaryDiv = document.getElementById("summaryContent");
  const total = data.length;
  
  const byProgram = {};
  data.forEach((row) => {
    const key = row.program_code || "อื่นๆ";
    byProgram[key] = (byProgram[key] || 0) + 1;
  });
  
  let html = '<div class="stats">';
  html += `<div class="stat-card"><div class="label">จำนวนโครงการทั้งหมด</div><div class="value">${total}</div></div>`;
  
  Object.entries(byProgram).sort((a, b) => b[1] - a[1]).slice(0, 5).forEach(([prog, count]) => {
    html += `<div class="stat-card"><div class="label">แผนงาน ${prog}</div><div class="value">${count}</div></div>`;
  });
  
  html += '</div>';
  summaryDiv.innerHTML = html;
}

(async () => {
  try {
    const dataUrl = "../data/projects_master_2569.csv";
    const allRows = await loadCSV(dataUrl);
    
    fillSelect("programFilter", unique(allRows, "program_code"));
    fillSelect("deputyFilter", unique(allRows, "deputy_owner"));
    fillSelect("section15Filter", unique(allRows, "section15_main"));
    fillSelect("fundFilter", unique(allRows, "fund_source_code"));
    
    function applyFilters() {
      const pf = document.getElementById("programFilter").value;
      const df = document.getElementById("deputyFilter").value;
      const sf = document.getElementById("section15Filter").value;
      const ff = document.getElementById("fundFilter").value;
      
      const filtered = allRows.filter((row) => {
        if (pf && row.program_code !== pf) return false;
        if (df && row.deputy_owner !== df) return false;
        if (sf && row.section15_main !== sf) return false;
        if (ff && row.fund_source_code !== ff) return false;
        return true;
      });
      
      renderTable(filtered);
      renderSummary(filtered);
    }
    
    document.getElementById("programFilter").addEventListener("change", applyFilters);
    document.getElementById("deputyFilter").addEventListener("change", applyFilters);
    document.getElementById("section15Filter").addEventListener("change", applyFilters);
    document.getElementById("fundFilter").addEventListener("change", applyFilters);
    
    renderTable(allRows);
    renderSummary(allRows);
  } catch (error) {
    document.getElementById("summaryContent").innerHTML = '<div style="color: red;">เกิดข้อผิดพลาดในการโหลดข้อมูล</div>';
    document.getElementById("projectsBody").innerHTML = '<tr><td colspan="8" style="text-align: center; color: red;">ไม่สามารถโหลดข้อมูลได้</td></tr>';
  }
})();
