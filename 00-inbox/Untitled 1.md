---
date created: Sun, 10 19th 25, 6:02:50 am
date modified: Sun, 10 19th 25, 6:14:00 am
---
```dataviewjs
// ═══════════════════════════════════════════════════════════
// OBSIDIA COMMAND CENTER - Obsidian Native Dashboard
// ═══════════════════════════════════════════════════════════

const container = dv.container;
container.style.cssText = "min-height: 100vh; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f1e 100%); color: #e0e0e0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 2rem; margin: -20px; border-radius: 0;";

// ═══════════════════════════════════════════════════════════
// HEADER SECTION
// ═══════════════════════════════════════════════════════════

const now = new Date();
const dateStr = now.toLocaleDateString('en-US', { 
  weekday: 'long', 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric' 
});
const timeStr = now.toLocaleTimeString('en-US', { 
  hour: '2-digit', 
  minute: '2-digit' 
});

dv.header(1, "⚡ OBSIDIA COMMAND");
dv.el('div', dateStr, { 
  cls: 'obsidia-subtitle',
  attr: { style: 'color: #888; font-size: 0.9rem; margin: 0.5rem 0 2rem 0;' }
});

dv.el('div', timeStr + ' • AEDT • South Coast NSW', {
  attr: { style: 'color: #00d4ff; font-size: 1.5rem; font-weight: 300; margin-bottom: 3rem;' }
});

// ═══════════════════════════════════════════════════════════
// TASK QUEUE MODULE
// ═══════════════════════════════════════════════════════════

const taskSection = dv.el('div', '', {
  attr: { 
    style: "background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);"
  }
});

const taskHeader = dv.el('div', '', {
  container: taskSection,
  attr: { 
    style: 'display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;' 
  }
});

dv.el('h2', '⚡ Task Queue', {
  container: taskHeader,
  attr: { style: 'margin: 0; font-size: 1.25rem; font-weight: 600;' }
});

// Get today's incomplete tasks
const tasks = dv.pages()
  .where(p => p.today && !p.Done)
  .sort(p => p.file.ctime, 'desc');

const totalTasks = tasks.length;
const completedCount = dv.pages().where(p => p.today && p.Done).length;

dv.el('div', completedCount + "/" + (totalTasks + completedCount), {
  container: taskHeader,
  attr: { style: 'font-size: 0.85rem; color: #888;' }
});

// Progress Bar
const progressPercent = totalTasks > 0 ? (completedCount / (totalTasks + completedCount)) * 100 : 0;
const progressBar = dv.el('div', '', {
  container: taskSection,
  attr: { 
    style: "width: 100%; height: 4px; background: rgba(255, 255, 255, 0.1); border-radius: 2px; margin-bottom: 1.5rem; overflow: hidden;"
  }
});

dv.el('div', '', {
  container: progressBar,
  attr: { 
    style: "width: " + progressPercent + "%; height: 100%; background: linear-gradient(90deg, #00d4ff 0%, #7c3aed 100%); transition: width 0.3s ease;"
  }
});

// Task List
if (tasks.length > 0) {
  for (const task of tasks.values) {
    const taskCard = dv.el('div', '', {
      container: taskSection,
      attr: { 
        style: "display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 0.75rem; cursor: pointer; transition: all 0.2s ease;"
      }
    });

    // Checkbox
    const checkbox = dv.el('input', '', {
      container: taskCard,
      attr: { 
        type: 'checkbox',
        style: 'width: 20px; height: 20px; cursor: pointer; accent-color: #00d4ff;'
      }
    });

    checkbox.onclick = async () => {
      const file = app.vault.getAbstractFileByPath(task.file.path);
      await app.fileManager.processFrontMatter(file, (fm) => {
        fm.Done = true;
      });
    };

    // Task Content
    const taskContent = dv.el('div', '', {
      container: taskCard,
      attr: { style: 'flex: 1;' }
    });

    dv.el('div', task.file.link, {
      container: taskContent,
      attr: { style: 'font-weight: 500;' }
    });

    if (task.description) {
      dv.el('div', task.description, {
        container: taskContent,
        attr: { style: 'font-size: 0.85rem; color: #888; margin-top: 0.25rem;' }
      });
    }

    // Hover effects
    taskCard.onmouseenter = () => {
      taskCard.style.background = 'rgba(255, 255, 255, 0.08)';
      taskCard.style.transform = 'translateX(4px)';
    };
    taskCard.onmouseleave = () => {
      taskCard.style.background = 'rgba(255, 255, 255, 0.05)';
      taskCard.style.transform = 'translateX(0)';
    };
  }
} else {
  dv.el('div', '✨ All tasks complete for today', {
    container: taskSection,
    attr: { style: 'color: #888; font-style: italic; text-align: center; padding: 2rem;' }
  });
}

// ═══════════════════════════════════════════════════════════
// TODAY'S EVENTS MODULE
// ═══════════════════════════════════════════════════════════

const todaySection = dv.el('div', '', {
  attr: { 
    style: "background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);"
  }
});

dv.el('h2', '📅 Today\'s Events', {
  container: todaySection,
  attr: { style: 'margin: 0 0 1.5rem 0; font-size: 1.25rem; font-weight: 600;' }
});

// Helper function to check if event occurs today
const today = dv.date('today');
function occursOn(event, checkDate) {
  const startDate = dv.date(event.when);
  if (!startDate) return false;

  const checkDateStr = checkDate.toFormat('yyyy-MM-dd');
  const startDateStr = startDate.toFormat('yyyy-MM-dd');

  let recurrencePattern = null;
  if (event.recurrence) {
    if (Array.isArray(event.recurrence)) {
      for (let item of event.recurrence) {
        const itemStr = String(item).trim();
        if (itemStr.match(/^\[x\]/i)) {
          recurrencePattern = itemStr.replace(/^\[x\]\s*/i, '').trim().toLowerCase();
          break;
        }
      }
    } else {
      recurrencePattern = String(event.recurrence).toLowerCase();
    }
  }

  if (!recurrencePattern) return startDateStr === checkDateStr;
  if (checkDate < startDate) return false;

  if (event.recurrence_end) {
    const endDate = dv.date(event.recurrence_end);
    if (checkDate > endDate) return false;
  }

  const daysDiff = Math.floor((checkDate - startDate) / (1000 * 60 * 60 * 24));
  switch(recurrencePattern) {
    case 'daily': return true;
    case 'weekly': return daysDiff % 7 === 0;
    case 'biweekly': return daysDiff % 14 === 0;
    case 'monthly': return startDate.day === checkDate.day;
    case 'yearly': return startDate.month === checkDate.month && startDate.day === checkDate.day;
    default: return false;
  }
}

const allEvents = dv.pages()
  .where(p => {
    if (!p.type) return false;
    const typeStr = Array.isArray(p.type) ? p.type.join(' ') : String(p.type);
    return typeStr.toLowerCase().includes("event");
  })
  .where(p => p.when);

const todayEvents = allEvents
  .where(p => occursOn(p, today))
  .sort(p => p.time || p.file.name);

if (todayEvents.length > 0) {
  for (const event of todayEvents.values) {
    const eventCard = dv.el('div', '', {
      container: todaySection,
      attr: { 
        style: "padding: 1rem; background: rgba(124, 58, 237, 0.05); border-radius: 12px; border: 1px solid rgba(124, 58, 237, 0.2); border-left: 3px solid #7c3aed; margin-bottom: 0.75rem;"
      }
    });

    if (event.time) {
      dv.el('div', '🕐 ' + event.time, {
        container: eventCard,
        attr: { 
          style: 'font-size: 0.9rem; font-weight: 600; color: #7c3aed; margin-bottom: 0.5rem;' 
        }
      });
    }

    dv.el('div', event.file.link, {
      container: eventCard,
      attr: { style: 'font-weight: 500; margin-bottom: 0.25rem;' }
    });

    if (event.note) {
      dv.el('div', event.note, {
        container: eventCard,
        attr: { style: 'font-size: 0.85rem; color: #888;' }
      });
    }
  }
} else {
  dv.el('div', 'No events scheduled for today', {
    container: todaySection,
    attr: { style: 'color: #888; font-style: italic; text-align: center; padding: 2rem;' }
  });
}

// ═══════════════════════════════════════════════════════════
// THIS WEEK'S EVENTS MODULE
// ═══════════════════════════════════════════════════════════

const weekSection = dv.el('div', '', {
  attr: { 
    style: "background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);"
  }
});

dv.el('h2', '📆 This Week\'s Timeline', {
  container: weekSection,
  attr: { style: 'margin: 0 0 1.5rem 0; font-size: 1.25rem; font-weight: 600;' }
});

// Generate next 7 days of events
const upcomingOccurrences = [];
for (let i = 1; i <= 7; i++) {
  const checkDate = today.plus({ days: i });
  allEvents.forEach(event => {
    if (occursOn(event, checkDate)) {
      upcomingOccurrences.push({ event: event, date: checkDate });
    }
  });
}

upcomingOccurrences.sort((a, b) => {
  const dateDiff = a.date - b.date;
  if (dateDiff !== 0) return dateDiff;
  const aTime = a.event.time || "";
  const bTime = b.event.time || "";
  return aTime.localeCompare(bTime);
});

if (upcomingOccurrences.length > 0) {
  for (const occ of upcomingOccurrences) {
    const weekCard = dv.el('div', '', {
      container: weekSection,
      attr: { 
        style: "padding: 1rem; background: rgba(0, 212, 255, 0.03); border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.1); margin-bottom: 0.75rem;"
      }
    });

    dv.el('div', occ.date.toFormat('EEE, MMM dd'), {
      container: weekCard,
      attr: { 
        style: "font-size: 0.8rem; color: #00d4ff; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;"
      }
    });

    if (occ.event.time) {
      dv.el('div', '🕐 ' + occ.event.time, {
        container: weekCard,
        attr: { style: 'font-size: 0.85rem; color: #888; margin-bottom: 0.5rem;' }
      });
    }

    dv.el('div', occ.event.file.link, {
      container: weekCard,
      attr: { style: 'font-weight: 500; margin-bottom: 0.25rem;' }
    });

    if (occ.event.note) {
      dv.el('div', occ.event.note, {
        container: weekCard,
        attr: { style: 'font-size: 0.85rem; color: #888;' }
      });
    }
  }
} else {
  dv.el('div', 'No events scheduled for the next week', {
    container: weekSection,
    attr: { style: 'color: #888; font-style: italic; text-align: center; padding: 2rem;' }
  });
}

// ═══════════════════════════════════════════════════════════
// QUICK ACCESS FOOTER
// ═══════════════════════════════════════════════════════════

const footer = dv.el('div', '', {
  attr: { 
    style: "margin-top: 2rem; padding: 1.5rem; background: rgba(255, 255, 255, 0.02); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);"
  }
});

dv.el('div', 'QUICK ACCESS', {
  container: footer,
  attr: { 
    style: "font-size: 0.8rem; color: #666; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em;"
  }
});

const quickLinks = dv.el('div', '', {
  container: footer,
  attr: { style: 'display: flex; gap: 1rem; flex-wrap: wrap;' }
});

const links = [
  { name: 'Mokai', path: '01-areas/business/mokai/INDEX' },
  { name: 'Commands', path: 'claudelife-commands-guide' },
  { name: 'MOK HOUSE HQ', path: 'mokhouse-dashboard' }
];

for (const link of links) {
  const linkEl = dv.el('a', link.name, {
    container: quickLinks,
    attr: { 
      href: link.path,
      style: "padding: 0.5rem 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; font-size: 0.85rem; cursor: pointer; border: 1px solid rgba(255, 255, 255, 0.1); text-decoration: none; color: inherit; transition: all 0.2s ease;"
    }
  });

  linkEl.onmouseenter = () => {
    linkEl.style.background = 'rgba(0, 212, 255, 0.1)';
    linkEl.style.borderColor = 'rgba(0, 212, 255, 0.3)';
  };
  linkEl.onmouseleave = () => {
    linkEl.style.background = 'rgba(255, 255, 255, 0.05)';
    linkEl.style.borderColor = 'rgba(255, 255, 255, 0.1)';
  };
}
```

