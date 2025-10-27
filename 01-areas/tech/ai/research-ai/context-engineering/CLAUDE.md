---
type: context
relation:
  - "[[tech]]"
  - "[[tech]]"
  - "[[deep-research]]"
  - "[[97-tags/context]]"
---
# **Advanced Context Engineering Guide for Claude (Coding & Second-Brain Use Cases)**



## **Prompt Engineering Best Practices**



**Structure Prompts Clearly with Tags:** Claude has been fine-tuned to pay special attention to structured prompts. Use XML-like tags or delimiters to separate different parts of your prompt (context, data, instructions, examples) . For example, you might wrap a long text or code snippet in <text>...</text> tags and place your question or instruction after it. This clearly tells Claude what is content versus what is the task. Always place critical instructions or questions at the **end** of the prompt – Claude gives higher weight to the final instructions, which can **improve response quality by ~30%** on complex long-context tasks .



**Be Explicit, Direct, and Precise:** Clearly state what you want Claude to do _instead_ of what not to do. Claude 2/3 models respond best to affirmative, specific directives rather than vague or negated ones . For instance, rather than saying _“Don’t use a casual tone”_, say _“Use a formal, professional tone.”_ Being concrete about the desired output, format, or style will yield more reliable results. Claude 4 models are more literal and may not “go above and beyond” unless you **explicitly ask** for it . Always include any necessary constraints (e.g. “respond in JSON format” or “limit the answer to 3 bullet points”) directly in the prompt. If you need Claude to possibly admit lack of knowledge, explicitly allow it: _“Only answer if you know; otherwise say you don’t know.”_ – this reduces hallucinations by giving Claude permission to say “I don’t know.”



**Use Few-Shot Examples to Demonstrate:** One of the most effective techniques is providing examples of inputs and ideal outputs (few-shot prompting). Claude will learn from these exemplars and mimic the pattern in its answer . Make sure your examples **truly reflect** the behavior or format you want – Claude pays close attention to the details of examples . For instance, if designing a Q&A assistant, you might show a couple of **User → Assistant** example exchanges that illustrate the desired answer style. This helps with both format and factuality, especially in coding (e.g. showing an example function docstring and its implementation) or workflow-oriented prompts. Keep in mind that more examples improve accuracy **at the cost of tokens and latency** , so balance the number of examples with performance needs.



**Guide the Output Format (Prefill & Templates):** Claude can be verbose by default, often adding unnecessary preambles. You can curb this by pre-defining the desired output structure in the prompt. One trick is to include a partial **assistant response** as a prompt primer to fix the format . For example:

```
System: (empty or role definition)
User: Summarize the main ideas from the article in a 4-bullet list.
<text> {{ARTICLE_TEXT}} </text>
Provide the summary as bullet points, nothing else.
Assistant: →
```

In the above, ending the prompt with **“Assistant: →”** forces Claude to continue from that symbol, ensuring the answer starts in list format rather than with extraneous prose . You can also supply a **template or format section** in the prompt. For instance, provide a <format> block showing the exact layout you expect (e.g. how the bullet points should look, or an example JSON structure). Claude will strive to match that format . Using such scaffolding, along with clear wording like _“Follow the format provided below”_, significantly improves compliance in output formatting .



**Leverage “Thinking” Steps for Complex Tasks:** If a task is complex or multi-step (like coding challenges or logical reasoning problems), it can help to explicitly prompt Claude to reason internally before answering. Claude supports _Chain-of-Thought_-style prompting. You can instruct it to produce a hidden reasoning trace, for example by saying: _“Think through the problem step by step, then give the final answer.”_ Use tags like <thinking>...</thinking> for the thought process and <answer>...</answer> for the final answer . Claude will then output a reasoning section and a separate answer section. The reasoning can be parsed out or omitted from the final user view, but it helps the model arrive at a correct solution . Another approach is using Anthropic’s special keywords: **“think”, “think hard”, “think harder”,** or **“ultrathink.”** These trigger increasing levels of Claude’s internal reasoning budget . For example: _“Before finalizing, think harder about edge cases.”_ – this gives Claude more “time” to reflect. Use the heavier thinking modes only when needed (they consume more tokens and latency) .



