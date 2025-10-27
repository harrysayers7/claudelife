---
date: "2025-10-22 14:30"
type: meeting-preparation
entity: MOKAI PTY LTD
meeting-date: "2025-10-24"
date created: Wed, 10 22nd 25, 4:23:55 pm
date modified: Thu, 10 23rd 25, 8:21:48 am
---

🧾 Accountant Meeting Preparation - MOKAI Setup

Meeting Date: Friday, October 24, 2025
Topic: MOKAI ABN/ACN setup, shareholders agreement, constitution
Attendee: Harrison Sayers
Goal: Maximize DIY work to reduce accountant costs

---

📋 Main Question: "How much work can I do myself?"

✅ What You CAN Do (Saves Accountant Time = Saves )



**1. Bank Statement Reconciliation**
- Export all bank transactions as CSV/Excel
- Categorize expenses (business vs personal)
- Match transactions to invoices/receipts
- Flag any unclear transactions
- **Your Status**: UpBank data already in `personal_transactions` table (~256 transactions categorized)

**2. Invoice Management**
- Organize all invoices sent (receivables)
- Organize all invoices received (payables)
- Mark paid vs outstanding
- Calculate totals per entity
- **Your Status**: Supabase `invoices` table already tracking this

**3. Receipt Collection & Categorization**
- Digital copies of all receipts
- Categorized by expense type
- Labeled with entity (MOKAI/MOK HOUSE/Sole Trader)
- Business use percentage noted (e.g., Tesla 50%)

**4. Transaction Tagging**
- Mark business vs personal expenses
- Flag tax-deductible items
- Note GST-inclusive amounts
- **Your Status**: ML categorization already doing this

**5. Asset Register**
- List all business assets (Tesla, instruments, equipment)
- Purchase dates and costs
- Current values (estimates okay)
- Business use percentages
- **Your Status**: ❌ MISSING - need to create this week

**6. Income Documentation**
- APRA royalty statements (SAFIA + solo)
- SAFIA live performance contracts/invoices
- MOK HOUSE client invoices
- Wife's payslips (for family trust distribution planning)

**7. Document Preparation**
- Draft shareholders agreement (you draft, accountant reviews)
- Company constitution (template + customizations)
- Trust deed notes (beneficiary preferences, distribution strategy)
- **Your Status**: ✅ SHA drafts exist in `/01-areas/business/mokai/docs/contracts/`

---

### ❌ What You CANNOT Do (Requires Qualified Accountant)

**1. Lodgement & Compliance**
- BAS statements (only registered BAS agents)
- Tax returns (only registered tax agents)
- ASIC annual reviews (accountant or company officer)
- Payroll tax calculations (specialist required)

**2. Complex Tax Planning**
- Trust distribution tax strategies
- Division 7A compliance (loans from company)
- Franking credit optimization
- Tax loss carry-forward strategies

**3. Financial Statements**
- Balance sheet preparation (requires accounting qualifications)
- Profit & Loss statements (requires GAAP compliance)
- Cash flow statements (formal accounting standards)
- Depreciation schedules (tax depreciation rules complex)

**4. Statutory Requirements**
- ASIC company registration
- ABN/TFN applications (can do yourself, but accountant faster)
- Supply Nation registration (Indigenous certification process)

---

## 💰 Cost Reduction Reality Check

### "Do accountants charge more by pretending you can't do anything?"

**Short answer**: Some do, but good ones don't.

**Reality**:
- **Value-based accountants**: Welcome DIY prep work, charge for strategic advice
- **Hourly rate accountants**: May prefer you NOT to prep (more billable hours)
- **Fixed-fee accountants**: Prefer tidy prep work (makes their job easier, maintains fixed price)

### 🚨 Red Flags (Accountant Might Be Over-Charging)
- ❌ Discourages you from organizing receipts ("we'll do it all")
- ❌ Doesn't provide cost breakdown (vague invoices)
- ❌ Charges data entry rates (should be admin, not accountant time)
- ❌ Won't explain tax strategies in plain English

### ✅ Green Flags (Accountant Values Your Prep Work)
- ✅ Provides checklist of what you can pre-organize
- ✅ Explains which tasks save them time (explicit cost breakdown)
- ✅ Charges different rates: admin/bookkeeping vs tax planning/strategy
- ✅ Offers training on DIY bookkeeping (cloud accounting software)

