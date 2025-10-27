# GST Threshold Monitoring Workflow

**Purpose**: Automated monitoring system to track GST registration thresholds for Harry's entities and trigger alerts when registration is required.

---

## Overview

### GST Thresholds
- **Mandatory registration**: Turnover ≥ $75,000
- **Alert threshold** (proactive): 70% of $75K = **$52,500**
- **Registration deadline**: Within 21 days of exceeding threshold

### Entities to Monitor

| Entity | Current Turnover | Status | Monitoring Frequency |
|--------|------------------|--------|---------------------|
| **Harrison (Sole Trader)** | $35,000 | ❌ Not registered, no action needed | Quarterly (APRA stable) |
| **MOK HOUSE PTY LTD** | $14,000 (19%) | ❌ Not registered, **monitor monthly** | Monthly |
| **SAFIA Unit Trust** | Variable | ✅ Already registered | Quarterly (BAS lodgment) |
| **MOKAI PTY LTD** | $0 (pre-revenue) | ⏳ Register before first invoice | On first contract |

---

## Monitoring Workflow

### STEP 1: Data Collection (UpBank → Supabase)

**Automated sync** (via n8n workflow):
1. UpBank transactions webhook → n8n
2. n8n categorizes transaction → Supabase `financial_transactions`
3. Supabase aggregates monthly turnover → `entity_financials` table

**Manual entry** (for non-UpBank income):
- SAFIA Unit Trust distributions
- Cash payments
- Direct transfers outside UpBank

### STEP 2: Calculate Rolling 12-Month Turnover

**Formula**:
```
Rolling turnover = SUM(monthly_income, last 12 months)
```

**SQL query** (Supabase):
```sql
SELECT
  entity_id,
  entity_name,
  SUM(income) as rolling_12m_income,
  (SUM(income) / 75000.0 * 100) as threshold_percentage,
  CASE
    WHEN SUM(income) >= 75000 THEN 'REGISTER NOW'
    WHEN SUM(income) >= 52500 THEN 'ALERT: 70% threshold'
    WHEN SUM(income) >= 37500 THEN 'WARNING: 50% threshold'
    ELSE 'OK'
  END as status
FROM financial_transactions
WHERE
  transaction_date >= NOW() - INTERVAL '12 months'
  AND transaction_type = 'income'
  AND entity_id = 'mok-house' -- Change per entity
GROUP BY entity_id, entity_name
```

**Example output** (MOK HOUSE):
```
Entity: MOK HOUSE PTY LTD
Rolling 12m income: $14,000
Threshold %: 18.7%
Status: OK
```

### STEP 3: Alert Thresholds

**Three-tier alert system**:

#### 🟢 Green Zone (0-49% threshold)
- **Range**: $0 - $37,499
- **Action**: No action required
- **Monitoring**: Monthly review
- **Dashboard**: Display current % and trend

#### 🟡 Yellow Zone (50-69% threshold)
- **Range**: $37,500 - $52,499
- **Action**: Review growth trend, prepare for registration
- **Alert**: Email notification to Harry
- **Monitoring**: Bi-weekly review
- **Dashboard**: Highlight warning status

**Alert email template**:
```
Subject: MOK HOUSE Approaching GST Threshold (50%)

Hi Harry,

MOK HOUSE has reached 50% of the GST registration threshold:

Current turnover: $42,000 (56% of $75K)
Projected (next 3 months): $48,000 (64% of $75K)

Next steps:
- Continue monitoring bi-weekly
- Prepare GST registration checklist
- Review invoice templates

Dashboard: https://dashboard.example.com/gst
```

#### 🔴 Red Zone (70%+ threshold)
- **Range**: $52,500 - $74,999
- **Action**: **Proactive registration recommended**
- **Alert**: Urgent email + SMS to Harry
- **Monitoring**: Weekly review
- **Dashboard**: Display "Action Required" status

**Urgent alert template**:
```
Subject: 🚨 MOK HOUSE GST Action Required (70% threshold)

Hi Harry,

MOK HOUSE has reached 70% of the GST registration threshold:

Current turnover: $55,000 (73% of $75K)
Projected (next 3 months): $62,000 (83% of $75K)

⚠️ RECOMMENDED ACTION:
Register for GST now to avoid rushing when hitting $75K.

Benefits of early registration:
✅ Time to update systems (invoices, accounting)
✅ Claim input tax credits immediately
✅ Professional appearance for clients

Registration checklist: [Link]
Dashboard: https://dashboard.example.com/gst
```

#### 🚨 Critical (≥100% threshold)
- **Range**: $75,000+
- **Action**: **Mandatory registration within 21 days**
- **Alert**: Immediate email + SMS + dashboard banner
- **Legal requirement**: Register or face penalties

