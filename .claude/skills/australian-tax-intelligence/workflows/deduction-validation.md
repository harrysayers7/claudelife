# Tax Deduction Validation Workflow

**Purpose**: Step-by-step process to validate whether an expense is tax-deductible for Harry's multi-entity structure.

---

## Quick Validation Flowchart

```
New Expense
    ↓
┌───────────────────────────────────────────────┐
│ STEP 1: Which entity incurred this expense?  │
└─────────────┬─────────────────────────────────┘
              ↓
    ┌─────────┴─────────┐
    │  Entity Routing   │
    └─────────┬─────────┘
              ↓
┌─────────────┴─────────────┐
│ Harrison (Sole Trader)    │───→ APRA income only (minimal deductions)
│ MOK HOUSE PTY LTD         │───→ Music production expenses
│ SAFIA Unit Trust          │───→ Band expenses (trust level)
│ MOKAI PTY LTD             │───→ Cybersecurity expenses
└─────────────┬─────────────┘
              ↓
┌───────────────────────────────────────────────┐
│ STEP 2: Apply Section 8-1 ITAA 1997 Test     │
└─────────────┬─────────────────────────────────┘
              ↓
    ┌─────────┴─────────┐
    │  1. Nexus Test    │───→ Incurred in gaining/producing income?
    │  2. Capital Test  │───→ Not capital in nature?
    │  3. Private Test  │───→ Not private/domestic?
    │  4. Prohibition   │───→ Not specifically denied?
    └─────────┬─────────┘
              ↓
         All YES?
              ↓
┌───────────────────────────────────────────────┐
│ STEP 3: Calculate Deductible Amount          │
└─────────────┬─────────────────────────────────┘
              ↓
    ┌─────────┴─────────┐
    │  Business Use %   │
    │  Apportionment    │
    │  Timing Rules     │
    └─────────┬─────────┘
              ↓
┌───────────────────────────────────────────────┐
│ STEP 4: Evidence & Documentation             │
└─────────────┬─────────────────────────────────┘
              ↓
    Claim Deduction ✅
```

---

## Detailed Validation Steps

### STEP 1: Entity Identification

**Question**: Which entity incurred the expense and will claim the deduction?

#### Harrison Robert Sayers (Sole Trader - ABN 89 184 087 850)

**Income source**: APRA royalties (~$35K/year)

**Deductible expenses** (rare):
- ✅ APRA membership fees (if any)
- ✅ Professional fees related to royalty agreements
- ✅ Union fees (if music industry union member)

**NOT deductible**:
- ❌ Musical instruments (not used to earn APRA income)
- ❌ Recording studio rent (APRA income is passive, not active music production)
- ❌ Vehicle expenses (no travel required for APRA income)

**Reason**: APRA income is passive (paid automatically), so very few expenses have nexus

#### MOK HOUSE PTY LTD (ABN 38 690 628 212)

**Income source**: Music production for clients, commercial music

**Deductible expenses**:
- ✅ Musical instruments and equipment (used for client work)
- ✅ Software subscriptions (DAW, plugins)
- ✅ Home office expenses (dedicated space)
- ✅ Internet and phone (business use %)
- ✅ Vehicle expenses (Tesla - business use %)
- ✅ Professional development (courses, workshops)
- ✅ Accountant fees
- ✅ Insurance (professional indemnity, public liability)

**Reason**: Direct nexus to income-producing activities (client projects)

#### SAFIA Unit Trust

**Income source**: Live performances, streaming, sync licensing

**Deductible expenses** (at trust level):
- ✅ Band manager fees
- ✅ Tour expenses (flights, accommodation, meals)
- ✅ Marketing and promotion
- ✅ Music video production
- ✅ Legal fees (contracts, licensing)

**NOT deductible by Harry individually**:
- ❌ Home studio equipment (claim via MOK HOUSE instead)
- ❌ Personal musical development (unless directly for SAFIA)

**Reason**: Expenses deducted at trust level before distribution to members

#### MOKAI PTY LTD (when operational)

**Income source**: Cybersecurity consulting, government contracts

**Deductible expenses**:
- ✅ Professional certifications (CISSP, CEH, etc.)
- ✅ Software licenses (security tools, testing platforms)
- ✅ Contractor payments (subcontracted specialists)
- ✅ Professional indemnity insurance
- ✅ Legal fees (contract reviews, compliance)
- ✅ Marketing (website, branding, conferences)

**Reason**: Direct nexus to income-producing activities (client services)

---

### STEP 2: Section 8-1 ITAA 1997 Test

**Apply ALL four tests**:

#### Test 1: Nexus (Income-Producing Connection)

