Retrieve Linear issues with flexible filtering: $ARGUMENTS

Steps:
1. Parse $ARGUMENTS for filter criteria:
   - Labels: "label:optimization", "label:bug,enhancement"
   - Status: "status:backlog", "status:in progress", "status:done"
   - Assignee: "assignee:me", "assignee:harry"
   - Date filters: "created:>2025-09-20", "updated:<7d" (last 7 days)
   - Search: "search:CLAUDE.md", "query:restructure"
   - Team: "team:Sayers" (default)
   - Limit: "limit:10" (default: 20)

2. Build filter object for mcp__linear-server__list_issues

3. Retrieve issues and format results with:
   - Issue identifier (e.g., SAY-84)
   - Title
   - Status
   - Labels
   - URL
   - Created/Updated dates (if requested)

4. Sort by most recent first unless specified

Examples:
- `/linear-retrieve label:optimization` → Issues with optimization label
- `/linear-retrieve status:backlog label:claudelife` → Backlog items for claudelife
- `/linear-retrieve assignee:me status:in progress` → My active issues
- `/linear-retrieve created:>2025-09-20` → Recent issues from Sept 20+
- `/linear-retrieve search:CLAUDE` → Issues mentioning CLAUDE
- `/linear-retrieve limit:5` → Last 5 issues

Filter combinations:
- Multiple labels: AND logic (must have all)
- Multiple filters: AND logic (all criteria must match)
- Date formats: ISO (2025-09-20) or relative (7d, 1w, 1m)