**Critical alert template**:
```
Subject: 🚨🚨 MOK HOUSE MUST REGISTER FOR GST IMMEDIATELY

Hi Harry,

MOK HOUSE has exceeded the GST registration threshold:

Current turnover: $76,500 (102% of $75K)
Date exceeded: 15 October 2025

⚠️ LEGAL REQUIREMENT:
Must register for GST within 21 days (by 5 November 2025)

URGENT ACTIONS:
1. Register via Business Portal: business.gov.au
2. Update invoice templates (add GST)
3. Set up BAS lodgment system
4. Notify clients of GST registration

Registration deadline: 5 November 2025
Penalty if late: Failure to Register penalties

Dashboard: https://dashboard.example.com/gst
Book accountant: [Link]
```

### STEP 4: Dashboard Visualization

**Supabase + React dashboard** (`/Users/harrysayers/Developer/sayers-data/dashboard`):

**Components**:
1. **GST Gauge Chart**:
   - Current % of threshold (0-100%)
   - Color-coded zones (green/yellow/red)
   - Target line at 70%

2. **Monthly Income Trend**:
   - 12-month line chart
   - Rolling average trendline
   - Projection (next 3 months)

3. **Entity Cards**:
   - MOK HOUSE, MOKAI, SAFIA
   - Current status, next action
   - Days until registration (if applicable)

4. **Registration Checklist**:
   - Pre-registration tasks
   - Progress tracking
   - Links to resources

**Dashboard mockup**:
```
┌─────────────────────────────────────────────────────────┐
│             GST Threshold Dashboard                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  MOK HOUSE PTY LTD                    [⚠️ WARNING]     │
│  ┌─────────────────────────────────────────────────┐   │
│  │         18.7% of GST Threshold                  │   │
│  │  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        │   │
│  │  $14,000 / $75,000                              │   │
│  │                                                  │   │
│  │  Projected (3 months): $18,500 (25%)            │   │
│  │  Alert threshold (70%): $52,500                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Monthly Income Trend (Last 12 months)                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │  $2,500 ┤                                        │   │
│  │         ┤           ●                            │   │
│  │  $2,000 ┤     ●           ●                      │   │
│  │         ┤ ●       ●   ●       ●                  │   │
│  │  $1,500 ┤     ●                   ●              │   │
│  │         ┤                             ●          │   │
│  │  $1,000 ┤                                 ●   ●  │   │
│  │         ┤                                        │   │
│  │    $500 ┤                                        │   │
│  │         └────────────────────────────────────────│   │
│  │          J F M A M J J A S O N D                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Next Actions:                                         │
│  ☑ Monitor monthly (Next review: 1 Nov 2025)          │
│  ☐ Alert at $52,500 (70% threshold)                   │
│  ☐ Register for GST                                   │
│                                                         │
│  [View Full Report] [Export Data] [Set Alerts]        │
└─────────────────────────────────────────────────────────┘
```

---

## Automated Workflows (n8n)

### Workflow 1: Monthly GST Threshold Check

**Trigger**: 1st of each month (9:00 AM)

**Steps**:
1. Query Supabase for rolling 12-month turnover (all entities)
2. Calculate % of $75K threshold
3. Determine alert status (Green/Yellow/Red/Critical)
4. Send email/SMS if Yellow/Red/Critical
5. Update Graphiti with threshold fact
6. Log to Serena (if new pattern detected)

**n8n workflow** (pseudocode):
```
Trigger: Cron (0 9 1 * *)
  ↓
Query Supabase: Rolling 12m income by entity
  ↓
For each entity:
  ├─ Calculate threshold %
  ├─ Determine alert level
  └─ If ≥50%:
      ├─ Send email alert
      └─ Update dashboard
  ↓
Store in Graphiti:
  "Entity [name] at [X]% of GST threshold on [date]"
```

### Workflow 2: UpBank Transaction → Threshold Update

**Trigger**: UpBank webhook (new transaction)

**Steps**:
1. Receive webhook payload
2. Extract transaction details (amount, description, date)
3. Categorize transaction (income/expense, entity)
4. Insert into Supabase `financial_transactions`
5. Recalculate rolling 12-month turnover
6. Check if crossed alert threshold (50%, 70%, 100%)
7. If threshold crossed, trigger immediate alert

