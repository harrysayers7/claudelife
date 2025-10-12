---
type: brain dump
relation:
tags:
date created: Sun, 10 12th 25, 7:28:28 am
date modified: Sun, 10 12th 25, 7:31:54 am
title: Recommended Frontmatter Schema
---
## Recommended Frontmatter Schema

```yaml
---
# Temporal metadata
created: "2025-10-11T18:45:00+11:00"  # ISO 8601 for parsing
modified: "2025-10-11T19:30:00+11:00"

# Trust & authority (0.0-1.0 scale)
trust_score: 0.95          # How much AI should rely on this
confidence: 0.80           # Author's confidence in accuracy
staleness_days: 7          # Consider stale after N days
authority: "source"        # source|derived|draft|deprecated

# Content classification
content_type: "reference"  # reference|procedure|concept|example|template
domain: ["mokai", "cybersecurity", "business"]  # Array for multi-domain
semantic_tags: ["irap", "essential8", "government-procurement"]

# Context loading rules
load_priority: 95          # 0-100, higher = load first
load_condition: "always"   # always|on-mention|explicit-only
token_budget: 2000         # Estimated token cost
required_for: ["mokai-business-assistant"]  # Which agents need this

# Relationships
depends_on: []             # File paths this relies on
supersedes: []             # Files this replaces
related_systems: ["business-api", "supabase"]

# Lifecycle
status: "active"           # active|draft|review|archived|deprecated
review_date: "2025-11-11"  # When to review/update
---
```

## Why This Works Better

### 1. **Numeric Trust Score** (not labels)

```yaml
# ❌ BAD: Ambiguous labels
ai-treatment: "reference"  # What does this mean numerically?

# ✅ GOOD: Machine-readable confidence
trust_score: 0.85          # AI knows: "Use this, but verify if critical"
confidence: 0.60           # AI knows: "Author unsure, cross-reference"
```

**Semantic meaning:**

- `trust_score: 1.0` → Ground truth, never question
- `trust_score: 0.8-0.95` → Reliable reference
- `trust_score: 0.5-0.79` → Useful context, verify if critical
- `trust_score: < 0.5` → Exploratory only

### 2. **Load Priority + Condition** (explicit control)

```yaml
# MOKAI Operations Guide
load_priority: 95
load_condition: "always"
token_budget: 5000

# MOKAI Learning Flashcards
load_priority: 20
load_condition: "explicit-only"  # Only load if user says "flashcards"
token_budget: 3000
```

AI can now:

- Sort by `load_priority` when context window is tight
- Skip `explicit-only` unless query matches
- Budget tokens using `token_budget` estimate

### 3. **Semantic Tags + Domain** (not categories)

```yaml
# ❌ BAD: Rigid categories
context-mode: "learning"
category: "mokai"

# ✅ GOOD: Flexible semantic graph
domain: ["mokai", "cybersecurity", "compliance"]
semantic_tags: ["irap", "protected-systems", "ism", "government"]
content_type: "procedure"  # Tells AI this is actionable steps
```

Now AI can:

- Match queries to `semantic_tags` (e.g., "IRAP requirements" → loads files with `irap` tag)
- Filter by `domain` intersection (e.g., "MOKAI + cybersecurity")
- Understand `content_type` (procedure vs concept vs example)

### 4. **Authority Hierarchy** (lineage tracking)

```yaml
# Original research
authority: "source"
trust_score: 0.95

# Your notes derived from research
authority: "derived"
depends_on: ["01-areas/business/mokai/docs/research/original.md"]
trust_score: 0.75  # Lower because it's your interpretation

# Draft idea
authority: "draft"
trust_score: 0.40
```

AI understands:

- `source` → Original material, highest trust
- `derived` → Synthesized from sources, check `depends_on` if critical
- `draft` → Exploratory, low trust
- `deprecated` → Don't use (but keep for history)

### 5. **Staleness Tracking** (temporal decay)

```yaml
created: "2025-01-15T09:00:00+11:00"
staleness_days: 30
review_date: "2025-02-15"

# AI can compute:
# days_old = now - created = 270 days
# if days_old > staleness_days → trust_score *= 0.5 (decay factor)
```

This is **huge** for fast-moving domains like cybersecurity where "Essential 8 v3.5" becomes outdated when v3.6 releases.

## Practical Implementation

### Filtering Logic Example