```dataviewjs 
// ESM Project Dashboard - Optimized for Mobile & Desktop
// Path: 02-projects/mokhouse (adjust if needed)

const projectPath = '"02-projects/mokhouse"';
const today = dv.date("today");

// Fetch all ESM projects
const projects = dv.pages(projectPath)
    .where(p => p["project name"])
    .sort(p => p["date received"], 'desc');

// === FINANCIAL SUMMARY ===
const paidDemo = projects
    .where(p => p["demo fee"] && p.paid === true)
    .map(p => parseFloat(p["demo fee"]) || 0)
    .reduce((sum, val) => sum + val, 0);

const paidAward = projects
    .where(p => p["award fee"] && p.awarded === true)
    .map(p => parseFloat(p["award fee"]) || 0)
    .reduce((sum, val) => sum + val, 0);

const pendingInvoices = projects
    .where(p => p.status === "Invoiced" && p.paid === false)
    .map(p => parseFloat(p["demo fee"] || p["award fee"]) || 0)
    .reduce((sum, val) => sum + val, 0);

const totalRevenue = paidDemo + paidAward;

// === STATUS COUNTS ===
const statusGroups = projects.groupBy(p => p.status || "Unknown");
const active = projects.where(p => !["Complete", "Archived"].includes(p.status)).length;

// === OVERDUE PROJECTS ===
const overdue = projects
    .where(p => p["due date"] && dv.date(p["due date"]) < today && p.status !== "Complete")
    .map(p => ({
        name: p["project name"],
        daysLate: Math.floor((today - dv.date(p["due date"])).days),
        link: p.file.link,
        status: p.status
    }))
    .sort(p => p.daysLate, 'desc');

// === AWAITING PO ===
const awaitingPO = projects
    .where(p => p.status === "Submitted" && !p.PO)
    .map(p => ({
        name: p["project name"],
        submitted: p["submitted date"],
        link: p.file.link
    }));

// === RECENT ACTIVITY ===
const recent = projects
    .where(p => p.status !== "Complete" && p.status !== "Archived")
    .sort(p => p.file.mtime, 'desc')
    .limit(5)
    .map(p => ({
        name: p["project name"],
        status: p.status,
        link: p.file.link
    }));

// === RENDER DASHBOARD ===

// Header
dv.header(2, "🎵 ESM Project Dashboard");
dv.el("div", `<small style="color: var(--text-muted);">Updated: ${today.toFormat("dd MMM yyyy")}</small>`);
dv.el("br", "");

// Financial Summary Card
dv.el("div", `
<div style="background: var(--background-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
  <div style="font-size: 0.9em; color: var(--text-muted); margin-bottom: 8px;">💰 FINANCIAL SUMMARY</div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px;">
    <div>
      <div style="font-size: 1.5em; font-weight: bold; color: var(--text-accent);">$${totalRevenue.toLocaleString()}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Total Paid</div>
    </div>
    <div>
      <div style="font-size: 1.5em; font-weight: bold; color: var(--text-warning);">$${pendingInvoices.toLocaleString()}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Pending</div>
    </div>
    <div>
      <div style="font-size: 1.5em; font-weight: bold;">${active}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Active Projects</div>
    </div>
  </div>
