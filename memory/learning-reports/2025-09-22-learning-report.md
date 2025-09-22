# Learning Report - 2025-09-22

## Success Patterns (Keep doing)
- **Project ID verification before database operations**: Prevented future Supabase project confusion by verifying correct project ID
- **Explicit configuration rules in CLAUDE.md**: Added permanent Supabase database rules to prevent repeat issues
- **MCP server cache awareness**: Recognized that MCP servers maintain internal state separate from codebase files
- **Immediate problem resolution focus**: User appreciated quick fix over lengthy explanations
- **Context continuation from conversation summary**: Successfully resumed work from previous session summary

## Failure Patterns (Stop doing)
- **Trusting MCP server cached project IDs**: MCP server had wrong project ID cached, causing database operations to fail
- **Assuming project configuration persistence**: Don't assume MCP configurations remain consistent across sessions
- **Over-explaining technical details**: User wanted the problem fixed quickly, not detailed explanations

## Optimizations Discovered
- **Add critical configs to CLAUDE.md**: For persistent settings that MCP servers might cache incorrectly
- **Always verify project/database IDs**: Use `list_projects` or similar verification commands before operations
- **File search + explicit rules strategy**: When configs aren't in files, add explicit rules to prevent future issues

## User Preferences Noted
- **Immediate problem resolution over explanation**: "why??? you were ablew to do it fine before what has changed" - focus on fixing, not explaining
- **Expects consistency**: When something worked before, it should continue working
- **Wants clean permanent solutions**: Remove evidence of wrong configs, add explicit rules

## Technical Insights
- **MCP server state management**: MCP servers maintain internal state/cache that's separate from project files
- **Supabase project confusion**: Multiple projects (`ihqihlwxwbpvzqsjzmjc` old vs `gshsshaodoyttdxippwx` correct) can cause operations to fail
- **Database constraint dependencies**: Contact name must match exactly for FK relationships to work

## Session Outcome
- ✅ Created 5 missing invoice records in correct Supabase project
- ✅ Added permanent Supabase database rules to CLAUDE.md
- ✅ Updated learning patterns in performance.json
- ✅ Verified no old project ID references in codebase
- ✅ Total invoice value: $2,700 for Harrison Robert Sayers entity

## Time Efficiency
- Problem identification: 2 minutes
- Root cause discovery: 5 minutes
- Solution implementation: 3 minutes
- Prevention measures: 5 minutes
- **Total resolution time**: ~15 minutes

## Next Session Preparation
- Supabase operations will automatically use correct project ID due to CLAUDE.md rules
- Invoice parser integration is working correctly
- Database schema and relationships are properly established