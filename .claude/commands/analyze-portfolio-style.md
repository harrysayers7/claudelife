---
created: "2025-10-16 16:15"
description: |
  Analyzes all MOK HOUSE portfolio blurbs to detect writing patterns and preferences. Examines selection data (which taglines/descriptions you chose), identifies trends in tone, structure, and word choice, then updates portfolio-style-guide.md with discovered patterns. Run after creating 3+ blurbs to improve future suggestions.

  Outputs:
    - Pattern analysis report (selection preferences, tone trends, structural patterns)
    - Updated style guide with "Learning from Past Selections" section
    - Recommendations for manual style guide refinements
    - Selection statistics and confidence scores
examples:
  - /analyze-portfolio-style
  - /analyze-portfolio-style --report-only (preview without updating style guide)
---

# Analyze Portfolio Style

This command analyzes your MOK HOUSE portfolio blurbs to detect writing patterns and automatically improve the `/mokhouse-portfolio-blurb` command's suggestions over time.

## Usage

```bash
# Analyze and update style guide
/analyze-portfolio-style

# Preview analysis without updating
/analyze-portfolio-style --report-only
```

## When to Use

Run this command:
- ✅ After creating 3+ portfolio blurbs
- ✅ When you notice the command isn't matching your preferences
- ✅ Periodically (every 5-10 new blurbs) to refresh learned patterns
- ✅ After manually editing the style guide significantly

**Minimum Data**: Requires at least 3 blurbs with selection tracking metadata to generate meaningful patterns.

## What It Analyzes

### 1. Selection Patterns
- **Tagline preferences**: Which tagline options (1, 2, 3) you choose most often
- **Description angle preferences**: Which description types (A-Technical, B-Creative, C-Impact) you prefer
- **Consistency trends**: Do you always choose the same type or vary?

### 2. Manual Edit Patterns
- **Common corrections**: Words/phrases you consistently change
- **Structural adjustments**: Do you shorten/lengthen descriptions?
- **Tone refinements**: Do you add more/less technical detail?

### 3. Word Choice Patterns
- **Preferred vocabulary**: Terms that appear in your selected options
- **Avoided terms**: Words from rejected options
- **Genre variations**: Different patterns for commercial vs. film vs. branding

### 4. Structure Patterns
- **Length preferences**: Average word count of selected descriptions
- **Pacing style**: Short punchy vs. flowing prose
- **4-part structure adherence**: How closely you follow the template

## Interactive Process

When you run this command, I will:

1. **Scan blurbs folder**: Find all blurbs in `01-areas/business/mokhouse/website/project-blurbs/`

2. **Verify minimum data**: Check for at least 3 blurbs with selection tracking

3. **Extract selection data**:
   - Which tagline options were chosen (1-3)
   - Which description angles were chosen (A-C)
   - Manual edit flags
   - Project types and clients

4. **Analyze patterns**:
   - Calculate selection frequencies
   - Identify word choice trends
   - Detect structural preferences
   - Determine confidence scores

5. **Generate report**: Show discovered patterns with examples and statistics

6. **Confirm updates**: Ask if you want to update style guide with findings

7. **Update style guide**: Add "Learning from Past Selections" section with patterns

8. **Provide recommendations**: Suggest manual style guide refinements based on analysis

## Process

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I'll analyze your portfolio style by:

1. **Scan for blurbs**:
   ```bash
   # Find all blurb files
   ls 01-areas/business/mokhouse/website/project-blurbs/*.md
   ```

2. **Read and parse each blurb**:
   - Extract frontmatter metadata: `selected_tagline`, `selected_description`, `manual_edits`
   - Parse full content for word choice analysis
   - Note project type and client

3. **Calculate selection statistics**:
   ```
   Tagline Selection Frequency:
   - Option 1: 2/5 (40%)
   - Option 2: 3/5 (60%) ← PREFERRED
   - Option 3: 0/5 (0%)

   Description Selection Frequency:
   - Option A (Technical): 1/5 (20%)
   - Option B (Creative): 4/5 (80%) ← STRONGLY PREFERRED
   - Option C (Impact): 0/5 (0%)
   ```

4. **Identify word patterns**:
   - Extract frequent words from selected blurbs
   - Compare against Repco gold standard
   - Note unique vocabulary preferences

5. **Detect structural patterns**:
   - Average word count of selected descriptions
   - Sentence length distribution
   - 4-part structure adherence rate

6. **Generate confidence scores**:
   - **High confidence (80-100%)**: 5+ consistent selections of same type
   - **Medium confidence (50-79%)**: 3-4 selections with clear preference
   - **Low confidence (<50%)**: Mixed selections, need more data

7. **Format update for style guide**:
   ```markdown
   ## Learning from Past Selections

   **Last Analyzed**: 2025-10-16
   **Blurbs Analyzed**: 5
   **Confidence Level**: High (85%)

   ### Pattern: Description Angle Preference
   Based on 5 blurbs analyzed:
   - Selected creative-focused descriptions: 4/5 times (80%)
   - Selected technical-focused descriptions: 1/5 times (20%)
   - Selected impact-focused descriptions: 0/5 times (0%)

   **Insight**: Strongly prefer creative direction narratives over technical process or impact results.
   **Recommendation**: Generate creative-focused option first, make it most detailed.

   ### Pattern: Tagline Style
   - Selected taglines with industry-specific verbs: 5/5 times (100%)
   - Selected generic action verbs: 0/5 times (0%)

   **Insight**: Always prefer taglines that connect to client's industry.
   **Example**: "Fueling" for automotive, "Driving" for sports, "Powering" for tech.
   ```