</div>
`);

// Status Breakdown
dv.el("div", `
<div style="background: var(--background-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
  <div style="font-size: 0.9em; color: var(--text-muted); margin-bottom: 12px;">📊 STATUS BREAKDOWN</div>
  <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    ${statusGroups.map(g => `
      <span style="background: var(--background-modifier-border); padding: 4px 12px; border-radius: 12px; font-size: 0.85em;">
        ${g.key}: <strong>${g.rows.length}</strong>
      </span>
    `).join('')}
  </div>
</div>
`);

// Alerts Section
if (overdue.length > 0 || awaitingPO.length > 0) {
  dv.header(3, "⚠️ Attention Required");
  
  if (overdue.length > 0) {
    dv.el("div", `<div style="color: var(--text-error); font-weight: 600; margin-bottom: 8px;">🔴 Overdue Projects (${overdue.length})</div>`);
    dv.list(overdue.map(p => 
      `${p.link} - **${p.daysLate} days late** (${p.status})`
    ));
    dv.el("br", "");
  }
  
  if (awaitingPO.length > 0) {
    dv.el("div", `<div style="color: var(--text-warning); font-weight: 600; margin-bottom: 8px;">🟡 Awaiting PO (${awaitingPO.length})</div>`);
    dv.list(awaitingPO.map(p => 
      `${p.link} - Submitted ${p.submitted || "recently"}`
    ));
    dv.el("br", "");
  }
}

// Recent Activity
dv.header(3, "📝 Recent Activity");
dv.table(
  ["Project", "Status"],
  recent.map(p => [p.link, p.status])
);

// Quick Stats Footer
dv.el("div", `
<div style="margin-top: 24px; padding: 12px; background: var(--background-secondary); border-radius: 8px; font-size: 0.85em; color: var(--text-muted);">
  <strong>Total Projects:</strong> ${projects.length} | 
  <strong>Demo Fees Paid:</strong> $${paidDemo.toLocaleString()} | 
  <strong>Award Fees Paid:</strong> $${paidAward.toLocaleString()}