**n8n workflow** (pseudocode):
```
Trigger: Webhook (UpBank transaction)
  ↓
Extract: amount, description, date, account
  ↓
Categorize:
  ├─ Entity (MOK HOUSE / Harrison / SAFIA)
  ├─ Type (income / expense)
  └─ Category (client payment / APRA / equipment)
  ↓
Insert Supabase: financial_transactions
  ↓
Recalculate: rolling_12m_income
  ↓
Check thresholds:
  ├─ Previous %: X%
  ├─ New %: Y%
  └─ If Y ≥ 50% AND X < 50%:
      └─ Send alert (threshold crossed)
```

### Workflow 3: GST Registration Reminder

**Trigger**: 7 days before critical deadline (if turnover ≥$75K)

**Steps**:
1. Query entities with turnover ≥$75K and not GST registered
2. Calculate days since threshold exceeded
3. Calculate days until registration deadline (21 days)
4. If 7 days before deadline, send urgent reminder
5. If past deadline, escalate alert

**n8n workflow** (pseudocode):
```
Trigger: Cron (0 9 * * *) -- Daily check
  ↓
Query Supabase: Entities WHERE turnover ≥ $75K AND gst_registered = false
  ↓
For each entity:
  ├─ Calculate: days_since_exceeded = TODAY - threshold_date
  ├─ Calculate: days_until_deadline = 21 - days_since_exceeded
  └─ If days_until_deadline ≤ 7:
      ├─ Send urgent reminder (email + SMS)
      └─ Display dashboard banner
  └─ If days_until_deadline < 0:
      └─ Send overdue alert (escalate to tax agent)
```

---

## Python Validation Script

**Script**: `scripts/validate_gst_threshold.py`

**Purpose**: Quick CLI check of GST threshold status

**Usage**:
```bash
python scripts/validate_gst_threshold.py --entity "MOK HOUSE"
```

**Output**:
```
GST Threshold Status - MOK HOUSE PTY LTD
─────────────────────────────────────────
Rolling 12-month income: $14,000
Threshold percentage: 18.7%
Status: ✅ OK (Green Zone)

Alert thresholds:
  50% ($37,500): Not reached
  70% ($52,500): Not reached
 100% ($75,000): Not reached

Projected (3 months): $18,500 (24.7%)
Next review: 1 November 2025

Action required: None
Monitor: Monthly
```

**Script content** (see `scripts/validate_gst_threshold.py` for full implementation)

---

## Entity-Specific Monitoring

### Harrison Robert Sayers (Sole Trader)

**Income source**: APRA royalties (~$35K/year)

**Monitoring frequency**: Quarterly

**Threshold status**: **Safe** (47% of threshold)

**Actions**:
- ✅ No GST registration needed
- ✅ Monitor APRA annual statement
- ✅ No invoice issuance required

**Why safe**: APRA income is passive, distributed automatically. No growth expected.

### MOK HOUSE PTY LTD

**Income source**: Music production, commercial music

**Current turnover**: $14,000/year (19% of threshold)

**Monitoring frequency**: **Monthly** (high growth potential)

**Projected growth**: 50% increase over next 12 months (based on pipeline)

**Threshold status**: **Monitor closely**

**Actions**:
- ⚠️ Track monthly income via UpBank sync
- ⚠️ Alert at $52,500 (70% threshold)
- ⚠️ Prepare invoice templates for GST (tax invoice format)
- ⚠️ Research BAS lodgment options (Xero integration)

**Key dates**:
- Current: $14,000 (19%)
- Projected (6 months): $21,000 (28%)
- Projected (12 months): $28,000 (37%)
- Alert threshold: $52,500
- Registration threshold: $75,000

**Growth scenarios**:
```
Scenario 1: Steady growth (20%/year)
  Year 1: $14,000 → $16,800 (22%)
  Year 2: $16,800 → $20,160 (27%)
  Year 3: $20,160 → $24,192 (32%)
  ✅ No registration needed for 3+ years

Scenario 2: New client (big project $30K)
  Current: $14,000 (19%)
  After project: $44,000 (59%) ⚠️ Yellow zone
  Action: Monitor closely, prepare for registration

Scenario 3: Multiple projects ($50K/year)
  Current: $14,000 (19%)
  After 12 months: $64,000 (85%) 🚨 Red zone
  Action: Register proactively at 70% ($52,500)
```

### SAFIA Unit Trust

**Income source**: Live shows, streaming, sync

**Current status**: ✅ **Already GST registered**

**Monitoring frequency**: Quarterly (BAS lodgment)

**Actions**:
- ✅ Lodge BAS quarterly (handled by band accountant)
- ✅ Ensure tax invoices issued to venues/promoters
- ✅ Track Harry's distribution (for personal tax return)

**No threshold monitoring needed** (already registered)

### MOKAI PTY LTD

**Income source**: Cybersecurity consulting (future)

**Current status**: Pre-revenue (setup phase)

