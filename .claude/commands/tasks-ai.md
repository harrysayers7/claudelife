# Tasks-AI Commands

## Create Task
/create-task [description]
Template:
```json
{
  "parent": {"data_source_id": "b105e972-10ba-4c45-b349-0105fd107cca"},
  "pages": [{
    "properties": {
      "Task": "[description]",
      "Status": "Not Started",
      "Assigner": "AI",
      "Category": "[auto-detected or prompt user]",
      "Priority": "[based on context]",
      "Tags": "[\"relevant\", \"tags\"]",
      "Area": "[\"detected area\"]",
      "Notes": "[context and details]"
    }
  }]
}
```

## Query Tasks
/my-tasks [filter]
- `today` - Tasks due today
- `urgent` - P0-Critical and P1-High
- `in-progress` - Currently active tasks
- `blocked` - Tasks waiting on dependencies
- `area:mokai` - Tasks for specific area

## Update Task Status
/task-done [task-id]
/task-progress [task-id]
/task-blocked [task-id] [reason]

## Smart Task Detection
Auto-detect task creation opportunities from:
- "I need to..." statements
- Document action items
- Meeting follow-ups
- Email requests
- Voice memos

Ask: "Should I create a task for [detected item]?"

## Priority Intelligence
Auto-assign priority based on:
- Deadline proximity
- Keywords (urgent, critical, asap)
- Project area importance
- Dependencies blocking others

## Area Auto-Detection
- MOKAI: cybersecurity, compliance, government, contracts
- Mok Music: production, recording, SAFIA, composing
- Brain: AI systems, automation, development
- Mac: system setup, maintenance, scripts