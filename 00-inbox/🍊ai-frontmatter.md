---
date created: Wed, 10 8th 25, 11:44:49 am
date modified: Wed, 10 8th 25, 11:46:06 am
---
### **AI-Optimized Properties**

```yaml
---
# Core Structure
type: reference
area: mokai
category: context
status: active

# AI Context Properties
ai-context: true  # Should AI load this for context?
context-priority: high  # [low|medium|high] - how important for AI understanding
context-scope: [mokai-business, indigenous-procurement, cybersecurity]
last-validated: 2025-10-02  # When was this info last confirmed accurate?

# AI Instruction Properties
ai-role: business-advisor  # What role should AI take with this doc?
ai-instructions: "Use this for all Mokai business decisions"
prompt-template: true  # Is this a reusable prompt?

# Searchability for AI
keywords: [indigenous, prime-contractor, cybersecurity, government]
summary: "One-line summary AI can use for quick context"

# Usage Tracking
used-in-prompts: ["mokai-strategy", "pricing-analysis"]
related-prompts: ["[[mokai-lawyer]]", "[[mokai-accountant]]"]

# Version Control (important for AI accuracy)
supersedes: "[[mokai-context-2024-09]]"
version: 2.1
source-of-truth: true  # Is this the authoritative version?
---
```

### **Most Useful for Claude/AI Tools**

**For Context Loading:**
```yaml
ai-context: true
context-priority: high
context-scope: [topic1, topic2]
```

**Why?** Claude Code or your custom scripts can query: "Load all notes where `ai-context: true` and `context-priority: high`"

**For Role/Instruction Docs:**
```yaml
type: prompt
category: ai-instruction
trigger: "!lawyer"
ai-role: legal-advisor
active: true
```

**Why?** Your instruction-box pattern already uses triggers—these properties make them queryable.

**For Currency/Accuracy:**
```yaml
last-validated: 2025-10-02
source-of-truth: true
supersedes: "[[old-doc]]"
confidence: high
```

**Why?** AI needs to know which docs are current and authoritative.

### **Example: Mokai Context Doc for AI**

```yaml
---
type: reference
area: mokai
category: context
ai-context: true
context-priority: high
context-scope: [business-model, indigenous-ownership, operations]
source-of-truth: true
last-validated: 2025-10-02
confidence: high
description: Current operational state of Mokai - AI should load this for all business queries
keywords: [indigenous, 51%, prime-contractor, cybersecurity, IPP]
---
```

### **Example: AI Instruction Doc**

```yaml
---
type: prompt
category: ai-instruction
trigger: "!lawyer"
ai-role: legal-advisor
active: true
context-priority: critical
requires-context: ["[[mokai-context]]", "[[shareholder-agreement]]"]
description: Legal advisory role for Mokai business decisions
---
```

### **Smart Query Examples**

**In Claude Code or scripts:**
```javascript
// Load all high-priority context
WHERE ai-context = true AND context-priority = "high"

// Get all active prompts
WHERE type = "prompt" AND active = true

// Find current source-of-truth docs
WHERE source-of-truth = true AND archived = false
```

### **Minimal AI-Optimized Set**

```yaml
---
type: reference
area: mokai
category: context
ai-context: true
context-priority: high
last-validated: 2025-10-02
description: What this doc is for AI context
---
```

### **Pro Tips for AI Usage**

1. **`ai-context: true`** - Flags docs AI should actively load
2. **`context-priority`** - Helps AI decide what to load first (token limits!)
3. **`last-validated`** - AI can warn if info is stale
4. **`source-of-truth: true`** - AI knows this overrides conflicting docs
5. **`keywords`** - Improves semantic search in Claude/RAG systems
6. **`summary`** - One-liner AI can use without reading full doc

### **Your Instruction-Box Pattern Enhanced**

```yaml
# mokai-lawyer.md
---
type: prompt
category: ai-instruction
trigger: "!lawyer"
ai-role: legal-advisor
active: true
context-priority: critical
load-context: ["mokai-context", "shareholder-agreement"]
specialization: [contracts, IP, indigenous-law]
---
```

This makes your instruction system **queryable and automatable**—Claude Code could automatically load relevant context based on these properties!