8. **Update style guide**: Append or replace "Learning from Past Selections" section

9. **Increment counters**: Update `last_analyzed` date and `total_selections_tracked`

## Output Format

### Analysis Report

```markdown
# MOK HOUSE Portfolio Style Analysis

**Date**: 2025-10-16 16:20
**Blurbs Analyzed**: 5
**Selection Data Available**: 5/5 (100%)
**Confidence Level**: High (85%)

---

## Selection Patterns

### Tagline Preferences
| Option | Count | Percentage | Confidence |
|--------|-------|------------|------------|
| 1      | 2     | 40%        | Medium     |
| 2      | 3     | 60%        | High       |
| 3      | 0     | 0%         | High (avoid) |

**Insight**: Consistently prefer Option 2 taglines.

**Common traits in Option 2**:
- Industry-specific action verbs
- Client mission connection
- Under 10 words
- Example: "Fueling Repco's centenary with sound"

### Description Angle Preferences
| Angle | Count | Percentage | Confidence |
|-------|-------|------------|------------|
| A (Technical) | 1 | 20% | High (avoid) |
| B (Creative) | 4 | 80% | Very High |
| C (Impact) | 0 | 0% | High (avoid) |

**Insight**: Strongly prefer creative direction narratives.

---

## Word Choice Patterns

### Frequently Selected Terms
- "partnered with" (5/5 blurbs)
- "crafted" (4/5 blurbs)
- "fused" (3/5 blurbs)
- "amplified" (3/5 blurbs)

### Avoided Terms (from rejected options)
- "created" (appeared in rejected options 3 times)
- "developed solution" (too corporate)
- "delivered" (too transactional)

---

## Structural Patterns

### Length Preferences
- **Average selected description**: 112 words
- **Range**: 95-125 words
- **Target**: Maintains 100-120 word guideline

### Sentence Structure
- **Average sentences per description**: 5.2
- **Average sentence length**: 21.5 words
- **Pattern**: Mix of short (10-15 words) and medium (20-30 words)

---

## Recommendations

Based on analysis, consider updating style guide:

1. **Tagline Generation**: Always generate Option 2 style first (industry-specific verbs)
2. **Description Focus**: Make Option B (Creative) the most detailed and refined
3. **Word Bank**: Add "fused", "amplified" to preferred terms
4. **Avoid List**: Add "created", "delivered" to avoid terms

---

## Update Style Guide?

Would you like me to update `portfolio-style-guide.md` with these findings?
- ✅ Yes, update the "Learning from Past Selections" section
- ⏸️  No, just show me the report (--report-only)
```

## Evaluation Criteria

A successful pattern analysis should:

1. **Require sufficient data**: At least 3 blurbs with selection tracking
2. **Calculate accurate statistics**: Selection frequencies and percentages
3. **Identify actionable patterns**: Clear preferences that can guide future generation
4. **Assign confidence scores**: Indicate reliability of each pattern
5. **Provide concrete examples**: Show actual text from selected options
6. **Generate clear insights**: Explain what the patterns mean
7. **Offer recommendations**: Suggest specific style guide updates
8. **Maintain style guide structure**: Append to existing guide without breaking format

## Related Resources

- **Style guide**: `01-areas/business/mokhouse/website/portfolio-style-guide.md`
- **Blurbs folder**: `01-areas/business/mokhouse/website/project-blurbs/`
- **Portfolio command**: `/mokhouse-portfolio-blurb`
- **Command guide**: `04-resources/guides/commands/claudelife-commands-guide.md`

## Tips for Best Results

- **Run periodically**: After every 5 new blurbs to keep patterns current
- **Review before accepting**: Check that detected patterns match your actual preferences
- **Manually refine**: Edit style guide directly if analysis misses nuances
- **Track consistently**: Always complete selection tracking in `/mokhouse-portfolio-blurb`
- **Vary projects**: Analyze blurbs from different clients/project types for robust patterns

## Notes

- Analysis is non-destructive (can preview with `--report-only`)
- Only updates "Learning from Past Selections" section (doesn't change your manual rules)
- Patterns complement (don't replace) your explicit style guide preferences
- Low confidence patterns are flagged and won't override strong manual rules
- Can re-run analysis anytime to refresh patterns with new data

---

## Command Execution

**ARGUMENTS**: [--report-only]

### Steps:

1. **Check for --report-only flag**: If present, preview analysis without updating

2. **Scan blurbs folder**: List all `.md` files in `01-areas/business/mokhouse/website/project-blurbs/`

3. **Verify minimum data**: Confirm at least 3 blurbs exist with selection metadata

4. **Read and parse blurbs**: Extract frontmatter and content from each blurb

5. **Calculate selection statistics**: Frequency of tagline options (1-3) and description angles (A-C)

6. **Analyze word patterns**: Extract frequently used terms from selected blurbs

7. **Detect structural patterns**: Calculate average word count, sentence length, structure adherence

8. **Generate confidence scores**: Assign confidence to each pattern based on consistency

9. **Format analysis report**: Present findings with statistics, examples, and insights

10. **Show recommendations**: Suggest specific style guide updates

11. **Confirm update** (unless --report-only): Ask permission to update style guide

12. **Update style guide**: Replace "Learning from Past Selections" section with new findings

13. **Update metadata**: Increment `last_analyzed`, `blurbs_analyzed`, `total_selections_tracked`

14. **Confirm completion**: Show what was updated and remind to use `/mokhouse-portfolio-blurb` with new patterns

Now execute the command with the provided arguments (if any).
