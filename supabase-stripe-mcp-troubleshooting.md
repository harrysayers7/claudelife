# Supabase & Stripe MCP Troubleshooting Log

## Problem
Supabase and Stripe MCP servers are configured in `~/.mcp.json` and enabled in `settings.local.json` but don't appear in Claude Code's MCP server list.

## Attempted Fixes (ALL FAILED)

### Attempt 1: Remove broken project overrides
- **Action**: Removed `graphiti` and `claudelife-obsidian` from project `.mcp.json`
- **Result**: FAILED - Still not showing
- **File**: `/Users/harrysayers/Developer/claudelife/.mcp.json`

### Attempt 2: Add to project .mcp.json
- **Action**: Added supabase and stripe configs directly to project `.mcp.json`
- **Result**: FAILED - Still not showing
- **Config added**:
```json
"supabase": {
  "command": "npx",
  "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref", "gshsshaodoyttdxippwx"],
  "env": {"SUPABASE_ACCESS_TOKEN": "sbp_..."}
}
```

### Attempt 3: Remove "type": "stdio" field
- **Action**: Removed explicit `"type": "stdio"` from configs (it's default)
- **Result**: FAILED - Still not showing

### Attempt 4: Use full npx path
- **Action**: Changed `"command": "npx"` to `"command": "/opt/homebrew/bin/npx"`
- **Result**: FAILED - Still not showing

### Attempt 5: Delete project .mcp.json entirely
- **Action**: Moved `.mcp.json` to `.mcp.json.backup` to force loading from global config
- **Result**: FAILED - Still not showing
- **Reasoning**: If no project config exists, should load from `~/.mcp.json` with `enabledMcpjsonServers` array

## Verified Working Info
- ✅ Both packages exist on npm:
  - `@supabase/mcp-server-supabase@0.5.6`
  - `@stripe/mcp@0.2.4`
- ✅ Both configs are in `~/.mcp.json`
- ✅ Both are in `enabledMcpjsonServers` array in `settings.local.json`
- ✅ Commands start successfully (timeout when testing = waiting for stdio, which is correct)
- ✅ npx found at `/opt/homebrew/bin/npx`

## Current State
- Global config: `~/.mcp.json` has both supabase and stripe
- Project config: `.mcp.json.backup` (disabled)
- Settings: Both in `enabledMcpjsonServers` array
- Result: STILL NOT SHOWING IN UI

## Logs Checked
- `/Users/harrysayers/Library/Logs/Claude/main.log` - No recent errors
- `/Users/harrysayers/Library/Logs/Claude/mcp-server-mcp-stripe.log` - Shows old errors from Oct 15
- No `mcp-server-supabase.log` file exists (server never started)

## Servers That ARE Working
These show up in the UI and work:
- serena (connected)
- trigger (connected)
- gpt-researcher (connected)
- notion (connected)
- memory (connected)
- github (connected)
- gmail (connected)
- context7 (connected)

## Servers That Show as Failed
- linear-server (failed) - Not configured anywhere, should remove from enabled list
- graphiti (failed) - Config issues
- claudelife-obsidian (failed) - Config issues

## SOLUTION THAT WORKED ✅

### Attempt 7: Remove `"type": "stdio"` fields from config
- **Action**: Used Context7 MCP to research official MCP config format
- **Discovery**: `"type": "stdio"` is NOT part of the `.mcp.json` spec - stdio is the DEFAULT transport
- **Fix**: Removed all `"type": "stdio"` lines from `~/.mcp.json` using:
  ```bash
  sed -i.bak '/^[[:space:]]*"type": "stdio",$/d' ~/.mcp.json
  ```
- **Result**: Config now matches official spec from MCP docs

### Correct MCP Config Format

**WRONG (what we had):**
```json
{
  "supabase": {
    "type": "stdio",  ← THIS BREAKS IT
    "command": "npx",
    "args": [...]
  }
}
```

**CORRECT (per official docs):**
```json
{
  "supabase": {
    "command": "npx",
    "args": [...],
    "env": {...}
  }
}
```

### Additional Fix: Context7 Hook

Also enabled the Context7 detector hook that was created but never configured:
- Added `UserPromptSubmit` hook in `.claude/settings.local.json`
- Made hook executable: `chmod +x .claude/hooks/context7_detector.py`
- Hook now automatically suggests Context7 when asking about library APIs

## Test Results

**After removing `"type": "stdio"` fields:**
- Restart Claude Code required
- Both Supabase and Stripe should now appear in MCP server list
- Tools should be available as `mcp__supabase__*` and `mcp__stripe__*`

## Key Learnings

1. **Claude Code uses `~/.claude.json` NOT `.mcp.json`** - This was the actual root cause
2. **Always use `claude mcp add` CLI** - Never manually edit config files
3. **Verify with `claude mcp list`** - Shows what's actually loaded
4. **Check official docs first** - The Context7 MCP could have answered this immediately
5. **Agent instructions can be wrong** - The mcp-expert agent was teaching the wrong method

## Lesson Learned Documentation

This debugging session is fully documented in:
- **[Lessons Learned: MCP Config Location](2025-10-16-mcp-config-location.md)**

Includes:
- Complete timeline of failed attempts
- Correct workflow going forward
- Agent and documentation fixes applied
- Prevention measures implemented
