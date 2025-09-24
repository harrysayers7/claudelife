# Show Business Transactions

This command displays recent business transactions with filtering and analysis options.

## Usage

```bash
/show-business-transactions [days] [--category=type] [--uncategorized] [--summary]
```

## Parameters

- `days` - Number of days to look back (default: 30)
- `--category=type` - Filter by business category (software, marketing, office, travel, equipment)
- `--uncategorized` - Show only uncategorized business transactions
- `--summary` - Show summary statistics only

## Examples

```bash
/show-business-transactions                    # Last 30 days, all business transactions
/show-business-transactions 7                 # Last 7 days
/show-business-transactions --category=software # Software expenses only
/show-business-transactions --uncategorized    # Business transactions needing categorization
/show-business-transactions --summary          # Summary stats only
```

## Output Format

### Standard View
```
💼 Business Transactions (Last 30 days)

📅 2025-01-23
  💻 Software & Tools: $52.99
    • Adobe Creative Cloud Subscription
    • Method: Manual entry | Tax Deductible: Yes

📅 2025-01-22
  🤖 AI & Development: $20.00
    • OpenAI API Credits
    • Method: Auto-detected (keyword: openai) | Tax Deductible: Yes

  📱 Software & Tools: $4.99
    • Notion Pro Subscription
    • Method: Auto-detected (keyword: notion) | Tax Deductible: Yes

📅 2025-01-21
  ❓ Uncategorized: $127.50
    • STRIPE PAYMENT - DESIGN TOOLS
    • Method: Manual review needed | Tax Deductible: Unknown
    • 💡 Suggestion: Add 'stripe' or 'design' keyword for auto-detection
```

### Summary View (--summary)
```
📊 Business Expense Summary (Last 30 days)

💰 Total Business Expenses: $1,247.83
🧾 Total Transactions: 23
📈 Tax Deductible Amount: $1,189.33

📋 By Category:
  • Software & Tools: $687.45 (14 transactions)
  • Marketing & Advertising: $320.50 (4 transactions)
  • Office & Administration: $142.38 (3 transactions)
  • Travel & Transport: $97.50 (2 transactions)

🤖 Detection Methods:
  • Auto-detected: 18 transactions ($956.83)
  • Manual entry: 3 transactions ($152.50)
  • Needs review: 2 transactions ($138.50)

📈 Trends:
  • Average per transaction: $54.25
  • Most expensive: Adobe Annual License ($299.99)
  • Most frequent: Notion Pro ($4.99 × 12 times)
```

## Interactive Features

When showing transactions, I can:

### 1. Quick Actions
For each transaction, offer:
- **Categorize** - Update business category
- **Add keyword** - Add automatic detection
- **Flag review** - Mark for tax review
- **Add notes** - Add additional context

### 2. Bulk Operations
- **Categorize similar** - Apply category to similar transactions
- **Export for tax** - Generate tax-ready export
- **Mark reviewed** - Bulk mark as reviewed

### 3. Analysis
- **Spending patterns** - Identify trends
- **Keyword suggestions** - Suggest new keywords based on descriptions
- **Missing categorization** - Highlight gaps

## Process

When you run this command, I will:

1. **Query Supabase** for business transactions in the specified period
2. **Group by date** and category for easy reading
3. **Show detection method** (auto vs manual)
4. **Highlight issues** (uncategorized, duplicate detection methods)
5. **Provide quick actions** for each transaction
6. **Calculate totals** and show summary statistics

## Filters Explained

### `--category=software`
Shows only transactions categorized as business software expenses

### `--uncategorized`
Shows business transactions that need manual categorization:
- `is_business_related: true` but no `business_category`
- `ai_confidence` below auto-categorization threshold
- Manual review flagged

### `--summary`
Condensed view with totals, averages, and trends without individual transaction details

## Related Commands

- `/add-business-transaction` - Manually add a business expense
- `/add-business-keyword` - Add keywords for auto-detection
- `/categorize-transaction [id]` - Update specific transaction category
- `/export-business-expenses` - Export for tax/accounting software

## Use Cases

- **Monthly review** - Check all business expenses before month-end
- **Tax preparation** - Review deductible expenses
- **Budget tracking** - Monitor spending by category
- **Audit preparation** - Ensure proper categorization
- **Keyword optimization** - Identify patterns for auto-detection

## Tips

- **Review uncategorized** regularly to improve auto-detection
- **Check for duplicates** if you mix manual entry with UpBank sync
- **Use category filters** to focus on specific expense types
- **Export summaries** for accounting software import
- **Add keywords** for recurring transactions you manually enter
