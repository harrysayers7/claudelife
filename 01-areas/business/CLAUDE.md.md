---
date created: Sun, 10 19th 25, 9:33:08 pm
date modified: Sun, 10 19th 25, 9:34:21 pm
---
# Business Domain Context

**Purpose:** Strategic coordination and intelligence for all revenue-generating activities across Mokai, MOK HOUSE, SAFIA, and sole trader work.

## What This Domain Covers

**Business** = anything that generates revenue, has clients, requires contracts, involves compliance, or impacts financial decisions.

## Subdomain Functions

**`/mokai/`** → Cybersecurity consultancy operations
**`/mokhouse/`** → Creative/music business operations  
**`/safia/`** → Band business & royalty management
**`/soletrader/`** → Personal commercial work
**`/accounting/`** → Cross-entity financial oversight & tax strategy

## Domain Expectations

When working in `/01-areas/business/`:
- **Financial context matters** → Pull from Supabase when analyzing decisions
- **Compliance is critical** → Indigenous status, GST, tax structures affect everything
- **Context folders override** → Most recent operational docs take precedence
- **Cross-entity awareness** → Decisions in one business may impact others (tax, capacity, brand)

## Integration Points

- **Database:** Supabase for financial data
- **Server:** sayers-server (n8n automations)
- **Accounting:** White Sky (strategy) + The Practice (compliance)

**See subfolder `claude.md` for entity-specific operational context.**