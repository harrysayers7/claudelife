---
date: 2025-10-02 13:05
location: "[[claudelife]]"
status:
  - active
---

# Supabase MCP Server - Setup & Troubleshooting

## ✅ Setup Complete

### 1. Environment Variables (in `~/.zshrc`)
```bash
export SUPABASE_SERVICE_KEY="eyJhbGci..."
export SUPABASE_ACCESS_TOKEN="$SUPABASE_SERVICE_KEY"
export SUPABASE_PROJECT_REF="gshsshaodoyttdxippwx"
export SUPABASE_URL="https://gshsshaodoyttdxippwx.supabase.co"
```

### 2. MCP Server Configuration (in `~/.mcp.json`)
```json
"supabase": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@supabase/mcp-server-supabase"],
  "env": {
    "SUPABASE_ACCESS_TOKEN": "$SUPABASE_ACCESS_TOKEN",
    "SUPABASE_PROJECT_REF": "$SUPABASE_PROJECT_REF"
  }
}
```

### 3. Claude Code Permissions (in `~/.claude/settings.local.json`)
```json
"enabledMcpjsonServers": [
  "task-master-ai",
  "notion",
  "context7",
  "linear-server",
  "supabase"
]
```

## 🔄 Activation Steps

### Required Actions
1. **Reload terminal**: `source ~/.zshrc`
2. **Restart Claude Code**: Close and reopen Claude Code completely
3. **Verify connection**: Use MCP tools to test

### Test Commands
```bash
# Check environment variables
check_api_keys

# Verify MCP server is enabled
cat ~/.claude/settings.local.json | grep supabase

# Test Supabase connection (after Claude Code restart)
# Use mcp__supabase__list_projects or mcp__supabase__get_project
```

## 🧪 Testing the Connection

After restarting Claude Code, test with these MCP tools:

```javascript
// List all projects
mcp__supabase__list_projects()

// Get SAYERS DATA project
mcp__supabase__get_project({ id: "gshsshaodoyttdxippwx" })

// List tables
mcp__supabase__list_tables({
  project_id: "gshsshaodoyttdxippwx",
  schemas: ["public"]
})
```

## 📊 Available MCP Tools

### Project Management
- `mcp__supabase__list_projects` - List all Supabase projects
- `mcp__supabase__get_project` - Get project details

### Database Operations
- `mcp__supabase__list_tables` - List all tables in schema
- `mcp__supabase__execute_sql` - Run SQL queries
- `mcp__supabase__apply_migration` - Apply DDL migrations

### Analysis
- `mcp__supabase__get_advisors` - Security/performance advisories
- `mcp__supabase__generate_typescript_types` - Generate TypeScript types

### Edge Functions
- `mcp__supabase__list_edge_functions` - List Edge Functions
- `mcp__supabase__get_edge_function` - Get function details
- `mcp__supabase__deploy_edge_function` - Deploy Edge Function

## ⚠️ Troubleshooting

### Error: "Unauthorized"
**Cause**: MCP server can't access environment variables

**Solutions**:
1. Verify `~/.zshrc` has all required variables
2. Run `source ~/.zshrc` in terminal
3. **Restart Claude Code** (MCP servers load environment on startup)
4. Check variables: `echo $SUPABASE_ACCESS_TOKEN`

### Error: "Project not found"
**Cause**: Wrong project reference

**Solution**:
- Verify project ID: `gshsshaodoyttdxippwx` (SAYERS DATA)
- Check `SUPABASE_PROJECT_REF` is set correctly

### MCP Server Not Available
**Cause**: Server not enabled in Claude Code settings

**Solutions**:
1. Check `~/.claude/settings.local.json` includes `"supabase"` in `enabledMcpjsonServers`
2. Verify `~/.mcp.json` has supabase server configuration
3. Restart Claude Code after changes

## 📝 Quick Reference

**Project ID**: `gshsshaodoyttdxippwx`
**Project Name**: SAYERS DATA
**URL**: https://gshsshaodoyttdxippwx.supabase.co

**Tables**: 13 total (7 core financial + 6 ML/AI)
**Records**: ~74 total

See [supabase-sayers-data.md](./supabase-sayers-data.md) for complete database documentation.
