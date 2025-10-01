# Build n8n Workflow: $ARGUMENTS

Invoke the n8n Workflow Automation Agent to systematically plan and build n8n workflows.

## What This Command Does

1. **Loads n8n Expert Context** - Activates specialized agent with n8n, Task Master, and integration knowledge
2. **Clarifies Requirements** - Asks targeted questions about workflow needs
3. **Creates PRD** - Writes comprehensive workflow specification
4. **Generates Task Plan** - Uses Task Master to break down implementation
5. **Gathers Latest Context** - Uses Context7 for up-to-date n8n documentation
6. **Systematic Implementation** - Builds workflow using n8n MCP tools
7. **Tests & Documents** - Validates locally and updates documentation

## How It Works

### Phase 1: Planning
The agent will:
- Analyze your workflow request: "$ARGUMENTS"
- Ask clarifying questions about:
  - Trigger type (webhook, schedule, manual)
  - Data sources and destinations
  - Transformation logic needed
  - Error handling requirements
  - Testing criteria

### Phase 2: Task Master Setup
```bash
# Creates PRD at .taskmaster/docs/n8n-workflow-prd.txt
# Generates tasks with: task-master parse-prd --research
# Analyzes complexity: task-master analyze-complexity
# Expands tasks: task-master expand --all --research
```

### Phase 3: Context Gathering
```bash
# Gets latest n8n docs via Context7
# Checks available n8n nodes
# Verifies integration points (Supabase schema, APIs)
```

### Phase 4: Implementation
```bash
# Works through Task Master tasks systematically
# Uses n8n MCP to create workflows programmatically
# Logs progress: task-master update-subtask
# Marks complete: task-master set-status --done
```

### Phase 5: Testing & Documentation
```bash
# Tests workflow at http://localhost:5678
# Updates 07-context/tech/n8n-local-setup.md
# Provides deployment instructions for production
```

## Example Usage

### Simple Webhook Workflow
```
/n8n-workflow Create webhook that receives Stripe events and logs to Supabase
```

### Scheduled Sync
```
/n8n-workflow Build hourly UpBank transaction sync to Supabase with error handling
```

### ML Pipeline
```
/n8n-workflow Create ML categorization workflow that processes uncategorized transactions with confidence scoring
```

### Complex Multi-Step
```
/n8n-workflow Build anomaly detection workflow that monitors transactions, calculates stats, and sends alerts based on severity
```

## What You'll Get

1. **Complete PRD** - Workflow specification with requirements and success criteria
2. **Task Breakdown** - Detailed implementation plan in Task Master
3. **Working Workflow** - Programmatically created n8n workflow ready to test
4. **Error Handling** - Comprehensive error branches and recovery logic
5. **Documentation** - Updated workflow documentation with IDs and troubleshooting
6. **Testing Guide** - How to test locally and deploy to production

## Integration Points Available

- **Supabase**: Project `gshsshaodoyttdxippwx` - transactions, entities, contacts, invoices
- **UpBank API**: Via `mcp__upbank__*` MCP tools
- **Stripe API**: Direct HTTP node integration
- **ML Pipeline**: Confidence-based categorization (>0.9 auto, 0.7-0.9 review, <0.7 manual)
- **Custom APIs**: Any HTTP-based service

## Prerequisites

Before running this command, ensure:
- [ ] n8n is running locally: `docker-compose up -d` in `/Users/harrysayers/Developer/claudelife`
- [ ] n8n accessible at http://localhost:5678
- [ ] Task Master initialized: `task-master init` (if not already)
- [ ] API credentials in environment variables

## Advanced Options

### With Custom PRD
If you've already written a PRD:
```
/n8n-workflow Use PRD at .taskmaster/docs/my-workflow-prd.txt
```

### Skip Planning (Existing Tasks)
If tasks already exist:
```
/n8n-workflow Continue implementation from task 3.2
```

### Research Mode
For complex workflows needing research:
```
/n8n-workflow Build complex multi-API orchestration workflow (use research mode)
```

## Related Commands

- `/project:tm/status` - Check Task Master progress
- `/project:tm/next` - Get next workflow task to implement
- `/project:tm/show <id>` - View specific task details
- `/project:tm/complexity-report` - View workflow complexity analysis

## Agent Capabilities

The n8n Workflow Automation Agent excels at:
- ✅ Systematic planning using Task Master
- ✅ Research-backed implementation via Context7
- ✅ Production-ready error handling
- ✅ Checkpoint-based resumable syncs
- ✅ Confidence-scored ML routing
- ✅ Multi-API orchestration
- ✅ Comprehensive testing and validation

## Notes

- **Local Testing First**: Always tests in local Docker before production
- **Task Tracking**: All progress logged in Task Master
- **Idempotent Design**: Workflows are safely re-runnable
- **Error Recovery**: Automatic retry and fallback logic
- **Documentation**: Workflow IDs and details automatically documented

---

**Ready to build?** Provide your workflow requirements and the agent will handle the rest systematically using Task Master, Context7, and n8n MCP tools.
