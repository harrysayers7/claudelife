---
type: Research Prompt
relation:
  - "[[mokai]]"
tags:
  - research-prompt
  - pricing
  - cybersecurity
  - financial-planning
project: mokai
category: research
research-type:
  - Market intelligence
status: pending
priority: critical
date created: 2025-10-11
---

# Research Prompt: Project-Level Pricing Intelligence

## Objective
Establish fixed-price and range estimates for standard cybersecurity service offerings to enable accurate quoting, bid/no-bid decisions, and margin planning.

## Current State
- **Have**: Day rate benchmarks ($800-$1,600/day depending on specialization)
- **Have**: General margin targets (20-40% for services, 5-15% for products)
- **Missing**: Project-level pricing for deliverable-based engagements
- **Missing**: Competitor fixed-price offerings

## Research Questions

### 1. Essential Eight Maturity Assessments
- **Q1.1**: What is the typical fixed price for an Essential 8 maturity assessment for:
  - 50-person organization?
  - 200-person organization?
  - 500+ person organization?
- **Q1.2**: What factors drive price variation? (Industry, complexity, data classification)
- **Q1.3**: How do competitors package this? (Day rate vs. fixed price vs. tiered packages)
- **Q1.4**: What's included in scope? (Documentation review, interviews, technical testing, reporting, presentation)
- **Q1.5**: Typical timeline? (1 week? 2-4 weeks? Longer?)

### 2. IRAP Assessments
- **Q2.1**: Fixed price ranges for IRAP assessments by:
  - System size (small/medium/large)
  - Classification level (Unclassified, Protected, Secret)
  - Cloud vs. on-premises
- **Q2.2**: How are IRAP engagements typically priced? (Daily rate, fixed fee, milestone-based)
- **Q2.3**: Average engagement length? (Weeks? Months?)
- **Q2.4**: What's the price delta between assessment-only vs. assessment + remediation support?
- **Q2.5**: Pre-IRAP readiness assessments - how priced?

### 3. Penetration Testing
- **Q3.1**: Fixed-price pen test packages:
  - External network pen test (X IPs)?
  - Web application pen test (X pages/endpoints)?
  - Internal network pen test?
  - Full red team engagement?
- **Q3.2**: How do boutique firms package pen testing vs. Big 4?
- **Q3.3**: Productized tiers? (Bronze/Silver/Gold with defined scope)
- **Q3.4**: Typical pricing for annual pen test retainers?
- **Q3.5**: Re-testing pricing (post-remediation validation)?

### 4. GRC Consulting
- **Q4.1**: Risk assessment engagement pricing:
  - Cyber risk assessment (1-day workshop vs. comprehensive)
  - Business impact analysis
  - Third-party risk assessment
- **Q4.2**: Policy development pricing:
  - Single policy (e.g., Acceptable Use Policy)
  - Full policy suite (10-15 policies)
  - ISO 27001 policy package
- **Q4.3**: Compliance gap analysis:
  - ISO 27001 readiness assessment
  - NSW Cyber Security Policy compliance
  - PSPF compliance review
- **Q4.4**: Virtual CISO retainer pricing:
  - Entry-level (monthly check-ins)
  - Standard (weekly engagement)
  - Comprehensive (embedded support)

### 5. Incident Response
- **Q5.1**: IR retainer pricing models:
  - Annual retainer with X hours included
  - Priority response SLA pricing
  - Tabletop exercise facilitation
- **Q5.2**: Incident response callout rates (after-hours, emergency)?
- **Q5.3**: Post-incident forensics and reporting?

### 6. Training & Awareness
- **Q6.1**: Security awareness training pricing:
  - Per-user per-year for e-learning platform
  - In-person workshop (half-day, full-day)
  - Phishing simulation campaigns
- **Q6.2**: Specialized training (e.g., secure coding, incident response)?

## Research Sources

### Primary Sources
1. **Government Tender Databases**
   - AusTender: Search for awarded cybersecurity contracts (filter by Essential 8, IRAP, pen test)
   - NSW eTendering: State government pricing
   - QLD, VIC tender portals
   - Filter for contracts $50k-$500k to see typical project values

