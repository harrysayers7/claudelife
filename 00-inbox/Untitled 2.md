```dataviewjs
// ESM Project Dashboard - Kanban/Board View (Monday.com/Asana style)
// Mobile-optimized with horizontal scrolling boards

const projectPath = '"02-projects/mokhouse"';
const today = dv.date("today");

// Fetch all ESM projects
const allProjects = dv.pages(projectPath)
    .where(p => p["project name"])
    .array();

// Define status columns in order
const statusColumns = [
    { name: "Brief Received", color: "#6B7280", emoji: "📥" },
    { name: "In Progress", color: "#3B82F6", emoji: "🎵" },
    { name: "Submitted", color: "#F59E0B", emoji: "📤" },
    { name: "PO Received", color: "#8B5CF6", emoji: "📋" },
    { name: "Invoiced", color: "#10B981", emoji: "💰" },
    { name: "Complete", color: "#6B7280", emoji: "✅" }
];

// Group projects by status
const projectsByStatus = {};
statusColumns.forEach(col => {
    projectsByStatus[col.name] = allProjects.filter(p => p.status === col.name);
});

// Calculate stats
let totalPaid = 0;
let totalPending = 0;
let overdueCount = 0;

allProjects.forEach(p => {
    if (p.paid === true) {
        totalPaid += parseFloat(p["demo fee"] || 0) + parseFloat(p["award fee"] || 0);
    }
    if (p.status === "Invoiced" && p.paid === false) {
        totalPending += parseFloat(p["demo fee"] || p["award fee"] || 0);
    }
    if (p["due date"] && dv.date(p["due date"]) < today && p.status !== "Complete") {
        overdueCount++;
    }
});

// === RENDER HEADER ===
dv.header(2, "🎵 ESM Projects");
dv.el("div", `<div style="color: var(--text-muted); font-size: 0.9em; margin-bottom: 20px;">Updated ${today.toFormat("dd MMM yyyy")}</div>`);

// === STATS BAR ===
dv.el("div", `
<div style="display: flex; gap: 8px; margin-bottom: 20px; overflow-x: auto; padding-bottom: 8px;">
  <div style="min-width: 140px; background: var(--background-secondary); padding: 12px; border-radius: 8px; border-left: 3px solid #10B981;">
    <div style="font-size: 1.3em; font-weight: bold;">$${totalPaid.toLocaleString()}</div>
    <div style="font-size: 0.8em; color: var(--text-muted);">Paid YTD</div>
  </div>
  <div style="min-width: 140px; background: var(--background-secondary); padding: 12px; border-radius: 8px; border-left: 3px solid #F59E0B;">
    <div style="font-size: 1.3em; font-weight: bold;">$${totalPending.toLocaleString()}</div>
    <div style="font-size: 0.8em; color: var(--text-muted);">Pending</div>
  </div>
  <div style="min-width: 140px; background: var(--background-secondary); padding: 12px; border-radius: 8px; border-left: 3px solid #3B82F6;">
    <div style="font-size: 1.3em; font-weight: bold;">${allProjects.length}</div>
    <div style="font-size: 0.8em; color: var(--text-muted);">Total Projects</div>
  </div>
  ${overdueCount > 0 ? `
  <div style="min-width: 140px; background: var(--background-secondary); padding: 12px; border-radius: 8px; border-left: 3px solid #EF4444;">
    <div style="font-size: 1.3em; font-weight: bold;">⚠️ ${overdueCount}</div>
    <div style="font-size: 0.8em; color: var(--text-muted);">Overdue</div>
  </div>
  ` : ''}
</div>
`);

// === KANBAN BOARD ===
dv.el("div", `
<div style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 20px; margin-bottom: 20px;">
  ${statusColumns.map(col => {
    const projects = projectsByStatus[col.name] || [];

    return `
    <div style="min-width: 280px; max-width: 320px; flex-shrink: 0;">
      <div style="background: var(--background-secondary); border-radius: 8px; padding: 12px; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div style="font-weight: 600; font-size: 0.9em;">
            ${col.emoji} ${col.name}
          </div>
          <div style="background: var(--background-modifier-border); padding: 2px 8px; border-radius: 12px; font-size: 0.75em; font-weight: 600;">
            ${projects.length}
          </div>
        </div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 8px;">
        ${projects.length === 0 ? `
          <div style="background: var(--background-secondary); border-radius: 6px; padding: 16px; text-align: center; color: var(--text-muted); font-size: 0.85em;">
            No projects
          </div>
        ` : projects.map(p => {
          const isOverdue = p["due date"] && dv.date(p["due date"]) < today;
          const dueDate = p["due date"] ? dv.date(p["due date"]).toFormat("MMM dd") : null;
          const fee = p["demo fee"] || p["award fee"] || null;

          return `
          <div style="background: var(--background-primary-alt); border: 1px solid var(--background-modifier-border); border-radius: 6px; padding: 10px; cursor: pointer; transition: all 0.2s;">
            <div style="font-weight: 500; font-size: 0.9em; margin-bottom: 6px; line-height: 1.3;">
              <a href="${p.file.path}" style="text-decoration: none; color: var(--text-normal);">
                ${p["project name"]}
              </a>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 6px; font-size: 0.75em; color: var(--text-muted);">
              ${fee ? `<span style="background: var(--background-modifier-border); padding: 2px 6px; border-radius: 4px;">$${fee}</span>` : ''}
              ${dueDate ? `
                <span style="background: ${isOverdue ? '#EF4444' : 'var(--background-modifier-border)'}; color: ${isOverdue ? 'white' : 'inherit'}; padding: 2px 6px; border-radius: 4px;">
                  ${isOverdue ? '⚠️ ' : '📅 '}${dueDate}
                </span>
              ` : ''}
              ${p.PO ? `<span style="background: var(--background-modifier-border); padding: 2px 6px; border-radius: 4px;">PO-${p.PO}</span>` : ''}
              ${p.awarded === true ? '<span style="background: #10B981; color: white; padding: 2px 6px; border-radius: 4px;">🏆 Awarded</span>' : ''}
            </div>
          </div>
          `;
        }).join('')}
      </div>
    </div>
    `;
  }).join('')}
</div>
`);

// === QUICK ACTIONS / FILTERS ===
const awaitingPO = allProjects.filter(p => p.status === "Submitted" && !p.PO);
const needsInvoice = allProjects.filter(p => p.PO && p.status === "PO Received");

if (awaitingPO.length > 0 || needsInvoice.length > 0) {
  dv.header(3, "⚡ Quick Actions");

  if (awaitingPO.length > 0) {
    dv.el("div", `<div style="background: #FEF3C7; border-left: 3px solid #F59E0B; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
      <div style="font-weight: 600; margin-bottom: 6px;">📤 ${awaitingPO.length} project(s) awaiting PO</div>
      ${awaitingPO.map(p => `<div style="font-size: 0.9em; margin-left: 8px;">• ${p.file.link}</div>`).join('')}
    </div>`);
  }

  if (needsInvoice.length > 0) {
    dv.el("div", `<div style="background: #DBEAFE; border-left: 3px solid #3B82F6; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
      <div style="font-weight: 600; margin-bottom: 6px;">💰 ${needsInvoice.length} project(s) ready to invoice</div>
      ${needsInvoice.map(p => `<div style="font-size: 0.9em; margin-left: 8px;">• ${p.file.link} (PO-${p.PO})</div>`).join('')}
    </div>`);
  }
}
```
