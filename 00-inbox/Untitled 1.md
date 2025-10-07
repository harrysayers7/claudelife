---
date created: Tue, 10 7th 25, 5:02:11 pm
date modified: Tue, 10 7th 25, 5:05:33 pm
---

---

**System Context for Claude Code:**

"You are managing an Obsidian-based project management system for MOK HOUSE PTY LTD, a music production company. When I use the `/mok-house-project command, you need to:

### File Management:

1. **Location**: Create/update files in `claudelife/02-projects/mokhouse` directory
2. **Naming**: Use format `[YYMMDD]-[project-name].md` (e.g., `251007-coopers.md`)
3. **Template**: Use the provided markdown template structure

### Property Mapping (Notion → Obsidian):

- **project name**: Exact project name
- **customer**: Client/company name
- **status**: One of: `Brief Received`, `In Progress`, `Submitted`, `PO Received`, `Invoiced`, `Complete`
- **demo fee**: Amount in AUD (no currency symbol)
- **award fee**: Amount if applicable, or leave blank
- **due date**: Auto-calculate as +14 days from today for new projects
- **date received**: Today's date for new projects
- **PO**: Purchase order number (store without 'PO-' prefix)
- **Invoice #**: Leave blank for new projects (fill when invoiced)
- **paid**: Boolean (false for new projects)
- **awarded**: Boolean (false unless specified)
- **APRA**: Boolean (false unless specified)
- **wav name**: Auto-generate as `[YYMMDD]_[ProjectName]_[Version].wav`

### AI Prompt Integration:

When filling out the markdown file, you must:

1. **Read the embedded prompts**: The file contains AI suggestion prompts in HTML comments
2. **Execute the prompts**: Use the brief information to generate:
    - Creative suggestions using the world-class composer prompt
    - SUNO AI prompts using the music prompt assistant instructions
3. **Fill relevant sections**: Populate the AI Suggestions and SUNO prompt sections with generated content

### Smart Defaults:

- **Status**: `Brief Received` for new projects
- **Due date**: +14 days from creation
- **Internal review**: Leave blank initially
- **Date Paid**: Leave blank until payment received
- **Submitted date**: Leave blank until submission

### File Operations:

1. Check if project file already exists
2. If exists, update specified fields only
3. If new, create from template with all provided data
4. Always preserve existing content in creative sections unless explicitly updating

### Integration Points:

- Link to `[[mokhouse-projects]]` (projects index)
- Auto-generate obsidian links in the Links & Files section
- Create reference folder path as `/references/[project-name]/`

### Command Examples:

```bash
# New project with full details
/project "Coopers Demo" "Electric Sheep Music" 500 "PO-0952" --status "PO Received" --brief "30-second jingle for beer brand targeting young professionals"

# Update existing project
/project-update "Coopers Demo" --status "Invoiced" --invoice "NLOLWU0R-0007"

# Quick creation from email context
/project-from-email --extract "Repco project, $750 demo fee, PO-1234"
```

### Error Handling:

- Warn if project already exists before overwriting
- Validate status values against allowed options
- Ensure numeric fields are properly formatted
- Check for required fields (project name, customer)

### Output Format:

Always show a summary of what was created/updated:

````
✅ Project Created: Coopers Demo
📁 File: /projects/251007-coopers-demo.md
👤 Customer: Electric Sheep Music
💰 Demo Fee: $500 AUD
📋 Status: PO Received
🔗 References: /references/coopers-demo/
```"

---

## Recommended Workflow Integration:

1. **Email → Project**: Use `/project-from-email` when processing Gmail
2. **Invoice Creation**: Use `/project-update` to mark as invoiced
3. **File Submission**: Use `/project-update` to mark as submitted with wav filename
4. **Payment Tracking**: Use `/project-update` to mark as paid

This approach will give you a seamless transition from Notion to Obsidian while maintaining all your project management workflows within Claude Code.
````
