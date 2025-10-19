---
created: "2025-10-18 07:45"
description: |
  Creative systems thinking framework that helps reframe problems from first principles.
  Applies:
    - Multi-level systems analysis (zoom out to higher-order contexts)
    - Assumption challenging and alternate framings
    - Cross-domain analogies from unrelated fields
    - Divergent solution pathway generation with novelty/impact scoring
    - Meta-reflection to uncover blind spots and new directions

  Outputs structured analysis under 600 words with clear markdown sections.
  Works in two modes: apply to current conversation context (no args) or explicit problem (with args).
examples:
  - /rethink
  - /rethink "How to scale consulting without hiring more people"
  - /rethink "Why isn't our automation reducing manual work?"
---

# Universal Creative Rethink

This command applies a creative systems thinking framework to reframe problems, challenge assumptions, and discover unconventional, high-leverage solutions by combining first-principles reasoning, cross-domain insights, and lateral creativity.

## Usage

```bash
# Apply to current conversation context
/rethink

# Apply to explicit problem
/rethink "Your problem description here"
```

## How It Works

**IMPORTANT**: Use Serena to search through the codebase if implementation context is needed. If you get any errors using Serena, retry with different Serena tools.

When you run this command, I will:

1. **Determine context**:
   - If no arguments: Apply framework to current conversation context
   - If arguments provided: Use that as the problem statement
   - If context is vague: Ask up to 3 clarifying questions

2. **Execute the creative rethink framework** through 5 structured steps

3. **Deliver analysis** using exact markdown headers with 2-3 high-leverage insights per section

## The Framework

### Step 1: 🛰️ Zoom Out
**Goal:** Identify the larger system or structure shaping this problem.

- Define which higher-order context this belongs to (economic, cultural, biological, technological, psychological, etc.)
- Example: "Instead of optimizing this app feature → we're really optimizing how humans interact with uncertainty"
- Limit to the **2-3 most significant system layers**

### Step 2: 🧩 Break the Frame
**Goal:** Challenge default assumptions and reveal hidden constraints.

- List at least 3 implicit assumptions guiding the current framing
- For each, briefly test: *What if we reversed it, removed it, or exaggerated it?*
- Present **3 alternate framings**, each tagged as:
  - 🔮 **Wild but Brilliant** – radical, imaginative
  - ⚙️ **Systemic Solution** – structural redesign
  - 💡 **Elegant Shortcut** – simple, leverage-based
  - 🧭 **Counterintuitive Wisdom** – defies common logic

### Step 3: 🔗 Cross-Domain Analogies
**Goal:** Import insight from other fields — without forcing relevance.

- Find **1-2 analogies** from unrelated domains (nature, tech, art, psychology, etc.)
- State clearly: *why the analogy is structurally similar*, not just poetic
- If the analogy is hypothetical, label it as such (e.g., "hypothetical parallel")
- Include a brief **practical lesson** extracted from the analogy

### Step 4: 🚀 Divergent Pathways
**Goal:** Generate 3-5 distinct solution paths and rank them by *novelty × impact*.

| Path | Description | Novelty (1-5) | Impact (1-5) | Distinguishing Assumption |
|------|-------------|---------------|---------------|----------------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

- **Novelty** = originality vs. mainstream solutions
- **Impact** = potential leverage, efficiency, or transformative effect

After listing, label feasibility:
- ⚡ = realistic / testable
- 🧩 = speculative / experimental

**IMPORTANT**: Keep purely theoretical and creative. Do NOT limit to existing tech stack or current constraints. Push beyond conventional approaches.

### Step 5: 🪞 Meta-Reflection
**Goal:** Extract higher-order insights and new directions.

Answer succinctly:
1. Two blind spots uncovered
2. One core assumption overturned
3. One new question worth exploring
4. One actionable experiment or next test

## Output Format

I will use these exact markdown headers for consistent structure:

```markdown
## Zoomed-Out View
## Reframes
## Analogies
## Divergent Pathways
## Meta-Reflection
```

- Each section limited to **2-3 high-leverage insights** (avoid filler or repetition)
- Total output ideally under **600 words**
- Explicit about uncertainty; marked speculative ideas
- No clichés or ungrounded metaphors
- Prioritize leverage, clarity, and truth over quantity
- Always explain *why* an idea is unconventional or breaks the norm

## Serena Memory Integration

After generating analysis, I will:
- Store novel patterns or insights discovered via `mcp__serena__write_memory`
- Update relevant memory files if this rethink reveals systemic patterns
- Tag insights with the problem domain for future reference

## Examples

### Example 1: Apply to Current Conversation

```bash
# During a discussion about automating invoice generation
/rethink
```

I'll apply the framework to the invoice automation context from our conversation, zooming out to payment systems, challenging assumptions about what "automation" means, finding analogies from other domains, etc.

### Example 2: Explicit Problem

```bash
/rethink "Our MCP servers keep failing with authentication errors"
```

I'll reframe the auth problem through systems thinking, challenge assumptions about client-server architecture, explore analogies from other distributed systems, and suggest divergent approaches beyond "fix the auth flow."

### Example 3: Strategic Question

```bash
/rethink "Should we build vs buy for financial analytics?"
```

I'll zoom out to the economics of build/buy decisions, reframe the question beyond binary choice, import insights from other domains, and generate creative third options.

## Constraints

- **Be explicit about uncertainty** - mark speculative ideas clearly
- **Avoid clichés** - no "think outside the box" or vague metaphors
- **Prioritize leverage** - prefer one transformative insight over five incremental tweaks
- **Stay grounded** - creative but logically defensible
- **Explain unconventionality** - always articulate why an idea breaks norms

## Evaluation Criteria

A successful rethink should:
1. **Reveal hidden system layers** - expose the "game behind the game"
2. **Challenge core assumptions** - overturn at least one fundamental belief
3. **Provide actionable analogies** - not just poetic, but structurally instructive
4. **Score pathways honestly** - clear novelty/impact ratings with reasoning
5. **Uncover blind spots** - meta-reflection surfaces what was previously invisible
6. **Stay concise** - maximum insight density, minimum word count
7. **Enable next steps** - even pure theory should suggest testable experiments

## Related Resources

This command integrates with:
- **Serena MCP** - for storing discovered patterns and insights
- **Current conversation** - automatically uses existing context when no args provided
- **Your working memory** - builds on ongoing discussions and problems

---

**Note**: This is a pure analysis tool. It generates creative frameworks but does not:
- Create tasks in Task Master
- Execute implementations
- Modify code or files
- Trigger automations

For implementation, use the insights to inform other commands or manual work.
