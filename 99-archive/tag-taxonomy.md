---
created: 2025-01-29
type: reference
status: active
---

# Claudelife Tag Taxonomy

## Primary Domain Tags
Use ONE per file to establish primary context:

- `#mokai` - Cybersecurity consultancy content
- `#mokhouse` - Music business operations
- `#personal` - Personal productivity/development
- `#finance` - Financial management/tracking
- `#ai-brain` - AI/automation systems
- `#health` - Health & fitness tracking

## Type Tags (Secondary)
Describes the content type:

### Core Content Types
- `#profile` - Entity/company/person profiles
- `#project` - Active projects
- `#workflow` - Automation workflows
- `#memory` - Captured learnings/insights
- `#command` - Slash commands/scripts
- `#report` - Analysis/research reports
- `#template` - Reusable templates
- `#guide` - How-to documentation

### Technical Types
- `#mcp` - MCP server configurations
- `#database` - Database schemas/queries
- `#api` - API endpoints/integrations
- `#ml` - Machine learning/AI models
- `#infrastructure` - Server/deployment

### Business Types
- `#compliance` - Regulatory/compliance docs
- `#contract` - Legal agreements
- `#tender` - Government procurement
- `#invoice` - Financial records
- `#client` - Client-related content

## Status Tags
Current state of content:

- `#active` - Currently maintained/used
- `#archived` - Historical reference
- `#draft` - Work in progress
- `#review` - Needs attention/review
- `#deprecated` - Outdated but retained

## Action Tags
For actionable items:

- `#todo` - General tasks
- `#todo/urgent` - High priority tasks
- `#todo/back-burn` - Low priority tasks
- `#blocked` - Waiting on dependencies
- `#in-progress` - Currently being worked on

## Specialized Tags

### Cybersecurity (Mokai)
- `#essential8` - Essential Eight compliance
- `#irap` - IRAP assessments
- `#pentest` - Penetration testing
- `#grc` - Governance, Risk, Compliance
- `#soc2` - SOC2 compliance

### Financial
- `#tax` - Tax-related
- `#deductible` - Tax deductible expenses
- `#business-expense` - Business costs
- `#receivable` - Income/payments due
- `#payable` - Expenses/payments owed

### Automation
- `#trigger` - Trigger.dev tasks
- `#n8n` - n8n workflows
- `#scheduled` - Scheduled automations
- `#sync` - Data synchronization

## Relationship Tags
For cross-referencing:

- `#requires/[tag]` - Dependencies
- `#blocks/[tag]` - Blocking relationships
- `#related/[tag]` - Related content

## Date-based Tags (Auto-generated)
- `#created/2025-01` - Creation month
- `#modified/2025-01` - Last modification
- `#quarter/Q1-2025` - Quarterly grouping

## Usage Guidelines

### Wiki-links vs Tags in Obsidian

**Use Wiki-links `[[]]` for:**
- Entities (companies, people, projects): `[[MOKAI]]`, `[[Harrison Sayers]]`
- Key concepts that deserve their own page: `[[Essential Eight]]`, `[[IRAP Assessment]]`
- Creating strong bidirectional connections in the graph

**Use Tags `#` for:**
- Categorization and filtering: `#draft`, `#active`, `#todo`
- Metadata that doesn't need its own page: `#2025-01`, `#urgent`
- Grouping similar content for searches

1. **Minimum Requirements**: Each file should have:
   - 1 primary domain wiki-link: `[[MOKAI]]` or `[[MOK HOUSE]]`
   - 1-2 categorization tags: `#project`, `#active`
   - Related entity links where relevant

2. **Maximum Limits**:
   - 3-5 wiki-links to avoid over-connection
   - 3-5 tags for categorization

3. **Connection Hierarchy**:
   ```
   Wiki-links (strong) > Tags (weak) > Mentions (implicit)
   ```

4. **Naming Convention**:
   - Wiki-links: Natural casing `[[MOKAI]]`, `[[Essential Eight Compliance]]`
   - Tags: All lowercase with hyphens `#in-progress`, `#todo-urgent`

5. **Front Matter Format**:
   ```yaml
   ---
   domain: mokai
   type: profile
   status: active
   entities: ["[[MOKAI]]", "[[Harrison Sayers]]"]
   tags: ["#active", "#compliance", "#cybersecurity"]
   created: 2025-01-29
   ---
   ```

6. **In-content Usage**:
   ```markdown
   This project for [[MOKAI]] implements [[Essential Eight]] compliance
   for [[Department of Defence]]. #cybersecurity #government

   Related: [[IRAP Assessment]], [[Supply Nation]]
   ```

## Auto-tagging Rules

Based on file location:
- `01-areas/business/mokai/` → `#mokai`
- `01-areas/business/mokhouse/` → `#mokhouse`
- `01-areas/finance/` → `#finance`
- `02-projects/` → `#project`
- `.claude/commands/` → `#command`
- `memory/` → `#memory`
- `04-resources/reports/` → `#report`

## Graph View Optimization

For best Obsidian graph visualization:
- Use consistent primary tags for clustering
- Include [[wiki-links]] for strong connections
- Tag relationships create weaker connections
- Combine tags + links for multi-dimensional graphs

## Maintenance

Weekly review checklist:
- [ ] Check for untagged files
- [ ] Validate tag consistency
- [ ] Update deprecated content
- [ ] Review #review tagged items
- [ ] Clean up #draft items older than 30 days
