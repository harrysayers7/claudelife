---
date: "2025-10-25 14:30"
---

# Invoice Template Comparison: Your Design vs Production

## Quick Comparison

| Aspect | Your Design (Google Docs) | Current Production Template | Match? |
|--------|--------------------------|---------------------------|--------|
| **Company Name** | `MOK HOUSE` (92px) | `MOK HOUSE` (48px) | ⚠️ Size differs |
| **ABN Display** | `[ABN]: 38 690 628 212` | Not in header | ❌ Location differs |
| **Invoice Title** | `[INVOICE] MH-001` | `INVOICE` (separate) | ⚠️ Format differs |
| **Meta Info** | `[PO]` `[DATE]` (right-aligned) | 4-column grid | ⚠️ Layout differs |
| **Line Items** | Bracketed headers `[DESCRIPTION] [QTY]` | Regular table headers | ❌ Styling differs |
| **Payment Section** | `[PAYMENT]` heading | `PAYMENT DETAILS` heading | ⚠️ Formatting differs |
| **Brackets** | Heavy use of brackets `[ ]` | Minimal/none | ❌ Style differs |
| **Font** | Arial (from Google Docs export) | Arial | ✅ Matches |
| **Layout** | Centered, spacious | Centered, grid-based | ✅ Similar |
| **Colors** | Black & gray (#999) | Black & gray (#999) | ✅ Matches |

---

## Detailed Differences

### 1. Header Section

#### Your Design
```html
MOK HOUSE (92px, bold)
[ABN]: 38 690 628 212 (13px, gray)

[INVOICE] MH-001 (33px + 23px)

[PO] 0404          [DATE] DD-MM-YYYY (right-aligned)
```

#### Current Production
```html
MOK HOUSE (48px, bold, centered)
INVOICE (32px, bold, centered)

Date: 25-10-2025          Invoice Number: #MH-001
Due Date: 01-11-2025      PO Number: 0404
(4-column grid layout)
```

**Difference**: Your design places ABN in header; production template doesn't.
**Difference**: Your design uses brackets heavily for labels; production uses plain text.

---

### 2. Company Name Font Size

Your Design:
- **92px** - Very large, bold, prominent
- Uses maximum visual hierarchy

Production Template:
- **48px** - Large but proportional
- Still prominent but leaves room for other elements

**Impact**: Your design makes company name much larger. For MOK HOUSE branding, this might be preferred.

---

### 3. Invoice Number Display

Your Design:
```html
[INVOICE] MH-001
(Brackets around word, invoice # after)
```

Production:
```html
INVOICE
Invoice Number: #MH-001
```

**Difference**: Your design puts both on same line with brackets.
**Production separates them with labels in 4-column meta row.

---

### 4. Metadata Layout

Your Design (Right-aligned):
```
                                [PO] 0404
                        [DATE] DD-MM-YYYY
```

Production (4-column grid):
```
Date          Invoice Number     Due Date       PO Number
25-10-2025    #MH-001           01-11-2025      0404
```

**Impact**: Production template shows all info clearly in structured layout.
**Your design emphasizes PO and Date only, right-aligned.

---

### 5. Line Items Headers

Your Design:
```
[DESCRIPTION]          [QTY]     [UNIT PRICE]     [TOTAL]
(Bracketed labels, uppercase)
```

Production:
```
Description      Qty      Unit Price      Tax %      Total
(Regular headers, light gray background)
```

**Difference**: Your design uses brackets; production uses plain text headers with background color.

---

### 6. Line Items Data

Your Design:
```
REPCO                    1        $2000           $2000
(Gray text, single entry)
```

Production:
```
REPCO - Bathurst 500 Campaign    1    $2000.00    10%    $2000.00
Additional Creative Services     2    $500.00     10%    $1000.00
(Multiple entries, formatted with currencies)
```

**Difference**: Your design shows minimal; production shows full descriptions and tax rate column.

---

### 7. Totals Section

Your Design:
```
[TOTAL]
$3,300.00 (large, bold, right-aligned)
```

Production:
```
Subtotal:     $3,000.00
GST (10%):    $300.00
Total:        $3,300.00
(Detailed breakdown, right-aligned, border)
```

**Difference**: Your design shows just total; production shows breakdown.

---

### 8. Payment Section

Your Design:
```html
[PAYMENT]
Account Name: MOK HOUSE PTY LTD
BSB: 013-943
Account Number: 612281562
```

Production:
```html
PAYMENT DETAILS
Bank Transfer
  Account: MOK HOUSE PTY LTD
  BSB: 013-943
  Account Number: 612281562
Payment Terms
  Due within 7 days of invoice date
```

**Difference**: Your design is simpler; production includes payment terms section.

---

### 9. Contact Section

Your Design:
```
For any questions please contact me at:
hello@mokhouse.com.au
```

Production:
```
CONTACT INFORMATION
Mok House
  Email: hello@mokhouse.com.au
  ABN: 38 690 628 212
```

**Difference**: Production template is more formal with structure; your design is conversational.

---

## Feature Matrix

| Feature | Your Design | Production | Notes |
|---------|------------|-----------|-------|
| Bracket styling | ✅ Yes | ❌ No | You prefer brackets for labels |
| Large company name | ✅ 92px | ⚠️ 48px | Larger in your design |
| ABN in header | ✅ Yes | ❌ No | Your design shows it prominently |
| Metadata grid layout | ❌ No | ✅ Yes | Production is more structured |
| Line item details | ⚠️ Minimal | ✅ Full | Production shows tax rate |
| Totals breakdown | ❌ No | ✅ Yes | Production shows GST separately |
| Payment terms | ❌ No | ✅ Yes | Production includes payment terms |
| Formal structure | ⚠️ Semi | ✅ Full | Production is more professional |
| Simple/minimal | ✅ Yes | ❌ No | Your design is cleaner |

---

## Recommendations

### If You Prefer the Bracket Style (Your Design)
I can update the production template to:
1. **Increase company name to 92px** (from 48px)
2. **Add brackets** around labels: `[INVOICE]`, `[PAYMENT]`, `[DESCRIPTION]`
3. **Move ABN to header** (below company name)
4. **Simplify metadata layout** (right-align PO and DATE only)
5. **Remove payment terms section** (keep simple)
6. **Simplify contact section** (more conversational)

### If You Prefer the Current Production Template
It offers:
- ✅ Professional, structured layout
- ✅ Complete financial details (tax breakdown)
- ✅ Clear payment terms
- ✅ Proper business formatting
- ✅ Better for complex multi-item invoices

---

## Implementation Path

### Option 1: Update to Match Your Design
```bash
# Update /src/invoicing/templates/invoice.html to:
- Increase heading sizes
- Add bracket styling via CSS
- Reorganize header with ABN
- Simplify layout
```

### Option 2: Keep Current Production Template
```bash
# Use as-is:
- Professional structure
- All financial details
- Proper invoice format
- Ready for PDF generation
```

### Option 3: Hybrid Approach (Recommended)
```bash
# Combine best of both:
- Use bracket styling for readability
- Keep structured metadata grid
- Keep totals breakdown
- Keep payment terms
- Keep formal structure
```

---

## What Should We Do?

**Current Status**: Production template is functional and tested ✅

**Your Design Intent**: Cleaner, bracket-focused, simpler layout

**Recommendation**:

I suggest keeping the production template as-is for now because:
1. ✅ It's fully tested and working
2. ✅ It's more complete (includes tax, payment terms)
3. ✅ It's professional and business-ready
4. ✅ It handles complex invoices better

**Future Option**:
Once the system is live and working, you can create a variant with bracket styling using CSS:
- Add brackets via CSS `::before` and `::after` pseudo-elements
- Maintain all professional structure underneath
- No need to rebuild from scratch

Would you like me to:
1. ✅ Keep current production template as-is (recommended)
2. ❌ Update to match your bracket design
3. ⚙️ Create a CSS variant with brackets

---

**Comparison Generated**: 2025-10-25 14:30
