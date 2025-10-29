---
tags: [mokhouse, music, production]
date created: Sat, 10 18th 25, 7:30:00 pm
date modified: Mon, 10 20th 25, 2:20:47 pm
type: dashboard
relation:
  - "[[mokhouse]]"
  - "[[mokhouse]]"
aliases:
  - MOK HOUSE HQ
---

# MOK HOUSE HQ

```dataviewjs
// Get all mokhouse project files (including archive)
// Filter by type: project and relation contains mokhouse
const projects = dv.pages('"02-projects/mokhouse"')
    .where(p => {
        if (p.file.name === "CLAUDE") return false;
        if (p.type !== "project") return false;

        // Check if relation contains mokhouse
        const relation = p.relation;
        if (!relation) return false;
        if (Array.isArray(relation)) {
            return relation.some(r => String(r).includes("mokhouse"));
        }
        return String(relation).includes("mokhouse");
    })
    .sort(p => p["date received"] || p["date created"], 'desc');

// Calculate financials
let totalPaid = 0;
let totalOutstanding = 0;
let totalPending = 0;
let totalActiveProjectValue = 0; // New: track active project potential revenue
let paidProjects = [];
let outstandingProjects = [];
let pendingProjects = [];
let apraNeeded = [];
let overdueInvoices = [];

// Calculate date 2 weeks ago
const twoWeeksAgo = new Date();
twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);

for (let project of projects) {
    const demoFee = Number(project["demo fee"]) || 0;
    const awardFee = Number(project["award fee"]) || 0;
    const isPaid = project.paid === true;
    const isAwarded = project.awarded === true;
    const apraRegistered = project.APRA === true;
    const status = project.status;
    const submittedDate = project["submitted date"];

    // Track awarded projects that need APRA registration
    if (isAwarded && !apraRegistered) {
        apraNeeded.push({
            name: project["project name"],
            link: project.file.link,
            customer: project.customer,
            awardFee: awardFee,
            status: status,
            paid: isPaid
        });
    }

    // Calculate project total (demo fee + award fee)
    // Most projects have demo fee even when won, award fee is additional
    const projectTotal = demoFee + awardFee;

    // Categorize
    if (isPaid) {
        totalPaid += projectTotal;
        paidProjects.push({
            name: project["project name"],
            link: project.file.link,
            customer: project.customer,
            amount: projectTotal,
            datePaid: project["Date Paid"],
            dateReceived: project["date received"],
            invoice: project["Invoice #"],
            isArchived: project.file.path.includes("archive")
        });
    } else if (status === "sent" || status === "paid") {
        totalOutstanding += projectTotal;

        // Check if invoice is overdue (submitted more than 2 weeks ago and unpaid)
        let isOverdue = false;
        if (submittedDate) {
            const submitted = new Date(submittedDate);
            isOverdue = submitted < twoWeeksAgo;
        }

        outstandingProjects.push({
            name: project["project name"],
            link: project.file.link,
            customer: project.customer,
            amount: projectTotal,
            status: status,
            invoice: project["Invoice #"],
            submittedDate: submittedDate,
            isOverdue: isOverdue
        });

        // Add to overdue list
        if (isOverdue) {
            const daysOverdue = Math.floor((new Date() - new Date(submittedDate)) / (1000 * 60 * 60 * 24));
            overdueInvoices.push({
                name: project["project name"],
                link: project.file.link,
                customer: project.customer,
                amount: projectTotal,
                invoice: project["Invoice #"],
                submittedDate: submittedDate,
                daysOverdue: daysOverdue
            });
        }
    } else {
        // Pending projects - show potential based on status
        const potentialAmount = isAwarded ? (demoFee + awardFee) : demoFee;
        totalPending += potentialAmount;

        // Add all active projects to outstanding (at minimum the demo fee)
        // Demo fee is guaranteed, award fee only if awarded
        const guaranteedAmount = isAwarded ? (demoFee + awardFee) : demoFee;
        totalOutstanding += guaranteedAmount;
        totalActiveProjectValue += guaranteedAmount; // Track separately for display

        pendingProjects.push({
            name: project["project name"],
            link: project.file.link,
            customer: project.customer,
            demoFee: demoFee,
            awardFee: awardFee,
            status: status,
            dueDate: project["due date"],
            isAwarded: isAwarded
        });
    }
}

const totalRevenue = totalPaid + totalOutstanding;
const totalPotential = totalRevenue + totalPending;

// Calculate active projects count
const activeProjects = outstandingProjects.length + pendingProjects.length;

// Calculate 12-month average income from Supabase invoice data
// This data is fetched from Supabase invoices table (entity_id: MOK HOUSE)
// Data source: Supabase invoices.paid_on dates (more accurate than Obsidian frontmatter)
// Last updated: 2025-10-19
const supabasePaidInvoices = [
    { invoice_number: "HS-FF-001", total_amount: 3300, paid_on: "2025-12-16" },
    { invoice_number: "HS-STK-001", total_amount: 1000, paid_on: "2025-11-18" },
    { invoice_number: "NLOLWU0R-0006", total_amount: 500, paid_on: "2025-10-17" },
    { invoice_number: "NLOLWU0R-0007", total_amount: 500, paid_on: "2025-10-17" },
    { invoice_number: "NLOLWU0R-0002", total_amount: 500, paid_on: "2025-10-17" },
    { invoice_number: "NLOLWU0R-0003", total_amount: 4500, paid_on: "2025-10-17" },
    { invoice_number: "INV-58", total_amount: 5250, paid_on: "2025-10-03" },
    { invoice_number: "NLOLWU0R-0001", total_amount: 500, paid_on: "2025-10-03" },
    { invoice_number: "HS-RP-001", total_amount: 500, paid_on: "2025-08-11" },
    { invoice_number: "HS-MER-001", total_amount: 300, paid_on: "2025-07-10" },
    { invoice_number: "HS-SAP-001", total_amount: 250, paid_on: "2025-07-10" },
    { invoice_number: "INV-GATORADE", total_amount: 500, paid_on: "2025-05-19" },
    { invoice_number: "HS-SAR2-001", total_amount: 700, paid_on: "2025-04-11" },
    { invoice_number: "HS-C4C-001", total_amount: 3000, paid_on: "2025-03-28" }
];

// Calculate 12-month average
const last12MonthsRevenue = supabasePaidInvoices.reduce((sum, inv) => sum + inv.total_amount, 0);
const monthlyAverage12 = last12MonthsRevenue / 12;

// Calculate 6-month average
const sixMonthsAgo = new Date();
sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
const sixMonthsAgoStr = sixMonthsAgo.toISOString().split('T')[0];

const last6MonthsInvoices = supabasePaidInvoices.filter(inv => inv.paid_on >= sixMonthsAgoStr);
const last6MonthsRevenue = last6MonthsInvoices.reduce((sum, inv) => sum + inv.total_amount, 0);
const monthlyAverage6 = last6MonthsRevenue / 6;

// Calculate 3-month average
const threeMonthsAgo = new Date();
threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
const threeMonthsAgoStr = threeMonthsAgo.toISOString().split('T')[0];

const last3MonthsInvoices = supabasePaidInvoices.filter(inv => inv.paid_on >= threeMonthsAgoStr);
const last3MonthsRevenue = last3MonthsInvoices.reduce((sum, inv) => sum + inv.total_amount, 0);
const monthlyAverage3 = last3MonthsRevenue / 3;

// Calculate Australian Financial Year (FY) revenue
// Australian FY runs from July 1 to June 30
const now = new Date();
const currentYear = now.getFullYear();
const currentMonth = now.getMonth() + 1;

let fyYear, fyStartDate, fyEndDate;
if (currentMonth >= 7) {
    // Jul-Dec: FY is next year (e.g., Oct 2025 = FY2026)
    fyYear = currentYear + 1;
    fyStartDate = currentYear + '-07-01';
    fyEndDate = (currentYear + 1) + '-06-30';
} else {
    // Jan-Jun: FY is current year (e.g., Mar 2025 = FY2025)
    fyYear = currentYear;
    fyStartDate = (currentYear - 1) + '-07-01';
    fyEndDate = currentYear + '-06-30';
}

const fyInvoices = supabasePaidInvoices.filter(inv => inv.paid_on >= fyStartDate && inv.paid_on <= fyEndDate);
const fyRevenue = fyInvoices.reduce((sum, inv) => sum + inv.total_amount, 0);

// Note: Run /mokhouse-sync-invoices to update this data from Supabase

// Display summary cards
dv.header(3, "💰 Financial Summary");
dv.paragraph(`
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">Total Paid</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #10b981;">$${totalPaid.toLocaleString()}</div>
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">Outstanding (Invoiced + Active)</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #f59e0b;">$${totalOutstanding.toLocaleString()}</div>
        ${totalActiveProjectValue > 0 ? `<div style="font-size: 0.75em; opacity: 0.7; margin-top: 0.25rem;">Includes $${totalActiveProjectValue.toLocaleString()} from active projects</div>` : ''}
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">Total Revenue</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #3b82f6;">$${totalRevenue.toLocaleString()}</div>
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">In Progress</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #8b5cf6;">$${totalPending.toLocaleString()}</div>
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">Completed Projects</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #10b981;">${paidProjects.length}</div>
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">Active Projects</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #f59e0b;">${activeProjects}</div>
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">APRA Registration Needed</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #ef4444;">${apraNeeded.length}</div>
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">Overdue Invoices (>2 weeks)</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #dc2626;">${overdueInvoices.length}</div>
    </div>
    <div style="padding: 1rem; background: var(--background-secondary); border-radius: 8px;">
        <div style="font-size: 0.9em; opacity: 0.8;">Outstanding Invoices (Unpaid)</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #f59e0b;">${outstandingProjects.length}</div>
    </div>
