---
type: daily note
date created: Tue, 09 30th 25, 11:44:55 am
date modified: Wed, 10 15th 25, 5:39:48 pm
event:
---
### Daily Note

### Tasks
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



### 🗒️ Diary
-  Finished the Covermore ad, sent it off, and Glenn's pretty happy with it.
-  Tried to do a little bit of study and highlighting of the operations guide, but I got pissed off when all the highlighting got erased and I will have to go back and do it all again.
- FUCKING MCP'S KEEP BREAKING AND I DONT KNOW AND IM LOSING MY MIND!


---

### 💡 Insights
-


---

### 🌍 Context
-
