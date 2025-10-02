# Git Add and Commit: $ARGUMENTS

Quick git add and commit with message.

## Usage
- `/commit "fix: resolve database connection issue"`
- `/commit "feat: add invoice management system"`
- `/commit "docs: update API documentation"`

## Steps

1. **Stage all changes**:
   ```bash
   git add .
   ```

2. **Create commit with message**:
   ```bash
   git commit -m "$ARGUMENTS"
   ```

3. **Show status**:
   ```bash
   git status
   ```

## Commit Message Format
Follow conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

If no message provided, will prompt for one.

Follow up with questions, would you like to push to main?

## **Serena MCP Usage Rules**

IMPORTANT: Use Serena FIRST before reading files when you need to:
- Understand project structure or architecture
- Find where functionality is implemented
- Search for specific symbols, classes, or functions
- Understand relationships between code components
- Find references to variables, methods, or imports
- Explore unfamiliar codebases before making changes
- Search for patterns across multiple files
