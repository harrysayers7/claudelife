# System Patterns and Guidelines

## MCP Server Configuration Pattern

### Configuration Scopes and Files

Claude Code supports **multiple MCP configuration scopes** with the following precedence (highest to lowest):

1. **Local scope** (`~/.claude.json`) - **Highest precedence**
   - Managed by Claude CLI commands
   - Per-machine configuration
   - Overrides project and user scopes

2. **Project scope** (`.mcp.json` in project root) - **Middle precedence**
   - Project-specific MCP servers
   - Committed to version control (or gitignored for sensitive configs)
   - Valid and supported by Claude Code

3. **User scope** (`~/.mcp.json`) - **Lowest precedence**
   - Global user configuration
   - Available across all projects

### Enabling MCP Servers

MCP servers configured in `.mcp.json` or `~/.mcp.json` must also be listed in `~/.claude/settings.local.json`:

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": [
    "serena",
    "graphiti",
    "task-master-ai"
  ]
}
```

**Important**: Even with `enableAllProjectMcpServers: true`, servers in `~/.mcp.json` must be explicitly enabled in `enabledMcpjsonServers`.

### CLI Management (Recommended)

Use Claude CLI for managing MCP servers:

```bash
# List all configured MCP servers
claude mcp list

# Get details of specific server
claude mcp get <server-name>

# Add new MCP server
claude mcp add <server-name> \
  --command "/path/to/command" \
  --arg "arg1" --arg "arg2" \
  --env KEY=value \
  --scope local  # or project, user

# Remove MCP server
claude mcp remove <server-name> -s local

# Test MCP server connection
claude mcp test <server-name>
```

### Debugging MCP Servers

When MCP server doesn't appear in available resources:

1. **Check connection status**:
   ```bash
   claude mcp list  # Look for ✓ Connected or ✗ Failed
   ```

2. **Verify configuration**:
   ```bash
   claude mcp get <server-name>
   ```

3. **Check logs**:
   ```bash
   # Logs location: ~/Library/Logs/Claude/mcp-server-<name>.log
   tail -n 50 ~/Library/Logs/Claude/mcp-server-<name>.log
   ```

4. **Test server manually**:
   ```bash
   # Run the command directly to verify it starts
   /path/to/command --transport stdio
   ```

5. **Check for scope conflicts**:
   - If server exists in multiple scopes, CLI commands may fail
   - Remove from specific scope: `claude mcp remove <name> -s <scope>`
   - Verify with `claude mcp list` after removal

6. **Restart Claude Code**:
   ```bash
   # After configuration changes
   exit  # or Ctrl+D
   claude  # restart
   ```

### Common Issues

**Server shows "✗ Failed to connect"**:
- Check server logs for connection errors
- Verify dependencies are running (e.g., Neo4j for Graphiti)
- Ensure environment variables are correct
- Remove and re-add server via CLI

**"Server exists in multiple scopes"**:
- Specify scope when removing: `claude mcp remove <name> -s local`
- Check all scopes: local (`~/.claude.json`), project (`.mcp.json`), user (`~/.mcp.json`)

**Server configured but not available**:
- Verify server is in `enabledMcpjsonServers` in `~/.claude/settings.local.json`
- Restart Claude Code after configuration changes
- Check server logs for startup errors

**Server connects but tools don't appear** (ListMcpResourcesTool returns empty array):
- **Root cause**: Missing wildcard permission in `.claude/settings.local.json`
- **Check first**: Does `allowedTools` contain `mcp__{server-name}__*`?
- **Solution**: Add wildcard permission matching exact server name
- **Common mistake**: Having similar server permissions (e.g., `mcp__graphiti-personal__*`) but not the base server permission
- **Verification order**:
  1. Check `enabledMcpjsonServers` contains server name
  2. Check `allowedTools` has `mcp__{server-name}__*` wildcard
  3. Verify exact name match between `.mcp.json` and permission entry
  4. Only then check debug logs for connection issues

### Example: Graphiti MCP Server

```bash
# Add Graphiti MCP server via CLI
claude mcp add graphiti \
  --command "/opt/homebrew/bin/uv" \
  --arg "run" \
  --arg "--directory" \
  --arg "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server" \
  --arg "graphiti_mcp_server.py" \
  --arg "--transport" \
  --arg "stdio" \
  --env NEO4J_URI=bolt://localhost:7687 \
  --env NEO4J_USER=neo4j \
  --env NEO4J_PASSWORD=neo4j \
  --env OPENAI_API_KEY=sk-proj-... \
  --env MODEL_NAME=gpt-4o-mini \
  --env GRAPHITI_TELEMETRY_ENABLED=false \
  --scope local

# Verify connection
claude mcp get graphiti
# Should show: ✓ Connected

