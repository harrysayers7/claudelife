# MOK Music Project Status Dashboard

Get a comprehensive overview of all MOK Music projects with financial summaries and next actions.

## Usage
```
/mok-music-project-status [filter]
```

**Optional filters:**
- `current` - Show only active/current projects
- `invoiced` - Show projects awaiting payment
- `complete` - Show completed projects
- `all` - Show all projects (default)

## Steps

1. **Connect to ESM Projects database**
   ```javascript
   mcp__notion__API-post-database-query({
     database_id: "1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac",
     page_size: 20,
     sorts: [{"property": "Submitted On", "direction": "descending"}]
   })
   ```

2. **Calculate financial summaries**
   - Total outstanding amount (sum of "Total Owed" where > 0)
   - Current projects value (sum of "Current Projects Owed")
   - Completed projects paid (sum of "Paid Projects Total")
   - Projects awaiting PO (count of "Awaiting PO" status)

3. **Present organized dashboard**
   ```
   📊 MOK MUSIC PROJECT STATUS - [Current Date]

   💰 FINANCIAL OVERVIEW
   • Outstanding: $X,XXX (X projects)
   • Current Projects: $X,XXX (X projects)
   • Completed & Paid: $X,XXX (X projects)
   • Awaiting PO: X projects

   🎵 ACTIVE PROJECTS
   [Project Name] - [Status] - $[Amount] - [Days since submission]

   ⚡ NEXT ACTIONS
   • [Specific actions based on project statuses]
   ```

4. **Identify urgent items**
   - Projects over 30 days in "Invoiced" status
   - Projects missing PO numbers
   - APRA registrations marked "Check" or "Not Done"

## Context
This command provides Harry with a complete MOK Music business overview, helping prioritize follow-ups, identify cash flow issues, and track project progress with ESM.