</div>
`);

```
```dataviewjs
// ESM Project Dashboard - Optimized for Mobile & Desktop
// Path: 02-projects/mokhouse (adjust if needed)

const projectPath = '"02-projects/mokhouse"';
const today = dv.date("today");

// Fetch all ESM projects
const projects = dv.pages(projectPath)
    .where(p => p["project name"])
    .sort(p => p["date received"], 'desc');

// === FINANCIAL SUMMARY ===
const paidDemo = projects
    .where(p => p["demo fee"] && p.paid === true)
    .map(p => parseFloat(p["demo fee"]) || 0)
    .reduce((sum, val) => sum + val, 0);

const paidAward = projects
    .where(p => p["award fee"] && p.awarded === true)
    .map(p => parseFloat(p["award fee"]) || 0)
    .reduce((sum, val) => sum + val, 0);

const pendingInvoices = projects
    .where(p => p.status === "Invoiced" && p.paid === false)
    .map(p => parseFloat(p["demo fee"] || p["award fee"]) || 0)
    .reduce((sum, val) => sum + val, 0);

const totalRevenue = paidDemo + paidAward;

// === STATUS COUNTS ===
const statusGroups = projects.groupBy(p => p.status || "Unknown");
const active = projects.where(p => !["Complete", "Archived"].includes(p.status)).length;

// === OVERDUE PROJECTS ===
const overdue = projects
    .where(p => p["due date"] && dv.date(p["due date"]) < today && p.status !== "Complete")
    .map(p => ({
        name: p["project name"],
        daysLate: Math.floor((today - dv.date(p["due date"])).days),
        link: p.file.link,
        status: p.status
    }))
    .sort(p => p.daysLate, 'desc');

// === AWAITING PO ===
const awaitingPO = projects
    .where(p => p.status === "Submitted" && !p.PO)
    .map(p => ({
        name: p["project name"],
        submitted: p["submitted date"],
        link: p.file.link
    }));

// === RECENT ACTIVITY ===
const recent = projects
    .where(p => p.status !== "Complete" && p.status !== "Archived")
    .sort(p => p.file.mtime, 'desc')
    .limit(5)
    .map(p => ({
        name: p["project name"],
        status: p.status,
        link: p.file.link
    }));

// === RENDER DASHBOARD ===

// Header
dv.header(2, "🎵 ESM Project Dashboard");
dv.el("div", `<small style="color: var(--text-muted);">Updated: ${today.toFormat("dd MMM yyyy")}</small>`);
dv.el("br", "");

// Financial Summary Card
dv.el("div", `
<div style="background: var(--background-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
  <div style="font-size: 0.9em; color: var(--text-muted); margin-bottom: 8px;">💰 FINANCIAL SUMMARY</div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px;">
    <div>
      <div style="font-size: 1.5em; font-weight: bold; color: var(--text-accent);">$${totalRevenue.toLocaleString()}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Total Paid</div>
    </div>
    <div>
      <div style="font-size: 1.5em; font-weight: bold; color: var(--text-warning);">$${pendingInvoices.toLocaleString()}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Pending</div>
    </div>
    <div>
      <div style="font-size: 1.5em; font-weight: bold;">${active}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Active Projects</div>
    </div>
  </div>
