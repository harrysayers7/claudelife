---
Done: false
today: false
follow up: false
this week: false
back burner: false
type: Task
status:
relation:
description:
effort:
ai-assigned: true
priority:
ai-ignore: true
---
Explore this idea and come up with some other options. I feel like the h1-4 s
## Universal Semantic Heading System

### H1 - **Primary Claim/Title** (Default Color)
**Semantic meaning**: The main topic or argument - what this document IS
- Use for: Document title, primary subject, core concept
- Think: "This note is about..."

---

### H2 - **Synthesis/Summary** (Blue/Highlight Color)
**Semantic meaning**: Distilled insights, TL;DR, key takeaways
- Use for: Executive summaries, conclusions, "what matters most"
- Think: "If you read nothing else, read this"
- Perfect for: Quick scanning, spaced repetition, sharing with others

---

### H3 - **Actionable Content** (Green/Action Color)
**Semantic meaning**: Steps, processes, things to DO
- Use for: Workflows, instructions, next actions, checklists
- Think: "How to execute this"
- Signals: This section requires action/implementation

---

### H4 - **Context/Explanation** (Orange/Info Color)
**Semantic meaning**: Background info, definitions, "why this matters"
- Use for: Rationale, definitions, theory, historical context
- Think: "Understanding before doing"
- Provides: The frame for H3 actions

---

### H5 - **Evidence/Examples** (Purple/Reference Color)
**Semantic meaning**: Proof, sources, case studies, data
- Use for: Research findings, examples, quotes, citations
- Think: "Show me the receipts"
- Supports: Claims made in H4 or arguments in H1

---

### H6 - **Metadata/System** (Gray/Muted Color)
**Semantic meaning**: Document housekeeping, not content
- Use for: Timestamps, tags, status, version control
- Think: "File cabinet info"
- Usually: Bottom of doc or in frontmatter-style block

---

## Real-World Example

```markdown
# Indigenous Procurement Strategy

## Summary: IPP provides 3-10% price advantage + sole-source opportunities up to $200k

### Action Steps
1. Maintain Supply Nation certification (annual renewal)
2. Monitor AusTender for Indigenous set-asides
3. Build relationship with agency procurement teams

#### Context: Why IPP Matters
Commonwealth agencies have 3% Indigenous procurement target. Only 66 certified Indigenous tech vendors exist, creating undersupply.

##### Evidence
- Finance.gov.au IPP policy (2015, updated 2020)
- Supply Nation: 2,700 members, only 66 in tech/cyber
- Mokai case: Won 4/7 tenders citing Indigenous status

###### Last Updated: 2025-10-14 | Source: [[mokai-sales-playbook]]
```

---

## How This Works Across PARA

### In a Project Note:
- **H1**: Project name
- **H2**: Current status/outcome goal
- **H3**: Next actions/milestones
- **H4**: Why this project exists
- **H5**: Past decisions/references
- **H6**: Admin metadata

### In an Area Note:
- **H1**: Area of responsibility
- **H2**: Standards/principles for this area
- **H3**: Recurring workflows
- **H4**: Context on why this area matters
- **H5**: Examples of good/bad execution
- **H6**: Ownership/review schedule

### In a Resource Note:
- **H1**: Concept/framework name
- **H2**: Core insight/definition
- **H3**: How to apply it
- **H4**: Background/theory
- **H5**: Research/case studies
- **H6**: Source attribution

### In Learning Notes:
- **H1**: Topic being learned
- **H2**: The "aha moment" / key insight
- **H3**: Practice exercises
- **H4**: Explanations/breakdowns
- **H5**: Examples/analogies
- **H6**: Review schedule metadata

---

## Obsidian CSS Snippet for Color-Coding

```css
/* H2 - Summary (Blue) */
.markdown-preview-view h2,
.cm-header-2 {
  color: #3b82f6;
  border-left: 4px solid #3b82f6;
  padding-left: 12px;
}

/* H3 - Action (Green) */
.markdown-preview-view h3,
.cm-header-3 {
  color: #10b981;
  border-left: 4px solid #10b981;
  padding-left: 12px;
}

/* H4 - Context (Orange) */
.markdown-preview-view h4,
.cm-header-4 {
  color: #f59e0b;
  border-left: 4px solid #f59e0b;
  padding-left: 12px;
}

/* H5 - Evidence (Purple) */
.markdown-preview-view h5,
.cm-header-5 {
  color: #8b5cf6;
  border-left: 4px solid #8b5cf6;
  padding-left: 10px;
}

/* H6 - Metadata (Gray) */
.markdown-preview-view h6,
.cm-header-6 {
  color: #6b7280;
  font-size: 0.85em;
  font-style: italic;
  padding-left: 8px;
}
```

---

## Cognitive Benefits

**Visual Scanning**:
- Blue = "Give me the insight"
- Green = "Tell me what to do"
- Orange = "Help me understand why"
- Purple = "Show me proof"

**Spaced Repetition**:
- Review only H2 sections for quick recall
- Drill H3 sections for skill practice
- Reference H5 for evidence when needed

**Writing Flow**:
- Start with H1 (what)
- Write H2 (synthesis) - forces clarity
- Fill H3 (actions) - makes it practical
- Add H4 (context) - provides depth
- Support with H5 (evidence) - builds trust
- Tag with H6 (metadata) - keeps organized

**Collaboration**:
- H2 = what to share in Slack/email
- H3 = what to delegate
- H4 = what to explain to new team members
- H5 = what to cite in proposals

---

**This system means**: Every time you see green text, you know "this is something to execute" - regardless of whether it's in a Mokai tender doc, a personal health note, or a music production workflow.

Want the CSS snippet customized for your specific color preferences, or need help setting up Obsidian to auto-format this way?
