---
created: "2025-10-20 07:20"
description: |
  Creates secure vault entries for frequently-referenced information like bank details, API keys, passwords, ID numbers, tax info, and company credentials. Generates structured markdown files with YAML frontmatter (type: vault, entity relation, sensitivity level, category). Stores in entity-specific folders (04-resources/vault/{entity}/) and automatically manages .gitignore for sensitive items. Supports both reference info (bank accounts, ABN) and credentials (API keys, passwords) with appropriate security warnings.
examples:
  - /vault-add "MOKAI Commonwealth Bank business account details"
  - /vault-add "Supabase API keys for production database"
  - /vault-add "ABN and ACN for MOK HOUSE PTY LTD"
  - /vault-add "Stripe secret keys and webhook endpoints"
---

# Vault Add

This command helps you create secure, structured vault entries for frequently-needed information that's annoying to search for repeatedly. Handles both non-sensitive reference info (bank details, ID numbers, company info) and sensitive credentials (API keys, passwords, tokens) with automatic .gitignore protection.

## Usage

```bash
/vault-add "description of what to add"

# OR provide structured input directly
/vault-add "API Name: Supabase Production
API Key: sb_prod_xxxxxxx
Project ID: abc123xyz
URL: https://abc123xyz.supabase.co"

# OR reference current conversation context
/vault-add "add these Stripe keys to vault"
```

## Interactive Process

When you run this command, I will:

1. **Analyze your input** to determine:
   - What type of vault item (bank details, API key, ID number, license, password, etc.)
   - Which entity it relates to (MOKAI, MOK HOUSE, Personal, or other)
   - Sensitivity level (reference info vs. credentials)

2. **Ask clarifying questions** if needed:
   - Item name/title for the vault entry
   - Which entity this relates to (for proper folder organization)
   - Additional fields specific to the item type
   - Whether this is sensitive data requiring .gitignore protection

3. **Generate the vault file** in appropriate location:
   - Reference info: `04-resources/vault/{entity}/{Item Name}.md`
   - Sensitive credentials: Same location, but added to .gitignore

4. **Update .gitignore** automatically if the item is marked as sensitive

5. **Confirm creation** and show file location for future reference

## Input Requirements

You can provide vault information in three ways:

1. **Quick description**: `/vault-add "MOKAI bank account details"`
   - I'll ask follow-up questions to gather specifics

2. **Structured input**: Paste formatted info directly
   ```
   /vault-add "Account Name: MOKAI PTY LTD
   BSB: 123-456
   Account Number: 12345678
   Bank: Commonwealth Bank
   Swift: CTBAAU2S"
   ```

3. **Context reference**: If we just discussed API keys or credentials in conversation
   ```
   /vault-add "add those Supabase credentials to vault"
   ```

## Process

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I'll help you create a vault entry by:

1. **Determining vault item type**:
   - Bank account (BSB, account number, SWIFT, bank name)
   - API credentials (API key, secret, project ID, endpoints)
   - Tax identifiers (ABN, ACN, TFN, GST registration)
   - ID numbers (company registration, business licenses)
   - Passwords (service logins, admin credentials)
   - License keys (software licenses, certifications)
   - Insurance details (policy numbers, provider info)

2. **Structuring YAML frontmatter**:
   ```yaml
   type: vault
   entity_type: bank | api | tax | license | password | id-number | insurance
   name: Item name (e.g., "MOKAI Commonwealth Account")
   relation: [["mokai"]] | [["mokhouse"]] | [["personal"]]
   category: bank-details | api-key | tax-info | license | credential | id-number
   sensitive: true | false  # Determines .gitignore treatment
   tags: [searchable, keywords, for, filtering]
   last_verified: YYYY-MM-DD  # When info was last confirmed current
   expiry_date: YYYY-MM-DD    # For licenses, credentials that expire
   date created: Day, MM DD YY, HH:MM:SS am/pm
   date modified: Day, MM DD YY, HH:MM:SS am/pm
   ```

3. **Creating structured content sections**:
   - **Details**: Key-value pairs for the actual information
   - **Access/Usage**: How to use these credentials or where they apply
   - **Related Information**: Links, contact info, documentation
   - **Security Notes**: Special instructions or warnings
   - **Notes**: Any additional context

