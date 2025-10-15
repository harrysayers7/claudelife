---
created: "2025-10-15 13:15"
description: |
  Interactive command update assistant for modifying existing slash commands. Features:
    - Updates commands with validation and version tracking
    - Shows diff preview before applying changes
    - Validates structure, frontmatter, and broken links
    - Auto-updates documentation in claudelife-commands-guide.md
    - Flags when Serena memory needs updating
    - Supports both minor edits and major restructuring
    - Maintains version history in frontmatter
examples:
  - /command-update mokai-status "add inbox task scanning"
  - /command-update "improve error handling in research command"
  - /command-update --list
---

# Command Update

This command helps you modify and improve existing slash commands in `.claude/commands/` with comprehensive validation, version tracking, automatic documentation sync, and change previews.

## Usage

```bash
# Update specific command
/command-update {command-name} "description of changes"

# Interactive selection from list
/command-update "description of what needs updating"

# List all commands
/command-update --list
```

## Interactive Process

When you run this command, I will:

1. **Identify the command** to update:
   - If command name provided: Load that command directly
   - If description provided: Show list of matching commands for selection
   - If `--list` flag: Display all available commands with descriptions

2. **Understand your changes**:
   - Clarify whether this is a minor edit (typos, examples) or major restructuring (purpose change)
   - Ask specific questions about:
     - What's changing and why
     - Impact on existing workflows
     - Need for new examples or validation rules
     - Performance considerations

3. **Show change preview**:
   - Display diff of proposed changes
   - Highlight frontmatter updates (version history)
   - Show documentation updates that will be made
   - Request confirmation before applying

4. **Validate modifications**:
   - Verify frontmatter YAML format
   - Check command structure matches template
   - Scan for broken file path references
   - Validate example code syntax

5. **Apply changes and sync**:
   - Update command file with version history
   - Auto-update entry in claudelife-commands-guide.md
   - Flag if Serena memory needs updating
   - Provide summary of what changed

## Input Requirements

Before running this command, prepare:
1. **Command identifier**: Either exact command name (e.g., "mokai-status") or clear description
2. **Change description**: What you want to modify and why
3. **Scope clarity**: Is this fixing bugs, adding features, or restructuring?

## Process

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I'll help you update the command by:

1. **Loading the existing command**:
   - Read current command file from `.claude/commands/`
   - Parse frontmatter to extract current version history
   - Read corresponding documentation from `claudelife-commands-guide.md`

2. **Analyzing proposed changes**:
   - Determine change category: minor edit, feature addition, major restructure
   - Identify sections that need updating
   - Check if companion scripts need updates
   - Verify if change impacts other commands

3. **Generating updated version**:
   - Modify content according to requirements
   - Update frontmatter with version history:
     ```yaml
     created: "2025-10-15 13:15"
     updated: "2025-10-15 14:30"
     version_history:
       - version: "1.1"
         date: "2025-10-15 14:30"
         changes: "Added inbox task scanning feature"
       - version: "1.0"
         date: "2025-10-15 13:15"
         changes: "Initial creation"
     ```
   - Maintain consistent structure and formatting
   - Update examples if behavior changed

4. **Validation checks**:
   - **Structure validation**: Verify all required sections present
   - **Frontmatter validation**: Check YAML syntax and required fields
   - **Link validation**: Scan for broken file references in examples
   - **Code validation**: Verify code block syntax (if present)
   - **Documentation consistency**: Ensure description matches implementation

5. **Preview and confirmation**:
   ```diff
   --- .claude/commands/mokai-status.md
   +++ .claude/commands/mokai-status.md
   @@ -1,6 +1,11 @@
    ---
    created: "2025-10-14 16:00"
   +updated: "2025-10-15 14:30"
   +version_history:
   +  - version: "1.1"
   +    date: "2025-10-15 14:30"
   +    changes: "Added inbox task scanning feature"
    description: |
   -  Daily strategic status command...
   +  Daily strategic status command that reads unprocessed diary notes, scans MOKAI task files...
   ```

6. **Applying updates**:
   - Write updated command file
   - Update `claudelife-commands-guide.md` entry:
     - Modify "What it does" if description changed
     - Update "When to use it" if use cases changed
     - Add "Updated: YYYY-MM-DD" to header if major change
   - Create git commit with descriptive message:
     ```bash
     git add .claude/commands/{command-name}.md
     git add 04-resources/guides/commands/claudelife-commands-guide.md
     git commit -m "docs(commands): update /{command-name} - {brief description}"
     ```

7. **Post-update actions**:
   - Flag if Serena memory needs updating (new patterns, scripts, or workflows)
   - Suggest running `/update-serena-memory` if applicable
   - Provide summary of changes and new capabilities

## Change Categories

### Minor Edits
- Fixing typos or grammar
- Updating examples with better clarity
- Adding clarifying notes
- Correcting file paths

**Updates**: Command file only, quick doc sync

### Feature Additions
- Adding new options or parameters
- Including additional examples
- Expanding validation rules
- Adding companion script integration

**Updates**: Command file, documentation, potentially Serena memory