2. **Competitor Pricing Intelligence**
   - Baidam Solutions: Website, marketing materials, case studies
   - Willyama Services: Public contract awards, panel rate cards
   - Phronesis Security: Productized offerings on website
   - CyberCX: Published service packages
   - Boutique firms: Ionize, Gridware, Sekuro pricing pages

3. **Industry Rate Cards & Panel Pricing**
   - Digital Marketplace: Published rate cards for panel members
   - Defence ICT panels: Rate schedules (if publicly available)
   - NSW Government ICT Services Panel: Rate card ranges
   - Managed Service Providers: Compare MSP pricing for similar services

4. **Professional Services Benchmarking**
   - Australian Information Security Association (AISA): Industry surveys
   - Cyber Security Cooperative Research Centre: Reports on service pricing
   - Supply Nation: Indigenous business pricing benchmarks (if available)

### Secondary Sources
1. **Industry Reports**
   - Gartner: Cybersecurity services pricing
   - Forrester: Australian cybersecurity market sizing
   - IDC: Professional services pricing trends

2. **Procurement Guides**
   - ASD: IRAP assessment procurement guide (mentions pricing considerations)
   - Department of Finance: SME procurement value-for-money guidance

3. **Competitor Analysis**
   - LinkedIn: Job postings with salary/rate information
   - Glassdoor: Competitor revenue estimates
   - ASIC: Company financial reports (if available)

## Deliverable Format

### Pricing Matrix Template
Create a comprehensive pricing matrix:

```markdown
## Essential Eight Maturity Assessment

| Organization Size | Scope | Timeline | Low End | Mid Range | High End | Notes |
|-------------------|-------|----------|---------|-----------|----------|-------|
| 1-50 users | Basic assessment | 1 week | $8,000 | $12,000 | $18,000 | Single site, simple architecture |
| 51-200 users | Standard assessment | 2 weeks | $15,000 | $25,000 | $35,000 | Multiple sites, moderate complexity |
| 201-500 users | Comprehensive assessment | 3-4 weeks | $30,000 | $50,000 | $75,000 | Complex architecture, multiple classifications |

**Scope Inclusions:**
- Documentation review (X hours)
- Stakeholder interviews (Y people)
- Technical configuration review
- Maturity scoring against ACSC model
- Executive report + technical findings
- Presentation/debrief (1-2 hours)

**Common Add-ons:**
- Remediation roadmap: +$5,000-$10,000
- Quarterly re-assessment: 30% of initial fee
- Implementation support: $X per strategy
```

Repeat for each service category.

### Competitive Positioning Analysis
For each service, document:
- **Big 4 Pricing**: Typical range (often 30-50% premium)
- **Boutique Pricing**: Mid-market benchmark
- **Indigenous Competitor Pricing**: Baidam, Willyama positioning
- **Freelancer/Individual Pricing**: Low-end benchmark
- **MOKAI Target Positioning**: Where to price (rationale)

### Margin Calculation Examples
```markdown
## Example: Essential 8 Assessment (200-person org)

**Client Price**: $25,000 (fixed fee)

**Cost Breakdown**:
- Senior consultant (3 days @ $1,200/day): $3,600
- Mid-level consultant (5 days @ $900/day): $4,500
- Report production (2 days @ $800/day): $1,600
- Project management overhead (10%): $950
- **Total Direct Costs**: $10,650

**Gross Margin**: $14,350 (57%)
**Less Overheads** (insurance, admin, sales, 25%): $6,250
**Net Margin**: $8,100 (32%)

**Conclusion**: Meets 20-40% target margin ✅
```

## Success Criteria
- [ ] Pricing ranges established for top 5 service offerings
- [ ] Validated against at least 3 competitor data points per service
- [ ] Margin calculations confirm 20-40% net achievable
- [ ] Identified price positioning vs. Big 4, boutiques, Indigenous competitors
- [ ] Clear scope definitions to prevent scope creep
- [ ] Add-on/upsell pricing established

## Timeline
- **Phase 1** (Week 1): AusTender scraping, competitor website analysis
- **Phase 2** (Week 2): Panel rate card research, industry reports
- **Phase 3** (Week 3): Validation with industry contacts, final matrix creation

## Next Actions After Research
1. Create MOKAI pricing calculator/template
2. Develop proposal templates with standard pricing tiers
3. Build bid/no-bid decision framework using pricing data
4. Train team on pricing strategy and negotiation boundaries