---

## 🎯 Priority Questions for Friday's Meeting

### 1. Work Allocation & Cost Structure

**Questions to Ask**:

> "I've already reconciled my bank statements and categorized transactions in my system. Can you review my categorization instead of re-doing it? What format works best for you (CSV/Excel/accounting software export)?"

> "What's your hourly rate for data entry vs strategic tax advice? I want to do the data entry myself to save costs."

> "Can you provide a checklist of documents/data I should prepare before our next meeting to minimize your billable hours?"

> "Do you charge differently for bookkeeping vs tax planning? I'm happy to handle routine data entry if that reduces my bill."

**Expected Good Answer**:
- "Yes, send me your categorized transactions, I'll review for tax compliance. My data entry rate is $X, tax advice is $Y."

**Expected Bad Answer**:
- "No, we prefer to do everything ourselves to ensure accuracy." (Translation: We want billable hours)

---

### 2. MOKAI Entity Structure & Setup

**Questions to Ask**:

> "For MOKAI's ABN/ACN registration, what's the fastest path? Can I register the ABN myself and have you review, or should you handle it?"

<mark style="background: #FF5582A6;">> "Should MOKAI register for GST immediately (planning government contracts >$75K), or wait until first contract signed?"
</mark>

> "What insurance and compliance requirements trigger immediately vs 'can wait until first contract'? (PI insurance, cyber insurance, workers comp, etc.)"

**Why These Matter**:
- ABN registration: Free DIY vs $200-500 via accountant (5 mins of work)
- GST registration: Timing affects invoicing, pricing strategy
- Legal docs: Template + review vs full drafting = $500 vs $3,000+
- Contractor structure: Affects tax treatment, invoice tracking

---

### 3. MOK HOUSE → HS Family Trust Transfer

**Questions to Ask**:

> "What's the tax implication of transferring MOK HOUSE ownership from me to the HS Family Trust? CGT event? Stamp duty?"

> "Can we do a 'rollover relief' transfer to avoid triggering CGT?"

> "What's the process and timeline? Do we need a business valuation?"

> "After transfer, can I still be paid a salary from MOK HOUSE, or only trust distributions?"

**Context**: MOK HOUSE currently has minimal value (no significant assets), so transfer while value is low = minimal CGT risk.

---

### 4. Salary vs Dividend Strategy (MOK HOUSE)

**Questions to Ask**:

> "I'm targeting <$45K personal income to stay in 19% tax bracket. Should MOK HOUSE pay me a minimal salary ($20K-30K) + dividends, or just dividends via the trust?"

> "What's the Superannuation Guarantee obligation if I take a salary? Does that push me over $45K threshold?"

> "Can the trust receive franked dividends from MOK HOUSE and pass franking credits to beneficiaries?"

> "Division 7A rules - if the trust owns MOK HOUSE and I draw money, is that a 'loan' triggering Div 7A, or a distribution?"

**Why This Matters**:
- Salary = 12% super on top (reduces take-home, but builds retirement savings)
- Dividends = 25% company tax, but can be franked (tax credits)
- Trust distributions = flexibility to split income with wife

---

### 5. APRA Royalties & SAFIA Income Tax Treatment

**Questions to Ask**:

> "APRA royalties (SAFIA + solo) are irregular. Should I calculate tax on a monthly average, or pay as I earn (PAYG installments)?"

> "SAFIA Unit Trust distributes royalties to members. Is that already taxed at trust level, or do I pay tax when I receive distributions?"

> "SAFIA live shows pay $50K-$80K per event. Should I set aside 30% for tax immediately, or are there deductions that reduce the taxable amount?"

> "Can I claim music production expenses (studio time, equipment, software) against APRA royalties, even if the income is from old songs?"

**Context**: Irregular income needs smart tax planning to avoid big PAYG debt at tax time.

---

### 6. Asset Deductions (Tesla, Home Office, Instruments)

**Questions to Ask**:

> "Tesla Model 3: I've been using cents/km method (5,000km × $0.85). Should I switch to logbook method? What's the potential deduction increase?"

> "Tesla has a $41,676 balloon payment due Dec 2026. Can I refinance that through the business and deduct interest?"

> "Home office: I work from a dedicated room 50%+ of the time. Should I use the $0.67/hour fixed rate or actual costs method (electricity, internet, etc.)? What's the deduction difference?"

