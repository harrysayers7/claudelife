---
Done: false
today: false
follow up: false
this week: false
back burner: false
type: Task
status:
relation:
description:
effort:
ai-assigned: true
ai-ignore: false
priority:
---
Ive added property field in the task template that is a list property that will assign to a certain agent claudelife
#### need to figure out if this is even possible

Perform a /quick-search aboit using frontmatter to assign a claude sub agent


#### This is the research I found. Please verify:

can claude code agents be triggered by having a agent assignee property in the frontmatter in markdown files?

Yes, Claude Code agents can be triggered and configured using properties defined in the frontmatter of Markdown files (specifically YAML frontmatter)[1][2][3]. The agent framework scans the appropriate directories (project-level `.claude/agents/` or user-level `~/.claude/agents/`), and recognizes custom YAML properties such as `name`, `description`, `priority`, `allowed-tools`, and more[1][2]. While standard fields like `name` and `description` are required, you are free to add additional properties such as an `assignee` or any custom field you want in the frontmatter.

### How Agent Triggering Works
Claude Code selects and invokes sub-agents based on several factors extracted from frontmatter and context, including:
- Task description matching to the agent's description
- Available tools specified for the agent
- Current project context and matching agent scope
- Agent priority and explicit mentions in workflow or commands[1][4].

If you define an `agent-assignee` property (or similar) in frontmatter, that data is available for triggers, routing, or filtering agents; for example:
```
---
name: performance-optimizer
agent-assignee: "harry"
description: "Optimizes audio plugin chains for minimal CPU usage"
tools: file_read, file_write
priority: high
---
```
#### Claude Code can reference this property to select or filter agents if your workflow or slash command logic is set up for it[1][3].

### Customization and Automation
The system’s flexibility means you can use any structured property in agent definitions for automation. However, to actively trigger agents by assignee, you either need a workflow or slash command that references that field, or use hooks to automate selection and assignment actions based on frontmatter values[5][6].

### Practical Notes
- The property alone does not trigger agents—your workflow/configuration (via commands, hooks, or automation) must reference it for routing.
- Custom agent frameworks, hooks, or integration scripts can utilize properties like `agent-assignee` to perform smart automation and context management[7][6].

What this means for you: If you want to auto-route tasks or files to agents based on an assignee property in Markdown frontmatter, you can achieve this using Claude Code’s agent framework in combination with hooks or slash commands. With your expertise in agency automation, you may want to design workflows that leverage these flexible metadata fields for dynamic agent assignment, making your creative and security processes more streamlined[1][5][6].

Citations:
[1] How Claude Code's Sub Agents Transform Task Management https://htdocs.dev/posts/revolutionizing-ai-development-how-claude-codes-sub-agents-transform-task-management/
[2] Claude Code's Custom Agent Framework Changes ... https://dev.to/therealmrmumba/claude-codes-custom-agent-framework-changes-everything-4o4m
[3] Custom agents with Claude Code and Otto https://www.ascend.io/blog/custom-agents-with-claude-code-and-otto
[4] Claude Code Workflows & Agents https://github.com/wshobson/agents
[5] A developer's guide to Claude Code workflow automation ... https://www.eesel.ai/blog/claude-code-workflow-automation
[6] How I use Claude Code (+ my best tips) https://www.builder.io/blog/claude-code
[7] Automate Your AI Workflows with Claude Code Hooks https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks
[8] Streamline Your Coding Workflow with Claude Code Sub ... https://joshuaberkowitz.us/blog/news-1/streamline-your-coding-workflow-with-claude-code-sub-agents-647
[9] Claude Code now supports Custom Agents : r/ClaudeAI https://www.reddit.com/r/ClaudeAI/comments/1m8ik5l/claude_code_now_supports_custom_agents/
[10] Subagents https://docs.claude.com/en/docs/claude-code/sub-agents
[11] Claude Code: Best practices for agentic coding https://www.anthropic.com/engineering/claude-code-best-practices
[12] [BUG] Claude Code subagent YAML Frontmatter ... https://github.com/anthropics/claude-code/issues/8501
[13] Building Agents with Claude Code's SDK https://blog.promptlayer.com/building-agents-with-claude-codes-sdk/
[14] Tip: Managing Large CLAUDE.md Files with Document ... https://www.reddit.com/r/ClaudeAI/comments/1lr6occ/tip_managing_large_claudemd_files_with_document/
[15] How do you make Claude Code (or other AI coding agents) ... https://www.reddit.com/r/ClaudeCode/comments/1mvbcnb/how_do_you_make_claude_code_or_other_ai_coding/
[16] Enabling Claude Code to work more autonomously https://anthropic.com/news/enabling-claude-code-to-work-more-autonomously
[17] Your complete guide to slash commands Claude Code https://www.eesel.ai/blog/slash-commands-claude-code
[18] Cooking with Claude Code: The Complete Guide https://www.siddharthbharath.com/claude-code-the-complete-guide/
[19] How to automate development journaling with Claude Code https://www.devas.life/how-to-automate-development-journaling-with-claude-code/
[20] Common workflows https://docs.claude.com/en/docs/claude-code/common-workflows
