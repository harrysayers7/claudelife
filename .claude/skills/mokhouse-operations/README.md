# MOK HOUSE Operations Skill

A comprehensive Claude Code Skill for MOK HOUSE business operations, creative workflows, and client relationships.

## Purpose

This skill eliminates the need to manually load MOK HOUSE context each session. Claude automatically recognizes MOK HOUSE-related conversations and loads the appropriate business knowledge, creative patterns, and operational guidelines.

## What This Skill Provides

### Business Knowledge
- MOK Music & MOK Studio divisions
- ESM/Panda Candy submission workflows
- Indigenous positioning and procurement advantages
- Team structure and contact information
- Pricing strategy and financial context

### Creative Intelligence
- Client preferences and patterns (from Graphiti)
- Winning creative approaches
- Project outcome analysis
- Portfolio examples and blurbs

### Operational Tools
- Project creation templates
- Invoice generation guides
- Brief checklists
- Financial tracking patterns

## Skill Structure

```
mokhouse-operations/
├── SKILL.md                      # Main skill instructions for Claude
├── README.md                     # This file
├── scripts/
│   └── create-project.sh         # Project file creation helper
└── resources/
    ├── project-template.md       # Standard project file template
    ├── invoice-template.md       # Invoice format template
    └── brief-checklist.md        # Brief requirements checklist
```

## How It Works

### Automatic Activation

Claude automatically loads this skill when it detects:
- MOK HOUSE business discussions
- Music project or submission questions
- Client relationship or creative preference queries
- Financial or invoicing requests
- Indigenous procurement context
- Shortcut phrases: "MH", "mh", "mock house", "mok house"

### Knowledge Sources

The skill integrates multiple knowledge sources:

1. **SKILL.md** - Core business model, workflows, team structure
2. **Graphiti Knowledge Graph** - Client preferences, project outcomes, creative patterns
3. **Dashboard** - Real-time financial metrics, active projects
4. **Project Files** - Detailed creative briefs, client feedback
5. **Diary** - Daily operations, learnings, timeline context

### Automatic Learning

The skill is designed to evolve through Graphiti integration:
- Captures client feedback during conversations
- Stores project outcomes and budgets
- Documents winning creative patterns
- Records team expertise and relationships

## Usage Examples

### Example 1: Client Question

**You:** "How much was the Nintendo job?"

**Claude (skill active):**
Queries Graphiti for Nintendo budget:
- Usage Fee: $3,250
- Demo Fee: $650
- Total: $3,900
- Status: Paid Oct 17, 2025

### Example 2: Creative Direction

**You:** "What creative approach worked for GWM?"

**Claude (skill active):**
References project files and Graphiti:
- Creative: [Approach details]
- Why Won: [Success factors]
- Client Feedback: [Quoted feedback]
- Pattern: [Reusable insights]

### Example 3: Workflow Question

**You:** "What happens if we don't win?"

**Claude (skill active):**
ESM submission workflow:
- Submit alongside 3-4 composers
- If Won: Usage fee ($2,500-$8,000)
- If Not Won: Demo fee ($250-$1,000) guaranteed
- Invoice regardless of outcome

## Templates & Scripts

### Create New Project

**Using Script:**
```bash
.claude/skills/mokhouse-operations/scripts/create-project.sh
```

**Using Template:**
Copy `resources/project-template.md` to `02-projects/mokhouse/` and fill in details.

**Using Claude:**
```
/mokhouse-create-project [or describe project, skill handles it]
```

### Generate Invoice

Reference `resources/invoice-template.md` for standard format including:
- Indigenous ownership notation
- GST compliance
- Project details
- Payment terms

### Process New Brief

Use `resources/brief-checklist.md` to ensure all critical information is captured:
- Creative requirements
- Technical specifications
- Financial terms
- Timeline and deliverables

## Integration with Existing System

### Replaces `/mokhouse-master`

This skill provides the same context as `/mokhouse-master` but:
- ✅ Automatically activated (no manual command needed)
- ✅ Available across all projects (not just claudelife folder)
- ✅ Persists across sessions
- ✅ Continuously learns via Graphiti

### Works With Existing Commands

The skill complements existing MOK HOUSE slash commands:
- `/mokhouse-create-project` - Still useful for quick project creation
- `/mokhouse-create-invoice` - Generates invoices with skill context
- `/mokhouse-update-status` - Updates with skill awareness
- `/mokhouse-mark-paid` - Financial tracking enhanced by skill
- `/mokhouse-portfolio-blurb` - Portfolio generation with skill patterns

### Graphiti Integration

The skill automatically stores learnings in Graphiti:

**Automatic Storage When Detecting:**
- "Client prefers..." → Store preference
- "We won because..." → Store winning pattern
- "Invoice #123 for $X" → Store financial detail
- "Client feedback: ..." → Store quoted feedback

**Example Storage:**
```javascript
mcp__graphiti__add_memory({
  name: "MOK HOUSE project outcome - [Project]",
  episode_body: `Project details, creative direction,
                 why won, budget, client feedback...`,
  group_id: "mokhouse",
  source: "message"
})
```

## Updating the Skill

### When to Update

Update SKILL.md when:
- New major client wins (capture patterns)
- Business model or service changes
- New agency relationships
- Updated pricing strategy
- Supply Nation certification complete
- MOK Studio division launches

### How to Update

1. Edit `.claude/skills/mokhouse-operations/SKILL.md`
2. Update relevant sections (Client Preferences, Financial Context, etc.)
3. Claude automatically uses updated version in next session

### Version History

- **v1.0 (2025-10-20)**: Initial skill creation
  - Business model and ESM/Panda Candy workflows
  - Team structure and Indigenous positioning
  - Client patterns from Graphiti (Nintendo, GWM examples)
  - Templates for projects, invoices, brief checklists

## Success Metrics

The skill is successful when:

✅ **Context Loading Time**: Zero manual context loading needed
✅ **Consistency**: Same business knowledge across all Claude sessions
✅ **Learning**: Automatically captures and applies client patterns
✅ **Portability**: MOK HOUSE context available in any project
✅ **Accuracy**: Correct agency contacts, pricing, workflows automatically

## Testing Checklist

Test the skill by asking Claude (in a new session):

- [ ] "How does the ESM submission workflow work?"
- [ ] "What was the Nintendo project budget?"
- [ ] "Who should I contact at ESM for a creative question?"
- [ ] "What's our Indigenous advantage for procurement?"
- [ ] "What creative approach works for automotive clients?"

Claude should answer accurately without loading additional context.

## Related Documentation

- **Main CLAUDE.md**: `/Users/harrysayers/Developer/claudelife/CLAUDE.md`
- **MOK HOUSE Profile**: `/01-areas/business/mokhouse/mokhouse-profile.md`
- **MOK HOUSE Context**: `/01-areas/business/mokhouse/CLAUDE.md`
- **Dashboard**: `/01-areas/business/mokhouse/mokhouse-dashboard.md`
- **Projects**: `/02-projects/mokhouse/`

## Support

For questions or issues with this skill:
1. Check SKILL.md for comprehensive documentation
2. Review README examples
3. Test with specific MOK HOUSE questions
4. Update SKILL.md if business context changes

---

**Skill Version:** 1.0
**Created:** 2025-10-20
**Last Updated:** 2025-10-20
**Owner:** Harry Sayers (MOK HOUSE)
