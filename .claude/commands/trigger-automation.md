Trigger an n8n workflow:

Available workflows:
- daily-summary: Generates daily report
- process-inbox: Processes email inbox
- backup-workspace: Backs up all workspaces
- send-update: Sends stakeholder update

Steps:
1. Validate workflow name exists
2. Gather any required parameters
3. Call n8n webhook trigger
4. Log execution in memory/automations.log
5. Report status

Format: /trigger-automation [workflow-name] [parameters]
