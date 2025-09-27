Create a new MOK Music project in the ESM Projects database: $ARGUMENTS

## Usage
- Basic: `/mok-music-new-project "Project Name"`
- With fees: `/mok-music-new-project "Project Name" 750 5250`
- Arguments: [project_name] [demo_fee] [award_fee]

## Steps

1. **Parse arguments**
   - Extract project name (required)
   - Extract demo fee (default: 750)
   - Extract award fee (default: 5250)

2. **Create project in Notion ESM Projects database**
   - Database ID: `1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac`
   - Set Name property with project name
   - Set Demo Fee (number)
   - Set Award Fee (number)
   - Set Status to "New Project"
   - Set Date Received to today
   - Set APRA to "Check"

3. **Initialize workflow setup**
   - Log project creation details
   - Provide Notion page URL for quick access
   - Suggest next steps (contract, timeline, resources)

## Example Output
```
✅ Created MOK Music project: "New Track for Agency X"
📊 Demo Fee: $750 | Award Fee: $5,250
📅 Date Received: 2025-01-15
🔗 Notion URL: [project link]

Next Steps:
- Review and finalize contract terms
- Set submission deadline
- Assign resources and schedule
```

## Error Handling
- Validate project name is provided
- Check for duplicate project names
- Handle Notion API errors gracefully
- Provide clear feedback on success/failure
