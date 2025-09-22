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