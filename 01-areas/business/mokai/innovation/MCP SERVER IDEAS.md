---
tags: [mokai, business]
relation:
  - "[[mokai]]"
  - "[[mokai]]"
date created: Fri, 10 10th 25, 4:52:37 am
date modified: Fri, 10 10th 25, 4:54:35 am
---
I'll search for the instruction box to understand the context better.

Now I understand the context! Based on Mokai's business model and the MCP tools you already have (Supabase, Fireflies, Notion, Stripe, Cloudflare, Google integrations), here are 5 fast MCP v2 use cases you could build:

## 1. **AusTender Opportunity Monitor**
**Problem**: Missing Commonwealth contract opportunities worth $20M+ annually
**MCP Server**: Scrapes AusTender RSS/API → filters for cyber/IT → checks Indigenous requirements → posts to Notion pipeline
**Fast because**: Simple RSS parser + webhook, no complex auth
**Business impact**: First-mover advantage on tender responses

## 2. **Contractor Utilization & Margin Tracker**
**Problem**: Need real-time visibility on contractor billing vs actual revenue
**MCP Server**: Integrates Fireflies meeting notes + Google Calendar + Supabase → tracks billable hours → calculates margin against Stripe invoices
**Fast because**: You already have the data sources connected
**Business impact**: Prevents the "really fuck you" payroll tax surprise Jack warned about

## 3. **Supply Nation Compliance Monitor**
**Problem**: Must maintain 51%+ Indigenous ownership for IPP qualification
**MCP Server**: Monitors Stripe revenue splits → tracks Indigenous contractor spend % → alerts if falling below threshold
**Fast because**: Basic arithmetic on existing Stripe data
**Business impact**: Protects your competitive advantage (only 66 Indigenous vendors out of 2,700)

## 4. **Essential Eight Auto-Documenter**
**Problem**: Every engagement needs E8 compliance evidence → manual = slow
**MCP Server**: Templates in Notion → pulls client context from Google Drive → generates compliance checklists → exports to PDF
**Fast because**: Template-driven, no complex logic
**Business impact**: Speeds up your "productized services" strategy (Module 9)

## 5. **GST-Aware Cash Flow Forecaster**
**Problem**: Commonwealth 20-day rule + GST timing can create cash crunches
**MCP Server**: Pulls Stripe invoices → calculates GST liability → projects BAS dates → warns if working capital needed
**Fast because**: Date math + your existing financial data
**Business impact**: Avoids the distributor Net-30 trap Jack mentioned

**Quickest win**: Start with #2 (Contractor Utilization) since you already have Fireflies, Calendar, and Supabase connected. Would take ~2 hours to build and immediately shows Harry/Jack/Kelly where money's leaking.

Want me to spec out the MCP server code for any of these?