**Threshold status**: **Register before first invoice**

**Why register early**:
- Government contracts require GST invoicing
- Can claim ITCs on setup costs immediately
- Professional appearance for B2G clients

**Actions**:
- ⚠️ Register for GST **before first government contract**
- ⚠️ Set up BAS lodgment system (quarterly)
- ⚠️ Design tax invoice template
- ⚠️ Configure accounting software (Xero)

**Timeline**:
```
Now: Pre-revenue, not registered
Month 1: First client contract signed → Register for GST
Month 2: Issue first tax invoice (with GST)
Month 3: End of quarter → Lodge first BAS
```

---

## Integration with Graphiti & Serena

### Graphiti: Store Threshold Facts

**Monthly threshold update**:
```javascript
mcp__graphiti__add_memory({
  name: "GST Threshold: [Entity] [Month] [Year]",
  episode_body: "Entity [Entity name] reached [X]% of GST registration threshold on [date]. Rolling 12-month turnover: $[amount]. Status: [Green/Yellow/Red/Critical]. Next action: [action].",
  source: "message",
  group_id: "harry-financial-entities"
})
```

**Example**:
```javascript
mcp__graphiti__add_memory({
  name: "GST Threshold: MOK HOUSE October 2025",
  episode_body: "Entity MOK HOUSE PTY LTD reached 18.7% of GST registration threshold on 2025-10-01. Rolling 12-month turnover: $14,000. Status: Green (OK). Next action: Monitor monthly, no registration required.",
  source: "message",
  group_id: "harry-financial-entities"
})
```

### Serena: Store Monitoring Patterns

**Store calculation methods**:
```javascript
mcp__serena__write_memory({
  memory_name: "harry_gst_monitoring_methods",
  content: `
# GST Threshold Monitoring Methods

## Rolling 12-Month Calculation
\`\`\`sql
SELECT SUM(income) as rolling_12m
FROM financial_transactions
WHERE transaction_date >= NOW() - INTERVAL '12 months'
  AND transaction_type = 'income'
  AND entity_id = 'mok-house'
\`\`\`

## Alert Thresholds
- Green: 0-49% ($0-$37,499)
- Yellow: 50-69% ($37,500-$52,499) - Email alert
- Red: 70-99% ($52,500-$74,999) - Urgent alert + SMS
- Critical: 100%+ ($75,000+) - Mandatory registration

## Projection Formula
Projected (3 months) = Current + (Avg monthly × 3)
Avg monthly = Rolling 12m / 12
`
})
```

---

## Workflow Checklist

**Monthly GST review**:
- [ ] Run SQL query (rolling 12-month turnover)
- [ ] Calculate % of $75K threshold
- [ ] Update dashboard with current status
- [ ] Check alert thresholds (50%, 70%, 100%)
- [ ] Send alerts if thresholds crossed
- [ ] Store threshold fact in Graphiti
- [ ] Update projection (next 3 months)

**If approaching 70% threshold ($52,500)**:
- [ ] Review growth trend (monthly income chart)
- [ ] Prepare GST registration checklist
- [ ] Update invoice templates (add GST line)
- [ ] Research BAS lodgment options
- [ ] Book accountant for GST advice
- [ ] Set up accounting software (Xero)

**If exceeding 100% threshold ($75,000)**:
- [ ] **Register for GST immediately** (within 21 days)
- [ ] Update all systems (invoices, website, marketing)
- [ ] Notify clients (prices now include GST)
- [ ] Set BAS lodgment calendar reminders
- [ ] Configure accounting software for BAS
- [ ] Coordinate with tax agent

---

## Quick Reference: Registration Timeline

**Example** (MOK HOUSE exceeds threshold on 15 October 2025):

```
15 Oct 2025: Turnover reaches $75,500 (threshold exceeded)
  ↓
16 Oct 2025: Automated alert sent to Harry
  ↓
17-22 Oct 2025: Harry registers for GST via Business Portal
  ↓
23 Oct 2025: GST registration confirmed, effective from 15 Oct
  ↓
24-31 Oct 2025: Update invoices, website, systems
  ↓
1 Nov 2025: Start issuing tax invoices (with GST)
  ↓
31 Dec 2025: End of Q2 FY2025-26
  ↓
28 Jan 2026: Lodge first BAS (Q2: Oct-Dec 2025)
```

**Key dates**:
- Day 0: Threshold exceeded
- Day 1: Alert sent
- Day 1-21: **Registration window** (legal requirement)
- Day 21: Registration deadline (avoid penalties)

---

**Use this workflow to ensure timely GST registration and ATO compliance.**
**Automate monitoring via Supabase + n8n for hands-off tracking.**
