---
created: "2025-10-12 11:45"
description: |
  Automates task management by executing AI-assigned tasks and cleaning up old completed tasks.
  This command:
    - Scans /00-inbox/tasks/ for tasks with ai-assigned: true
    - Executes each incomplete ai-assigned task sequentially
    - Verifies completion before marking done: true
    - Deletes completed tasks (done: true) older than 2 weeks
    - Provides summary of failures and deletions
examples:
  - /sort-tasks
---

# Sort Tasks

This command automates task management in your claudelife inbox by executing AI-assigned tasks and cleaning up old completed tasks.

## Usage

```bash
/sort-tasks
```

## What This Command Does

**IMPORTANT**: If individual tasks require codebase exploration (e.g., "refactor authentication module", "add new MCP tool"), use Serena MCP to search through the codebase. If you get any errors using Serena, retry with different Serena tools. Tasks that are self-contained and don't reference the broader codebase won't need Serena.

### Phase 1: Execute AI-Assigned Tasks
1. Runs `./scripts/scan-tasks.sh --json` for instant task filtering (<1 second)
2. Identifies all `.md` files where `ai-assigned: true` in frontmatter
3. Filters out tasks where `ai-ignore: true` (reserved for future work, not ready for execution)
4. Skips tasks that already have `Done: true` (already completed)
5. Executes each eligible ai-assigned task sequentially in the order found
6. Verifies task completion before updating the file
7. Updates frontmatter to set `Done: true` upon successful completion
8. If a task fails or cannot be completed, skips it and continues to the next task

**Performance Optimization**: Using `scan-tasks.sh` script dramatically speeds up task scanning (100+ tasks in <1 second vs 30+ seconds reading individually)

### Phase 2: Clean Up Old Completed Tasks
1. Scans the same directory for all tasks where `done: true` (regardless of `ai-assigned` value)
2. Checks each file's modification date
3. Deletes files that are marked `done: true` AND have a modification date older than 2 weeks from today
4. Provides summary: "Deleted X completed tasks older than 2 weeks"

### Phase 3: Git Commit Changes
1. Stage all modified and deleted task files
2. Create a commit with summary of work completed
3. Commit message format: `chore: auto-sort tasks - completed X tasks, deleted Y old tasks`

## Task File Structure

Tasks in `/00-inbox/tasks/` follow this frontmatter structure:

```yaml
---
Done: false           # Completion status (boolean)
today: false
follow up: false
this week: false
back burner: false
type: Task
status:
relation:
description:
effort:
ai-assigned: false    # If true, AI will execute this task
ai-ignore: false      # If true, skip this task (reserved for future work)
---

[Task content/description here]
```

### Important Notes:
- If `ai-assigned` property doesn't exist in frontmatter, treat as `ai-assigned: false`
- If `ai-ignore: true`, skip this task entirely - it's marked for future work and should not be executed now
- Task content is in the markdown body after the frontmatter
- The `Done` field (capital D) is updated to `true` upon completion

## Process

I'll help you manage your task inbox by:

1. **Get Today's Date**: Establish current date for age calculations

2. **Scan for AI-Assigned Tasks** (Fast Method):
   ```bash
   # Use the scan-tasks.sh script for instant filtering
   ./scripts/scan-tasks.sh --json

   # This returns:
   # - eligible: tasks ready to execute (ai-assigned: true, Done: false, no ai-ignore)
   # - ignored: tasks with ai-ignore: true
   # - done: tasks with Done: true

   # Performance: <1 second vs 30+ seconds reading files individually
   ```

3. **Execute Each Task Sequentially**:
   - Read task file content (body after frontmatter)
   - Parse and understand what needs to be done
   - Execute the task using appropriate tools
   - Verify completion before marking done
   - If successful: Update frontmatter `Done: true`
   - If failed: Log failure reason, skip, continue to next

4. **Clean Up Old Completed Tasks**:
   ```javascript
   // Find all .md files where Done: true
   // Check file modification date
   // If modified > 2 weeks ago: delete file
   // Count deletions
   ```

5. **Commit Changes to Git**:
   ```bash
   # Stage all changes in tasks directory
   git add /Users/harrysayers/Developer/claudelife/00-inbox/tasks/

   # Create descriptive commit message
   git commit -m "chore: auto-sort tasks - completed X tasks, deleted Y old tasks"
   ```

