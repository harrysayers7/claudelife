---
relation:
  - "[[resources]]"
  - "[[97-tags/AI-Research]]"
  - "[[97-tags/claude-code|claude-code]]"
  - "[[YouTube-Video]]"
tags:
description:
type:
date created: Mon, 10 6th 25, 12:41:02 pm
date modified: Mon, 10 6th 25, 1:40:02 pm
---
Here's a guide based on the video "I was using sub-agents wrong... Here is my way after 20+ hrs test" by AI Jason [00:04]:
Understanding Sub-Agents in Claude Code for Context Optimization
The video explains that sub-agents were introduced in Claude Code primarily for context engineering and optimization [02:11]. The initial idea was to prevent the main agent from getting overloaded with context, especially when dealing with large files, which could lead to "compact conversation" commands and a drop in performance [01:05].
How Sub-Agents Help:
 * A sub-agent is assigned a task by the parent agent [01:21].
 * It has the same set of tools as the parent agent, including file reading and searching [01:26].
 * The sub-agent performs its task (e.g., scanning a codebase) and returns a summarized research report to the parent agent [01:49]. This summary, being much smaller, saves tokens and guides the parent agent's next actions [01:59].
Common Pitfalls and Best Practices
The "Wrong" Way:
 * Many users, including the creator, initially tried to use sub-agents for direct implementation (e.g., a "front-end dev agent" and a "backend dev agent") [02:18].
 * This approach fails when corrections are needed because each sub-agent session is contained and has limited context of previous actions or other agents' work [02:48]. The parent agent also lacks detailed information about the sub-agents' actions [03:22].
The "Right" Way (Sub-Agents as Researchers):
 * Consider each sub-agent as a researcher [03:58]. Their primary role is to gather information, plan, and provide summaries, not to directly implement [04:05].
 * Focus on information retrieval and small summaries back to the main conversation thread [04:15].
Designing Specialized Sub-Agents
The video proposes creating expert sub-agents for specific service providers or technologies, such as:
 * Chassis Front-End Expert: Equipped with knowledge about Chassis documentation, best practices, and tools (MCP tool for components, example code, relevant blocks, and design themes) [04:41].
 * Vercel AI SDK Expert: Loaded with the latest Vercel AI SDK documentation (e.g., v5) and migration guides [04:54].
 * Stripe Expert: Familiar with the latest Stripe documentation and tools for complex setups like usage-based pricing [05:00].
Context Management System Using the File System
A key learning from the video is to use the file system as the ultimate context management system [05:24].
 * Instead of storing all tool results in the conversation history (which can consume many tokens), save them to local files (e.g., Markdown files) [05:28].
 * Example: When an agent runs a web scraping tool, save the script content to a local Markdown file instead of directly including it in the conversation history [05:41].
Implementation of this System:
 * doc/cloud folder: Contains a task folder for the context of each feature [05:53].
 * Sub-agents create MD files: Each sub-agent creates Markdown files for their research reports and implementation plans [06:04].
 * Parent agent creates context file: A central context file (e.g., in doc/task/context.md) includes overall project information [06:10].
 * Workflow:
   * Sub-agents read the context file first to understand the project [06:16].
   * After finishing, they update the context file with core steps and save their research report to an MD file in doc [06:27].
   * Other agents can then read these doc files for more context [06:33].
Building Sub-Agents in Claude Code
General Rules for Sub-Agent Creation:
 * Include important documentation directly in the system prompt to ensure adherence to best practices [07:59].
 * Equip them with relevant tools for information retrieval [08:05].
Example - Chassis Front-End Expert Agent:
 * MCP Tools: Utilize specific MCP tools for Chassis components (retrieving components, example code, relevant blocks) [08:11] and design themes [08:24].
 * Global Settings (code.claw.json): Configure the MCP server to include these Chassis tools [08:41].
 * Personal Settings (code.doc.claw): Create a new agent and generate its title, description, and system prompt based on a quick explanation [09:00].
 * System Prompt Customization:
   * Paste documentation directly into the system prompt [09:36].
   * Attach special MCP tools and rules for their usage [09:42].
   * Define a clear goal: "design and propose a detailed implementation plan and never do the actual implementation" [10:11].
   * Instruct the agent to save the design file to doc/cloud/doc once finished [10:22].
   * Specify an output format for the final message, indicating the file to read [10:28].
   * Include rules to always look at the context file first and update it after work [10:43].
   * Add a rule to prevent sub-agents from calling cloud.mcp.client on themselves [10:54].
Example Workflow: Building a ChatGPT Replica [11:49]
 * Project Setup: Initialize a Next.js project with Chassis [11:49].
 * Parent Agent Rules (cloud.md):
   * Parent agent maintains the project plan in doc/task/context.md [12:10].
   * Parent agent updates this file after finishing work [12:22].
   * Sub-agents are delegated tasks and passed the context file name [12:27].
   * Sub-agents read documentation before executing tasks [12:37].
 * Prompt: "Help me build a replica of ChatGPT using Chassis as front end and Vercel as SDKs AI service. Let's firstly build the UI making sure we consult sub agent" [12:42].
 * UI Building Process:
   * Parent agent creates context_session_one.md [12:54].
   * Parent agent triggers the Chassis agent with the context file and specific tasks [12:54].
   * Chassis sub-agent reads the context file and uses MCP tools to design the UI [13:10].
   * Chassis agent creates a doc file detailing the UI design [13:34].
   * Parent agent reads the plan, breaks down implementation, and finishes the UI [13:42].
   * Parent agent updates the context session file [13:54].
   * The implemented UI is high-fidelity and addresses interactions [14:05].
   * Parent agent can then fix any errors, as it has the full context [14:18].
 * Vercel SDK Integration:
   * Prompt: "Let's do the Vercel SDK integration and make sure consult the sub agent" [14:42].
   * Vercel AI SDK implementation planner agent is triggered [14:48].
   * Sub-agent reads the context file and reviews the codebase [14:55].
   * Sub-agent creates a doc file with the implementation plan for Vercel AI SDK [15:00].
   * Sub-agent updates the context session MD file [15:07].
   * Parent agent reads the plan, implements, and continuously updates the context file [15:13].
   * The application then connects to the large language model [15:21].
This guide highlights the importance of using sub-agents for strategic research and planning rather than direct execution, and leveraging the file system for robust context management.
You can find the video at: http://www.youtube.com/watch?v=LCYBVpSB0Wo

YouTube video views will be stored in your YouTube History, and your data will be stored and used by YouTube according to its Terms of Service