</div>
`);

// Status Breakdown
dv.el("div", `
<div style="background: var(--background-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
  <div style="font-size: 0.9em; color: var(--text-muted); margin-bottom: 12px;">📊 STATUS BREAKDOWN</div>
  <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    ${statusGroups.map(g => `
      <span style="background: var(--background-modifier-border); padding: 4px 12px; border-radius: 12px; font-size: 0.85em;">
        ${g.key}: <strong>${g.rows.length}</strong>
      </span>
    `).join('')}
  </div>
</div>
`);

// Alerts Section
if (overdue.length > 0 || awaitingPO.length > 0) {
  dv.header(3, "⚠️ Attention Required");
  
  if (overdue.length > 0) {
    dv.el("div", `<div style="color: var(--text-error); font-weight: 600; margin-bottom: 8px;">🔴 Overdue Projects (${overdue.length})</div>`);
    dv.list(overdue.map(p => 
      `${p.link} - **${p.daysLate} days late** (${p.status})`
    ));
    dv.el("br", "");
  }
  
  if (awaitingPO.length > 0) {
    dv.el("div", `<div style="color: var(--text-warning); font-weight: 600; margin-bottom: 8px;">🟡 Awaiting PO (${awaitingPO.length})</div>`);
    dv.list(awaitingPO.map(p => 
      `${p.link} - Submitted ${p.submitted || "recently"}`
    ));
    dv.el("br", "");
  }
}

// Recent Activity
dv.header(3, "📝 Recent Activity");
dv.table(
  ["Project", "Status"],
  recent.map(p => [p.link, p.status])
);

// Quick Stats Footer
dv.el("div", `
<div style="margin-top: 24px; padding: 12px; background: var(--background-secondary); border-radius: 8px; font-size: 0.85em; color: var(--text-muted);">
  <strong>Total Projects:</strong> ${projects.length} | 
  <strong>Demo Fees Paid:</strong> $${paidDemo.toLocaleString()} | 
  <strong>Award Fees Paid:</strong> $${paidAward.toLocaleString()}