# Test tools are accessible
# After restart, use ListMcpResourcesTool or check available tools
```

### MCP Server Directory Structure

MCP servers can be:
- **NPM packages**: Installed globally or run via `npx`
- **Python scripts**: Run via `python`, `uv`, or virtual environments
- **Local executables**: Any binary that implements stdio transport

Example local Python MCP server:
```
/Users/harrysayers/Developer/claudelife/graphiti_mcp_server/
├── graphiti_mcp_server.py  # Main server implementation
├── pyproject.toml           # Python dependencies
└── .venv/                   # Virtual environment (if using venv)
```

### Best Practices

1. **Use CLI for management**: Preferred over manual JSON editing
2. **Specify scope explicitly**: Avoid conflicts between local/project/user configs
3. **Check logs first**: Most connection issues visible in logs
4. **Test manually**: Run server command directly to verify it works
5. **Restart after changes**: Claude Code requires restart to pick up config changes
6. **Document environment variables**: Keep track of required env vars for each server
7. **Use project scope for team sharing**: Commit `.mcp.json` for team-wide MCP servers
8. **Use local scope for personal tools**: Keep personal MCP servers in local config

### Learned 2025-10-18

- `.mcp.json` IS valid for project scope (contrary to earlier belief)
- Configuration hierarchy: local > project > user
- CLI is recommended for managing MCP servers to avoid scope conflicts
- Stale logs can be misleading - always verify current connection status
- Multiple scopes can cause "server exists" errors - specify scope explicitly
- Environment variables must be passed to CLI with `--env KEY=value` format

## Claude Code uses Serena MCP for context-aware file operations

When exploring codebases or searching for patterns, Claude Code should use Serena's symbolic tools first:
- `get_symbols_overview` - Get high-level view of file structure
- `find_symbol` - Find specific symbols by name path
- `search_for_pattern` - Search for patterns across codebase
- `find_referencing_symbols` - Understand symbol relationships

Only use `Read` tool after understanding structure via Serena.

## Sensitive Data Management

Never commit sensitive data to git. Always use environment variables for:
- API keys and secrets
- Database credentials
- Authentication tokens
- Personal information

### Detection and Prevention

Tools configured for pre-commit scanning:
- **gitleaks**: Detects hardcoded secrets, API keys, credentials
- **trufflehog**: Finds sensitive data patterns, authentication tokens
- **bandit**: Python security linter for code vulnerabilities

### Git Hooks

Pre-commit hook (`.git/hooks/pre-commit`) runs automatically before each commit:
```bash
#!/bin/bash
# Runs gitleaks, trufflehog, and bandit security scans
# Prevents commit if sensitive data detected
```

### GitHub Actions

CI/CD workflow (`.github/workflows/security-audit.yml`) runs on push:
- Secret scanning with gitleaks and trufflehog
- Dependency vulnerability scanning with pip-audit
- Python security analysis with bandit
- Blocks merges if security issues found

### Manual Scanning

```bash
# Scan current changes for secrets
gitleaks detect --verbose --no-git

# Scan entire git history
trufflehog git file://. --only-verified

# Scan Python code for vulnerabilities
bandit -r . -ll
```

### Remediation

If sensitive data is committed:
1. **Immediately rotate/revoke** the exposed credential
2. **Remove from history**: Use `git filter-branch` or BFG Repo-Cleaner
3. **Force push** to update remote (coordinate with team)
4. **Update secrets management**: Move to environment variables

### Environment Variable Pattern

Always reference sensitive data from environment:

```python
# ❌ WRONG - Hardcoded secret
api_key = "sk-proj-xxxxx"  # Example - don't do this

# ✅ CORRECT - From environment
import os
api_key = os.getenv("OPENAI_API_KEY")
```

```typescript
// ❌ WRONG - Hardcoded secret
const apiKey = "sk-proj-xxxxx";  // Example - don't do this

// ✅ CORRECT - From environment
const apiKey = process.env.OPENAI_API_KEY;
```

### Pre-commit Configuration

Install pre-commit hooks:
```bash
# Install pre-commit framework
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

Configuration in `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    hooks:
      - id: gitleaks
  
  - repo: https://github.com/trufflesecurity/trufflehog
    hooks:
      - id: trufflehog
  
  - repo: https://github.com/PyCQA/bandit
    hooks:
      - id: bandit
```

Learned: 2025-10-18 - Comprehensive security scanning prevents accidental exposure of sensitive data in git commits and CI/CD pipelines.

## MCP Server Setup Automation

### Available Commands

**`/mcp-setup-checklist {server-name}`** - Interactive MCP server setup
- Guides through complete configuration (config, enable, permissions)
- Validates each step before proceeding
- Generates exact CLI commands or manual config entries
- Tests connection and tool accessibility
- Provides targeted troubleshooting if steps fail

**Verification mode**: `/mcp-setup-checklist {server-name} --verify`
- Runs after Claude Code restart to verify setup
- Tests connection status and tool exposure
- Quick health check for existing servers

### Setup Checklist (Manual)

When adding MCP server without the command:

1. ✅ Add config to `.mcp.json` or via `claude mcp add`
2. ✅ Add to `enabledMcpjsonServers` in `~/.claude/settings.local.json`
3. ✅ **Add `mcp__{server-name}__*` to `allowedTools`** (commonly missed!)
4. ✅ Restart Claude Code
5. ✅ Verify with `ListMcpResourcesTool({ server: "{name}" })`

### Related Resources

- Command: `.claude/commands/mcp-setup-checklist.md`
- Troubleshooting: `04-resources/guides/mcp-troubleshooting.md`
- Lesson: `04-resources/lessons-learnt/251020-issue-002-mcp-permissions.md`

Learned: 2025-10-20 - Interactive setup command prevents missing critical steps (especially permissions) when adding MCP servers.