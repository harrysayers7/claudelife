# Show Business Expense Keywords

This command displays the current list of keywords used for automatic business expense detection.

## Usage

```bash
/show-business-keywords [--test-recent]
```

## What this command does

1. **Extract current keywords** from the enhanced UpBank sync script
2. **Display the keyword list** in an organized format
3. **Show keyword statistics** (total count, recently added, etc.)
4. **Optionally test keywords** against recent transactions

## Options

- `--test-recent` - Test keywords against recent transactions to show detection results

## Output Format

```
📋 Business Expense Keywords (12 total)

💼 Software & Services:
  • apple, dropbox, notion, raycast
  • setapp, quickbooks, splice

🤖 AI & Development:
  • anthropic, openai, make

📺 Content & Media:
  • youtube

🆕 Recently Added:
  • github, figma, slack (added today)

📊 Detection Statistics (last 30 days):
  • Total business expenses: 47 transactions
  • Most frequent: notion (12), apple (8), openai (6)
  • Total amount: $1,247.83
```

## Process

When you run this command, I will:

1. **Read the sync script** to extract current keywords
2. **Categorize keywords** by type (software, AI, content, etc.)
3. **Show statistics** from recent transaction categorizations
4. **Highlight recent additions** if any
5. **Test detection** if `--test-recent` flag is used

## With Testing Flag

If you use `--test-recent`, I'll also show:

```
🧪 Recent Detection Test (last 7 days):

✅ Detected Business Expenses:
  • NOTION LABS INC - $10.00 (keyword: notion)
  • APPLE.COM/BILL - $4.99 (keyword: apple)
  • OPENAI - $20.00 (keyword: openai)

❓ Potential Misses:
  • GITHUB, INC - $7.00 (consider adding "github")
  • FIGMA INC - $15.00 (consider adding "figma")
```

## Related Commands

- `/add-business-keyword` - Add new keywords
- `/remove-business-keyword` - Remove problematic keywords
- `/test-business-keywords` - Test keywords against specific transactions
- `/sync-upbank` - Run sync with current keywords

## Use Cases

- **Review current setup** before adding new keywords
- **Audit keyword effectiveness** to identify gaps
- **Prepare for tax season** by reviewing business expense detection
- **Troubleshoot false positives** by seeing which keywords trigger
- **Optimize detection** by analyzing keyword performance

## Tips

- **Review regularly** to ensure keywords stay relevant
- **Add specific keywords** rather than generic ones
- **Test new services** to see if they need keyword addition
- **Monitor false positives** and remove problematic keywords
