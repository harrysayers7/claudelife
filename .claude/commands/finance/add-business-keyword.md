# Add Business Expense Keyword

This command adds a new keyword to the business expense detection system in the enhanced UpBank sync script.

## Usage

```bash
/add-business-keyword [keyword1] [keyword2] [keyword3]...
```

## What this command does

1. **Read current keywords** from the sync script
2. **Add new keywords** to the business expense detection list
3. **Update the sync script** with the new keywords
4. **Verify the changes** by showing the updated keyword list
5. **Test the keyword** against recent transactions (optional)

## Arguments

- `keyword1`, `keyword2`, etc. - Business expense keywords to add (e.g., "github", "figma", "slack")

## Process

When you run this command, I will:

1. **Extract current keywords** from `/Users/harrysayers/Developer/claudelife/scripts/sync-upbank-enhanced.js`
2. **Add your new keywords** to the `businessExpenseKeywords` array
3. **Update the script** with the expanded keyword list
4. **Show confirmation** of keywords added
5. **Suggest testing** with recent transactions to verify detection

## Example

```bash
/add-business-keyword github figma slack
```

This would add "github", "figma", and "slack" to the business expense keyword detection.

## Technical Details

The command modifies this section of the sync script:

```javascript
// Business expense keywords from Notion formula
this.businessExpenseKeywords = [
  'apple', 'dropbox', 'notion', 'raycast', 'youtube',
  'make', 'anthropic', 'openai', 'setapp', 'quickbooks', 'splice',
  // Your new keywords will be added here
];
```

## Validation

- **Duplicates**: Prevents adding keywords that already exist
- **Format**: Converts keywords to lowercase for consistency
- **Length**: Warns if keywords are very short (might cause false positives)
- **Testing**: Optionally test new keywords against recent transactions

## Related Commands

- `/sync-upbank` - Run the enhanced sync with your new keywords
- `/show-business-transactions` - View recently categorized business expenses
- `/remove-business-keyword` - Remove keywords if needed

## Safety

- **Backup**: The original keyword list is preserved in comments
- **Validation**: Keywords are validated before adding
- **Reversible**: You can remove keywords if they cause false positives

## Examples of Good Keywords

- **Software subscriptions**: "github", "figma", "canva", "slack"
- **Business services**: "stripe", "paypal", "xero", "mailchimp"
- **Infrastructure**: "aws", "vercel", "heroku", "digitalocean"
- **Communication**: "zoom", "teams", "discord"

## Examples to Avoid

- **Too generic**: "pay", "inc", "ltd" (would match many non-business transactions)
- **Personal brands**: Your name or personal accounts
- **Common words**: "service", "payment", "transfer"

Use specific, unique identifiers that clearly indicate business expenses.
