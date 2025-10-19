---
date created: Mon, 10 20th 25, 8:23:06 am
date modified: Mon, 10 20th 25, 8:24:16 am
---
# Brainstorming Folder Context

**Purpose:** Pre-project creative ideation and concept development **Status:** Experimental → ideas may not become projects **Location:** `01-areas/business/mokhouse/brainstorming/`

---

## What This Folder Contains

Raw creative ideas, client pitches, sonic concept explorations, and early-stage project thinking before formal brief receipt. Not all ideas here will become actual projects.

**Typical contents:**

- Unsolicited pitch concepts
- Sonic branding experiments
- Genre/style exploration notes
- Reference track analysis
- Client research and positioning ideas
- Technical approach brainstorms (new plugins, AI tools, production techniques)

---

## How to Treat These Files

### ✅ When Working Here:

- **Encourage wild ideas** - no constraints from formal briefs yet
- **No project lifecycle tracking** - these aren't in the standard workflow
- **Cross-pollinate concepts** - suggest connections to other brainstorm files
- **Reference real projects** - link to `02-projects/mokhouse/` when relevant
- **Suggest SUNO experiments** - low-stakes place to test AI generation approaches
- **Track inspiration sources** - keep references for future brief matching

### ❌ Don't:

- Create formal project files (YYMMDD-format) - those live in `02-projects/`
- Add invoice/PO tracking - no commercial structure yet
- Enforce brief template formatting - keep it loose
- Auto-generate full AI suggestions unless requested - this is human-led ideation

---

## File Structure Recommendations

**Naming:** Descriptive, not date-prefixed

- `sonic-branding-luxury-automotive.md`
- `vocal-processing-techniques-2025.md`
- `pitch-qantas-sonic-refresh.md`

**Minimal frontmatter:**

```yaml
---
type: brainstorm
relation:
  - "[[mokhouse]]"
status: ideation | pitched | shelved | evolved-to-project
created: YYYY-MM-DD
---
```

**Loose structure:**

- Concept overview
- Reference materials
- Technical notes
- Potential applications
- Links to similar work

---

## Transition to Formal Projects

When a brainstorm becomes a real brief:

1. Keep original brainstorm file (reference later)
2. Create formal project in `02-projects/mokhouse/` using standard template
3. Link back to brainstorm in project's "Creative References" section
4. Update brainstorm status to `evolved-to-project`

---

## Claude Code Behavior

When user says:

- **"Brainstorm..."** → Work in this folder, loose format
- **"New project from brief..."** → Create in `02-projects/`, full template
- **"This brainstorm became real..."** → Link to new project file

Track evolution: brainstorm → pitch → brief → project → invoice → payment

---

## Integration Points

- **SUNO prompts:** Test experimental ideas without client pressure
- **Reference library:** Build `/references/brainstorm/` for inspiration
- **Knowledge graph:** Link concepts across brainstorms for pattern recognition
- **AI suggestions:** Use as playground for refining prompt engineering

---

**Key Difference from 02-projects:** This is creative sandbox. Projects are commercial workflow.

Brainstorm = "What if we..." Project = "Client wants... by [date]"