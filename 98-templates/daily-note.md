---
type: daily note
date created: Tue, 09 30th 25, 11:44:55 am
date modified: Fri, 10 3rd 25, 12:33:39 pm
event:
---
## Daily Note

```dataviewjs
// Get tasks for today that aren't done
const pages = dv.pages()
  .where(p => p.today && !p.Done)
  .sort(p => p.file.ctime, 'desc');

// Create table with checkbox in first column
dv.table(
  ["✓", "Task", "Description"],
  pages.map(p => {
    const checkbox = dv.el('input', '', {
      attr: { type: 'checkbox' },
      cls: 'task-checkbox'
    });

    checkbox.onclick = async () => {
      const file = app.vault.getAbstractFileByPath(p.file.path);
      await app.fileManager.processFrontMatter(file, (fm) => {
        fm.Done = true;
      });
    };

    return [
      checkbox,
      p.file.link,
      p.description || ""
    ];
  })
);
```

## 📅 Today's Events

```dataviewjs
// Get today's date in YYYY-MM-DD format
const today = dv.date('today').toFormat('yyyy-MM-dd');
const todayDate = dv.date('today');

// Helper function to check if event occurs on a specific date
function occursOn(event, checkDate) {
  const startDate = dv.date(event.when);
  if (!startDate) return false;

  const checkDateStr = checkDate.toFormat('yyyy-MM-dd');
  const startDateStr = startDate.toFormat('yyyy-MM-dd');

  // Extract recurrence pattern from checkbox list
  let recurrencePattern = null;
  if (event.recurrence) {
    if (Array.isArray(event.recurrence)) {
      // Checkbox list format: find the checked item
      for (let item of event.recurrence) {
        const itemStr = String(item).trim();
        if (itemStr.match(/^\[x\]/i)) {
          // Extract pattern after [x] checkbox
          recurrencePattern = itemStr.replace(/^\[x\]\s*/i, '').trim().toLowerCase();
          break;
        }
      }
    } else {
      // String format (backwards compatibility)
      recurrencePattern = String(event.recurrence).toLowerCase();
    }
  }

  // Non-recurring: direct date match
  if (!recurrencePattern) {
    return startDateStr === checkDateStr;
  }

  // Recurring: check if date falls on recurrence pattern
  if (checkDate < startDate) return false; // Before start date

  // Check end date
  if (event.recurrence_end) {
    const endDate = dv.date(event.recurrence_end);
    if (checkDate > endDate) return false;
  }

  // Calculate if date matches recurrence pattern
  const daysDiff = Math.floor((checkDate - startDate) / (1000 * 60 * 60 * 24));

  switch(recurrencePattern) {
    case 'daily':
      return true;
    case 'weekly':
      return daysDiff % 7 === 0;
    case 'biweekly':
      return daysDiff % 14 === 0;
    case 'monthly':
      return startDate.day === checkDate.day;
    case 'yearly':
      return startDate.month === checkDate.month && startDate.day === checkDate.day;
    default:
      return false;
  }
}

// Filter for event files
const allEvents = dv.pages()
  .where(p => {
    if (!p.type) return false;
    const typeStr = Array.isArray(p.type) ? p.type.join(' ') : String(p.type);
    return typeStr.toLowerCase().includes("event");
  })
  .where(p => p.when);

// Get events for today (including recurring)
const events = allEvents
  .where(p => occursOn(p, todayDate))
  .sort(p => p.time || p.file.name);

// Display events table
if (events.length > 0) {
  dv.table(
    ["Event", "Time", "Note"],
    events.map(p => [
      p.file.link,
      p.time || "",
      p.note || ""
    ])
  );
} else {
  dv.paragraph("*No events scheduled for today*");
}
```

## 📆 This Week's Events

```dataviewjs
// Get today's date and date 7 days from now
const today = dv.date('today');
const nextWeek = today.plus({ days: 7 });

// Helper function to check if event occurs on a specific date
function occursOn(event, checkDate) {
  const startDate = dv.date(event.when);
  if (!startDate) return false;

  const checkDateStr = checkDate.toFormat('yyyy-MM-dd');
  const startDateStr = startDate.toFormat('yyyy-MM-dd');

  // Extract recurrence pattern from checkbox list
  let recurrencePattern = null;
  if (event.recurrence) {
    if (Array.isArray(event.recurrence)) {
      // Checkbox list format: find the checked item
      for (let item of event.recurrence) {
        const itemStr = String(item).trim();
        if (itemStr.match(/^\[x\]/i)) {
          // Extract pattern after [x] checkbox
          recurrencePattern = itemStr.replace(/^\[x\]\s*/i, '').trim().toLowerCase();
          break;
        }
      }
    } else {
      // String format (backwards compatibility)
      recurrencePattern = String(event.recurrence).toLowerCase();
    }
  }

  // Non-recurring: direct date match
  if (!recurrencePattern) {
    return startDateStr === checkDateStr;
  }

  // Recurring: check if date falls on recurrence pattern
  if (checkDate < startDate) return false;

  if (event.recurrence_end) {
    const endDate = dv.date(event.recurrence_end);
    if (checkDate > endDate) return false;
  }

  const daysDiff = Math.floor((checkDate - startDate) / (1000 * 60 * 60 * 24));

  switch(recurrencePattern) {
    case 'daily':
      return true;
    case 'weekly':
      return daysDiff % 7 === 0;
    case 'biweekly':
      return daysDiff % 14 === 0;
    case 'monthly':
      return startDate.day === checkDate.day;
    case 'yearly':
      return startDate.month === checkDate.month && startDate.day === checkDate.day;
    default:
      return false;
  }
}

// Filter for event files
const allEvents = dv.pages()
  .where(p => {
    if (!p.type) return false;
    const typeStr = Array.isArray(p.type) ? p.type.join(' ') : String(p.type);
    return typeStr.toLowerCase().includes("event");
  })
  .where(p => p.when);

// Generate occurrences for the next 7 days
const upcomingOccurrences = [];
for (let i = 1; i <= 7; i++) {
  const checkDate = today.plus({ days: i });

  allEvents.forEach(event => {
    if (occursOn(event, checkDate)) {
      upcomingOccurrences.push({
        event: event,
        date: checkDate
      });
    }
  });
}

// Sort by date, then time
upcomingOccurrences.sort((a, b) => {
  const dateDiff = a.date - b.date;
  if (dateDiff !== 0) return dateDiff;

  const aTime = a.event.time || "";
  const bTime = b.event.time || "";
  return aTime.localeCompare(bTime);
});

// Display upcoming events table
if (upcomingOccurrences.length > 0) {
  dv.table(
    ["Event", "Date", "Time", "Note"],
    upcomingOccurrences.map(occ => [
      occ.event.file.link,
      occ.date.toFormat('EEE, MMM dd'), // "Mon, Oct 21"
      occ.event.time || "",
      occ.event.note || ""
    ])
  );
} else {
  dv.paragraph("*No events scheduled for the next week*");
}
```