**Include Function or Tool Use Cues (when relevant):** For coding tasks or agent-like behaviors, you may want Claude to use a particular tool or call a function. While Claude’s API supports tools via the **Model Context Protocol**, you can also prompt it via examples. If you expect Claude to output a function call, show an example function signature and usage. In Claude Code, you can literally tell it steps like _“Use the_ _gh_ _CLI to fetch issue details”_ or _“Run the tests after writing the function”_, and it will attempt to perform those actions . In general, **enumerating steps** in the prompt (1, 2, 3…) is useful for procedural tasks – Claude will often follow the step-by-step approach in its solution. For instance, a prompt for debugging might say: _“1. Read the error log, 2. Form a hypothesis, 3. Propose a code change, 4. Show the diff.”_ Breaking it down like this guides Claude to produce a structured, stepwise answer or to actually execute those steps if it has tool access.



**Prompt Case Study – Example:** Below is an example prompt pattern combining several of the above techniques for a document summarization task:

```
System: You are an expert technical writer and analyst.
User: You’re the best technical writer in the world. Summarize the main ideas from the report within the <report> tags, focusing on key findings and recommendations.
Only output a 3-bullet-point list of the most important conclusions.

<format>
- Conclusion 1
- Conclusion 2
- Conclusion 3
</format>

<report>
{{REPORT_CONTENT}}
</report>

Assistant: -
```

In this prompt, we set a role (“expert technical writer”), clearly state the task, use XML tags to delineate the report text, provide a format template, and even start the assistant response with a dash to ensure a bullet list format. Such a prompt will reliably yield a concise bulleted summary without extra verbiage. The use of **structured prompting and explicit instructions** is critical for Claude to perform optimally in any scenario .



## **System Message Tuning (Role & Behavior)**



**Leverage the System Role for Contextual Priming:** Claude allows a system message (with the API’s system parameter or via the chat UI’s “Customize Persona” in some versions) where you define its role and persona. This is incredibly powerful for aligning Claude’s behavior with your needs . By assigning a role, you essentially turn Claude into a domain expert or dedicated assistant of a certain kind. For example, a system prompt like _“You are a seasoned data scientist at a Fortune 500 company”_ will prime Claude to respond with that perspective . Compared to a generic assistant, a role-specific Claude will be more accurate, stay on topic, and use appropriate terminology for that role . Official Anthropic guidance notes that role prompting can **boost performance in complex tasks** (like legal or financial analysis) by keeping the model focused and in-character .



**Define Persona, Tone, and Scope in System Prompt:** A good system message not only names the role but also describes _how_ Claude should behave. You can include details about personality, tone, and limits. For instance, setting tone: “You speak in a professional, concise manner with a polite tone,” or behavior: “Always double-check reasoning and never reveal confidential information.” This becomes a persistent guideline. It’s often helpful to list the assistant’s **responsibilities and style** in bullet points within the system prompt . For example, a system prompt for an enterprise chatbot might be:



> _System_: _You are AcmeBot, the enterprise-grade AI assistant for AcmeTechCo. Your role includes:_

> • _Analyzing technical documents (TDDs, PRDs, RFCs) and providing actionable insights for engineering, product, and ops teams._

> • _Maintaining a professional, concise tone at all times._

> _Rules:_

> • _Always reference AcmeTechCo standards or industry best practices in your answers._

> • _If unsure about a question, ask for clarification before proceeding._

> • _Never disclose confidential AcmeTechCo information._  



Such a system message sets a clear character and boundaries. By front-loading these instructions in the system role, you won’t have to repeat them in every user query; Claude will consistently apply them.



**Maintain Consistency and In-Character Responses:** Once a role and style are set, you can further reinforce it by _prefilling_ Claude’s first response or including role indicators. For example, in the prompt you can start the assistant reply with a tag or persona signature (as shown in the Vellum tip: _Assistant: [Jack, the best content writer in the world] →_ to force staying in character ). In long conversations, if Claude starts deviating from the persona, gently remind it of the role by restating key aspects from the system instructions or even resending the system prompt. Anthropic suggests that providing a few **example behaviors or catch-phrases** in the system description can help – basically, “how would a person in this role respond in common scenarios.” For example, define in system prompt: _“If asked about proprietary info, you should respond: ‘I’m sorry, I cannot disclose that.’”_ . This way, even as the conversation grows, Claude is less likely to break character or tone .



**Scope Claude’s Capabilities and Limits:** The system message is also a place to **disable or enable certain capabilities**. If you want Claude _only_ to perform certain tasks, you can say “You only have expertise in X, do not answer questions outside of X.” Conversely, if you want a broad generalist, you might explicitly say “You have a vast knowledge across domains.” Importantly, if using Claude via API with tools (e.g. code execution, browsing), the system message can specify how and when to use those: _“If the user asks for coding help, feel free to write and execute code using the provided tools, but always show the code and results.”_ Keep the scope focused: a tightly scoped system role (e.g. “Python coding assistant specializing in data analysis”) yields more precise assistance than an all-purpose assistant.



