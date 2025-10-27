---
tags: [mokai, business]
relation:
  - "[[mokai]]"
  - "[[mokai]]"
date: "2025-10-14"
date created: Tue, 10 14th 25, 4:34:53 pm
date modified: Thu, 10 16th 25, 4:22:08 pm
---
# MOKAI Mission Control

**Last Updated**: 2025-10-16
**Current Phase**: Phase 1 - Foundation (Pre-Launch)
**Primary Goal**: Master business fundamentals while waiting for legal setup

---

## 🎯 This Week's Focus (Week 1: Oct 14-20)
#### **Operations Guide Mastery Week 1**
1. [ ] Read Indigenous Business & Procurement section (1 hour)
2. [ ] Read Prime Contractor Management section (1 hour)
3. [ ] Do daily flashcard review (15 min/day)
4. [ ] Write summary: "How MOKAI makes money" in own words

**Daily Time**: 5-7 hours available (allocate 2 hours/day to learning)

---

## 📬 MOKAI Tasks

### 🔥 Quick Wins (High Impact, Low Effort)
```dataviewjs
const tasks = dv.pages('"00-inbox/tasks/tasks-mokai"')
  .where(t => t.status !== "done" && t.status !== "archive")
  .where(t => t.impact >= 7 && t.effort <= 4)
  .sort(t => t.impact, 'desc');

if (tasks.length === 0) {
  dv.paragraph("*No quick wins available - focus on strategic work*");
} else {
  dv.table(
    ["✓", "Task", "Brief", "Impact", "Effort"],
    tasks.map(t => {
      const impactColor = t.impact >= 8 ? "🔴" : "🟡";
      const effortBar = "▓".repeat(Math.round(t.effort)) + "░".repeat(10 - Math.round(t.effort));

      return [
        `<input type="checkbox" ${t.Done ? "checked" : ""} onclick="
          const file = app.vault.getAbstractFileByPath('${t.file.path}');
          app.fileManager.processFrontMatter(file, fm => { fm.Done = !fm.Done; fm.status = fm.Done ? 'done' : 'in-progress'; });
        ">`,
        t.file.link,
        t.description || "",
        `${impactColor} ${t.impact}`,
        `${effortBar} ${t.effort}`
      ];
    })
  );
}
```

### 🎯 Strategic Work (High Impact, High Effort)
```dataviewjs
const tasks = dv.pages('"00-inbox/tasks/tasks-mokai"')
  .where(t => t.status !== "done" && t.status !== "archive")
  .where(t => t.impact >= 7 && t.effort >= 5)
  .sort(t => t.impact, 'desc');

if (tasks.length === 0) {
  dv.paragraph("*No strategic work scheduled*");
} else {
  dv.table(
    ["✓", "Task", "Brief", "Impact", "Effort"],
    tasks.map(t => {
      const impactColor = t.impact >= 8 ? "🔴" : "🟡";
      const effortBar = "▓".repeat(Math.round(t.effort)) + "░".repeat(10 - Math.round(t.effort));

      return [
        `<input type="checkbox" ${t.Done ? "checked" : ""} onclick="
          const file = app.vault.getAbstractFileByPath('${t.file.path}');
          app.fileManager.processFrontMatter(file, fm => { fm.Done = !fm.Done; fm.status = fm.Done ? 'done' : 'in-progress'; });
        ">`,
        t.file.link,
        t.description || "",
        `${impactColor} ${t.impact}`,
        `${effortBar} ${t.effort}`
      ];
    })
  );
}
```

### 📋 Next Up
```dataviewjs
const tasks = dv.pages('"00-inbox/tasks/tasks-mokai"')
  .where(t => t.status === "next-up" || t.status === "inbox")
  .sort(t => t.impact, 'desc');

if (tasks.length === 0) {
  dv.paragraph("*Inbox empty - all tasks triaged*");
} else {
  dv.table(
    ["✓", "Task", "Brief", "Impact", "Effort", "Category"],
    tasks.map(t => {
      const impactColor = t.impact >= 8 ? "🔴" : (t.impact >= 5 ? "🟡" : "⚪");
      const effortBar = "▓".repeat(Math.round(t.effort)) + "░".repeat(10 - Math.round(t.effort));

      return [
        `<input type="checkbox" ${t.Done ? "checked" : ""} onclick="
          const file = app.vault.getAbstractFileByPath('${t.file.path}');
          app.fileManager.processFrontMatter(file, fm => { fm.Done = !fm.Done; fm.status = fm.Done ? 'done' : 'in-progress'; });
        ">`,
        t.file.link,
        t.description || "",
        `${impactColor} ${t.impact}`,
        `${effortBar} ${t.effort}`,
        t.category || ""
      ];
    })
  );
}
```


### ⏳ Waiting (Blocked)
```dataviewjs
const tasks = dv.pages('"00-inbox/tasks/tasks-mokai"')
  .where(t => t.status === "waiting");