</div>
`);
```
```dataviewjs
// ESM Project Dashboard - Optimized for Mobile & Desktop
// Path: 02-projects/mokhouse (adjust if needed)

const projectPath = '"02-projects/mokhouse"';
const today = dv.date("today");

// Fetch all ESM projects
const projects = dv.pages(projectPath)
    .where(p => p["project name"])
    .sort(p => p["date received"], 'desc');

// === FINANCIAL SUMMARY ===
const paidDemoProjects = projects
    .where(p => p["demo fee"] && p.paid === true)
    .array();

let paidDemo = 0;
for (let p of paidDemoProjects) {
    paidDemo += parseFloat(p["demo fee"]) || 0;
}

const paidAwardProjects = projects
    .where(p => p["award fee"] && p.awarded === true)
    .array();

let paidAward = 0;
for (let p of paidAwardProjects) {
    paidAward += parseFloat(p["award fee"]) || 0;
}

const pendingInvoiceProjects = projects
    .where(p => p.status === "Invoiced" && p.paid === false)
    .array();

let pendingInvoices = 0;
for (let p of pendingInvoiceProjects) {
    pendingInvoices += parseFloat(p["demo fee"] || p["award fee"]) || 0;
}

const totalRevenue = paidDemo + paidAward;

// === STATUS COUNTS ===
const statusGroups = projects.groupBy(p => p.status || "Unknown");
const active = projects.where(p => !["Complete", "Archived"].includes(p.status)).length;

// === OVERDUE PROJECTS ===
const overdue = projects
    .where(p => p["due date"] && dv.date(p["due date"]) < today && p.status !== "Complete")
    .map(p => ({
        name: p["project name"],
        daysLate: Math.floor((today - dv.date(p["due date"])).days),
        link: p.file.link,
        status: p.status
    }))
    .sort(p => p.daysLate, 'desc')
    .array();

// === AWAITING PO ===
const awaitingPO = projects
    .where(p => p.status === "Submitted" && !p.PO)
    .map(p => ({
        name: p["project name"],
        submitted: p["submitted date"],
        link: p.file.link
    }))
    .array();

// === RECENT ACTIVITY ===
const recent = projects
    .where(p => p.status !== "Complete" && p.status !== "Archived")
    .sort(p => p.file.mtime, 'desc')
    .limit(5)
    .map(p => ({
        name: p["project name"],
        status: p.status,
        link: p.file.link
    }))
    .array();

// === RENDER DASHBOARD ===

// Header
dv.header(2, "🎵 ESM Project Dashboard");
dv.el("div", `<small style="color: var(--text-muted);">Updated: ${today.toFormat("dd MMM yyyy")}</small>`);
dv.el("br", "");

// Financial Summary Card
dv.el("div", `
<div style="background: var(--background-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
  <div style="font-size: 0.9em; color: var(--text-muted); margin-bottom: 8px;">💰 FINANCIAL SUMMARY</div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px;">
    <div>
      <div style="font-size: 1.5em; font-weight: bold; color: var(--text-accent);">$${totalRevenue.toLocaleString()}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Total Paid</div>
    </div>
    <div>
      <div style="font-size: 1.5em; font-weight: bold; color: var(--text-warning);">$${pendingInvoices.toLocaleString()}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Pending</div>
    </div>
    <div>
      <div style="font-size: 1.5em; font-weight: bold;">${active}</div>
      <div style="font-size: 0.85em; color: var(--text-muted);">Active Projects</div>
    </div>
  </div>