4. **Organizing by entity**:
   - MOKAI items → `04-resources/vault/mokai/`
   - MOK HOUSE items → `04-resources/vault/mokhouse/`
   - Personal items → `04-resources/vault/personal/`
   - Other entities → `04-resources/vault/{entity-name}/`

5. **Managing .gitignore**:
   - If `sensitive: true`, add file path to `.gitignore`
   - Verify .gitignore entry was added successfully
   - Warn user to never commit sensitive vault files

6. **Validating completeness**:
   - Ensure all required frontmatter fields populated
   - Verify entity folder structure exists (create if needed)
   - Confirm file saved in correct location

## Technical Implementation Guide

### Frontmatter Structure

```yaml
---
type: vault                           # Always "vault"
entity_type: api                      # Type of vault item
name: Supabase Production API         # Human-readable name
relation:                             # Entity associations
  - "[[mokai]]"
category: api-key                     # Category for filtering
sensitive: true                       # Requires .gitignore protection
tags: [database, api, production, supabase]
last_verified: 2025-10-20            # When last confirmed working
expiry_date:                         # Optional expiry date
source: Supabase Dashboard           # Where info came from
date created: Mon, 10 20th 25, 7:20:00 am
date modified: Mon, 10 20th 25, 7:20:00 am
---
```

### Content Structure Examples

#### Bank Account Vault Entry
```markdown
# MOKAI Commonwealth Bank Account

## 📋 Account Details
- **Account Name**: MOKAI PTY LTD
- **BSB**: 123-456
- **Account Number**: 12345678
- **Bank**: Commonwealth Bank of Australia
- **Branch**: Sydney CBD
- **SWIFT Code**: CTBAAU2S
- **Account Type**: Business Transaction Account

## 🔗 Access Information
- **Online Banking**: https://www.commbank.com.au/netbank
- **Customer ID**: MB123456
- **Phone Banking**: 13 2221

## 📝 Notes
Primary operating account for MOKAI business transactions. Used for client payments and contractor invoices.

## 🔒 Security
- Two-factor authentication enabled
- Primary contact: harry@mokai.com.au
- Authorized signatories: Harry Sayers
```

#### API Credentials Vault Entry
```markdown
# Supabase Production Database

## 🔑 API Credentials
- **Project ID**: abc123xyz
- **API URL**: https://abc123xyz.supabase.co
- **Anon Key**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
- **Service Role Key**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (ADMIN ACCESS)
- **Database Password**: [stored in .env]

## 🌐 Access & Usage
- **Dashboard**: https://supabase.com/dashboard/project/abc123xyz
- **Database Host**: db.abc123xyz.supabase.co
- **Database Name**: postgres
- **Port**: 5432

## 📝 Configuration
Used for MOKAI production database. Connected services:
- MCP server (supabase-mcp)
- Financial tracking system
- Client data storage

## 🔒 Security Warnings
- **NEVER commit Service Role Key to git**
- Service Role bypasses Row Level Security
- Use Anon Key for client-side operations only
- Rotate keys if compromised: Settings > API > Generate new key
```

#### Tax Information Vault Entry
```markdown
# MOKAI PTY LTD Tax Identifiers

## 📋 Tax Details
- **ABN**: 12 345 678 901
- **ACN**: 123 456 789
- **GST Registered**: Yes
- **GST Registration Date**: 2024-01-15
- **TFN**: 123 456 789
- **Business Name**: MOKAI PTY LTD

## 🔗 Related Information
- **ABR Lookup**: https://abr.business.gov.au/ABN/View?abn=12345678901
- **ATO Portal**: https://onlineservices.ato.gov.au/
- **Accountant**: [Contact details]

## 📝 Notes
Trading name: MOKAI
Registered for GST quarterly reporting (BAS)
Financial year: July 1 - June 30
```

### File Naming Convention

```javascript
// Format: Entity-specific folders with descriptive names
const entityFolder = `04-resources/vault/${entity.toLowerCase()}/`;
const fileName = `${itemName}.md`;  // Human-readable name
const filePath = `${entityFolder}${fileName}`;

// Examples:
// 04-resources/vault/mokai/Commonwealth Bank Account.md
// 04-resources/vault/mokai/Supabase Production API.md
// 04-resources/vault/mokhouse/Stripe API Keys.md
// 04-resources/vault/personal/Passport Details.md
```

### .gitignore Management

When `sensitive: true`, automatically append to `.gitignore`:

