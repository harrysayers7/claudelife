---
Done: true
today: false
follow up: false
this week: false
back burner: false
type: Task
status:
  - urgent
relation:
description:
effort:
ai-assigned: true
date created: Sun, 10 12th 25, 10:40:41 pm
date modified: Sun, 10 12th 25, 10:47:49 pm
---
## here's some questions
- Did sonething in mcp-expert agent break something?
- make sure all permissions set correctly

## Below is some recent reports:

Here are the most recent and relevant user reports and issues (from August to October 2025) regarding the MCP server loading bug in Claude Code:

### GitHub Issue (10 Oct 2025)
- **Title:** Project-scoped MCP servers don't trigger approval prompt
- **Details:** When starting a Claude Code session with `.mcp.json` in the project directory, the expected approval prompt for project-scoped MCP servers never appears. This suggests that the project-level file is either not being read at all or is silently ignored. This was reported just a few days ago, and the issue remains open and unresolved as of October 2025[1].

### Major Open Bug (Aug–Oct 2025)
- **Title:** MCP servers in .claude/.mcp.json not loading properly
- **Summary:** Multiple users confirm that only one or none of the servers load from `.claude/.mcp.json`, even though they all work from a root-level `.mcp.json`. There are at least three duplicate issues and related bug reports, all describing the problem where project-level MCP servers are not respected, causing major workflow problems. Workarounds involve moving everything to the project root or using CLI overrides, but these are not proper fixes[2].

### Reddit Report (Aug 29, 2025)
- **Details:** Users attempting to run `claude mcp list` inside a project with a configured `.mcp.json` file see "No MCP servers configured." The only workaround is to move servers into the global config, echoing frustration and confirming persistent bugs at the project scope[3].

### Other Mentions
- **July–September 2025:** Consistent confirmations on Reddit and GitHub that `.claude/.mcp.json` files (even with `enableAllProjectMcpServers: true`) are silently ignored or load only one server[4][5].
- **CLI Suggestions:** Multiple threads suggest using `claude --strict-mcp-config --mcp-config /path/to/.mcp.json` as a workaround, with mixed effectiveness[2].

**Summary:** This is an unresolved, high-impact bug currently affecting most Claude Code users who attempt to use project-based MCP server configs. The only reliable workaround remains moving or duplicating MCP server definitions to the project root `.mcp.json`[2][3][1].

Citations:
[1] Project-scoped MCP servers don't trigger approval prompt https://github.com/anthropics/claude-code/issues/9189
[2] MCP servers in .claude/.mcp.json not loading properly ... https://github.com/anthropics/claude-code/issues/5037
[3] MCP servers not showing in claude mcp list or /mcp after ... https://www.reddit.com/r/ClaudeAI/comments/1n35e7p/mcp_servers_not_showing_in_claude_mcp_list_or_mcp/
[4] Weird MCP issue using Claude Code, not loading ... https://www.reddit.com/r/ClaudeCode/comments/1mbqa0x/weird_mcp_issue_using_claude_code_not_loading_the/
[5] [BUG] .mcp.json is not read #3321 - anthropics/claude-code https://github.com/anthropics/claude-code/issues/3321
[6] Add MCP Servers to Claude Code with MCP Toolkit https://www.docker.com/blog/add-mcp-servers-to-claude-code-with-mcp-toolkit/
[7] Claude Code - MCP https://learn.netdata.cloud/docs/netdata-ai/mcp/mcp-clients/claude-code
[8] Top 10 Essential MCP Servers for Claude Code (2025 ... https://apidog.com/blog/top-10-mcp-servers-for-claude-code/
[9] [BUG] npx MCP servers fail to load after "claude update" https://github.com/anthropics/claude-code/issues/2731
[10] Figma MCP not working https://forum.figma.com/report-a-problem-6/figma-mcp-not-working-43506
[11] Customize Claude Code with plugins https://www.anthropic.com/news/claude-code-plugins
[12] [BUG] claude won't load mcp config for scope project #6476 https://github.com/anthropics/claude-code/issues/6476
[13] Configuring MCP Tools in Claude Code - The Better Way https://scottspence.com/posts/configuring-mcp-tools-in-claude-code
[14] Remote MCP support in Claude Code https://www.anthropic.com/news/claude-code-remote-mcp
[15] Why MCP Prompts Fail & How to Fix https://www.arsturn.com/blog/why-is-claude-ignoring-your-mcp-prompts-a-troubleshooting-guide
[16] One-click MCP server installation for Claude Desktop https://www.anthropic.com/engineering/desktop-extensions
[17] This MCP FIXES 99% of Claude Code Errors FOR FREE https://www.youtube.com/watch?v=x7aJyavuKL4
[18] Claude Code: Best practices for agentic coding https://www.anthropic.com/engineering/claude-code-best-practices
[19] [BUG] In-process MCP servers bug in Claude Code ... https://github.com/anthropics/claude-code/issues/7279
[20] mcp server not showing up in visual studio but same ... https://developercommunity.visualstudio.com/t/mcp-server-not-showing-up-in-visual-stud/10908945?sort=active
