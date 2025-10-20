---
Done: false
today: false
follow up: false
this week: false
back burner: false
ASAP: false
type: Task
status:
relation:
description:
effort:
ai-assigned: false
ai-ignore: false
ai-ask: false
priority:
agent:
---
#### how many agents would you split this into?

#### Was thinking it would be good to add **agent**-**receptionist** for admin and also agent-university


For the **MOKAI business assistant** you described, the most efficient design—aligned with Claude Code best practices—is to **split the current monolithic agent into 5 specialized sub-agents**, coordinated via an orchestrator or the main Claude instance. This mirrors Anthropic’s hierarchical “orchestrator-worker” pattern and avoids context pollution while maintaining strong modular control[1][2][3][4].

### Recommended Agent Architecture

| Agent | Core Focus | Responsibilities | Tools & Access Scope |
|--------|--------------|----------------|-----------------------|
| **Business Strategist** | Long-term growth, partnerships, Indigenous market positioning | Growth forecasting, service expansion, client diversification, strategic planning | Read dashboards, business docs, planning APIs |
| **Financial Controller (Accountant)** | Cash flow, margins, contractor rates, invoices | Financial modeling, budgeting, profitability tracking, Supabase finance data | Supabase access, reporting tools |
| **Compliance Manager** | Risk and government standards | IRAP, Essential Eight, insurance, DISP workflows, Supply Nation checks | Read-only access to Operations Guide + compliance docs |
| **Client Engagement Manager** | Proposal prep, tender writing, meeting briefs | Draft tenders, prepare proposals, position Indigenous advantages, capture win/loss analysis | AusTender integration, document template tools |
| **Operations Coordinator** | Daily business and workflow tracking | Diary parsing, task queue review, performance summaries, weekly dashboard updates | File access, task management, n8n workflow integration |

Optional sixth agent for larger automation setups:
- **Technical Service Manager** — focused strictly on cybersecurity service delivery templates and quality assurance.

### How They Interact
- The **main Claude (or an Orchestrator agent)** delegates based on intent detection:
  - Strategic inquiries → Strategist
  - Financial metrics → Controller
  - Compliance/tender specifics → Compliance or Engagement Manager
  - Routine or operational summaries → Operations Coordinator
- Each sub-agent summarizes its result back into a common “MOKAI Dashboard Update” format for context continuity[2][3].

### Why Five Is Optimal
- Mirrors real business departments (strategy, finance, compliance, delivery, operations).
- Preserves clear context isolation and reduces prompt length.
- Enables targeted system prompt tuning and tool permissions per area.
- Allows parallel agent orchestration for complex tasks like tender analysis (e.g., Accountant + Compliance + Strategist working together).

In summary:
The **ideal split is 5 sub-agents**, with a **central orchestrator** coordinating their interactions. This setup maximizes modularity, minimizes context conflicts, and scales seamlessly with future automation or command expansion.

Citations:
[1] Subagents https://docs.claude.com/en/docs/claude-code/sub-agents
[2] Claude Subagents: The Complete Guide to Multi-Agent AI ... https://www.cursor-ide.com/blog/claude-subagents
[3] Claude Code Subagents Enable Modular AI Workflows ... https://www.infoq.com/news/2025/08/claude-code-subagents/
[4] Building Multi-Agent Workflows for Complex Projects https://claudecodeagents.org/blog/multi-agent-workflows
[5] Best practices for Claude Code subagents https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
[6] VoltAgent/awesome-claude-code-subagents https://github.com/VoltAgent/awesome-claude-code-subagents
[7] What custom sub-agents are you building with Claude Code? https://www.reddit.com/r/ClaudeAI/comments/1masyia/what_custom_subagents_are_you_building_with/
[8] Claude Code: Best practices for agentic coding https://www.anthropic.com/engineering/claude-code-best-practices
[9] Building agents with the Claude Agent SDK https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
[10] How I Built a Multi-Agent Orchestration System with Claude ... https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how_i_built_a_multiagent_orchestration_system/
[11] 7 powerful Claude Code subagents you can build in 2025 https://www.eesel.ai/blog/claude-code-subagents
[12] Best Claude Code Agents and Their Use Cases https://www.superprompt.com/blog/best-claude-code-agents-and-use-cases
[13] wshobson/agents - Claude Code Plugins https://github.com/wshobson/agents
[14] Subagents - Claude Code - Coding - Real life benefits https://www.reddit.com/r/ClaudeAI/comments/1mobxyp/subagents_claude_code_coding_real_life_benefits/
[15] AI agents https://www.claude.com/solutions/agents
[16] How we built our multi-agent research system https://www.anthropic.com/engineering/built-multi-agent-research-system
[17] How I Use 10 AI Agents in Claude Code to Build Features ... https://www.youtube.com/watch?v=c68Rqn8PriE
[18] How to add multi-agent systems to your workflow with ... https://www.linkedin.com/posts/mrmarciaong_ai-agent-claude-activity-7381315764764585984-l57J