```bash
# Sensitive vault entries (auto-generated by /vault-add)
04-resources/vault/**/Supabase Production API.md
04-resources/vault/**/Stripe API Keys.md
04-resources/vault/**/Admin Passwords.md
```

**Security Protocol**:
1. Check if file path already in .gitignore
2. If not, append to .gitignore with comment
3. Verify addition with `git check-ignore` command
4. Warn user to verify .gitignore before committing

## Output Format

I'll provide:

1. **Vault entry summary**:
   - Item name and type
   - Entity association (MOKAI/MOK HOUSE/Personal)
   - Sensitivity level
   - File location

2. **File creation confirmation**:
   - Full file path for future reference
   - .gitignore status (added/already ignored/not sensitive)

3. **Security reminder** (for sensitive items):
   - Warning about git commits
   - Recommendation to verify .gitignore
   - Suggestion to use environment variables for runtime access

4. **Quick access tip**:
   - How to search for this item (by entity, tags, keywords)
   - Related vault items you might need

## Examples

### Example 1: Bank Account Details (Non-Sensitive Reference)

**Input**: `/vault-add "MOKAI Commonwealth Bank business account"`

**Interactive Process**:
```
Analyzing input... Detected: Bank account details for MOKAI

Q: I'll need the following details:
   - Account name
   - BSB
   - Account number
   - Bank name
   - Any additional info (SWIFT, branch, account type)

A: [User provides details]

Q: Is this sensitive information that should be added to .gitignore?
A: No, it's reference info but not credentials

Creating vault entry...
```

**Output File** (`04-resources/vault/mokai/Commonwealth Bank Account.md`):
```markdown
---
type: vault
entity_type: bank
name: MOKAI Commonwealth Bank Account
relation:
  - "[[mokai]]"
category: bank-details
sensitive: false
tags: [bank, commonwealth, business-account, mokai]
last_verified: 2025-10-20
source: Bank statement
date created: Mon, 10 20th 25, 7:25:00 am
date modified: Mon, 10 20th 25, 7:25:00 am
---

# MOKAI Commonwealth Bank Account

## 📋 Account Details
- **Account Name**: MOKAI PTY LTD
- **BSB**: 123-456
- **Account Number**: 12345678
- **Bank**: Commonwealth Bank of Australia
- **Account Type**: Business Transaction Account

## 🔗 Access Information
- **Online Banking**: https://www.commbank.com.au/netbank
- **Phone Banking**: 13 2221

## 📝 Notes
Primary operating account for MOKAI business transactions.
```

**Confirmation**:
```
✅ Vault entry created: 04-resources/vault/mokai/Commonwealth Bank Account.md
📂 Entity: MOKAI
🔓 Sensitivity: Reference info (not in .gitignore)
🏷️ Tags: bank, commonwealth, business-account, mokai

💡 Quick Access:
   - Search "MOKAI bank" in Obsidian
   - Filter by tag: #bank #mokai
```

### Example 2: API Credentials (Sensitive)

**Input**: `/vault-add "Stripe production API keys - secret key, publishable key, webhook signing secret"`

**Interactive Process**:
```
Analyzing input... Detected: API credentials (Stripe) - SENSITIVE

Q: Which entity does this relate to?
A: MOKAI

Creating sensitive vault entry with .gitignore protection...
```

**Output File** (`04-resources/vault/mokai/Stripe API Keys.md`):
```markdown
---
type: vault
entity_type: api
name: Stripe Production API Keys
relation:
  - "[[mokai]]"
category: api-key
sensitive: true
tags: [stripe, api, production, payment, credentials]
last_verified: 2025-10-20
expiry_date:
source: Stripe Dashboard
date created: Mon, 10 20th 25, 7:30:00 am
date modified: Mon, 10 20th 25, 7:30:00 am
---

# Stripe Production API Keys

## 🔑 API Credentials
- **Publishable Key**: pk_live_[REDACTED]
- **Secret Key**: sk_live_[REDACTED]
- **Webhook Signing Secret**: whsec_[REDACTED]

## 🌐 Access & Usage
- **Dashboard**: https://dashboard.stripe.com
- **Account Email**: billing@mokai.com.au
- **API Version**: 2024-10-15

## 📝 Configuration
Used for MOKAI payment processing and invoice management.

Connected services:
- Invoice generation system
- Client payment portal
- Subscription management

## 🔒 Security Warnings
- **NEVER commit these keys to git**
- Secret key has full account access
- Rotate keys immediately if compromised
- Use webhook secret to verify webhook signatures
- Store in environment variables for runtime access

## 🔗 Key Management
- Rotate keys: Dashboard > Developers > API Keys > Roll key
- Test keys available for development: pk_test_... / sk_test_...
```