### Major Restructuring
- Changing command purpose or workflow
- Redesigning interactive process
- Modifying output format significantly
- Updating technical implementation approach

**Updates**: Full command rewrite, comprehensive doc updates, Serena memory update required

## Validation Criteria

### Frontmatter Validation
- ✅ Valid YAML syntax
- ✅ `created` date present and properly formatted
- ✅ `updated` date present if modifications exist
- ✅ `version_history` array properly structured
- ✅ `description` field accurately reflects functionality
- ✅ `examples` array contains valid usage patterns

### Structure Validation
- ✅ Title matches filename pattern
- ✅ Usage section present with bash code block
- ✅ Interactive Process section describes workflow
- ✅ Process section includes Serena reminder
- ✅ Examples section provides concrete use cases
- ✅ Related Resources section (if applicable)

### Content Validation
- ✅ All file path references exist in codebase
- ✅ Code blocks have valid syntax
- ✅ Links to documentation are valid
- ✅ Technical details are accurate
- ✅ Examples demonstrate actual functionality

### Documentation Sync Validation
- ✅ Entry exists in `claudelife-commands-guide.md`
- ✅ Description matches command frontmatter
- ✅ Usage syntax is correct
- ✅ "Updated" date added if significant change
- ✅ Word count under 100 words (guide constraint)

## Examples

### Example 1: Minor Edit - Fix Typos

**Input**: `/command-update mokai-status "fix typos in description"`

**Process**:
1. Load mokai-status.md
2. Identify typos in description section
3. Show diff preview:
   ```diff
   - Daily stratigic status command
   + Daily strategic status command
   ```
4. Update frontmatter with minor version bump
5. Sync to commands guide (no description change)
6. Commit: "docs(commands): fix typos in /mokai-status"

### Example 2: Feature Addition - Add Script Integration

**Input**: `/command-update rename-file "integrate rename-file.sh script for 10x speedup"`

**Process**:
1. Load rename-file.md
2. Confirm understanding: "Adding companion script for batch reference scanning?"
3. Generate updates:
   - Add script performance note to frontmatter
   - Update "What it does" section with speed comparison
   - Add "Performance" section with benchmark
   - Include script usage in examples
4. Show comprehensive diff
5. Update commands guide with performance note
6. Flag Serena memory: "New script pattern: reference scanning optimization"
7. Suggest: "Run `/update-serena-memory` to sync script patterns"
8. Commit: "feat(commands): add rename-file.sh integration to /rename-file (10x speedup)"

### Example 3: Major Restructure - Change Command Purpose

**Input**: `/command-update research "convert to use Context7 MCP instead of GPT Researcher"`

**Process**:
1. Load research.md
2. Confirm: "This changes the research provider - major restructure. Will need to update workflow, examples, and validation rules. Proceed?"
3. Generate full rewrite:
   - Update frontmatter description
   - Rewrite Interactive Process section
   - Update all technical implementation examples
   - Change validation criteria
   - Add Context7-specific error handling
   - Update version to 2.0
4. Show side-by-side comparison
5. Comprehensively update commands guide entry
6. Flag Serena memory: "CRITICAL: Research workflow changed from GPT Researcher to Context7 MCP"
7. Require: "MUST run `/update-serena-memory` immediately"
8. Commit: "refactor(commands): migrate /research to Context7 MCP (breaking change)"

## Output Format

I'll provide:

1. **Change Summary**:
   - Command name and file path
   - Change category (minor/feature/major)
   - Version bump (e.g., 1.0 → 1.1)
   - List of modified sections

2. **Diff Preview**:
   - Unified diff showing all changes
   - Frontmatter updates highlighted
   - Documentation changes shown separately

3. **Validation Results**:
   - ✅ All validation checks passed
   - ⚠️ Warnings (if any)
   - ❌ Errors that need fixing (if any)

4. **Post-Update Actions**:
   - Git commit command executed
   - Serena memory update flag (if needed)
   - Related commands that might need updates

## Evaluation Criteria

A successful command update should:
1. **Maintain consistency**: Follow same template structure as original
2. **Preserve version history**: Track all changes with dates and descriptions
3. **Sync documentation**: Auto-update commands guide accurately
4. **Pass validation**: All structure, link, and syntax checks pass
5. **Improve clarity**: Changes make command more effective or easier to use
6. **Flag memory updates**: Identify when Serena needs context refresh
7. **Show clear diffs**: Preview makes changes obvious before applying

## Related Resources

- Command template: [create-command.md](.claude/commands/create-command.md)
- Commands guide: [claudelife-commands-guide.md](04-resources/guides/commands/claudelife-commands-guide.md)
- Serena memory update: [update-serena-memory.md](.claude/commands/update-serena-memory.md)
- Version control best practices: `git log .claude/commands/`

## Starting the Command Update Process

What command would you like to update? Please provide:
- **Command name** (e.g., "mokai-status") OR **description** of what needs updating
- **Change description**: What you want to modify and why
- **Change scope**: Is this a minor edit, feature addition, or major restructure?

I'll load the command, show you a preview of changes, validate everything, and sync documentation automatically.