**Example – System Prompt for Executive Assistant:** Suppose we want Claude to act as a personal/business “second brain” assistant for a busy professional. A system prompt could be structured as follows:



> **System (Role Prompt):** _You are an efficient AI executive assistant for [Name], a busy entrepreneur. Your primary goal is to enhance [Name]’s productivity and help manage his professional and personal responsibilities_ _._

> **Key Aspects of Your Role:**

> • **Task Management:** Keep track of [Name]’s task lists and project backlogs, update them as tasks are added or completed.

> • **Schedule Organization:** Manage [Name]’s daily planner, ensuring the day is structured effectively (work blocks, meetings, breaks).

> • **Meeting Support:** Prepare agendas before meetings and provide summaries with action items after.

> • **Project Tracking:** Monitor progress on [Name]’s key projects across Company A, Company B, and personal initiatives, reminding of deadlines and next steps.

> • **Information Management:** Organize and retrieve information from [Name]’s notes, documents, and past conversations as needed.

> **Working Style & Rules:**

> • Be proactive in offering suggestions to improve productivity or wellbeing.

> • Keep responses concise and to the point, unless a detailed explanation is requested.

> • Always follow [Name]’s established “Rules of Engagement” document for preferences (e.g. communication style, do-not-disturb hours, etc.).

> • If you are unsure or need confirmation, ask [Name] a clarifying question rather than guessing.

> • **Never disclose private or confidential information** to anyone. Only discuss [Name]’s data with [Name] directly.



This comprehensive system prompt defines the assistant’s identity, duties, and boundaries. It provides role alignment and ensures tone consistency (professional and concise) and it explicitly sets guardrails (like the confidentiality rule). Once this system context is in place, each user request can be shorter, since Claude already “knows” its role and priorities. System tuning in this way is critical for complex, multi-turn interactions – it keeps Claude’s behavior stable and on-mission across a long chat session.



## **Memory Handling and Context Management**



One of Claude’s strengths (especially Claude 2 and Claude 100K context models) is a very large context window, but to use it effectively, you need to manage the context content strategically. Here are best practices for handling long conversations or large data with Claude:



**Utilize the Full Context Window Wisely:** Claude 2 can handle up to 100K tokens (about ~75,000 words) in a single prompt, which is enormous . To get the most from this, **order your prompt wisely**. Always put extensive background materials **at the top** of the prompt, and your specific query or instructions at the bottom . This way, Claude ingests the long content first, and your final question remains fresh in short-term memory when it generates an answer. If you have multiple documents, use structured tags per document, including metadata like titles or sources . For example:

```
<documents>
  <document index="1">
    <source>ProjectProposal.txt</source>
    <document_content>{{PROJECT_PROPOSAL}}</document_content>
  </document>
  <document index="2">
    <source>Requirements.xlsx</source>
    <document_content>{{REQUIREMENTS}}</document_content>
  </document>
</documents>

Analyze the proposal and requirements above. Where are the gaps or risks? Suggest improvements.
```

This XML structure labels each document clearly, which helps Claude navigate large inputs. It’s also a good practice to **ground Claude’s answers in the provided content** – you can literally ask it to quote relevant parts before answering. For instance: “Identify key facts from the documents (quote them) and then give an analysis.” For very long documents, instructing Claude to first extract _“quotes”_ or evidence in an initial step helps it focus . This acts as a _scratchpad_: Claude will pull out the most pertinent snippets and then reason over them, improving recall of important details.



**Chaining Prompts for Long or Complex Sessions:** Instead of pushing the entire task in one giant prompt, break complex workflows into a sequence of prompts (prompt chaining). This is especially useful if the conversation is becoming too lengthy or if multiple distinct tasks are involved. By resetting or summarizing between steps, you **refresh Claude’s focus** and free up context window for the next task. For example, in a research assistant scenario: you might have one prompt to summarize an article, then another prompt (with that summary as input) to ask questions about it. Each link in the chain tackles a subtask with full attention . Chaining is recommended for multi-step processes like _“Gather info → Analyze → Draft → Refine”_ pipelines . It reduces the chance of Claude forgetting earlier instructions or mixing contexts. When chaining, you can carry forward **only the essential information** from one step to the next (e.g. “Key findings from analysis: …” as input for the next prompt). This acts as a rolling summary – maintaining continuity without overloading the context with the entire history.