**Confirmation**:
```
✅ Vault entry created: 04-resources/vault/mokai/Stripe API Keys.md
🔒 SENSITIVE ITEM - Added to .gitignore

⚠️  SECURITY REMINDERS:
   - This file is now git-ignored and will NOT be committed
   - Verify .gitignore before running git add
   - Never share this file via email or messaging
   - Consider using environment variables for runtime access

📂 Entity: MOKAI
🏷️ Tags: stripe, api, production, payment, credentials

💡 Quick Access:
   - Search "Stripe API" in Obsidian (local only)
   - File location: 04-resources/vault/mokai/Stripe API Keys.md
```

**.gitignore Addition**:
```bash
# Sensitive vault entries (auto-generated by /vault-add)
04-resources/vault/mokai/Stripe API Keys.md
```

### Example 3: Tax Information (Reference)

**Input**: `/vault-add "ABN and ACN for MOK HOUSE PTY LTD"`

**Output File** (`04-resources/vault/mokhouse/Tax Identifiers.md`):
```markdown
---
type: vault
entity_type: tax
name: MOK HOUSE Tax Identifiers
relation:
  - "[[mokhouse]]"
category: tax-info
sensitive: false
tags: [tax, abn, acn, mokhouse, registration]
last_verified: 2025-10-20
source: ABR Lookup
date created: Mon, 10 20th 25, 7:35:00 am
date modified: Mon, 10 20th 25, 7:35:00 am
---

# MOK HOUSE PTY LTD Tax Identifiers

## 📋 Tax Details
- **ABN**: 12 345 678 901
- **ACN**: 123 456 789
- **GST Registered**: Yes
- **Business Name**: MOK HOUSE PTY LTD
- **Entity Type**: Australian Proprietary Company

## 🔗 Related Information
- **ABR Lookup**: https://abr.business.gov.au/ABN/View?abn=12345678901
- **ASIC**: https://connectonline.asic.gov.au

## 📝 Notes
Trading name: MOK HOUSE
GST quarterly reporting required
```

## Evaluation Criteria

A successful vault entry should:

1. **Complete frontmatter** with all required fields:
   - `type: vault` always present
   - Entity relation clearly defined
   - Sensitivity level accurately set
   - Appropriate category and tags

2. **Proper security handling**:
   - Sensitive items added to .gitignore
   - Security warnings included for credentials
   - No accidental commits of secrets

3. **Clear organization**:
   - Stored in correct entity folder
   - Descriptive file name
   - Searchable by entity, tags, or keywords

4. **Structured content**:
   - Details section with all relevant information
   - Access/usage instructions where applicable
   - Related information and notes

5. **Practical usability**:
   - Easy to find via search
   - All necessary info in one place
   - Clear instructions for use

## Related Resources

- Template: `98-templates/vault.md` (to be created)
- Vault root: `04-resources/vault/`
- Entity folders: `04-resources/vault/{mokai|mokhouse|personal}/`
- .gitignore: Root `.gitignore` file

## Security Best Practices

### What to Store in Vault
✅ Bank account details (BSB, account number)
✅ Tax identifiers (ABN, ACN, TFN)
✅ API keys and tokens (with .gitignore)
✅ Passwords and credentials (with .gitignore)
✅ License keys and certificates
✅ Insurance policy numbers
✅ Company registration details

### What NOT to Store in Vault
❌ Credit card CVV codes (regenerate each use)
❌ Temporary access tokens (use environment variables)
❌ Personal passwords for non-business accounts
❌ Social security numbers (unless absolutely necessary)

### Security Workflow
1. Create vault entry with `sensitive: true`
2. Verify .gitignore addition before git operations
3. For runtime access, copy to environment variables
4. Regularly verify `git status` shows vault files as ignored
5. Never email or message vault file contents directly

---

**Ready to add a vault entry. Provide:**
- What information you want to store (description or structured data)
- Which entity it relates to (MOKAI/MOK HOUSE/Personal/Other)
- Whether it's sensitive (credentials/keys) or reference info (account numbers/IDs)

I'll create a structured vault entry with proper frontmatter, organization, and security handling.
