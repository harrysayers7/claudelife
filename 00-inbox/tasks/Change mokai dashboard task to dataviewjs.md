---
Done: true
today: true
follow up: false
this week: false
back burner: false
ASAP: false
type: Task
status: done
relation:
description:
effort:
ai-assigned: true
ai-ignore: false
priority:
agent:
  - agent-mokai
---
Use the ultra-think slash command

Remind me to use plan mode before executing this task. Ask me any questions to make sure we build the best system prossible

Change mokai dashboard tasks to Dataviewjs so claude can make separate files for each task which enables you to add more detail into each task even add subtasks within the files content.

1. Create a task template in 98-templates called mokai-task
2. Task properties (please suggest an addition ideas or modifications if you see any):
title: (keep to 2-4)
type: Task
relation: [[mokai]]
priority: urgent, high, low (leave blank if isnt relevant i dont)
status: inbox , next up, in progress, waiting, review, done, archive (if task no longer relevent)
done: check box - if status is done or archive then mark this as true
project:
[project] (name of project or job - this is obviously for when we start actual jobs and would be a wikilink to a project)
client: [client] - would link to a client profile
category: let's discuss this but maybe would be learning, marketing, admin etc
effort: [5]  - a number out of 10 of how much effort can be decimal like 1.5 if really necessary etc so I can sort tasks by effort if I want
impact: how much impact


The dataview must display (from left to right):
Done: check box
Filename (keep to 2-4 word for file name)
Short 4-6 word description

---
### alternative or more advanced approach

Could combine this with the first approach. Also be aware that the below was copied from chat gpt which doesnt have context of our current system

From ChatGPT:


---

🧠 Core Idea

We build Claude’s reasoning around 5 key dimensions from the video:

1. Impact – Short- and long-term effect on your goals.


2. Energy Cost – How much mental energy it needs.


3. Energy Match – When you’re best able to do it.


4. Time Block – Where it fits in your day.


5. Adaptability – Claude can reshuffle tasks dynamically based on your state.




---

🧰 Claude-Optimised Task Frontmatter

Here’s the frontmatter I’d use for each task:

---
title: "Design onboarding automation"
type: "task"
status: "next-up"
category: "Business"         # Business | Learning | Personal
project:
tags:

# 🎯 Impact Matrix
impact_short: 8              # 0–10 short-term importance
impact_long: 9               # 0–10 long-term importance
impact_total: 17             # sum of above (Claude calculates if omitted)

# ⚡ Energy Requirements
energy_cost: 3               # 1 = low | 2 = medium | 3 = high
energy_window: "09:00-11:00" # best time for high-energy work

# 🗓️ Time & Scheduling
due: 2025-10-25
time_block: "Morning Peak"
duration: "2h"
frequency: "once"            # once | daily | weekly | recurring
adaptable: true              # Claude can move this block based on energy state

# 🔁 Dependencies & Context
dependencies: ["Research webhook triggers"]
context: "Laptop"
assigned: "Harry"

# 📈 Reflection & Review
success_criteria: "Workflow triggers automatically from client form"
review_notes: ""
created: 2025-10-15
updated: 2025-10-15
---


---

🧭 How Claude Would Use Each Field

Field	Purpose for Claude

impact_short / impact_long	Lets Claude prioritise tasks not by urgency but by true impact.
impact_total	Claude can sort and surface the top impact tasks automatically.
energy_cost	Helps Claude match tasks to your daily energy cycle.
energy_window	Aligns tasks with your peak focus times.
adaptable	Enables dynamic time-blocking — Claude can reshuffle tasks if your energy dips.
time_block	Claude builds a “flow-aligned” day plan.
dependencies	Lets Claude warn you when prerequisites aren’t met.
success_criteria	Allows Claude to verify outcomes and suggest improvements.



---

🧠 Claude Task Pipeline (Workflow)

Here’s how the full workflow would look:

1. 🧠 Brain Dump – Capture all tasks quickly in an “Inbox” folder. Claude tags them with impact_short, impact_long, and energy_cost.


2. 📊 Prioritise by Impact – Claude calculates impact_total and ranks tasks.


3. ⚡ Match Energy Levels – Claude maps each task’s energy_cost to your daily energy_window.


4. 📅 Build Adaptive Schedule – Claude time-blocks high-impact, high-energy tasks during your peak windows and fills the rest of the day with lower-energy items.


5. 🔁 Real-Time Adjust – If you feel tired, Claude re-orders tasks by energy cost without breaking priorities.


6. 📈 Review Loop – Claude uses success_criteria and review_notes to refine your future planning.




---

🧪 Example – Learning Task

---
title: "Deep dive into Supabase RLS"
type: "task"
status: "next-up"
category: "Learning"
project: "Security Fundamentals"

impact_short: 7
impact_long: 10
impact_total: 17

energy_cost: 3
energy_window: "09:00-11:00"

due: 2025-10-30
duration: "2h"
frequency: "once"
adaptable: true

context: "Laptop"
dependencies: ["Read Supabase docs first"]
success_criteria: "Be able to implement row-level security in a project"
---


---

🧠 Claude Code Prompts You Can Use

“Sort all tasks by impact_total and match them to today’s energy windows.”

“Which tasks require high energy and have the highest impact?”

“Reschedule today’s plan for low energy mode.”

“Show only tasks with impact_total > 14 and energy_cost = 3.”



---
