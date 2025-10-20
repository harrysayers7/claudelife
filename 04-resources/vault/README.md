# Vault

Secure storage for frequently-referenced information organized by entity.

## Structure

- `mokai/` - MOKAI PTY LTD business information
- `mokhouse/` - MOK HOUSE PTY LTD business information
- `personal/` - Personal reference information

## Usage

Use `/vault-add` command to create new vault entries. Sensitive items (API keys, passwords) are automatically added to .gitignore.

## Security

- **Sensitive items**: Automatically git-ignored, never committed
- **Reference info**: Safe to commit (bank details, ABN, public info)
- Files marked `sensitive: true` in frontmatter are protected

## Search

Find vault items by:
- Entity: Search within specific folder (mokai/mokhouse/personal)
- Tags: Filter by frontmatter tags
- Keywords: Full-text search in Obsidian
