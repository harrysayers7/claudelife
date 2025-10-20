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
slash-command:
sub-type:
  - idea
tags:
  - graphiti
  - serena
---

---

# 🎯 Alright, Let's Actually Make This Work Then

If Serena + Graphiti are **already installed**, the question isn't *"should I use them?"* — it's **"how do I orchestrate them intelligently?"**

Here's the real implementation strategy:

---

## 🧠Tool Selection Logic**

As your second-brain architect, here's when I should use each tool:

### **🔍 Tool Decision Tree:**

```
USER QUERY ARRIVES
│
├─ About CODE/AUTOMATION in ClaudeLife?
│  └─> Use SERENA
│     - "How does my Templater setup work?"
│     - "Refactor my daily note automation"
│     - "What functions exist in my vault scripts?"
│
├─ About TEMPORAL PATTERNS / RELATIONSHIPS?
│  └─> Use GRAPHITI
│     - "How has my focus changed since October?"
│     - "What projects were affected by my routine change?"
│     - "Show connections between cold exposure and creative output"
│
├─ About SEMANTIC CONTENT in notes?
│  └─> Use PROJECT_KNOWLEDGE_SEARCH
│     - "What did I write about Mokai last week?"
│     - "Find all notes mentioning cybersecurity"
│     - "Summarize my thoughts on AI agents"
│
└─ About EXTERNAL DATA?
   └─> Use SUPABASE / GOOGLE_DRIVE / WEB_SEARCH
      - "Show my spending patterns"
      - "Find that Google Doc about contracts"
      - "What's the latest on Claude API updates?"
```

---

## 🛠️ **Concrete Workflows Using Both Tools**

### **Workflow 1: Pattern-Driven Code Improvement**

**Scenario:** You notice creative output improves after cold exposure

```yaml
Step 1 (Graphiti):
  Query: "Show relationship between cold-exposure and creative-output
          entities over last 90 days"
  Result: Correlation exists - 73% of high-output days followed cold swims

Step 2 (Serena):
  Query: "Analyze current daily note template structure"
  Result: Template captures mood/energy but not pre-session activities

Step 3 (Claude Code + Me):
  Action: Write automation to add "Pre-Work Activity" field to template
  Action: Build Dataview query that surfaces this correlation in dashboard
```

**Outcome:** System evolves based on discovered patterns

---

### **Workflow 2: Knowledge Graph → Automation Loop**

**Scenario:** You want to understand how project completion relates to habits

```yaml
Step 1 (Graphiti):
  Query: "Map entities: [Projects] → [Completion] → [Daily Habits]"
  Result: Projects completed faster when sleep-quality > 7/10

Step 2 (Me + Project Knowledge Search):
  Query: "Find all project notes with completion dates"
  Result: Extract actual timeline data from vault

Step 3 (Serena):
  Query: "Check if sleep tracking automation exists"
  Result: No automated sleep score calculation

Step 4 (Claude Code):
  Action: Write script that calculates sleep quality from daily notes
  Action: Add sleep score to project dashboard Dataview query
```

**Outcome:** Discovered insight → automated tracking → dashboard visibility

---

### **Workflow 3: System Self-Analysis**

**Scenario:** You ask "How can I improve my second brain?"

```yaml
Step 1 (Serena):
  Query: "Analyze ClaudeLife codebase structure and identify unused functions"
  Result: Several Templater scripts exist but aren't called anywhere

Step 2 (Project Knowledge Search):
  Query: "Find mentions of abandoned workflows or unused templates"
  Result: Notes about "weekly review template" that you stopped using

Step 3 (Graphiti):
  Query: "When did weekly review entity stop appearing in notes?"
  Result: Dropped off in September 2024

Step 4 (Me):
  Analysis: "You abandoned weekly reviews. Should we:
            A) Remove the template (declutter)
            B) Redesign it to be easier
            C) Automate parts that felt tedious"
```

**Outcome:** System audits itself and proposes improvements

---

## 📋 **Updated OBSIDIA Decision Protocol**

Here's what I should do when you ask me something:

### **Phase 1: Intent Classification**
```
Is this about:
→ Code/automation mechanics? (Serena territory)
→ Temporal/relational patterns? (Graphiti territory)
→ Content/semantic search? (Project Knowledge territory)
→ External data? (Supabase/Drive/Web territory)
```

