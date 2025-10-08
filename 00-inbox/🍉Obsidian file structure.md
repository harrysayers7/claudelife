---
date created: Wed, 10 8th 25, 10:54:28 am
date modified: Wed, 10 8th 25, 10:57:49 am
---


> []
> turn this into a rule in claude code
>

## Property & Tag Strategy for Obsidian

### **Core Principles**

**Properties (Frontmatter)** = Structured metadata for queries and filtering
**Tags** = Cross-cutting themes and concepts for discovery
**Relations** = Explicit connections between specific notes

### **Property Schema**

```yaml
---
type: [document|note|template|artifact|journal|reference]
status: [draft|review|active|archived|complete]
area: [mokai|personal|learning]
category: [context|course|contract|research|deliverable]
relation: ["[[linked-note]]"]
tags: [concept-names]
date created: YYYY-MM-DD
description: Brief summary
---
```

### **When to Use What**

**Use `type` property for:** Document classification (document, note, template, artifact, journal). Properties are better than tags for systematic filtering.

**Use `tags` for:** Concepts (#IRAP, #Essential8), skills (#risk-assessment), action states (#todo, #review), cross-cutting themes. Tags enable flexible discovery across your entire vault regardless of folder location.

**Use `relation` property for:** Parent-child connections, sequential dependencies, explicit links between notes. These create queryable connections and show up in graph view.

**Use `category` property for:** Subtype classification within an area (context, course, contract). Better than folders because documents from different locations can share categories.

### **Your `97-tags` Folder**

Excellent pattern! Keep creating tag index notes (`97-tags/IRAP.md`) for major concepts. Inside each, define the concept, link related notes, and add resources.

### **Quick Decision Tree**

1. **Structural metadata?** → Property (`type`, `status`, `area`)
2. **Global concept/theme?** → Tag
3. **Direct note connection?** → Relation
4. **Classification within area?** → Property (`category`)

### **Key Insight**

Don't use `#context` as a tag—it's too vague. Instead use `type: note` and `category: context` with specific tags like `#indigenous-business` or `#government-contracting` to indicate what the context is about.

This approach keeps structure (properties), flexibility (tags), and connections (relations) cleanly separated and scalable.