**Question**: Was the expense incurred in **gaining or producing** assessable income?

**Strong nexus** ✅:
- Musical instrument purchased for client project (MOK HOUSE)
- Security certification for client requirement (MOKAI)
- Tour transport for live show (SAFIA)
- Accountant preparing tax return (all entities)

**Weak nexus** ❌:
- Gym membership for "general wellbeing" (no income connection)
- Personal grooming (not required for work)
- Commute to regular workplace (private travel)

**Examples**:

| Expense | Entity | Nexus? | Reason |
|---------|--------|--------|--------|
| **Serum plugin** ($189) | MOK HOUSE | ✅ Strong | Used in client music production |
| **Anytime Fitness** ($15/week) | Harrison | ❌ None | Personal health, no income link |
| **CISSP exam** ($749) | MOKAI | ✅ Strong | Required for government contracts |
| **Haircut** ($50) | Any | ❌ None | Personal appearance (unless performer) |

**Graphiti storage** (if nexus confirmed):
```javascript
mcp__graphiti__add_memory({
  name: "Deduction Rule: [Expense Type]",
  episode_body: "Expense '[Expense]' for [Entity] has [strong/weak/no] nexus to income because [reason]. Deductible: [Yes/No]. Reference: Section 8-1 ITAA 1997.",
  source: "message",
  group_id: "harry-financial-entities"
})
```

#### Test 2: Capital vs Revenue

**Question**: Is the expense **capital** in nature (enduring asset) or **revenue** (repairs/maintenance)?

**Revenue** ✅ (immediate deduction):
- Repairs and maintenance (Tesla service)
- Software subscriptions (monthly/annual)
- Office supplies
- Professional fees

**Capital** ❌ (depreciation over time):
- Purchase of equipment >$1,000 (audio interface, computer)
- Vehicle purchase (Tesla - depreciate over 8 years)
- Website development (if enduring value >$1,000)

**Examples**:

| Expense | Capital? | Treatment |
|---------|----------|-----------|
| **Tesla service** ($500) | ❌ No (maintenance) | Immediate deduction (50% business use) |
| **New MacBook** ($3,000) | ✅ Yes (enduring asset) | Depreciate at 40% (2.5 year life) |
| **Spotify subscription** ($12/month) | ❌ No (recurring expense) | Immediate deduction (if business use) |
| **Logic Pro purchase** ($350) | ⚠️ Borderline | Immediate if <$1,000, depreciate if >$1,000 |

**Depreciation calculation** (if capital):
```
Diminishing value method:
Year 1: Cost × (200% / Effective life) × (Business use %)
Year 2: (Cost - Year 1 deduction) × Rate × Business use %
```

**Example** (MacBook $3,000, 90% business use, 2.5 year life):
```
Rate: 200% / 2.5 = 80% (diminishing value)
Year 1: $3,000 × 80% × 90% = $2,160
Year 2: ($3,000 - $2,400) × 80% × 90% = $432
```

#### Test 3: Private vs Business Use

**Question**: Is the expense **private/domestic** in nature, or for business purposes?

**Private/domestic** ❌ (never deductible):
- Gym membership (personal wellbeing)
- Regular meals (private sustenance)
- Commute to regular workplace (home → studio)
- Personal grooming (haircuts, clothing)
- Child care (domestic expense)

**Business use** ✅ (deductible):
- Professional subscriptions (APRA, industry bodies)
- Client meals (business development)
- Work-to-work travel (studio → client meeting)
- Compulsory uniforms with logo
- Overtime meals (genuine overtime, reasonable amount)

**Mixed use** ⚠️ (apportion):
- Vehicle (Tesla - 50% business, 50% private)
- Home office (dedicated 25% space)
- Phone/internet (70% business, 30% private)
- Computer (90% business, 10% private)

**Apportionment method**:
```
Deductible amount = Total cost × Business use %
```

**Example** (Tesla insurance $2,508, 50% business use):
```
Deductible: $2,508 × 50% = $1,254
```

**Proof required**:
- Vehicle: 12-week logbook (repeat every 5 years)
- Home office: Floor plan (m² calculation) + diary (hours worked)
- Phone: 4-week usage diary (business calls/data %)

#### Test 4: Specific Denial Provisions

**Question**: Is the expense **specifically denied** by another tax provision?