</div>
`);

// Display average income and FY revenue (compact layout)
dv.paragraph(`
<div style="margin: 1rem 0; padding: 0.75rem; background: var(--background-secondary); border-radius: 8px;">
    <div style="font-size: 0.8em; opacity: 0.8; margin-bottom: 0.5rem; font-weight: 600;">📊 Income Metrics</div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.75rem;">
        <div style="padding: 0.75rem; background: var(--background-primary); border-radius: 6px; border-left: 3px solid #ef4444;">
            <div style="font-size: 0.7em; opacity: 0.7;">3-Mo Avg</div>
            <div style="font-size: 1.3em; font-weight: bold; color: #ef4444;">$${monthlyAverage3.toLocaleString(undefined, {maximumFractionDigits: 0})}/mo</div>
            <div style="font-size: 0.65em; opacity: 0.6;">$${last3MonthsRevenue.toLocaleString()} (${last3MonthsInvoices.length} inv)</div>
        </div>
        <div style="padding: 0.75rem; background: var(--background-primary); border-radius: 6px; border-left: 3px solid #10b981;">
            <div style="font-size: 0.7em; opacity: 0.7;">6-Mo Avg</div>
            <div style="font-size: 1.3em; font-weight: bold; color: #10b981;">$${monthlyAverage6.toLocaleString(undefined, {maximumFractionDigits: 0})}/mo</div>
            <div style="font-size: 0.65em; opacity: 0.6;">$${last6MonthsRevenue.toLocaleString()} (${last6MonthsInvoices.length} inv)</div>
        </div>
        <div style="padding: 0.75rem; background: var(--background-primary); border-radius: 6px; border-left: 3px solid #3b82f6;">
            <div style="font-size: 0.7em; opacity: 0.7;">12-Mo Avg</div>
            <div style="font-size: 1.3em; font-weight: bold; color: #3b82f6;">$${monthlyAverage12.toLocaleString(undefined, {maximumFractionDigits: 0})}/mo</div>
            <div style="font-size: 0.65em; opacity: 0.6;">$${last12MonthsRevenue.toLocaleString()} (${supabasePaidInvoices.length} inv)</div>
        </div>
        <div style="padding: 0.75rem; background: var(--background-primary); border-radius: 6px; border-left: 3px solid #8b5cf6;">
            <div style="font-size: 0.7em; opacity: 0.7;">🇦🇺 FY${fyYear}</div>
            <div style="font-size: 1.3em; font-weight: bold; color: #8b5cf6;">$${fyRevenue.toLocaleString()}</div>
            <div style="font-size: 0.65em; opacity: 0.6;">${fyStartDate} to ${fyEndDate.slice(5)} (${fyInvoices.length} inv)</div>
        </div>
    </div>