**Summarize or Reset When Needed:** Even with a large window, there’s benefit in cleaning up context periodically. If a conversation has gone through many turns or detoured significantly, consider summarizing the relevant points and starting a _fresh session_ (or using the /clear command in Claude’s interface for a new chat) . Summarizing can be done by asking Claude to recap: _“Summarize the discussion so far in 5 bullet points,”_ then carry those bullet points into the next prompt as context. This avoids the model being confused by stale or irrelevant content in the older parts of the chat. Developers using Claude’s API sometimes implement an automatic summarizer when the token count exceeds a threshold – archiving older conversation parts into a concise summary that stays in context while discarding the raw verbosity. Anthropic’s own tooling for coding (Claude Code) even provides a /compact command which does exactly this (compacting conversation into notes) . Use these tactics carefully: a summary should preserve key instructions or decisions, and you must update it if new important info comes. If an entirely new task starts, it can be more effective to reset context fully (fresh system prompt and conversation) than to carry irrelevant baggage. _“Don’t use_ _/compact_ _unless you really need the past context”_ is a tip from experienced Claude Code users – fresh starts often yield more focused answers.



**Anchor Important Background Information:** For persistent themes or knowledge (like project details, user profile, coding style guidelines), consider **anchoring them in a reference document** instead of repeating them every time. In the coding domain, Anthropic suggests maintaining a CLAUDE.md in your repo – a file that contains key info about the project (commands, style rules, key facts) which Claude will always load . In a general assistant context, this could be a “User Profile & Preferences” document or a “Knowledge Base” that you either prepend to the conversation or upload to Claude’s workspace (Claude supports a “project knowledge” feature where you can attach documents). By having a curated background doc, you ensure Claude always has that info without you manually re-entering it. Keep such files **concise and relevant**, and update them as needed. For example, the Rules of Engagement document from the earlier Reddit example serves this purpose – it teaches Claude the user’s preferences (formatting, what to avoid) and is updated whenever Claude makes a mistake so it won’t repeat it . Storing long-term facts in a persistent memory doc or the Claude “Memory” feature (for those using the chat app) can greatly enhance continuity. _Tip:_ In Claude’s chat UI, you can actually **view and edit the memory summary** (for Pro/Enterprise versions) which is Claude’s understanding of you and prior chats . Editing that summary is a way to correct any mis-remembered details.



**Use Projects or Separate Threads to Avoid Context Bleed:** If you’re using Claude for distinct topics or roles, separate them. Claude’s memory in the consumer app is segmented by **Projects**, each with its own context memory . Take advantage of this – keep work chats, personal journal chats, coding sessions, etc., in separate projects or chat threads so that information doesn’t leak across them. This also aligns with the principle of “one session, one purpose” which makes context management easier. For instance, have one project for “Coding Assistant – Project X” and another for “Life Organizer Assistant.” This way, when you ask Claude about a code function, it won’t accidentally inject your grocery list from yesterday’s personal chat 😅. On the API side, simply starting a new conversation (no prior messages) when switching tasks achieves the same isolation.



**Monitor the Token Usage:** Always be mindful of how much of the context window is left. If you’re approaching the limit (e.g., tens of thousands of tokens in), it’s time to condense. Claude’s response quality will degrade if it starts to trim earlier parts of the prompt due to length. Tools like Anthropic’s token_count API or third-party libraries can help estimate tokens. Pre-empt large transcripts with something like: _“(The above text is a detailed log. Summarize it if needed due to length.)”_ – Claude can then shorten earlier content to save space if necessary.



**Temporal Context and Updates:** For “second brain” applications, you often feed Claude information that changes over time (today’s schedule, latest progress, etc.). To handle temporal context, make sure to **remove or mark outdated information** in the prompt. For example, if yesterday’s tasks were listed, and you ask Claude today, clarify what’s done versus what’s new. A good practice is maintaining a dated log or using sections like <today> and <yesterday> in the prompt to distinguish time-sensitive info. Always explicitly tell Claude the current date or time reference if relevant (Claude doesn’t have a built-in clock). For scheduling or iterative planning, you might say: _“(Context: It is 2025-09-25. The following tasks are pending as of today…)”_ then list tasks. Then your query: _“Update my planner given the above.”_ Keeping temporal cues explicit prevents Claude from mixing up past and present details.



In summary, treat the context window as a **working memory** that you control. Prune it, refresh it, and feed it with structured, tagged knowledge. The combination of **structured long prompts** (with important data up top, questions at bottom) , plus **prompt chaining** , plus **persistent reference docs** , will let Claude tackle very complex, long-running tasks without losing the thread.



## **Code-Specific Context Engineering**



