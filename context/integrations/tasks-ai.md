# Tasks-AI Notion Integration

## Database Details
- **Database Name**: Tasks AI
- **Database ID**: bb278d48-954a-4c93-85b7-88bd4979f467
- **Data Source ID**: b105e972-10ba-4c45-b349-0105fd107cca

## Integration Points

### With @task-manager Agent
The task-manager agent should use this as the primary task storage system instead of local files.

### With Predictive Engine
Pattern recognition should analyze:
- Task completion patterns by time/day
- Priority vs actual completion patterns
- Category-based time estimation
- Area-based workload distribution

### With Daily Review
Pull tasks due today and high-priority items for morning briefings.

## Property Schema

### Required Fields
- **Task** (title): string
- **Status**: "Not Started" | "In Progress" | "Blocked" | "Review" | "Done" | "Cancelled"
- **Assigner**: "AI" | "Human"
- **Category**: "Development" | "Research" | "Meeting" | "Admin" | "Review" | "Bug Fix" | "Feature" | "Accounting" | "ESM" | "Coding" | "Mac" | "Education"
- **Priority**: "P0 - Critical" | "P1 - High" | "P2 - Medium" | "P3 - Low" | "P4 - Someday"

### Multi-Select Fields (JSON string format)
- **Tags**: `"[\"urgent\", \"quick-win\", \"technical\", \"documentation\", \"client-facing\", \"internal\", \"blocked\", \"needs-review\"]"`
- **Area**: `"[\"Mokai\", \"Mok Music\", \"Brain\", \"Mac\"]"`

### Optional Fields
- **Notes**: Detailed context
- **Dependencies**: Text description
- **AI Suggested prompt (if necessary)**: Prompt text
- **userDefined:URL**: URL format
- **Completion Checkbox**: "__YES__" | "__NO__"
- **date:Due Date:start**: ISO date format

## Auto-Task Creation Triggers

Based on claudelife interactions:
- Voice commands mentioning "I need to..."
- Document ingestion with action items
- Meeting notes with follow-ups
- Email processing with tasks identified
- Project planning outputs