## 🎵 Active MOK HOUSE Projects

```dataviewjs
// Get active MOK HOUSE projects (not paid, not invoiced, not archived)
const activeProjects = dv.pages('"02-projects/mokhouse"')
  .where(p => {
    // Must be a project type with mokhouse relation
    if (p.type !== "project") return false;

    const relation = p.relation;
    if (!relation) return false;
    const hasMokhouse = Array.isArray(relation)
      ? relation.some(r => String(r).includes("mokhouse"))
      : String(relation).includes("mokhouse");

    if (!hasMokhouse) return false;

    // Exclude paid projects, invoiced projects, and archived projects
    if (p.paid === true) return false;
    if (p.status === "Invoiced" || p.status === "Complete") return false;
    if (p.file.path.includes("archive")) return false;

    return true;
  })
  .sort(p => p["due date"] || p["date received"], 'asc');

if (activeProjects.length > 0) {
  dv.table(
    ["Project", "Customer", "Status", "Due Date"],
    activeProjects.map(p => [
      p.file.link,
      p.customer || "—",
      p.status || "—",
      p["due date"] || "—"
    ])
  );
} else {
  dv.paragraph("*No active MOK HOUSE projects*");
}
```

---

### 🧠 Notes




>[!info]- 📅 Monthly Calendar
>```dataviewjs
>// Get current date
>const now = dv.date('today');
>const currentMonth = now.month;
>const currentYear = now.year;
>const today = now.day;
>
>// Get first day of month and total days
>const firstDay = dv.date(`${currentYear}-${String(currentMonth).padStart(2, '0')}-01`);
>const lastDay = firstDay.plus({ months: 1 }).minus({ days: 1 });
>const daysInMonth = lastDay.day;
>const startDayOfWeek = firstDay.weekday; // 1 = Monday, 7 = Sunday
>
>// Month name
>const monthName = firstDay.toFormat('MMMM yyyy');
>
>// Create calendar HTML
>let calendarHTML = `
><div style="font-family: monospace; text-align: center; margin: 20px 0;">
>  <h3>${monthName}</h3>
>  <table style="width: 100%; border-collapse: collapse; margin: 10px auto;">
>    <thead>
>      <tr style="background-color: var(--background-modifier-border);">
>        <th style="padding: 8px; text-align: center;">Mon</th>
>        <th style="padding: 8px; text-align: center;">Tue</th>
>        <th style="padding: 8px; text-align: center;">Wed</th>
>        <th style="padding: 8px; text-align: center;">Thu</th>
>        <th style="padding: 8px; text-align: center;">Fri</th>
>        <th style="padding: 8px; text-align: center;">Sat</th>
>        <th style="padding: 8px; text-align: center;">Sun</th>
>      </tr>
>    </thead>
>    <tbody>
>`;
>
>let dayCounter = 1;
>let currentWeek = [];
>
>// Fill first week with empty cells before month starts
>for (let i = 1; i < startDayOfWeek; i++) {
>  currentWeek.push('<td style="padding: 8px;"></td>');
>}
>
>// Fill in the days of the month
>for (let day = 1; day <= daysInMonth; day++) {
>  const isToday = day === today;
>  const cellStyle = isToday
>    ? 'padding: 8px; text-align: center; background-color: var(--interactive-accent); color: var(--text-on-accent); font-weight: bold; border-radius: 4px;'
>    : 'padding: 8px; text-align: center;';
>
>  currentWeek.push(`<td style="${cellStyle}">${day}</td>`);
>
>  // End of week (Sunday) or last day of month
>  if (currentWeek.length === 7 || day === daysInMonth) {
>    // Fill remaining cells in last week
>    while (currentWeek.length < 7) {
>      currentWeek.push('<td style="padding: 8px;"></td>');
>    }
>
>    calendarHTML += '<tr>' + currentWeek.join('') + '</tr>';
>    currentWeek = [];
>  }
>}
>
>calendarHTML += `
>    </tbody>
>  </table>
></div>
>`;
>
>// Render the calendar
>dv.el('div', calendarHTML);
>```

## Index

- [[01-areas/business/mokai/INDEX|Mokai]]
- [[claudelife-commands-guide|Commands]]
- [[mokhouse-dashboard|MOK HOUSE HQ]]
-