When using Claude as a coding assistant (Claude 2 and Claude 3 “Claude Code” models), context engineering revolves around providing the right code context and instructions for coding tasks. Claude can read and write large codebases, but you need to guide it effectively:



**Provide Sufficient Code Context:** If you want Claude to generate or modify code, include the relevant code snippets or file contents in the prompt (within code fences or tags). Claude 2 can handle entire source files, but you should still isolate only the necessary parts to avoid running out of context. For example, if asking Claude to refactor a function, show that function (and perhaps its usage or definition) rather than the entire repository. Use filenames or comments to give orientation, e.g.:

````
Here is `database.py`:
```python
# code content here
```
Refactor the `connect()` function in `database.py` to use the new configuration format.
````

This way Claude knows exactly which file and section to focus on. In Anthropic’s Claude Code CLI, simply referencing a file by name (e.g. _“read logging.py”_) will pull it into context . In a custom prompt, doing it manually as above works too. Also consider providing the expected **function signature or usage** if generating a new function, so Claude’s output matches your integration points.



**Be Clear About Code Goals and Constraints:** When prompting for code, explicitly state what the goal is (e.g. improve performance, fix a bug, follow a certain style guide). Claude is much more effective when it knows the success criteria. For instance, _“Optimize this function for speed and ensure memory usage stays < 100MB”_ or _“Rewrite this module to be asynchronous and thread-safe”_. If refactoring legacy code, specify priorities: _“Focus on maintainability and modern coding standards, even if the functionality remains the same.”_ The model will follow those goals. Also mention constraints: _“Do not change public API signatures”_ or _“Keep compatibility with Python 3.8.”_ These act as hard rules in its generation. A case study noted that Claude’s refactoring performs best when you **tell it what matters most** – e.g. are you aiming for performance, security, cleaner architecture, etc., and which parts of the code can be altered aggressively vs. which must remain untouched.



**Use Comments and Pseudo-Code for Guidance:** If you have a particular solution approach in mind, consider describing it to Claude in plain language or pseudo-code **before** asking for the actual code. For example: _“To fix this bug, likely we need to check for null before calling_ _process_data__. Insert that check.”_ or _“I want to use a BFS algorithm here.”_ Claude will take these hints and incorporate them. You can even write a short pseudo-code snippet as part of the prompt; Claude will translate it into proper code. The prompt can mix natural language and code comments to direct the change. Another technique: put _“IMPORTANT:”_ before key instructions in your prompt or CLAUDE.md. Anthropic engineers found that emphasizing crucial instructions (like **“YOU MUST do X”**) in the context improved model adherence .



**Encourage Planning and Self-Checking:** A unique strength of Claude (especially in Claude 2 and onward) is its ability to reason about code changes. You can prompt it to **plan before writing code**. For example: _“Outline the steps or changes you will make, then implement them.”_ This prevents the model from jumping in blindly. In fact, Anthropic’s internal best practice is to **explicitly ask for a plan** in complex coding tasks – it yields better organized solutions . You can adopt a “Think then code” approach: instruct Claude to output a plan in markdown or comments (which you review), and only proceed to code once the plan is approved. In Claude Code’s interactive use, there’s a _Plan Mode_ that does exactly this . Even without that mode, you can simulate it via prompts. Likewise, encourage Claude to _self-review_ its code. After generation, ask: _“Double-check if your solution handles edge cases or potential errors.”_ Claude can then run through a mental checklist and even suggest additional fixes. This kind of prompt chaining – Code -> Review -> Refine – improves reliability, analogous to having the assistant run tests or static analysis in its head.



**Use Test-Driven Prompts for Debugging:** For debugging, give Claude as much context as possible: the code snippet, the error message or incorrect output, and any relevant input that causes the issue. Then prompt something like: _“Why is this error happening? Provide a step-by-step analysis and propose a fix.”_ Claude will often trace through the code in its explanation. You can also invert this: ask Claude to _generate tests first_ for a piece of functionality, then produce code to make them pass (TDD style). Anthropic notes that **test-driven prompts** work very well – e.g. _“Write unit tests for function X (which doesn’t yet handle Y case), then implement the function to make all tests pass.”_ . Claude will follow that multi-turn instruction, effectively debugging by ensuring tests cover the issue and then fixing the code. Remember to tell Claude _not_ to solve it in one go if you want the iterative process (you can say “Don’t write the function implementation yet, just the tests” to enforce the separation ).



