# Remove Business Expense Keyword

This command removes keywords from the business expense detection system to prevent false positives.

## Usage

```bash
/remove-business-keyword [keyword1] [keyword2] [keyword3]...
```

## What this command does

1. **Read current keywords** from the sync script
2. **Remove specified keywords** from the business expense detection list
3. **Update the sync script** with the reduced keyword list
4. **Show confirmation** of keywords removed
5. **Check recent transactions** that might be affected (optional)

## Arguments

- `keyword1`, `keyword2`, etc. - Business expense keywords to remove

## Process

When you run this command, I will:

1. **Extract current keywords** from the enhanced sync script
2. **Remove specified keywords** from the `businessExpenseKeywords` array
3. **Update the script** with the reduced keyword list
4. **Show confirmation** of what was removed
5. **Identify recent transactions** that were categorized by the removed keywords

## Example

```bash
/remove-business-keyword apple youtube
```

This would remove "apple" and "youtube" from business expense detection if they're causing false positives.

## Safety Features

- **Confirmation**: Shows exactly which keywords will be removed
- **Impact analysis**: Identifies transactions that might be affected
- **Backup preservation**: Original keywords remain in code comments
- **Validation**: Warns if removing keywords that don't exist

## When to Remove Keywords

- **False positives**: Keyword matches personal expenses (e.g., "apple" matching fruit purchases)
- **Too broad**: Keyword is too generic and matches unrelated transactions
- **No longer relevant**: Service is no longer used for business
- **Duplicate detection**: Multiple keywords detecting the same transactions

## Related Commands

- `/add-business-keyword` - Add new keywords for detection
- `/show-business-keywords` - View current keyword list
- `/test-business-keywords` - Test keywords against recent transactions
