# Add Business Transaction

This command allows you to manually add a business transaction to your financial database with proper categorization and business expense flagging.

## Usage

```bash
/add-business-transaction
```

## Interactive Process

When you run this command, I will prompt you for the following details:

### 1. Transaction Description
**Prompt**: "What is the description of this transaction?"
- **Example**: "Adobe Creative Cloud Subscription"
- **Purpose**: Clear identification of the expense

### 2. Amount
**Prompt**: "What is the transaction amount? (enter as positive number, I'll handle the sign)"
- **Example**: "52.99"
- **Format**: Positive number, I'll convert to negative for expenses
- **Currency**: Assumes AUD (Australian Dollars)

### 3. Transaction Date
**Prompt**: "What date did this transaction occur? (YYYY-MM-DD or 'today')"
- **Example**: "2025-01-15" or "today"
- **Default**: Today's date if not specified
- **Format**: ISO date format (YYYY-MM-DD)

### 4. Business Classification
**Prompt**: "Is this a business expense? (yes/no)"
- **Options**: yes, no, y, n
- **Impact**: Sets business flags and tax deductibility

### 5. Business Category (if business = yes)
**Prompt**: "What business category? (software, marketing, office, travel, equipment, other)"
- **Options**:
  - `software` - Software subscriptions and tools
  - `marketing` - Advertising and promotion
  - `office` - Office supplies and services
  - `travel` - Business travel expenses
  - `equipment` - Hardware and equipment
  - `other` - Other business expenses

### 6. Account Selection
**Prompt**: "Which account should this be added to?"
- **Shows**: List of your UpBank accounts
- **Default**: Primary transactional account
- **Format**: Account name or number

### 7. Additional Notes (optional)
**Prompt**: "Any additional notes for this transaction? (optional)"
- **Purpose**: Extra context for future reference
- **Examples**: "Annual subscription", "Conference expense", etc.

## Example Interaction

```
User: /add-business-transaction

Claude: I'll help you add a business transaction. Let me gather the details:

📝 What is the description of this transaction?
> Adobe Creative Cloud Subscription

💰 What is the transaction amount? (enter as positive number)
> 52.99

📅 What date did this transaction occur? (YYYY-MM-DD or 'today')
> today

💼 Is this a business expense? (yes/no)
> yes

🏷️ What business category? (software/marketing/office/travel/equipment/other)
> software

🏦 Which account should this be added to?
Available accounts:
1. Harry Spending Account
2. Harry Savings Account
> 1

📋 Any additional notes for this transaction? (optional)
> Monthly subscription for design work

✅ Transaction Summary:
• Description: Adobe Creative Cloud Subscription
• Amount: -$52.99 AUD
• Date: 2025-01-23
• Account: Harry Spending Account
• Business: Yes (Software & Tools)
• Tax Deductible: Yes
• Notes: Monthly subscription for design work

Confirm and add this transaction? (yes/no)
```

## What Happens Next

After confirmation, I will:

1. **Insert the transaction** into your Supabase `personal_transactions` table
2. **Set business flags** appropriately:
   - `is_business_related: true/false`
   - `is_tax_deductible: true/false`
   - `business_category: [selected category]`
   - `personal_category: [mapped category]`
3. **Generate a unique ID** for tracking
4. **Confirm successful addition** with transaction details
5. **Suggest related actions** (add keyword, review similar transactions)

## Business Category Mapping

| Input | Business Category | Personal Category | Tax Deductible |
|-------|------------------|-------------------|----------------|
| software | Software & Tools | Business Subscription | Yes |
| marketing | Marketing & Advertising | Business Marketing | Yes |
| office | Office & Administration | Business Office | Yes |
| travel | Travel & Transport | Business Travel | Yes |
| equipment | Equipment & Hardware | Business Equipment | Yes |
| other | Other Business | Business Other | Yes |

## Validation & Safety

- **Amount validation**: Ensures positive numbers, converts to cents
- **Date validation**: Checks date format and reasonableness
- **Account verification**: Confirms account exists in your system
- **Duplicate detection**: Warns if similar transaction exists
- **Category consistency**: Maps business categories to standard classifications

## Error Handling

If something goes wrong:
- **Database errors**: Clear error message with suggested fixes
- **Invalid input**: Re-prompts for correct format
- **Missing accounts**: Helps set up account mapping
- **Network issues**: Suggests retry with saved details

## Related Commands

- `/show-business-keywords` - View business expense detection rules
- `/add-business-keyword` - Add automatic detection for similar transactions
- `/sync-upbank` - Sync recent UpBank transactions
- `/show-transactions` - View recent transactions

## Use Cases

- **Manual expense entry**: When UpBank sync misses a transaction
- **Cash transactions**: Business expenses paid in cash
- **Credit card expenses**: Before they appear in UpBank
- **Estimated transactions**: Planned expenses for budgeting
- **Correction entries**: Fix miscategorized transactions

## Tips

- **Be specific** in descriptions for better tracking
- **Use consistent naming** for similar expenses
- **Add keywords** after entry if it's a recurring expense
- **Review monthly** to ensure all business expenses are captured
- **Keep receipts** and reference them in notes