**Take Advantage of Claude’s Large Memory for Code:** With large context, you can feed in entire logs or multiple files for context. For example, if a bug spans multiple modules, include the relevant parts of each module in the prompt. Claude 2 can handle not just a single file but an _entire_ project’s key files (100K tokens might equate to dozens of source files). Use this to your advantage for tasks like _“Find the cause of this bug across the codebase”_ – provide a brief description of each module and the code where you suspect the bug might be. However, keep the prompt **organized**: label each file, perhaps with <file name="X.py">...code...</file> tags. This helps Claude navigate and you can then ask something like: _“Does any part of the above code break on null inputs? If so, fix it.”_ Claude will scan through and pinpoint likely spots, thanks to the context.



**Style and Standards:** If you have coding standards or specific frameworks to follow, include those in context. A list of “Coding Guidelines” in the prompt or in CLAUDE.md (e.g. naming conventions, performance tips, etc.) will influence Claude’s output. For instance, _“Use ES6 module syntax, not CommonJS”_ or _“All functions must have a docstring”_ . These can be bullet points in the system or a project doc that Claude sees . Many users keep such guidelines minimal and tweak them over time – if you notice Claude repeatedly doing something undesired, add a rule about it. One tip: If Claude doesn’t obey a guideline, **rephrase it more strongly** (“IMPORTANT: You must do X” as mentioned) to improve compliance .



**Example – Prompt for Code Refactoring:** Here’s a sketch of a prompt that brings together context and instructions for a refactoring task:

````
System: You are a senior Python developer assistant, expert in refactoring code.
User: We have legacy code for a data processor. Below is the code and usage example.
Please refactor it for better maintainability and efficiency.
- Focus on readability and eliminating global state (maintainability).
- Ensure the logic remains **correct** (don’t change outputs).
- Aim to reduce runtime if possible (efficiency), but not at the expense of clarity.
- Use Python 3.10+ features (e.g. dataclasses, f-strings) where appropriate.
<code>
```python
# data_processor.py (legacy snippet)
import csv, json
global_config = {"mode": "FULL", "verbose": False}
# ... 100 lines of legacy code ...
````

````
</code>
<usage>
```python
# Example usage
from data_processor import process_data
result = process_data("input.csv")
```
</usage>
````

First, summarize what the code is doing in high-level steps, then propose specific refactorings, then show the refactored code.

```
In this prompt, we provided the code (truncated for brevity here), an example of how it’s used, and explicitly listed refactoring goals and constraints. We even asked for a summary and plan before code output. Claude, acting as a “senior developer”, would likely output a summary of the code’s function, a list of proposed changes (e.g. “1. Remove global state by passing config as a parameter. 2. Break down the 100-line function into smaller functions…”), and then the new refactored code implementation. All those instructions – given in bullet form – guide Claude’s changes so they align with our priorities.

## Context Engineering for Personal/Executive Assistant Use

Using Claude as a “second brain” or personal/business assistant requires a mix of good system prompt design and clever use of context to keep Claude informed about your life or work. Here’s how to engineer context for these use cases:

**Establish a Detailed Persona and Role (System Context):** As discussed in the system tuning section, start by defining Claude’s role as your personal or executive assistant. But beyond that, feed it the **key background info about you and your world**. This could include a brief bio of yourself (name, profession, major projects), your current priorities, and your general expectations of the assistant. For example: *“You assist John, who runs a tech startup and a non-profit. John’s typical schedule is packed with meetings and coding sessions. You help manage tasks, calendar, notes, and can draft emails or research info as needed.”* If there are recurring entities in your life – e.g. your companies, family members, common project names – mention them so Claude recognizes them. Essentially, onboard Claude with the context a real personal assistant would know. Keep this in a system message or in a persistent project memory so it doesn’t have to be repeated.

**Maintain Dynamic Knowledge Bases:** A second-brain assistant is only as good as the information it has. Leverage Claude’s ability to ingest large documents to give it your notes, plans, and reference materials. For instance, maintain a **“Task Backlog”** document and a **“Daily Planner”** document. The Reddit user example shows multiple backlogs (Company A tasks, Company B tasks, Personal tasks, etc.) which they manage via Claude [oai_citation:81‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=Daily%20Accomplishments%20Journal%3A%20Record%20completed,Task%20Backlogs). You can provide these as part of the prompt (perhaps truncated to what’s pending) or use the Claude Projects “knowledge” feature to attach them. Regularly update these documents with Claude’s help. A great practice is to have Claude update them and then **store the updated version** – e.g., *“Add this new task to the Personal Projects list”* and have Claude output the updated list. Always instruct Claude to output the full updated document rather than something like “(item added)” to avoid confusion [oai_citation:82‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=and%20delete%20previous%20versions%20to,maintain%20accuracy). By iteratively maintaining your to-do lists, notes, meeting minutes, etc., in structured formats (like markdown checkboxes for tasks, tables for schedules, etc.), you create an externalized memory that Claude can draw on.