</div>
`);

// Active projects table
if (pendingProjects.length > 0) {
    dv.header(4, `🎵 Active Projects (${pendingProjects.length})`);
    dv.table(
        ["Project", "Customer", "Status", "Demo Fee", "Award Fee", "Total", "Due Date"],
        pendingProjects.map(p => {
            const total = p.demoFee + p.awardFee;
            return [
                p.link,
                p.customer,
                p.isAwarded ? `✅ ${p.status}` : p.status,
                `$${p.demoFee.toLocaleString()}`,
                `$${p.awardFee.toLocaleString()}`,
                p.isAwarded ? `**$${total.toLocaleString()}**` : `$${p.demoFee.toLocaleString()}`,
                p.dueDate || "—"
            ];
        })
    );

    // Show note about awarded projects
    const awardedCount = pendingProjects.filter(p => p.isAwarded).length;
    if (awardedCount > 0) {
        dv.paragraph(`*✅ ${awardedCount} awarded project${awardedCount > 1 ? 's' : ''} included in Outstanding total*`);
    }
}

// Outstanding invoices table
if (outstandingProjects.length > 0) {
    dv.header(4, `⏳ Outstanding Invoices (${outstandingProjects.length})`);
    dv.table(
        ["Project", "Customer", "Amount", "Status", "Invoice #"],
        outstandingProjects.map(p => [
            p.link,
            p.customer,
            `$${p.amount.toLocaleString()}`,
            p.status,
            p.invoice || "Not invoiced"
        ])
    );
}

// APRA registration needed table
if (apraNeeded.length > 0) {
    dv.header(4, `⚠️ APRA Registration Needed (${apraNeeded.length})`);
    dv.table(
        ["Project", "Customer", "Award Fee", "Status", "Paid"],
        apraNeeded.map(p => [
            p.link,
            p.customer,
            `$${p.awardFee.toLocaleString()}`,
            p.status,
            p.paid ? "✅" : "❌"
        ])
    );
}

// Overdue invoices table
if (overdueInvoices.length > 0) {
    dv.header(4, `🚨 Overdue Invoices (${overdueInvoices.length})`);
    dv.table(
        ["Project", "Customer", "Amount", "Invoice #", "Submitted", "Days Overdue"],
        overdueInvoices.map(p => [
            p.link,
            p.customer,
            `$${p.amount.toLocaleString()}`,
            p.invoice || "—",
            p.submittedDate || "—",
            `${p.daysOverdue} days`
        ])
    );
}

// Activity metrics
const totalProjectsAllTime = paidProjects.length + outstandingProjects.length + pendingProjects.length;
const avgProjectValue = paidProjects.length > 0 ? (totalPaid / paidProjects.length) : 0;

// Count awarded projects (awarded: true)
const awardedProjects = projects.filter(p => p.awarded === true).length;

dv.header(4, "📊 Activity Metrics");
dv.paragraph(`
- **Average Paid Project Value**: $${avgProjectValue.toLocaleString(undefined, {maximumFractionDigits: 0})}
- **Total Projects Tracked**: ${totalProjectsAllTime}
- **Total Projects Awarded**: ${awardedProjects}
`);
```

