---
created: "2025-10-15 10:15"
description: |
  Launches a specialized Claude Code sub-agent with your specified task description.
  Automatically includes current conversation context and confirms agent activation.
  Supports all available agent types including mokai-business-strategist, trigger-dev-expert,
  mcp-integration-engineer, and others. Streamlines the agent invocation workflow.
examples:
  - /launch-agent mokai-business-strategist "analyze this government tender opportunity"
  - /launch-agent trigger-dev-expert "optimize this task's retry configuration"
  - /launch-agent mcp-integration-engineer "troubleshoot this MCP server connection"
  - /launch-agent general-purpose "research best practices for this implementation"
---

# Launch Agent

This command launches a specialized Claude Code sub-agent with your task description and automatically includes conversation context for seamless handoff.

## Usage

```bash
/launch-agent <agent-type> "<task-description>"
```

## Available Agent Types

### Business & Strategy
- **mokai-business-strategist**: MOKAI business strategy, operations, cybersecurity service delivery, government procurement, Indigenous business development
- **mokai-legal-finance-advisor**: Legal/financial matters for MOKAI (contracts, compliance, Indigenous procurement)
- **agent-mokai**: MOKAI business operations, strategy, compliance, client management
- **agent-mokhouse**: MOK HOUSE PTY LTD business operations and documentation

### Technical Development
- **trigger-dev-expert**: Trigger.dev background jobs, workflows, task design, build extensions
- **mcp-integration-engineer**: MCP server integration, multi-server orchestration, workflow automation
- **fastapi-mcp-specialist**: Building/configuring FastAPI MCP servers using fastapi_mcp library
- **mcp-deployment-orchestrator**: MCP server deployment, containerization, Kubernetes, production operations

### Code Quality & Testing
- **code-reviewer**: Expert code review for quality, security, maintainability (use proactively after writing code)
- **test-engineer**: Test automation, quality assurance, CI/CD testing

### Task Management
- **task-orchestrator**: Coordinate and manage Task Master tasks, handle dependencies, parallel execution
- **task-executor**: Implement/complete specific identified tasks
- **task-checker**: Verify tasks marked 'review' are properly implemented

### Planning & Architecture
- **strategic-planner**: Plan, architect, design solutions without code implementation
- **prompt-engineer**: Expert prompt optimization for LLMs and AI systems

### System & Architecture
- **obsidia**: Claudelife system orchestrator - discover capabilities, design components, troubleshoot integrations, optimize architecture

### General Purpose
- **general-purpose**: Research complex questions, search for code, multi-step tasks

## Process

When you run this command, I will:

1. **Validate Agent Type**: Confirm the agent type exists and is appropriate for your task
2. **Include Context**: Automatically capture current conversation context for seamless agent handoff
3. **Launch Agent**: Invoke the Task tool with:
   - Specified agent type (subagent_type)
   - Your task description (prompt)
   - Automatic context inclusion
4. **Confirm Activation**: Notify you that the agent is now active and ready to work

## Examples

### Example 1: Launch MOKAI Business Strategist

```bash
/launch-agent mokai-business-strategist "Review this government tender for Essential Eight assessment and help draft our Indigenous procurement positioning"
```

**Output**:
```
✓ Launching mokai-business-strategist agent...
✓ Agent is now active and working on your task.
```

### Example 2: Launch Trigger.dev Expert

```bash
/launch-agent trigger-dev-expert "Help me design a video processing workflow with proper retry logic and ffmpeg configuration"
```

**Output**:
```
✓ Launching trigger-dev-expert agent...
✓ Agent is now active and working on your task.
```

### Example 3: Launch MCP Integration Engineer

```bash
/launch-agent mcp-integration-engineer "Troubleshoot why my Gmail MCP server isn't connecting and fix the authentication"
```

**Output**:
```
✓ Launching mcp-integration-engineer agent...
✓ Agent is now active and working on your task.
```

### Example 4: Launch General Purpose Agent

```bash
/launch-agent general-purpose "Research best practices for implementing rate limiting in FastAPI applications"
```

**Output**:
```
✓ Launching general-purpose agent...
✓ Agent is now active and working on your task.
```

## Agent Selection Guide

**Choose based on your task domain:**

| Task Type | Recommended Agent |
|-----------|------------------|
| MOKAI business strategy, tenders, compliance | `mokai-business-strategist` |
| MOKAI contracts, legal docs, procurement | `mokai-legal-finance-advisor` |
| Trigger.dev tasks, workflows, background jobs | `trigger-dev-expert` |
| MCP server setup, integration, troubleshooting | `mcp-integration-engineer` |
| FastAPI MCP server development | `fastapi-mcp-specialist` |
| Code review after implementation | `code-reviewer` |
| Task planning without implementation | `strategic-planner` |
| Complex research or multi-step exploration | `general-purpose` |
| Implementing specific identified tasks | `task-executor` |
| System discovery, architecture design, integration help | `obsidia` |

## Best Practices

1. **Be Specific**: Provide clear, detailed task descriptions for better agent performance
2. **Right Agent**: Choose the most specialized agent for your task domain
3. **Context Matters**: The agent receives conversation context automatically - reference files/code naturally
4. **New Conversations**: For best results, start fresh conversations when launching agents for unrelated tasks
5. **Follow Up**: Once agent is active, continue the conversation naturally - the agent has full context

## Technical Implementation

This command uses Claude Code's Task tool:

```javascript
Task({
  subagent_type: "<agent-type>",
  description: "Brief task summary",
  prompt: `<task-description>

  [Current conversation context automatically included]`
})
```

## Related Commands

- `/create-command`: Create new custom commands
- `/update-serena-memory`: Sync new commands into Serena's knowledge

---

## Command Execution

ARGUMENTS: $ARGUMENTS

Parse the arguments to extract:
1. **Agent Type**: First argument (e.g., `mokai-business-strategist`)
2. **Task Description**: Remaining arguments as the task description

**Valid Agent Types**:
- mokai-business-strategist
- mokai-legal-finance-advisor
- agent-mokai
- agent-mokhouse
- trigger-dev-expert
- mcp-integration-engineer
- fastapi-mcp-specialist
- mcp-deployment-orchestrator
- code-reviewer
- test-engineer
- task-orchestrator
- task-executor
- task-checker
- strategic-planner
- prompt-engineer
- obsidia
- general-purpose

### Steps:

1. **Parse Arguments**: Extract agent type and task description from `$ARGUMENTS`
2. **Validate Agent**: Confirm agent type exists in the valid list above
3. **Launch Agent**: Use the Task tool with:
   - `subagent_type`: The validated agent type
   - `description`: First 3-5 words of task description
   - `prompt`: Full task description with automatic context
4. **Confirm**: Output simple confirmation message

### Error Handling:

- If no arguments provided: Show usage and available agent types
- If invalid agent type: Suggest closest match from valid agents
- If task description missing: Prompt for task description

Now execute the command with the provided arguments.