> "Musical instruments: I have multiple guitars, synths, etc. purchased over 5+ years. Can I claim depreciation even without original receipts? What proof do I need?"

**Expected Savings**:
- Tesla logbook method: ~$9K/year extra deductions vs cents/km
- Home office actual costs: ~$1,500/year vs fixed rate
- Instruments depreciation: ~$1K-$2K/year (if you can prove purchase costs)

---

### 7. UpBank Data & Cloud Accounting Integration

**Questions to Ask**:

> "I've synced my UpBank transactions to a database and categorized them (business vs personal, tax-deductible flags). Can you work with this data, or do you need me to use Xero/MYOB/QuickBooks?"

> "What's the cost difference if I continue my own system vs subscribing to cloud accounting software?"

> "Can I send you monthly CSV exports, or do you need live access to accounting software?"

> "If I switch to Xero/MYOB, can you train me on basic data entry so I only pay you for reviews and tax planning?"

**Why This Matters**:
- Cloud accounting software: $30-70/month + setup/training costs
- Your current system: Free, but accountant may charge extra to process
- Hybrid approach: DIY data entry in cloud software, accountant reviews monthly

---

### 8. GST Threshold Monitoring & Compliance

**Questions to Ask**:

> "MOK HOUSE is at ~$6,500 turnover (8.7% of $75K threshold). Should I register for GST now voluntarily, or wait until I'm certain I'll exceed $75K this financial year?"

> "If I register mid-year, how do I handle invoices already sent without GST?"

> "What's the BAS lodgement frequency (monthly/quarterly)? Can I do BAS myself using ATO's portal, or must I use a registered BAS agent?"

> "Sole trader (ABN 89 184 087 850) - separate GST threshold tracking? Or does ATO combine all my business activities?"

**Context**: Voluntary GST registration can be strategic (claim input tax credits on Tesla, equipment), but adds compliance burden.

---

### 9. Indigenous Business Compliance (MOKAI)

**Questions to Ask**:

> "MOKAI is Supply Nation registered. Are there specific accounting/reporting requirements for Indigenous businesses beyond standard company compliance?"

> "Government contracts often require Indigenous participation %. Do I need to track 'Indigenous business spend' separately for reporting?"

> "Can MOKAI claim R&D tax incentives or Indigenous business grants? What records do I need to keep?"

---

### 10. Quarterly vs Annual Tax Planning

**Questions to Ask**:

> "Should we meet quarterly to review tax position, or just at end of financial year?"

> "If we meet quarterly, what reports do you need from me? Can you provide a template?"

> "PAYG installments - should I pay quarterly estimates to avoid big tax bill in July? How do we calculate the right amount?"

> "Can you provide a 'tax calendar' with key deadlines (BAS, PAYG, super guarantee, tax return)?"

**Expected Outcome**:
- Quarterly reviews: Catch tax issues early, smooth cash flow, better planning
- Annual only: Cheaper, but risk of surprises (unexpected tax bill, GST errors)

---

## 📊 Data to Bring to Meeting

### Documents Already Prepared (Show Accountant)

1. ✅ **Shareholders Agreement Drafts**
   - Location: `/01-areas/business/mokai/docs/contracts/`
   - Files: `MOKAI-SHA-V3.md`, `BOARD_RESOLUTION v2.md`

2. ✅ **UpBank Transaction Data**
   - Supabase table: `personal_transactions` (~256 transactions)
   - Categorized: Business vs personal, tax-deductible flags
   - Export as CSV for accountant review

3. ✅ **Invoice Tracking**
   - Supabase table: `invoices`
   - MOK HOUSE receivables status

4. ✅ **GST Threshold Monitoring**
   - Supabase table: `gst_threshold_monitoring`
   - Current turnover tracking per entity

---

### Documents to Create BEFORE Friday

#### 1. ❌ Asset Register (MUST CREATE THIS WEEK)

