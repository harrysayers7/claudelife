# n8n Workflows

## Daily Summary
- **Webhook**: http://134.199.159.190:5678/webhook/daily-summary
- **Triggers**: Every day at 5pm or manual
- **Inputs**: None required
- **Output**: Sends email with summary

## Process Inbox
- **Webhook**: http://134.199.159.190:5678/webhook/process-inbox
- **Triggers**: Manual or every 2 hours
- **Inputs**: email_category (optional)
- **Output**: Sorted emails, created tasks

## Context-Aware Task Creation
- **Webhook**: http://134.199.159.190:5678/webhook/smart-task-creation
- **Triggers**: Email, voice note, or manual input
- **Inputs**: task_description, context_hints (business/personal/technical)
- **Logic**:
  - Analyze input for business keywords (Mokai, clients, cybersecurity)
  - Auto-assign to correct project based on context/business/projects.md
  - Set priority based on context/personal/routines.md
- **Output**: Task created in appropriate system with context tags

## Smart Email Processing
- **Webhook**: http://134.199.159.190:5678/webhook/context-email-processor
- **Triggers**: New emails to monitored addresses
- **Inputs**: Email content and sender
- **Logic**:
  - Check sender against context/business/ profiles
  - Route Mokai emails to business workflows
  - Route personal emails based on context/personal/ settings
- **Output**: Categorized, prioritized, and routed appropriately

## Context Sync
- **Webhook**: http://134.199.159.190:5678/webhook/context-sync
- **Triggers**: Daily at 6am
- **Inputs**: None
- **Logic**:
  - Check for updates in /context directory
  - Sync changes to Graphiti memory
  - Update automation rules based on context changes
- **Output**: Updated memory and automation rules