```javascript
function shouldLoadDocument(frontmatter, query, agent) {
  // 1. Check load condition
  if (frontmatter.load_condition === "explicit-only" && !query.match(/flashcard|quiz|study/)) {
    return false;
  }

  // 2. Check domain relevance
  const queryDomains = extractDomains(query);  // ["mokai", "compliance"]
  const overlap = intersection(frontmatter.domain, queryDomains);
  if (overlap.length === 0) return false;

  // 3. Compute effective trust (with staleness decay)
  const daysOld = (Date.now() - new Date(frontmatter.created)) / (1000 * 60 * 60 * 24);
  const decayFactor = daysOld > frontmatter.staleness_days ? 0.5 : 1.0;
  const effectiveTrust = frontmatter.trust_score * decayFactor;

  // 4. Check if agent requires this
  if (frontmatter.required_for?.includes(agent.id)) {
    return true;  // Always load
  }

  // 5. Priority threshold
  return frontmatter.load_priority >= 70 && effectiveTrust >= 0.6;
}
```

### Semantic Search Example

```javascript
function semanticSearch(query, documents) {
  return documents
    .filter(doc => shouldLoadDocument(doc.frontmatter, query, currentAgent))
    .map(doc => ({
      ...doc,
      relevance_score: computeRelevance(query, doc.frontmatter.semantic_tags),
      effective_trust: applyDecay(doc.frontmatter.trust_score, doc.frontmatter.created, doc.frontmatter.staleness_days)
    }))
    .sort((a, b) => {
      // Sort by: relevance × trust × priority
      const scoreA = a.relevance_score * a.effective_trust * (a.frontmatter.load_priority / 100);
      const scoreB = b.relevance_score * b.effective_trust * (b.frontmatter.load_priority / 100);
      return scoreB - scoreA;
    })
    .slice(0, tokenBudgetAllows);
}
```

## Example Templates

### System Documentation (Ground Truth)

```yaml
---
created: "2025-10-11T18:45:00+11:00"
modified: "2025-10-11T18:45:00+11:00"
trust_score: 1.0
confidence: 0.95
staleness_days: 90
authority: "source"

content_type: "reference"
domain: ["automation", "infrastructure"]
semantic_tags: ["hooks", "memory-sync", "claude-code"]

load_priority: 90
load_condition: "always"
token_budget: 3000
required_for: ["mokai-business-assistant"]

status: "active"
review_date: "2026-01-11"
---
```

### Learning Notes (Low Trust)

```yaml
---
created: "2025-10-11T14:00:00+11:00"
modified: "2025-10-11T14:30:00+11:00"
trust_score: 0.45
confidence: 0.60
staleness_days: 14
authority: "draft"

content_type: "concept"
domain: ["mokai", "cybersecurity"]
semantic_tags: ["irap", "learning", "personal-notes"]

load_priority: 30
load_condition: "explicit-only"
token_budget: 1500
required_for: []

status: "draft"
review_date: "2025-10-25"
---
```

### Operations Guide (High Trust)

```yaml
---
created: "2025-09-15T09:00:00+11:00"
modified: "2025-10-10T16:00:00+11:00"
trust_score: 0.95
confidence: 0.90
staleness_days: 30
authority: "source"

content_type: "procedure"
domain: ["mokai", "business", "operations"]
semantic_tags: ["indigenous-procurement", "service-delivery", "compliance"]

load_priority: 95
load_condition: "on-mention"  # Load when "MOKAI" mentioned
token_budget: 8000
required_for: ["mokai-business-assistant"]

status: "active"
review_date: "2025-11-15"
supersedes: ["01-areas/business/mokai/docs/old-operations-v1.md"]
---
```

### Research Paper (Reference)

```yaml
---
created: "2025-10-05T11:00:00+11:00"
modified: "2025-10-05T11:00:00+11:00"
trust_score: 0.80
confidence: 0.85
staleness_days: 180  # Academic research has longer shelf life
authority: "source"

content_type: "reference"
domain: ["cybersecurity", "research"]
semantic_tags: ["essential8", "maturity-model", "asd"]

load_priority: 70
load_condition: "on-mention"
token_budget: 5000
required_for: []

status: "active"
review_date: "2026-04-05"
related_systems: ["business-api"]
---
```

## Key Advantages

1. **Numeric scores** → AI can sort, filter, threshold
2. **Semantic tags** → Flexible keyword matching (not rigid categories)
3. **Staleness decay** → Auto-degrade old content
4. **Token budgeting** → Smart context window management
5. **Authority lineage** → Understand source vs derived
6. **Load conditions** → Explicit control over when to include

## Migration Strategy

Want me to:

1. **Create a frontmatter migration script** that auto-tags existing files based on directory patterns?
2. **Add this schema to CLAUDE.md** with filtering rules?
3. **Update domain pack loader** to use numeric scoring instead of keyword triggers?

This is **machine-first design** - optimized for AI semantic search, not human readability.

Ask before editsmcp__serena__think_about_collected_information tool output (0pa4w1)
