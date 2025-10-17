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

### 📅 Today's Events

```dataviewjs
// Get today's date in YYYY-MM-DD format
const today = dv.date('today').toFormat('yyyy-MM-dd');

// Filter for files where type contains "event" AND when matches today
const events = dv.pages()
  .where(p => {
    if (!p.type) return false;
    // Handle type as string or array
    const typeStr = Array.isArray(p.type) ? p.type.join(' ') : String(p.type);
    return typeStr.toLowerCase().includes("event");
  })
  .where(p => p.when)
  .where(p => {
    // Parse when date and compare to today
    const whenDate = dv.date(p.when);
    return whenDate && whenDate.toFormat('yyyy-MM-dd') === today;
  })
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

### 📆 This Week's Events

```dataviewjs
// Get today's date and date 7 days from now
const today = dv.date('today');
const nextWeek = today.plus({ days: 7 });

// Filter for events within the next 7 days (excluding today)
const upcomingEvents = dv.pages()
  .where(p => {
    if (!p.type) return false;
    // Handle type as string or array
    const typeStr = Array.isArray(p.type) ? p.type.join(' ') : String(p.type);
    return typeStr.toLowerCase().includes("event");
  })
  .where(p => p.when)
  .where(p => {
    const whenDate = dv.date(p.when);
    if (!whenDate) return false;

    // Event must be after today and within 7 days
    return whenDate > today && whenDate <= nextWeek;
  })
  .sort(p => p.when); // Sort by date

// Display upcoming events table
if (upcomingEvents.length > 0) {
  dv.table(
    ["Event", "Date", "Time", "Note"],
    upcomingEvents.map(p => [
      p.file.link,
      dv.date(p.when).toFormat('EEE, MMM dd'), // "Mon, Oct 21"
      p.time || "",
      p.note || ""
    ])
  );
} else {
  dv.paragraph("*No events scheduled for the next week*");
}
```

---

### 🧠 Notes




## Index

- [[01-areas/business/mokai/INDEX|Mokai]]
-
