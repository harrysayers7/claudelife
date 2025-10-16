---
created: "2025-10-15 03:25"
description: |
  Executes a specific task from the /00-inbox/tasks/ directory that you designate.
  This command:
    - Takes a task filename or description as input
    - Uses Serena to search codebase when needed
    - Implements the task directly (no confirmation unless requested)
    - Marks the task as Done: true upon completion
    - Commits changes to git with descriptive message
examples:
  - /complete-task "Fix authentication bug.md"
  - /complete-task "Install GPT Researcher mcp.md"
  - /complete-task "Create list of my Obsidian plugins.md"
---

# Complete Task

This command executes a specific task from your `/00-inbox/tasks/` directory that you designate, implements it, and marks it complete.

## Usage

```bash
/complete-task "[task-filename.md or task description]"
```

## What This Command Does

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

### Execution Flow

1. **Locate Task File**: Find the specified task in `/00-inbox/tasks/` or subdirectories
   - Match by exact filename (e.g., "Fix authentication bug.md")
   - Check subdirectories like `/00-inbox/tasks/tasks-mokai/` for MOKAI tasks
   - Or match by task content/description if filename not exact

2. **Parse Task Content**: Read the task file to understand requirements
   - Extract frontmatter metadata
   - Read task description from markdown body
   - Check if already `Done: true` (skip if so)

3. **Execute Task Directly**: Implement the task without confirmation
   - Use Serena MCP for codebase exploration if needed
   - Follow established project patterns
   - Apply appropriate tools and techniques
   - Run tests if applicable

4. **Verify Completion**: Ensure task was actually completed
   - Check files were modified/created
   - Verify expected outcomes
   - Validate against task requirements

5. **Mark Complete**: Update task file frontmatter
   - Set `Done: true`
   - Preserve all other frontmatter fields

6. **Commit to Git**: Save progress with descriptive commit
   ```bash
   git add [modified files] [task file]
   git commit -m "feat: [brief description of what was completed]"
   ```

7. **Report Results**: Provide completion summary
   - What was changed
   - Files modified
   - Any follow-up actions needed

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
ai-assigned: false
---

[Task content/description here]
```

## Process

I'll help you complete the designated task by:

1. **Locate Task File**:
   ```javascript
   // Find task in /00-inbox/tasks/
   // Match by filename or content description
   ```

2. **Parse and Understand Task**:
   - Read frontmatter to check if `Done: true` (skip if already complete)
   - Extract task description from markdown body
   - Identify required actions

3. **Execute Task**:
   - Use Serena MCP for codebase exploration when needed
   - Implement changes following project patterns
   - Use appropriate tools (Edit, Write, Bash, MCP tools)
   - Verify each step completes successfully

4. **Update Task Status**:
   ```javascript
   // Update frontmatter: Done: true
   // Preserve all other fields
   ```

5. **Commit Changes**:
   ```bash
   git add [modified files]
   git commit -m "feat: [description of completed task]"
   ```

6. **Generate Report**:
   - Summary of what was completed
   - Files modified
   - Any follow-up actions or notes

## Confirmation Mode (Optional)

By default, I'll execute tasks directly. If you want confirmation before execution:

```bash
/complete-task "task-name.md" --confirm
```

Or simply state: "Confirm before executing"

## Output Format

### During Execution
```
Located task: [filename]
Task description: [brief description]

Executing task...
✓ Step 1: [action taken]
✓ Step 2: [action taken]
✓ Step 3: [action taken]

Verifying completion...
✓ All checks passed

Updating task status...
✓ Marked Done: true

Committing changes...
[main abc1234] feat: [task description]
 X files changed, Y insertions(+), Z deletions(-)
```

### Final Report
```
Task Completion Summary:
✓ Task: [filename]
✓ Status: Completed successfully

Changes Made:
- [file1.ts]: [description of changes]
- [file2.md]: [description of changes]
- [task-file.md]: Marked Done: true

Git Commit:
✓ Committed: [commit message]

Follow-up Actions:
- [Any recommended next steps, if applicable]
```

## Examples

### Example 1: Installing MCP Server

**Command**: `/complete-task "Install GPT Researcher mcp.md"`

**Task File**: `/00-inbox/tasks/Install GPT Researcher mcp.md`
```yaml
---
Done: false
type: Task
---
Install and configure the GPT Researcher MCP server
```

**Execution**:
1. Locate task file
2. Read task content: "Install and configure GPT Researcher MCP server"
3. Use Serena to check current `.mcp.json` configuration
4. Add GPT Researcher MCP server configuration
5. Update `.claude/settings.local.json` to enable server
6. Verify configuration is valid
7. Update task: `Done: true`
8. Commit: `feat: add GPT Researcher MCP server`

### Example 2: Creating Documentation

**Command**: `/complete-task "Create list of my Obsidian plugins.md"`

**Task File**: `/00-inbox/tasks/Create list of my Obsidian plugins.md`
```yaml
---
Done: false
type: Task
---
Generate a markdown file listing all currently installed Obsidian plugins
```

**Execution**:
1. Locate task file
2. Use Serena to find Obsidian plugin configuration files
3. Read `.obsidian/community-plugins.json`
4. Create formatted markdown list with plugin names
5. Save to appropriate location (confirm with user if not specified)
6. Update task: `Done: true`
7. Commit: `docs: add Obsidian plugins list`

### Example 3: Code Refactoring

**Command**: `/complete-task "Refactor authentication module.md"`

**Task File**: `/00-inbox/tasks/Refactor authentication module.md`
```yaml
---
Done: false
type: Task
effort: high
---
Refactor the authentication module to use environment variables instead of hardcoded values
```

**Execution**:
1. Locate task file
2. Use Serena to find authentication-related files
3. Identify hardcoded values
4. Replace with environment variable references
5. Update `.env.example` with new variables
6. Run tests to verify refactoring works
7. Update task: `Done: true`
8. Commit: `refactor: use env vars in auth module`

### Example 4: Task Already Complete

**Command**: `/complete-task "Update README.md"`

**Task File Status**: `Done: true`

**Execution**:
1. Locate task file
2. Check frontmatter: `Done: true`
3. Skip execution
4. Report: "Task 'Update README.md' is already marked as complete. No action taken."

## Evaluation Criteria

A successful task completion should:

1. **Locate Correct Task**: Find the specified task file in `/00-inbox/tasks/`
2. **Parse Task Accurately**: Correctly understand task requirements from markdown body
3. **Check Completion Status**: Skip if `Done: true` already set
4. **Use Serena When Needed**: Search codebase for relevant files and patterns
5. **Follow Project Patterns**: Implement changes consistent with existing code
6. **Verify Completion**: Ensure task was actually completed before marking done
7. **Update Frontmatter**: Set `Done: true` while preserving other fields
8. **Commit Descriptively**: Create meaningful git commit message
9. **Provide Clear Summary**: Report what was done and files modified
10. **Handle Errors Gracefully**: Report failures clearly without marking task done

## Safety Considerations

- **No Execution Until Located**: Won't execute anything until task file is found and parsed
- **Skip Already Complete**: Tasks with `Done: true` are not re-executed
- **Verify Before Marking**: Only marks `Done: true` if task actually completed
- **Preserve Frontmatter**: All other frontmatter fields remain unchanged
- **Descriptive Commits**: Each completion gets its own meaningful commit message

## Related Resources

- Task template: `/98-templates/task.md`
- Related command: `/sort-tasks` (executes all `ai-assigned: true` tasks)
- Task directory: `/00-inbox/tasks/`
