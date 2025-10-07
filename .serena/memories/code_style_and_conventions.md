# Code Style and Conventions

## File Organization
- **Configuration files**: Root directory (.mcp.json, .env, package.json, etc.)
- **Scripts**: `scripts/` directory for automation and utilities
- **Context files**: `context/` for system context, `.claude/` for Claude-specific
- **Documentation**: CLAUDE.md (main), README.md, TASKS.md
- **Secrets**: Always use environment variables, never hardcode credentials

## Naming Conventions
- **Scripts**: Kebab-case (e.g., `sync-upbank-enhanced.js`)
- **npm scripts**: Kebab-case (e.g., `sync-upbank`, `system-health`)
- **Directories**: Kebab-case (e.g., `automation-system`, `finance-dashboard`)
- **Config files**: Dot-prefixed for hidden files (e.g., `.mcp.json`, `.gitignore`)

## Documentation Standards
- **Frontmatter**: All markdown files should include date frontmatter
  ```markdown
  ---
  date: "YYYY-MM-DD HH:MM"
  ---
  ```
- **File references**: Use markdown link syntax `[filename](path)` for clickability
- **Code blocks**: Always specify language for syntax highlighting

## Git Practices
- **Conventional commits**: Use semantic prefixes (feat:, fix:, chore:, docs:)
- **Security scanning**: Automated via pre-commit hooks (gitleaks, trufflehog)
- **Branch naming**: Feature branches for new work
- **Commit messages**: Clear, descriptive, reference task IDs when applicable

## Environment Variable Management
- Store all secrets in `.env` (git-ignored)
- Use `.env.example` to document required variables
- Reference via `process.env.VARIABLE_NAME` in Node.js
- MCP server configs can include env vars directly or reference from system