---

## 📋 MOK HOUSE Tasks

```dataviewjs
// Get all tasks with relation to mokhouse
const tasks = dv.pages('"00-inbox/tasks"')
  .where(t => {
    const relation = t.relation;
    if (!relation) return false;
    if (Array.isArray(relation)) {
      return relation.some(r => String(r).includes("mokhouse"));
    }
    return String(relation).includes("mokhouse");
  })
  .where(t => t.status !== "done" && t.status !== "archive")
  .where(t => t.Done !== true)
  .sort(t => t.file.ctime, 'desc');

if (tasks.length === 0) {
  dv.paragraph("*No active MOK HOUSE tasks*");
} else {
  dv.table(
    ["✓", "Task", "Status", "Created"],
    tasks.map(t => [
      `<input type="checkbox" ${t.Done ? "checked" : ""} onclick="
        const file = app.vault.getAbstractFileByPath('${t.file.path}');
        app.fileManager.processFrontMatter(file, fm => {
          fm.Done = !fm.Done;
          fm.status = fm.Done ? 'done' : 'in-progress';
        });
      ">`,
      t.file.link,
      t.status || "inbox",
      t.file.ctime.toFormat("yyyy-MM-dd")
    ])
  );
}
```

---
[[Mok House Projects.base]]

## This Week's Focus

<!-- Update this section weekly with current priorities -->

**Week of:** 2025-10-18

### Active Submissions
- Nintendo Exchange Mode (Due: Oct 30)
- [Add other active submissions]

### Priorities
1. Complete Nintendo demo by Oct 22 internal review
2. Follow up on outstanding invoices
3. [Add other priorities]

### Blockers
- [None / List any blockers]

---

## Recent Wins

<!-- Track wins as they happen -->

- **[2025-10-17]** GWM Tank 500 - Paid $4,500 ✅
- [Add other recent wins]

---

## Client Relationships

### Electric Sheep Music (ESM)
- **Contact**: Glenn, Kate
- **Relationship**: Primary music agency
- **Recent Projects**: Nintendo, GWM Tank 500
- **Notes**: Submit demos through ESM portal

### Panda Candy Pty Ltd
- **Contact**: [Primary contact]
- **Relationship**: Music production/licensing
- **Recent Projects**: Provider Care (Job 0078)
- **Notes**: Invoice outstanding ($500)

---

## Team

**MOK HOUSE Team:**
- **Harry Sayers** - Owner, Composer, Director
- **Kell Mendoza** - Operations Director

---

## Business Model Notes

**Submission Process (ESM/Panda Candy):**
1. Receive brief from agency (ESM or Panda Candy)
2. Submit demo along with 3-4 other composers
3. Agency sends demos to client for selection
4. **If Won**: Usage fee ($2,500 - $8,000)
5. **If Not Won**: Demo fee ($250 - $1,000)

**Project Types:**
- **Music Composition**: Advertising, sonic branding, sound design
- **Branding/Design**: Future MOK Studio division
- **Live Music**: Bookings and performances

**Indigenous Advantage:**
- 100% Indigenous-owned (Harry Sayers)
- Supply Nation certification pending
- Eligible for IPP procurement pathways

---

## Quick Links

- [[01-areas/business/mokhouse/mokhouse-profile|MOK HOUSE Profile]]
- [[01-areas/business/mokhouse/context-mokhouse|Business Context]]
- [[02-projects/mokhouse|All Projects]]
- [[01-areas/business/mokhouse/mokmusic/mokmusic-clients|Client List]]

---

## Notes

*This dashboard is auto-generated from project files in `02-projects/mokhouse/`. Update project metadata to reflect changes here.*

**Voice Note Correction**: When transcription shows "mock house" or "mok house", the correct spelling is **MOK HOUSE** (all caps, two words).