**Use Artifacts and Project Memory:** If you’re using Claude through the UI, *Projects* allow you to save key documents (artifacts) that Claude will refer to [oai_citation:83‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=I%27ve%20created%20a%20project%20where,Claude%20learns%20from%20each%20interaction). For example, you might have a “Contacts” artifact with names/titles of people you interact with, or a “Company Org Chart” artifact [oai_citation:84‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=Rules%20of%20Engagement%3A%20Adhere%20to,when%20organizing%20tasks%20and%20information). With the API, you’d include those as part of the prompt or retrieve them via a retrieval system. The point is to store relatively static info (or slowly evolving info) externally, and pull it in as needed. The Reddit workflow involved a “Rules of Engagement” doc (preferences) that was updated whenever a new preference was identified [oai_citation:85‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=I%27ve%20created%20a%20project%20where,Claude%20learns%20from%20each%20interaction) – this is an excellent idea. If Claude ever does something not quite to your liking, you edit the rules doc (e.g. “Claude should always format the date as DD/MM/YYYY” or “Claude should not schedule meetings before 8am”). Next time, include that updated rule set in context so Claude adapts. Over time, your assistant becomes increasingly personalized as this knowledge base grows.

**Regularly Update and Clean the Context:** For an ongoing assistant, you’ll be interacting daily. Adopt a routine to update Claude on what happened and what’s next. For example, at end of day, you might prompt: *“Here’s what I accomplished today: ... Please update the task backlog and daily journal.”* [oai_citation:86‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=throughout%20the%20day) Claude can then mark tasks as done, add notes to a “Daily Accomplishments Journal,” etc. Confirm and save those updates to your external docs. At the start of the next day, you might provide Claude with a fresh summary: *“Yesterday’s summary: ... Today’s priorities: ... Now help me plan the day.”* This ensures each day’s context is fresh and relevant. It also prevents Claude from dragging old context forward incorrectly. If something is no longer relevant (a project finished, or a meeting passed), you can remove or archive that info from the active context. Essentially, curate the context like a knowledge garden – weed out old items, keep it current.

**Ask for Recaps and Next Steps:** To ensure continuity, often ask Claude to **recap and propose next steps** at the end of a session. For instance, after a brainstorming session, you might say: *“Summarize the key decisions we made and list any follow-up tasks.”* Save that summary. This summary can then kick off the next session to prime Claude. It’s easier for Claude to continue a train of thought if you give it a synopsis of the previous discussion (unless you are in the *same* chat session, in which case it already has it in context – but if you start a new session the next day, use the saved recap). This approach also helps you as the user, to verify that Claude correctly understood the outcomes. If the summary misses or misstates something, you can correct it right away, preventing error accumulation in long-term memory.

**Keep Conversations Focused:** Even as a personal assistant, try to stick to one topic or task at a time in each prompt. If you jumble multiple requests, Claude might mix up the contexts. It’s better to have a sequence: e.g., first discuss your email draft to a client, then in a new prompt discuss your meeting agenda. You can certainly do multi-topic chats, but be mindful to **reorient Claude with each switch**: *“Now changing topic: let’s talk about my travel itinerary.”* This clears any lingering assumptions from the previous topic.

