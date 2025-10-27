---
type:
  - research 
relation:
  - "[[mokai]]"
  - "[[97-tags/claude-code|claude-code]]"
  - "[[agents]]"
tags:
sub-type:
effort:
location:
title: "{{title}}"
date created: Wed, 10 15th 25, 5:44:55 am
date modified: Wed, 10 15th 25, 5:49:07 am
---
┌─────────────────────────────────────────────────┐
│               CLAUDE CODE/DESKTOP                │
│              (Decision Engine)                   │
└──────────────┬──────────────────────────────────┘
               │
    ┌──────────▼──────────┐
    │   MindsDB MCP       │ ← THE INTEGRATION LAYER
    │   (Data Router)     │
    └──────────┬──────────┘
               │
    ┌──────────┴───────────────────┬─────────────┐
    │                              │             │
┌───▼────────┐  ┌─────────────────▼──┐  ┌──────▼──────┐
│ OBSIDIAN   │  │    SUPABASE        │  │  100+ OTHER │
│ (Mind)     │  │    (Transactions)  │  │  SOURCES    │
│            │  │                    │  │             │
│ • Context  │  │ • Financial data   │  │ • Stripe    │
│ • Plans    │  │ • Metrics          │  │ • Xero      │
│ • SOPs     │  │ • Analytics        │  │ • Notion    │
└────────────┘  └────────────────────┘  │ • GitHub    │
                                        │ • Slack     │
                                        │ • Calendar  │
                                        │ • Gmail     │
                                        └─────────────┘
``

## Why This Matters for Mokai

**Current state:**
- Claude Code can read Obsidian (via MCP)
- Claude Code can query Supabase (via direct connection)
- Everything else requires manual API work

**With MindsDB MCP:**

### 1. **Unified Business Intelligence**
`
You: "Show me this month's revenue vs burn rate,
     flag any overdue invoices in Xero,
     and check if Jack responded to the DTA tender email"

Claude Code:
├─ MindsDB → Supabase (revenue data)
├─ MindsDB → Xero (invoice status)
├─ MindsDB → Gmail (email search)
└─ Synthesizes answer from all three
``

### 2. **Automated Workflow Triggers**

`
### MindsDB can detect:
- New tender published → Update Obsidian tender tracker
- Invoice paid in Xero → Update Supabase cash flow
- Calendar meeting with "DTA" → Pull relevant context from Obsidian
- Contractor payment due → Alert in Slack
``

### 3. **Cross-System Analysis**
`
"Compare our actual project delivery times (from Notion)
 vs what we quoted (from Obsidian SOWs)
 vs what we billed (from Xero)"

MindsDB pulls from all three and Claude analyzes patterns


## Practical Mokai Use Cases

### Sales Pipeline
**Without MindsDB:**
- Manually check AusTender
- Copy to Obsidian
- Track in spreadsheet
- Remember to follow up

**With MindsDB:**
```
MindsDB monitors:
├─ AusTender RSS feeds → New opportunities
├─ Obsidian /mokai/sales/ → Your capability match
├─ Supabase → Current capacity
└─ Triggers: "You should bid on this DTA pentest - 85% match"
```

### Financial Management
`
Monthly board meeting prep:

Claude Code via MindsDB:
1. Pull P&L from Xero
2. Get transaction details from Supabase
3. Reference budget plans from Obsidian
4. Check contractor invoices pending
5. Generate board report artifact with full context
`
### Contractor Management
``
Jack uses contractor for DTA project:

MindsDB workflow:
├─ Check contractor availability (Notion database)
├─ Pull signed NDA from Google Drive
├─ Verify insurance expiry (spreadsheet)
├─ Create onboarding checklist (Obsidian template)
├─ Log engagement in Supabase
└─ Send Slack notification to team
