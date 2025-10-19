---
type: daily note
date created: Tue, 09 30th 25, 10:37:28 am
date modified: Thu, 10 16th 25, 12:44:04 pm
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
- BE MORE TANK Video came out! https://www.instagram.com/p/DP0ay4vEenR/?hl=en&img_index=1


---

### 💡 Insights
- i should build a nutrionist agent
- I seem to learn and think better when im not at my desk I guess its because I have no access to my computer 
- wimhof makes me creative but the caveat is it makes me think while im doing it which is not the way to do it. You're meant clear your mind. 


---

### 🌍 Context
-


## Index

- [[01-areas/business/mokai/INDEX|Mokai]]
