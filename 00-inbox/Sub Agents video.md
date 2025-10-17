---
date: "{{date}} {{time}}"
relation:
tags:
description:
type: guide
date created: Sun, 10 5th 25, 6:37:13 pm
date modified: Thu, 10 16th 25, 8:36:28 pm
---
##### Here's an instruction guide to implementing Claude Code Sub Agents, based on the provided video:

Implementing Claude Code Sub Agents: A Detailed Guide
#### This guide will walk you through setting up and utilizing Claude Code Sub Agents, focusing on best practices and common pitfalls to avoid.
1. Understanding Claude Code Sub Agents [01:23]
 * Flow of Information: It's crucial to understand how sub-agents interact. Your primary agent prompts the sub-agents, which then perform their work autonomously. Importantly, sub-agents report back to your primary agent, not directly to you, and your primary agent then reports to you [01:37]. This distinction influences how you write your sub-agent prompts.
 * System Prompt, Not User Prompt: When defining a sub-agent, you are writing its system prompt, not a user prompt [03:45]. This defines its top-level functionality and influences what information is available to it.
 * Delegation, Not Direct Prompting: You don't directly prompt your sub-agents. Instead, you write a prompt for your primary agent to delegate tasks to your sub-agents. Think of sub-agents as specialized tools for your primary agent [05:52].
2. Anatomy of a Sub-Agent Prompt [02:18]
### A sub-agent prompt typically includes:
 * Agent Name (Unique ID): A unique identifier for your agent [03:01].
 * Description: This is vital. It communicates to your primary agent when it should call this specific sub-agent [03:07]. Leverage this to instruct your primary agent on how to prompt the sub-agent effectively [22:15].
 * Tools: Specify the particular tools available to this sub-agent [03:14].
 * Sub-Agent Complete: A keyword indicating the sub-agent's completion [03:14].
 * Color: For visual identification in the terminal [03:14].
 * Report Format: Explicitly instruct the sub-agent on how to communicate its findings back to the primary agent [04:11]. For example, "Claude, respond to the user with this message."
### 3. Avoiding Common Mistakes [03:31]
 * Mistake 1: Not understanding it's a system prompt: As mentioned, what you write for a sub-agent is its system prompt, not a user prompt. This impacts how you structure the prompt and what information is available [03:45].
 * Mistake 2: Not understanding who the sub-agent reports to: Sub-agents report to the primary agent, not directly to the user [04:11]. Ensure your report format guides the sub-agent to communicate effectively with the primary agent.
### 4. Problem-Solution-Technology Approach [10:47]
When developing agents, follow this order:
 * Problem: Identify a clear engineering problem.
 * Solution: Design a solution to that problem.
 * Technology: Only then, consider which technology (e.g., Claude Code Sub Agents) can implement your solution.
Example:
 * Problem: Losing track of sub-agent actions in multi-agent coding at scale [11:27].
 * Solution: Add text-to-speech (TTS) to agents so they announce when they're done and what they've accomplished [11:33].
 * Technology: Use Claude Code Sub Agents with Eleven Labs TTS tools to build a "text-to-speech agent" [11:46].
5. Building a Text-to-Speech Agent (Practical Example) [12:07]
 * Identify Required Tools: Use the all tools prompt to list available tools. In this example, textToSpeech and playAudio from Eleven Labs are needed [12:18].
 * Validate Workflow: Before creating the agent, test the individual tool calls in your primary agent's context window to ensure they work as expected [13:06].
 * Utilize a Meta Agent: A "meta agent" can be used to build new agents based on a description of the desired agent [14:11]. This streamlines agent creation.
 * Meta Agent Prompt Structure: When using a meta agent, provide a detailed description of the sub-agent you want to create, including:
   * What it does (e.g., "generate a new complete Claude Code sub-agent configuration file from a user's description") [14:44].
   * When it should be triggered (e.g., "when a user asks you to create a new sub-agent") [14:58].
   * The desired workflow (e.g., "get the current working directory, text to speech, play") [15:14].
 * Refine the Generated Agent: Review and refine the generated sub-agent's configuration:
   * Description: Crucial for informing the primary agent when to call it. Add concrete triggers (e.g., "if they say TTS, TTS summary, use this agent") [17:06].
   * Prompting Instructions: Include instructions for the primary agent on how to prompt this specific sub-agent [18:19]. For example, emphasize that the sub-agent has no prior context from other conversations and should be given clear, concise instructions [18:40].
   * Best Practices: Specify tools the sub-agent should use and should not use (e.g., "run only bash pwd and the 11 labs mcbp tools, don't use any other tools") [19:11].
6. Benefits of Claude Code Sub Agents [21:04]
 * Context Preservation: Each sub-agent operates in its own isolated context, preventing pollution of the main conversation [21:04]. This means a fresh agent instance is booted for each task.
 * Specialized Agent Expertise: You can fine-tune instructions and tools for specific tasks, creating highly specialized agents [22:02].
 * Reusability: Agents can be stored in your repository and reused across your codebase [22:25].
 * Flexible Permissions: You can restrict which tools an agent can call, enhancing security [22:48].
 * Focused Agents: Sub-agents are focused on one task, leading to better performance and fewer mistakes [23:09].
 * Simple Multi-Agent Orchestration: Combine sub-agents with custom slash commands and Claude Code hooks to build powerful, yet simple, multi-agent systems [23:45].
 * Prompt Delegation: Offload prompting work to your primary agent, encoding powerful engineering practices into your prompts and sub-agents [25:14].
7. Issues and Considerations [25:41]
 * Lack of Context History: Because sub-agents have their own isolated context, they lack previous conversation history. You must be explicit when passing information to them [25:41]. Think of it like a one-shot prompt to the sub-agent [26:37].
 * Debugging Challenges: Sub-agents can be harder to debug as you don't get full details of the prompts or parameters for every tool call [26:55].
 * Decision Overload: As the number of agents grows, the primary agent might struggle to decide which sub-agent to call [27:19]. Clear descriptions for when to call a sub-agent are crucial [27:56].
 * Dependency Coupling: Chaining sub-agents can lead to dependencies, where changes in one agent's output format or behavior can break others in the chain [28:07]. Try to keep workflows isolated.
 * No Nested Sub-Agents (Currently): You cannot directly call sub-agents from within other sub-agents [29:01].
8. Key Principle: The Big Three [06:12]
Always remember the "Big Three" in agentic coding: Context, Model, and Prompt. The flow of these elements between different agents is paramount, especially as you scale to multi-agent systems [06:25].
By following these instructions, you can effectively implement and leverage Claude Code Sub Agents to build more powerful and efficient agentic workflows.
Video Link: My Claude Code Sub Agents BUILD THEMSELVES
YouTube video views will be stored in your YouTube History, and your data will be stored and used by YouTube according to its Terms of Service

https://youtu.be/7B2HJr0Y68g?si=7-Q23jtCc6ioV2y-