**Denied deductions** ❌:
- Fines and penalties (traffic fines, ATO penalties)
- Entertainment (50% limitation on client meals for companies)
- Gifts and donations (unless to DGR charity via trust)
- Illegal activities (can't deduct bribes, illegal payments)
- Prepaid expenses >$1,000 and >12 months (apportion over period)

**Examples**:

| Expense | Denied? | Reason |
|---------|---------|--------|
| **Parking fine** ($150) | ✅ Yes | Penalties not deductible |
| **Client lunch** ($200) | ⚠️ Partial | 50% limitation for companies (FBT rules) |
| **Charity donation** ($500) | ✅ Yes (individual) | Only via trust or company (special rules) |
| **Annual software** ($1,200 paid June) | ⚠️ Apportion | Prepaid >$1,000 + >12 months |

---

### STEP 3: Calculate Deductible Amount

If expense passes all Section 8-1 tests, calculate the deductible amount:

#### Full Deduction (100%)

**Criteria**:
- Used solely for business
- No private use component
- Not capital (or <$1,000)

**Examples**:
- APRA membership fee
- Professional software (used only for client work)
- Accountant fees (tax return preparation)

**Claim**: Full amount in year incurred

#### Partial Deduction (Apportionment)

**Criteria**:
- Mixed business/private use
- Business use % can be substantiated

**Apportionment methods**:

**Method 1: Usage diary** (phone, internet)
- Track usage for 4 weeks
- Calculate business use %
- Apply to full year's cost

**Example** (iPhone $100/month):
```
4-week diary:
- Business calls: 70% of minutes
- Private calls: 30% of minutes

Annual deduction:
$100 × 12 months × 70% = $840
```

**Method 2: Logbook** (vehicle)
- 12-week continuous logbook
- Record all trips (date, km, purpose)
- Calculate business km %
- Apply to all vehicle expenses

**Example** (Tesla):
```
Logbook: 50% business km (2,500 / 5,000 km)

Annual expenses:
- Loan interest: $4,000 × 50% = $2,000
- Insurance: $2,508 × 50% = $1,254
- Electricity: $600 × 50% = $300
- Depreciation: $12,000 × 50% = $6,000
Total: $9,554
```

**Method 3: Floor space** (home office)
- Measure dedicated office space (m²)
- Calculate % of total home
- Apply to utilities (electricity, gas)

**Example** (Harry's home office):
```
Office: 25m² dedicated space
Home: 100m² total

Electricity: $200/quarter × 4 × 25% = $200/year
Gas (heating): $100/quarter × 4 × 25% = $100/year
Internet: $80/month × 12 × 100% = $960/year (dedicated business)
Total: $1,260
```

#### Depreciation (Assets >$1,000)

**Calculate annual deduction**:

**Diminishing value** (most common):
```
Annual deduction = Opening balance × (200% / Effective life) × Business use %
```

**Prime cost** (straight-line):
```
Annual deduction = Cost / Effective life × Business use %
```

**Example** (Audio interface $2,000, 100% business, 5-year life):
```
Diminishing value:
Year 1: $2,000 × 40% = $800
Year 2: $1,200 × 40% = $480
Year 3: $720 × 40% = $288
...

Prime cost:
Each year: $2,000 / 5 = $400
```

**Store in Serena** (calculation pattern):
```javascript
mcp__serena__write_memory({
  memory_name: "harry_depreciation_calculations",
  content: `
# Asset Depreciation Patterns

## [Asset Name] ([Entity])
- Cost: $X,XXX
- Effective life: X years
- Business use: XX%
- Method: Diminishing value / Prime cost
- Annual deduction: $XXX

## Calculation:
[Step-by-step calculation]
`
})
```

---

### STEP 4: Evidence & Documentation

**Required evidence** (must retain for 5 years):

#### Tax Invoice Requirements

**For expenses ≥$82.50 (inc GST)**:
- [ ] Tax invoice from supplier
- [ ] Shows supplier ABN
- [ ] Shows GST amount or "includes GST"
- [ ] Date of purchase
- [ ] Description of goods/services

**For expenses <$82.50**:
- [ ] Receipt (tax invoice not required)
- [ ] Shows date and amount

#### Apportionment Evidence

**Vehicle expenses** (if claiming >$4,250):
- [ ] 12-week logbook
- [ ] Records: Date, start/end odometer, km, purpose
- [ ] Keep for 5 years, update every 5 years

**Home office** (actual cost method):
- [ ] Floor plan (m² calculation)
- [ ] Diary of hours worked from home (representative period)
- [ ] Utility bills (electricity, gas, internet)

**Phone/internet** (business use %):
- [ ] 4-week usage diary
- [ ] Itemized bills (showing business calls)
- [ ] Calculation of business %

#### Asset Register (for assets >$1,000)

**Track depreciation**:
- [ ] Purchase date and cost
- [ ] Effective life (ATO determination)
- [ ] Business use %
- [ ] Depreciation method chosen
- [ ] Annual deduction calculations

**Example** (MOK HOUSE asset register):
```
Asset: MacBook Pro 16"
Purchase: 15 July 2024
Cost: $4,500
Effective life: 2.5 years (computer equipment)
Business use: 90%
Method: Diminishing value
Rate: 40% (200% / 2.5)

FY2024-25: $4,500 × 40% × 90% = $1,620
FY2025-26: ($4,500 - $1,800) × 40% × 90% = $972
FY2026-27: ($2,700 - $1,080) × 40% × 90% = $583
```

---

## Common Expense Categories (Quick Reference)

### ✅ Fully Deductible (MOK HOUSE)

| Expense | Annual Cost | Evidence |
|---------|-------------|----------|
| **APRA membership** | $120 | Receipt |
| **Adobe Creative Cloud** | $780 | Tax invoice |
| **Splice subscription** | $120 | Tax invoice |
| **Domain/hosting** | $200 | Tax invoice |
| **Accountant fees** | $1,500 | Tax invoice |
| **Professional indemnity** | $800 | Policy + payment |

**Total**: ~$3,520/year

### ⚠️ Partially Deductible (Apportionment)

| Expense | Annual Cost | Business % | Deduction | Evidence |
|---------|-------------|------------|-----------|----------|
| **Tesla (logbook)** | $19,108 | 50% | $9,554 | 12-week logbook |
| **iPhone** | $1,200 | 70% | $840 | 4-week diary |
| **MacBook** (depreciation) | ~$1,620 | 90% | $1,458 | Asset register |
| **Home office** | $1,260 | 25%-100% | $1,260 | Floor plan + diary |
| **Internet** | $960 | 100% | $960 | Dedicated business |

**Total**: ~$14,072/year

### ❌ Never Deductible

| Expense | Annual Cost | Reason |
|---------|-------------|--------|
| **Anytime Fitness** | $780 | Personal wellbeing |
| **Regular meals** | ~$2,000 | Private sustenance |
| **Home → studio commute** | N/A | Regular workplace |
| **Haircuts** | $400 | Personal appearance |
| **Apple Music** | $120 | Personal entertainment |

**Total denied**: ~$3,300/year

---

## Validation Script

For automated validation, use Python script:

```bash
python scripts/validate_deduction.py \
  --entity "MOK HOUSE" \
  --expense "Serum plugin" \
  --amount 189 \
  --business-use 100
```

**Output**:
```
✅ DEDUCTION VALID

Entity: MOK HOUSE PTY LTD
Expense: Serum plugin
Amount: $189.00

Section 8-1 Test:
✅ Nexus: Strong (music production for clients)
✅ Capital: No (software <$1,000, immediate deduction)
✅ Private: No (100% business use)
✅ Not denied: No specific denial

Deductible amount: $189.00 (100%)
Evidence required: Tax invoice
Claim in: FY2025-26
```

---

## Integration with Graphiti & Serena

### Graphiti: Store Deduction Facts

**After validating deduction**:
```javascript
mcp__graphiti__add_memory({
  name: "Deduction: [Expense Name]",
  episode_body: "Expense '[Expense]' ($XXX) for [Entity] validated as [fully/partially/not] deductible. Nexus: [reason]. Business use: XX%. Evidence: [type]. Claim in FY2025-26.",
  source: "message",
  group_id: "harry-financial-entities"
})
```

### Serena: Store Validation Patterns

**After establishing pattern**:
```javascript
mcp__serena__write_memory({
  memory_name: "harry_deduction_validation_patterns",
  content: `
# Deduction Validation Patterns

## [Category] Expenses
- Entity: [Entity name]
- Typical deductibility: [Full/Partial/None]
- Business use %: XX%
- Evidence required: [Type]
- Notes: [Special considerations]
`
})
```

---

## Workflow Checklist

When validating a new expense:

- [ ] **Entity**: Which entity incurred expense?
- [ ] **Nexus**: Incurred in gaining/producing income?
- [ ] **Capital**: Revenue (immediate) or capital (depreciate)?
- [ ] **Private**: Business use % calculated?
- [ ] **Denial**: Any specific denial provisions?
- [ ] **Amount**: Deductible amount calculated?
- [ ] **Evidence**: Tax invoice/receipt obtained?
- [ ] **Logbook**: Required for vehicle >$4,250?
- [ ] **Diary**: Required for home office actual costs?
- [ ] **Asset register**: Updated if asset >$1,000?
- [ ] **Graphiti**: Deduction fact stored?
- [ ] **Serena**: Pattern stored (if new category)?

---

**Use this workflow for every deduction claim to ensure ATO compliance.**
**Always consult registered tax agent before claiming uncertain deductions.**
