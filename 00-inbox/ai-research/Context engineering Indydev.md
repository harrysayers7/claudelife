---
description:
relation:
  - "[[97-tags/AI-Research|AI-Research]]"
  - "[[97-tags/claude-code|claude-code]]"
  - "[[YouTube-Video]]"
source:
type: guide
date created: Mon, 10 6th 25, 1:20:41 pm
date modified: Mon, 10 6th 25, 1:39:26 pm
---
Here's a guide based on the video "Elite Context Engineering with Claude Code" by IndyDevDan [00:00]:
Elite Context Engineering with Claude Code: The R&D Framework
The core concept of context engineering for agents like Claude Code revolves around managing the context window – a "precious and delicate resource" [00:38]. The video introduces the R&D Framework: Reduce and Delegate [01:02]. Every technique discussed fits into one or both of these categories.
Level 1: Beginner Context Engineering (Reduce)
 * Be Purposeful with MCP Servers:
   * Problem: Default MCP.json files can automatically load many MCP tools into your agent's context window, consuming a significant amount of tokens (e.g., 24,000 tokens or 12% of the context window) [01:31]. This is wasteful if you're not actively using them [01:41].
   * Solution:
     * Delete MCP.json: Get rid of the default MCP.json file in your codebase [02:12]. This immediately frees up context [02:27].
     * Fire up MCPs by hand: Use claw-smcp config to load specific MCP servers when needed [02:34]. You can also use a specialized config file for specific MCPs (e.g., firecrawl_mcp_server_4k.json to load only the Firecrawl MCP server and limit its context) [02:41].
     * Explicitly reference all needed MCP servers: Be conscious of the state entering your context window [03:12].
 * Context Priming vs. claw.md:
   * Problem with large claw.md files: While claw.md is useful as a reusable memory file, it can grow massive over time (e.g., 23,000 tokens or 10% of the context window) [04:13]. An "always-on" context is not dynamic and doesn't adapt to changing engineering work [05:20].
   * Solution: Context Priming:
     * Trim down claw.md: Reduce your claw.md to contain only "absolute universal essentials" that are 100% needed 100% of the time [08:11]. Keep it slim (e.g., 43 lines, 350 tokens) [05:34].
     * Use dedicated reusable prompts (/prime commands): Context priming uses custom slash commands to set up an agent's initial context window specifically for the task at hand [06:40].
     * Benefits of Priming:
       * Full control over initial context [07:39].
       * Can be tailored for different areas of focus (e.g., /prime bug for bug smashing, /prime chore, /prime feature, /prime CC for Claude Code updates) [07:47].
       * Acts as a "hot-loading memory file" [08:03].
Level 2: Intermediate Context Engineering (Delegate)
 * Using Sub-Agents Properly:
   * Sub-agents create partially forked context windows: When you use Claude Code sub-agents, their system prompts are not directly added to the primary agent's context window [09:48]. This is a massive point for delegation [10:16].
   * Delegating heavy tasks: Sub-agents are ideal for tasks that consume a lot of tokens, such as web scraping [11:12].
   * Example: load AI docs command: A custom command can kick off sub-agents to read and scrape AI documentation URLs. Each sub-agent consumes its own context window for this work, keeping it out of the primary agent's context (e.g., saving 3,000 tokens per sub-agent) [10:32].
   * Limitations:
     * You have to track multiple context windows [13:14].
     * Isolate sub-agent work into one concise prompt and one focused effort [13:26].
     * Information flow: Sub-agents respond back to the primary agent, not directly to you [13:41].
     * Ensure a clean context window for your primary agent before diving into sub-agents [14:02].
 * Context Bundles (Loop Active Context Management):
   * Problem: An agent's context window can "explode" during long-running tasks [15:25].
   * Solution: Claude Code hooks can create a "trail of work" by appending tool calls and their outputs to a log file, creating a context bundle [15:12].
   * How it works:
     * A context bundle is an append-only log of an agent's work, unique by day, hour, and session ID [16:10].
     * It captures read and search commands, giving a 60-70% understanding of what previous agents have done [16:38].
     * Reloading: You can loadbundle into a new Claude Code instance, which will re-prime the agent with the history of the previous agent's work, de-duplicating read commands and creating an understanding of past actions [17:30].
     * Benefits: Allows restarting agents after context overload, provides a story of the agent's work, and quickly remounts instances into a similar state [17:06].
     * Caution: Use selectively, as recording every operation can still overflow the next agent's context [18:53]. It provides a trimmed-down version, not every detail [18:46].
Level 3: Advanced Context Engineering (Primary Multi-Agent Delegation)
 * Running Background Agents:
   * Concept: Delegate work to other primary agents that run in the background [19:14]. This is about creating "on-the-fly" primary agents.
   * Lightweight Implementation: Use a simple reusable custom slash command (e.g., /background.md) to boot up a background Claude Code instance [20:23].
   * Workflow:
     * A background agent is kicked off to perform a specific task (e.g., create a plan) [21:00].
     * The primary agent (you) is "out of the loop" during this process [21:17].
     * The background agent writes its report to a specified file [22:18].
     * Context bundles can track the progress and actions of the background agent [22:59].
     * Once completed, the report file is renamed, signifying task completion [24:02].
   * Benefits: Frees up the primary Claude Code instance, allows for out-of-loop agent coding, and enables many focused agents to do one thing extraordinarily well [20:47].
Conclusion: Measure and Manage
The overarching theme is to measure and manage your agent's context window [27:54]. It's not just about saving tokens, but about spending them properly to avoid wasting time correcting agent mistakes [27:22]. The goal is one-shot, out-of-loop agent coding with minimal attempts.
The video emphasizes that investing in context engineering is a safe bet because language models generally decrease performance as context windows grow [28:28].
You can find the video at: http://www.youtube.com/watch?v=Kf5-HWJPTIE

YouTube video views will be stored in your YouTube History, and your data will be stored and used by YouTube according to its Terms of Service