if (tasks.length === 0) {
  dv.paragraph("*No blocked tasks*");
} else {
  dv.table(
    ["Task", "Brief", "Impact"],
    tasks.map(t => {
      const impactColor = t.impact >= 8 ? "🔴" : (t.impact >= 5 ? "🟡" : "⚪");
      return [
        t.file.link,
        t.description || "",
        `${impactColor} ${t.impact}`
      ];
    })
  );
}
```

### ✅ Recently Completed
```dataviewjs
const tasks = dv.pages('"00-inbox/tasks/tasks-mokai"')
  .where(t => t.status === "done")
  .sort(t => t.file.mtime, 'desc')
  .limit(5);

if (tasks.length === 0) {
  dv.paragraph("*No completed tasks yet*");
} else {
  dv.table(
    ["Task", "Brief", "Impact"],
    tasks.map(t => {
      const impactColor = t.impact >= 8 ? "🔴" : (t.impact >= 5 ? "🟡" : "⚪");
      return [
        t.file.link,
        t.description || "",
        `${impactColor} ${t.impact}`
      ];
    })
  );
}
```

**Task Legend:**
- **Impact**: 🔴 High (8-10) | 🟡 Medium (5-7) | ⚪ Low (1-4)
- **Effort**: ▓▓▓▓▓▓▓▓▓▓ = 10/10 effort
- **Categories**: learning | operations | sales | admin | technical

---

## 📊 Current Status (REALITY CHECK)

### Legal & Structure (⏸️ WAITING ON JACK'S FAMILY TRUST)
- **MOKAI Registration**: Not yet (waiting on Jack's trust setup)
- **Ownership**: Harry 51% / Jack 49% / Kelly COO
- **Supply Nation**: Will apply once ABN/ACN secured
- **Insurance**: Not yet (will get quotes once registered)
- **Contracts Ready**: Jack has templates for NDAs/subcontractor agreements

### Team Status
- **Harry**: Learning mode - 5-7 hrs/day available
- **Jack**: Has contractor network, leads technical/sales
- **Kelly**: Website + capability statements 90% done

### Sales Comfort
- **Harry's Sales Confidence**: 1/10 (Jack leads initial conversations)
- **Client Network**: Jack's network (Harry shadows and learns)
- **First Service to Sell**: Essential Eight Assessment ($50K, 5 days)

### Learning Progress
- **Operations Guide**: Starting today
- **Indigenous Procurement (IPP/MSA/Exemption 16)**: Can explain ✅
- **Cybersecurity Knowledge**: Jack leads technical, Harry learns basics
- **Flashcards**: Set up in Obsidian ✅

### Blockers 🚨
- **Obsidian syncing issues** (Oct 15) - Highlighted sections in Operations Guide got erased, frustrating workflow
- **Jack's family trust setup** (blocking ABN/ACN registration)
- **Haven't started structured Operations Guide reading yet** (only partial highlighting on Oct 15)

---

## 🏆 Recent Wins
- ✅ Implemented auto-diary capture hook for automatic logging (Oct 15)
- ✅ Created a few good workflows to make work run better (Oct 15)
- ✅ Created MOKAI dashboard system
- ✅ Clarified ownership split (51% Indigenous)
- ✅ Kelly's website almost done

---

## 📅 What Happens When (Timeline)

**Phase 1 (Next 30 Days)**: Learn & Prepare
- Harry masters Operations Guide
- Legal docs finalized (waiting on Jack's trust)
- Supply Nation application prep completed
- Insurance research done (3 quotes ready)

**Phase 2 (Days 31-60)**: Register & Activate
- MOKAI registered (ABN/ACN)
- Supply Nation application submitted
- Insurance purchased
- Jack activates network → 3-5 opportunities in pipeline

**Phase 3 (Days 61-90)**: First Client Delivery
- Close first Essential Eight engagement ($50K)
- Deliver with contractor (Jack/Harry QA)
- Create case study
- Net profit: $10-20K

**Full plan**: See [phase-1-foundation.md](status/phase-1-foundation.md)

---

## 🧠 Strategic Context (for AI)

**Harry's Real Burning Need**:
"Learn to talk the talk and be a credible CEO. Understand the business side (Operations Guide). Build solid foundation for execution."

**What Actually Moves MOKAI Forward Right Now**:
1. Harry learning Operations Guide (while waiting on legal)
2. Legal docs ready to sign the moment Jack's trust is done
3. Jack's network primed for activation post-registration

**Decision Framework**:
- Does this help Harry become a competent business operator? → Do it
- Does this prepare for fast execution once registered? → Do it
- Is this premature (requires legal entity)? → Note for Phase 2

---

## 📝 Weekly Scorecard

### Week of Oct 14, 2025
**Wins**:
- Set up tracking system
- Defined 3-phase plan
- Learned Essential Eight is easiest first sale

**Blockers**:
- Jack's trust setup
- Haven't started Ops Guide yet

**Next Week Focus**:
- Operations Guide mastery (Week 1)

**Learning Notes**:
- Operations Guide is key to credibility
- Essential Eight = $50K, 5 days, easiest to sell
- Need Jack's trust before registration

---

## 🗂️ Quick Links
- **This Week**: [Phase 1 - Next 30 Days](status/phase-1-foundation.md)
- **Future Reference**: [Phase 2-3 Plan](status/phase-2-3-future.md)
- [Operations Guide](docs/research/📘 - OPERATIONS GUIDE.md)
- [Profit Projections](docs/research/First year Profit projections for Mokai.md)