**Template**:
```markdown
# Asset Register - All Entities

## Tesla Model 3
- Purchase Date: December 2021
- Purchase Price: $104,365.50
- Loan: $90,254 @ 4.23%, 5-year term
- Balloon Payment: $41,676.82 due Dec 14, 2026
- Monthly Payment: $1,277 ($1,068 loan + $209 insurance)
- Business Use: 50% (estimate - needs logbook)
- Current Odometer: [check car]
- Business km this FY: [estimate]

## Musical Instruments
### Guitar 1: [Model/Brand]
- Purchase Date: [estimate if no receipt]
- Purchase Cost: $[estimate]
- Current Value: $[estimate]
- Business Use: 100% (APRA income)

### Synth 1: [Model/Brand]
- Purchase Date: [estimate]
- Purchase Cost: $[estimate]
- Current Value: $[estimate]
- Business Use: 100%

[Repeat for all instruments]

## Home Office Equipment
- Desk: [details]
- Chair: [details]
- Computer/Laptop: [details]
- Audio Interface: [details]
- Monitors/Speakers: [details]
```

**Action**: Create this file at `/01-areas/business/assets/asset-register-2025.md`

---

#### 2. ❌ Income Summary (FY2024-25 to date)

**Template**:
```markdown
# Income Summary - FY2024-25 (Jul 2024 to Oct 2025)

## APRA Royalties (SAFIA + Solo)
| Month | Amount | Source |
|-------|--------|--------|
| Jul 2024 | $X | SAFIA/Solo |
| Aug 2024 | $X | SAFIA/Solo |
| Sep 2024 | $X | SAFIA/Solo |
| Oct 2024 | $X | SAFIA/Solo |
| Nov 2024 | $X | SAFIA/Solo |
| Dec 2024 | $X | SAFIA/Solo |
| Jan 2025 | $X | SAFIA/Solo |
| Feb 2025 | $X | SAFIA/Solo |
| Mar 2025 | $X | SAFIA/Solo |
| Apr 2025 | $X | SAFIA/Solo |
| May 2025 | $X | SAFIA/Solo |
| Jun 2025 | $X | SAFIA/Solo |
| Jul 2025 | $X | SAFIA/Solo |
| Aug 2025 | $X | SAFIA/Solo |
| Sep 2025 | $X | SAFIA/Solo |
| Oct 2025 | $X | SAFIA/Solo |
| **Total** | **$X** | |

## SAFIA Live Shows
| Date | Venue | Amount | Paid? |
|------|-------|--------|-------|
| [Date] | [Venue] | $X | Yes/No |
| **Total** | | **$X** | |

## MOK HOUSE Client Work
| Client | Invoice # | Amount | Date | Paid? |
|--------|-----------|--------|------|-------|
| Client 1 | INV-001 | $X | [Date] | Yes/No |
| Client 2 | INV-002 | $X | [Date] | Yes/No |
| **Total** | | **$X** | | |

## Wife's Employment Income
- Monthly: ~$4,000
- Annual estimate: ~$48,000
- Employer: [Name]
```

**Action**: Query Supabase or check bank statements to fill this out

---

#### 3. ❌ Expense Summary by Category

**Template**:
```markdown
# Business Expenses - FY2024-25 to date

## Transport (Tesla)
- Loan repayments: $1,068/month × [16 months] = $[total]
- Insurance: $2,508/year = $[prorated]
- Charging/fuel: ~$300/year (estimate)
- **Total**: $[sum]
- **Business use**: 50% = **$[deductible]**

## Home Office
- Electricity: $[quarterly bill] × 4 quarters × 25% = $[total]
- Gas: $[quarterly bill] × 4 quarters × 25% = $[total]
- Internet: $[monthly bill] × 16 months × 100% = $[total]
- **Total deductible**: **$[sum]**

## Professional Services
- The Practice Pty: $[amount] (query if deductible)
- [Other services]: $[amount]
- **Total**: $[sum]

## Software & Subscriptions
- YouTube Premium: $[amount]/year (query if deductible)
- Apple iCloud: $[amount]/year (business use)
- [Other subscriptions]: $[amount]
- **Total**: $[sum]

## Equipment & Instruments
- [List any purchases this FY]
- **Total**: $[sum]
```

**Action**: Export from UpBank or query `personal_transactions` table

---

## 💡 Cost Optimization Strategy

### Immediate Actions (Before Friday)

- [x] Create Asset Register (save ~2 hours = $300-600)
- [x] Export UpBank transactions as CSV (save ~1 hour = $150-300)
- [x] Summarize APRA income by month (save ~1 hour = $150-300)
- [x] List outstanding MOK HOUSE invoices (already in Supabase)
- [x] Print this questions document