### **Phase 2: Multi-Tool Synthesis** (when appropriate)
```
Example Query: "Why am I more productive lately?"

Tool Combo:
1. Graphiti → Check temporal changes in productivity-related entities
2. Project Knowledge Search → Find recent notes mentioning productivity
3. Supabase → Pull cold exposure frequency data
4. Me → Synthesize: "Your productivity increased 23% since you started
   daily cold swims in October. Notes show better focus. Want me to
   analyze the mechanism?"
```

### **Phase 3: Proactive Improvement Suggestions**
```
After answering your question:
→ Did I discover a pattern worth tracking? → Suggest automation
→ Did I find broken workflows? → Propose fixes via Serena + Claude Code
→ Did I see knowledge gaps? → Suggest notes to create
```

---

## 🎯 **Practical Examples (Real Queries You Might Ask)**

### **Example 1: "Analyze my October productivity"**

**My process:**
1. **Graphiti:** Query entities tagged with "productivity" + "October 2024"
2. **Project Knowledge Search:** Find daily notes from October
3. **Supabase:** Pull habit tracking data (cold exposure, exercise)
4. **Synthesis:** "October showed 31% productivity increase. Graphiti shows this correlates with increased cold exposure (18 swims vs 9 in September). Notes mention improved morning focus. Supabase confirms you exercised 6 days/week vs 4 in September."

---

### **Example 2: "Help me refactor my daily note template"**

**My process:**
1. **Serena:** Analyze current template code structure
2. **Project Knowledge Search:** Find recent daily notes to see what you actually fill out
3. **Graphiti:** Check which template fields have temporal data (actually used over time)
4. **Synthesis:** "Your template has 12 fields but you only consistently use 6. The 'Evening Reflection' field hasn't been filled out since August (Graphiti confirms). Serena shows the template code is inefficient. Want me to rebuild it with just the fields you use + better automation?"

---

### **Example 3: "What should I focus on this week?"**

**My process:**
1. **Project Knowledge Search:** Check open projects and deadlines
2. **Graphiti:** Map recent entity relationships (what's connecting to what)
3. **Supabase:** Check if any business metrics need attention
4. **Calendar (MCP):** See time blocks available
5. **Synthesis:** "Your Mokai project has a deadline Friday (vault notes). Graphiti shows you've been researching AI agents heavily this week - that connects to Mokai's automation goals. You have 12 hours of deep work blocks available. Recommendation: Dedicate Monday-Wednesday to Mokai automation buildout, leverage your AI agent research."

---

## ✅ **What You Should Do RIGHT NOW:**

Since they're already installed, let's **audit their current usage**:

### **Quick Health Check:**

Ask me these to test the system:

1. **"Serena: Show me the structure of my ClaudeLife codebase"**
   *(Tests if Serena is properly analyzing your project)*

2. **"Graphiti: What entities exist related to 'cold exposure'?"**
   *(Tests if Graphiti has ingested your vault notes)*

3. **"Show me connections between my morning routine and creative output over the last 60 days"**
   *(Tests if I can orchestrate Graphiti + Project Knowledge Search together)*

---

## 🔧 **Likely Issues to Fix:**

If they're installed but underutilized, it's probably because:

1. **Graphiti isn't ingesting vault notes automatically**
   - Need to set up a watcher that feeds new/updated notes to Graphiti
   - Schema might need tuning (what entities to extract)

2. **Serena is only seeing ClaudeLife code, not vault scripts**
   - Might need to configure Serena to index your Templater/Dataview files

3. **I (OBSIDIA) don't have clear orchestration logic**
   - My system prompt needs explicit rules for when to use each tool
   - Should I update my decision-making framework with the logic above?

---

## **So... What Actually Happens Next?**

Tell me:

1. **Are Serena/Graphiti currently working?** (Can you query them successfully?)
2. **Is Graphiti ingesting your vault notes?** (Does it know about your projects/habits/patterns?)
3. **Do you want me to actively orchestrate them,** or are you doing that manually?

Because if they're installed but dormant, we should either:
- **A)** Configure them properly to integrate with ClaudeLife workflows
- **B)** Uninstall them if they're just sitting there unused

**No point having tools that don't actively serve the second-brain mission.**

What's the actual current state?