**Privacy and Safety Considerations:** Since a second brain might handle sensitive info, make use of instructions to **not reveal certain things**. For example, you might include in the system or rules: “If someone other than [Name] somehow asks, you must refuse. Only [Name]’s queries are valid.” Or if you use Claude in contexts where it could produce messages (like drafting emails), double-check that it’s not inadvertently including private info from context in an inappropriate place. Anthropic’s AI is trained to avoid leaking system prompts, but as a user, you should still set clear boundaries in the instructions (like the confidentiality rule we set in the system persona earlier) [oai_citation:87‡docs.claude.com](https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/keep-claude-in-character#:~:text=,information).

**Example – Task Update Interaction:** Imagine it’s the end of day and you want Claude to update your task lists. You could do the following:

- **User:** *“Update: Completed the quarterly report and emailed to the team. Postponed the website redesign task to next week. Had a new idea to improve customer onboarding – added to ideas list. Please update my task backlog and daily log accordingly.”*
- **Assistant:** *(Updates the “Company A Task Backlog” by marking the report task done, updating deadlines, etc., and updates “Daily Accomplishments” log.)* [oai_citation:88‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=throughout%20the%20day) [oai_citation:89‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=One%20of%20the%20most%20critical,to%20confusion%20or%20lost%20information)
- **User:** *“Great, save those changes.”* (You then save the assistant’s output to your files or note system.)

Next morning, you start a new chat:
- **User:** *“Here are my current backlogs and today’s schedule.”* (provide the updated backlog and planner in context, since it’s a new session) *“What should I focus on today and what’s the status of things?”*
- **Assistant:** *“Good morning! Here’s your focus for today...*” (It will use the provided context to generate a plan, knowing what’s done and what’s pending).

This illustrates a cycle of context refresh. By consistently feeding Claude the **latest state** (task lists, etc.), you ensure continuity even across sessions. In fact, Claude Pro now offers a persistent memory summary that it can maintain and edit for you [oai_citation:90‡simonwillison.net](https://simonwillison.net/2025/Sep/12/claude-memory/#:~:text=,time%20by%20chatting%20with%20Claude). If you have access to that, use it – check what Claude has summarized about your past chats via *Settings > View and Edit Memory*. You might find it useful to correct any misunderstandings there. For team use, the memory summary can be shared across team members’ chats too, which is powerful for a common assistant that multiple people use (with proper access controls).

---

**Conclusion:** Context engineering for Claude requires a thoughtful combination of **prompt craftsmanship** and **information management**. Whether you’re prompting Claude to write code or to manage your tasks, remember these key points:

- **Prompts**: Be clear, structured, and example-rich. Use tags and formatting to your advantage. Don’t hesitate to explicitly tell Claude how to think or what format to answer in [oai_citation:91‡vellum.ai](https://www.vellum.ai/blog/prompt-engineering-tips-for-claude#:~:text=1,separate%20instructions%20from%20context) [oai_citation:92‡vellum.ai](https://www.vellum.ai/blog/prompt-engineering-tips-for-claude#:~:text=6).
- **System Context**: Set the stage with a well-crafted system message defining roles, style, and scope [oai_citation:93‡docs.claude.com](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts#:~:text=Why%20use%20role%20prompting%3F) [oai_citation:94‡docs.claude.com](https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/keep-claude-in-character#:~:text=,strong%20foundation%20for%20consistent%20responses). This “personality anchor” will make interactions more consistent and on-target.
- **Long Context Strategies**: When dealing with lots of information, chunk it with structure, put important stuff up front and queries last [oai_citation:95‡docs.claude.com](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/long-context-tips#:~:text=,Claude%E2%80%99s%20performance%20across%20all%20models), use scratchpads/quotes [oai_citation:96‡anthropic.com](https://www.anthropic.com/news/prompting-long-context#:~:text=,not%20seem%20to%20help%20performance), and chain prompts for multi-step workflows [oai_citation:97‡docs.claude.com](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#:~:text=When%20working%20with%20complex%20tasks%2C,tasks%20into%20smaller%2C%20manageable%20subtasks).
- **Coding Use Case**: Give Claude the right code context and be explicit about what to do with it. Encourage it to plan (it can “think harder” when asked) and to verify its solutions [oai_citation:98‡anthropic.com](https://www.anthropic.com/engineering/claude-code-best-practices#:~:text=subagents%2C%20especially%20for%20complex%20problems,ultrathink) [oai_citation:99‡dinanjana.medium.com](https://dinanjana.medium.com/mastering-the-vibe-claude-code-best-practices-that-actually-work-823371daf64c#:~:text=Not%20all%20prompts%20are%20created,%E2%80%9Cultrathink%E2%80%9D). State your quality criteria so it knows what “good” looks like in code.
- **Assistant Use Case**: Treat Claude like an actual assistant – teach it about you, keep it updated, and gradually refine its knowledge. Use external documents as your extended memory and update them through Claude [oai_citation:100‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=I%27ve%20created%20a%20project%20where,Claude%20learns%20from%20each%20interaction) [oai_citation:101‡reddit.com](https://www.reddit.com/r/ClaudeAI/comments/1fnvvtc/leveraging_claude_ai_as_a_personal_assistant_my/#:~:text=Key%20Aspects%20of%20Your%20Role%3A). This creates a virtuous loop where Claude learns and improves over time.

By applying these best practices drawn from Anthropic’s documentation, community experts, and real-world experiments, you’ll harness Claude 2/3’s full potential. Whether it’s acting as an “ultrathinking” coding partner or an ever-organized executive secretary, careful context engineering will make Claude a far more capable and reliable AI assistant in your daily workflows. **Happy prompting!** 🎉


```