</div>
`);

// Status Breakdown
dv.el("div", `
<div style="background: var(--background-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
  <div style="font-size: 0.9em; color: var(--text-muted); margin-bottom: 12px;">📊 STATUS BREAKDOWN</div>
  <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    ${statusGroups.map(g => `
      <span style="background: var(--background-modifier-border); padding: 4px 12px; border-radius: 12px; font-size: 0.85em;">
        ${g.key}: <strong>${g.rows.length}</strong>
      </span>
    `).join('')}
  </div>
</div>
`);

// Alerts Section
if (overdue.length > 0 || awaitingPO.length > 0) {
  dv.header(3, "⚠️ Attention Required");
  
  if (overdue.length > 0) {
    dv.el("div", `<div style="color: var(--text-error); font-weight: 600; margin-bottom: 8px;">🔴 Overdue Projects (${overdue.length})</div>`);
    dv.list(overdue.map(p => 
      `${p.link} - **${p.daysLate} days late** (${p.status})`
    ));
    dv.el("br", "");
  }
  
  if (awaitingPO.length > 0) {
    dv.el("div", `<div style="color: var(--text-warning); font-weight: 600; margin-bottom: 8px;">🟡 Awaiting PO (${awaitingPO.length})</div>`);
    dv.list(awaitingPO.map(p => 
      `${p.link} - Submitted ${p.submitted || "recently"}`
    ));
    dv.el("br", "");
  }
}

// Recent Activity
dv.header(3, "📝 Recent Activity");
dv.table(
  ["Project", "Status"],
  recent.map(p => [p.link, p.status])
);

// Quick Stats Footer
dv.el("div", `
<div style="margin-top: 24px; padding: 12px; background: var(--background-secondary); border-radius: 8px; font-size: 0.85em; color: var(--text-muted);">
  <strong>Total Projects:</strong> ${projects.length} | 
  <strong>Demo Fees Paid:</strong> $${paidDemo.toLocaleString()} | 
  <strong>Award Fees Paid:</strong> $${paidAward.toLocaleString()}
</div>
`);
```
