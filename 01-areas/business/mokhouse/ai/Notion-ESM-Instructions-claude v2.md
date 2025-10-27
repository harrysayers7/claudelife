---
tags: [mokhouse, AI, automation]
date created: Fri, 10 3rd 25, 8:59:27 am
date modified: Fri, 10 3rd 25, 9:52:58 am
relation:
  - "[[mokhouse]]"
  - "[[97-tags/Claude-desktop|Claude-desktop]]"
  - "[[ESM]]"
---
## ESM NOTION PROJECT MANAGEMENT DATABASE

Database ID: 1e64a17b-b7f0-8115-be90-000b4548a3a6

IMPORTANT: Check Notion BEFORE creating invoices to:
  ✓ Verify project exists
  ✓ Prevent duplicate invoices
  ✓ Validate amounts
  ✓ Auto-update project status

PROPERTIES TO INTERACT WITH:

ALWAYS UPDATE:
  • Name (title): Project name
  • Status (status): Update to "Invoiced" after creating invoice
  • PO # (text): From extracted PO number
  • Demo Fee (number): Amount in AUD (no GST)

CONDITIONALLY UPDATE:
  • Invoice (text): Stripe invoice number (format: NLOLWU0R-####)
  • APRA (select): Set to "Not Done" if Status becomes "Awarded"

DO NOT TOUCH:
  • Award Fee (formula property)
  • Award (if won) (only update if explicitly told)
  • Any other properties not listed

WORKFLOW:
1. Search Notion for project by name
2. If found: verify not already invoiced
3. Create Stripe invoice
4. Update Notion with Status="Invoiced", PO#, Invoice#, Demo Fee
5. Confirm update completed
