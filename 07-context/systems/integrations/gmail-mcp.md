---
created: "2025-10-02 05:40"
system_type: "integration"
status: "active"
---

# Gmail MCP Server

## Overview

**Purpose**: Provides MCP server integration for Gmail operations, enabling Claude Code to send emails, search messages, manage labels, create filters, and handle attachments programmatically.

**Type**: MCP Server Integration (Third-party)

**Status**: Active

## Configuration

### MCP Server Setup

The Gmail MCP server is configured globally in Claude Code settings, not project-specific.

**Enabled in**: `.claude/settings.local.json`

```json
{
  "enabledMcpjsonServers": [
    "gmail"
  ],
  "permissions": {
    "allow": [
      "mcp__gmail__*"
    ]
  }
}
```

### Authentication

Gmail MCP uses OAuth2 authentication. The server handles authentication flow automatically on first use.

**Authentication Flow**:
1. Server prompts for Gmail OAuth consent
2. User authorizes Claude Code access to Gmail
3. Credentials cached for subsequent use

## Available Tools

### Email Management
- `send_email` - Send new emails with attachments
- `draft_email` - Create email drafts
- `read_email` - Read email content by message ID
- `search_emails` - Search using Gmail query syntax
- `delete_email` - Permanently delete emails

### Label Management
- `list_email_labels` - List all Gmail labels (system + custom)
- `modify_email` - Add/remove labels from messages
- `create_label` - Create new Gmail labels
- `update_label` - Update label properties
- `delete_label` - Delete Gmail labels
- `get_or_create_label` - Get existing or create new label

### Batch Operations
- `batch_modify_emails` - Modify labels on multiple emails
- `batch_delete_emails` - Delete multiple emails

### Filters
- `create_filter` - Create Gmail filters with criteria and actions
- `create_filter_from_template` - Use pre-defined filter templates
- `list_filters` - List all Gmail filters
- `get_filter` - Get filter details
- `delete_filter` - Delete Gmail filters

### Attachments
- `download_attachment` - Download email attachments to local filesystem

## Usage Examples

### List Available Labels

```javascript
mcp__gmail__list_email_labels()
```

Returns all system labels (INBOX, SENT, etc.) and custom labels.

### Search Emails

```javascript
mcp__gmail__search_emails({
  query: "from:example@gmail.com is:unread",
  maxResults: 10
})
```

### Send Email

```javascript
mcp__gmail__send_email({
  to: ["recipient@example.com"],
  subject: "Subject line",
  body: "Email body content",
  cc: ["cc@example.com"],
  attachments: ["/path/to/file.pdf"]
})
```

### Create Filter

```javascript
mcp__gmail__create_filter({
  criteria: {
    from: "notifications@service.com"
  },
  action: {
    addLabelIds: ["Label_123"],
    removeLabelIds: ["INBOX"]
  }
})
```

## Current Labels

**System Labels**: INBOX, SENT, DRAFT, TRASH, SPAM, STARRED, IMPORTANT, UNREAD

**Custom Labels** (as of 2025-10-02):
- Invoices
- Payments
- Accounting
- Tax Receipts
- Purchase Orders
- Zoho Invoices
- Reply Later
- invoice_checked
- Telstra
- SAFIA / SAFIA Accounting
- ESM
- Blocked
- Saved 🔒
- [Notion]
- AI Updates

## Integration Points

- **Automation workflows**: Can be triggered from GitHub Actions or n8n
- **FastAPI MCP servers**: Can call Gmail tools for email notifications
- **Business processes**: Automated invoice/receipt handling

## Dependencies

- **External Service**: Gmail API (via OAuth2)
- **MCP Package**: `@modelcontextprotocol/server-gmail` (managed by Claude Code)

## Notes

- Gmail MCP is a globally-configured server, not project-specific
- Authentication credentials are cached after initial OAuth flow
- All tools require appropriate Gmail API permissions
- Rate limits apply per Gmail API quotas

## Related Systems

- [Notion MCP](./notion-mcp.md) - Another third-party MCP integration
- Business API MCP - Can integrate Gmail for notifications