**Estimated savings**: $600-$1,200 in accountant data entry fees

---

### Medium-Term (Before Tax Time FY2024-25)

1. **Start Tesla logbook** (12 weeks required)
   - App: ATO myDeductions or third-party logbook app
   - Benefit: ~$9K/year extra deductions vs cents/km

2. **Calculate home office actual costs**
   - Electricity bill × 25% business use
   - Gas bill × 25% business use
   - Internet bill × 100% business use
   - Benefit: ~$1,500/year extra deductions vs fixed rate

3. **Inventory musical instruments**
   - Photos + descriptions
   - Purchase dates (best estimate)
   - Current market value (eBay/Reverb research)
   - Benefit: ~$1K-$2K/year depreciation deductions

---

### Long-Term (FY2025-26 Planning)

1. MOK HOUSE → Trust transfer (while value is low)
2. MOKAI entity setup (ABN, ACN, GST, company structure)
3. Quarterly tax reviews (catch issues early)
4. Cloud accounting software (if accountant recommends)

---

## 📝 Meeting Notes Template

Use this during Friday's meeting:

```markdown
# Accountant Meeting Notes - 2025-10-24

**Attendees**: Harry Sayers, [Accountant Name]
**Firm**: [Name]
**Duration**: [time]

## Key Decisions

### Cost Structure
- Data entry rate: $[X]/hour
- Tax advice rate: $[Y]/hour
- BAS preparation: $[Z]/quarter
- Annual fee (if applicable): $[total]

### DIY Work Approved
- [ ] Can provide CSV exports of categorized transactions
- [ ] Can create asset register myself
- [ ] Can reconcile bank statements
- [ ] Format preferred: [CSV/Excel/Xero/MYOB]

### MOKAI Setup
- ABN/ACN registration: [Accountant handling / DIY approved]
- GST registration: [Immediate / Wait for first contract]
- Shareholders agreement: [Template + review $X / Full drafting $Y]
- Timeline: [details]

### MOK HOUSE → Trust Transfer
- CGT implications: [details]
- Rollover relief available: [Yes/No]
- Timeline: [when to proceed]
- Business valuation needed: [Yes/No, Cost: $X]

### Tax Strategy
- Harry salary target: $[amount] (stay under $45K)
- Superannuation: [details]
- Trust distributions: [strategy]
- Dividend strategy: [franked/unfranked]

### Asset Deductions
- Tesla: [Logbook method approved / Start date: [date]]
- Home office: [Actual costs method / Fixed rate]
- Musical instruments: [Depreciation strategy]

### Meeting Frequency
- [ ] Quarterly reviews ($[X]/quarter)
- [ ] Annual only ($[Y]/year)
- Next meeting: [date]

## Action Items

### Harry's Tasks
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

### Accountant's Tasks
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

## Questions to Follow Up
- [Question 1]
- [Question 2]

## Red/Green Flags Observed
- [Note any red or green flags from the meeting]
```

---

## 🎯 Post-Meeting Actions

After Friday, update your knowledge systems:

1. **Save meeting notes** to `/01-areas/business/mokai/docs/accountant-meeting-notes-2025-10-24.md`

2. **Update Memory MCP** with key decisions:
```javascript
mcp__memory__add_observations({
  observations: [
    {
      entityName: "Accountant Partnership",
      contents: [
        "Accountant: [name], Firm: [firm]",
        "Data entry rate: $X/hour, Tax advice: $Y/hour",
        "DIY work approved: [details]",
        "MOKAI setup timeline: [details]",
        "Next meeting: [date]"
      ]
    }
  ]
})
```

3. **Create tasks** for any action items assigned to you

---

## 🧠 Final Advice

**Trust your instincts**. A good accountant:
- ✅ Makes you feel informed and empowered
- ✅ Explains tax concepts clearly
- ✅ Encourages DIY work to save you money
- ✅ Provides transparent pricing
- ✅ Proactively suggests optimizations

A bad accountant:
- ❌ Makes you feel dumb for asking questions
- ❌ Uses jargon without explanation
- ❌ Discourages DIY work (wants billable hours)
- ❌ Vague about costs
- ❌ Reactive only (no proactive advice)

**You're paying for expertise**, not just data entry. If this accountant doesn't feel like a good fit after Friday, get quotes from 2-3 others before committing.

---

**Good luck! 🍀**