6. **Generate Final Report**:
   - List failed tasks with failure reasons
   - Show deletion summary
   - Confirm git commit

## Output Format

### During Execution
```
Executing AI-assigned tasks...
⊘ Task 1: [filename] - Ignored (ai-ignore: true)
✓ Task 2: [filename] - Completed
✗ Task 3: [filename] - Failed: [reason]
✓ Task 4: [filename] - Completed

Cleaning up old completed tasks...
Deleted 5 completed tasks older than 2 weeks

Committing changes to git...
[main abc1234] chore: auto-sort tasks - completed 2 tasks, deleted 5 old tasks
 7 files changed, X insertions(+), Y deletions(-)
```

### Final Report
```
Task Execution Summary:
- Total AI-assigned tasks found: X
- Ignored (reserved for future): I
- Successfully completed: Y
- Already done (skipped): Z
- Failed: N

Failed Tasks:
1. [filename]: [failure reason]
2. [filename]: [failure reason]

Cleanup Summary:
- Deleted X completed tasks older than 2 weeks (modified before YYYY-MM-DD)

Git Commit:
✓ Changes committed successfully
```

## Examples

### Example 1: Executing a Simple Task

**Task File**: `/00-inbox/tasks/Update documentation.md`
```yaml
---
Done: false
ai-assigned: true
---
Update the README.md file to include new MCP server information
```

**Execution**:
1. Read task content: "Update the README.md file..."
2. Locate README.md using Serena
3. Add MCP server information
4. Verify changes were saved
5. Update frontmatter: `Done: true`

### Example 2: Handling Failed Task

**Task File**: `/00-inbox/tasks/Deploy to production.md`
```yaml
---
Done: false
ai-assigned: true
---
Deploy the latest changes to production server
```

**Execution**:
1. Read task content
2. Attempt to deploy
3. Deployment fails due to missing credentials
4. Log failure: "Deploy to production.md: Missing production credentials"
5. Skip to next task (do NOT mark as done)

### Example 3: Cleanup Old Tasks

**Scenario**: Today is 2025-10-12

**Files to Delete**:
- `task1.md` - Done: true, modified: 2025-09-15 (4 weeks ago) ✓ DELETE
- `task2.md` - Done: true, modified: 2025-10-05 (1 week ago) ✗ KEEP
- `task3.md` - Done: false, modified: 2025-08-01 (10 weeks ago) ✗ KEEP (not done)

**Result**: "Deleted 1 completed task older than 2 weeks"

## Evaluation Criteria

A successful execution should:

1. **Properly Parse Frontmatter**: Correctly identify `ai-assigned`, `ai-ignore`, and `Done` boolean values
2. **Respect ai-ignore Flag**: Skip tasks where `ai-ignore: true` - they're reserved for future work
3. **Execute Tasks in Order**: Process tasks sequentially, not in parallel
4. **Verify Before Marking Done**: Only set `Done: true` if task actually completed successfully
5. **Handle Missing Properties**: Treat missing `ai-assigned` as `ai-assigned: false`, missing `ai-ignore` as `ai-ignore: false`
6. **Skip Completed Tasks**: Don't re-execute tasks already marked `Done: true`
7. **Continue on Failure**: Log failures but continue processing remaining tasks
8. **Accurate Date Calculation**: Correctly calculate 2-week threshold from today's date
9. **Delete Only Eligible Files**: Only delete files with `Done: true` AND modified >2 weeks ago
10. **Provide Clear Summary**: Show counts of completed, failed, ignored, and deleted tasks
11. **Update Frontmatter Correctly**: Preserve all other frontmatter fields when updating `Done` field
12. **Git Commit Success**: Successfully stage and commit all changes with descriptive message

## Safety Considerations

- **No Recursive Deletion**: Only scans `/00-inbox/tasks/` directory, not subdirectories
- **Verification Before Deletion**: Checks BOTH `Done: true` AND modification date before deleting
- **Failure Handling**: Failed tasks are NOT marked as done, preventing premature deletion
- **Sequential Execution**: Tasks executed one at a time to avoid conflicts

## Related Resources

- Task template: `/98-templates/task.md`
- Frontmatter parsing: Use standard YAML parsing
- File operations: Node.js `fs` module or Bash commands
- Date calculations: JavaScript Date object or Bash `date` command
