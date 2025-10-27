---
created: "2025-10-16 15:30"
updated: "2025-10-16 18:05"
version_history:
  - version: "1.3"
    date: "2025-10-16 18:05"
    changes: "Added automatic append to master blurbs file (01-blurbs-master.md) without credits"
  - version: "1.2"
    date: "2025-10-16 17:00"
    changes: "Updated to use 'Harry' instead of full name, enforced 50-word maximum for descriptions"
  - version: "1.1"
    date: "2025-10-16 16:00"
    changes: "Added self-learning system with style guide integration and selection tracking"
  - version: "1.0"
    date: "2025-10-16 15:30"
    changes: "Initial creation"
description: |
  Generate professional portfolio project descriptions for the MOK HOUSE website. SELF-LEARNING: Reads portfolio-style-guide.md to understand your writing preferences and learns from your selections over time. Creates catchy taglines, detailed project descriptions highlighting creative direction and impact, and properly formatted credit sections. Tracks which options you select to improve future suggestions.

  Outputs:
    - 3 catchy one-sentence tagline options (following style guide patterns)
    - 3 complete project description drafts (technical, creative, impact angles)
    - Formatted "Appreciation" credits section
    - Saved markdown file with selection tracking metadata
    - Context log entry with date, client, and file link
    - Selection data for future pattern analysis
examples:
  - /mokhouse-portfolio-blurb "Just finished the Repco 100 Years campaign - sonic branding for their centenary"
  - /mokhouse-portfolio-blurb "link to project brief in vault: [[Spotify Brand Campaign]]"
  - /mokhouse-portfolio-blurb "Composed original score for Nike commercial, 30-second spot with orchestral elements"
---

# MOK HOUSE Portfolio Blurb

This command helps you create professional, impact-focused portfolio project descriptions for the MOK HOUSE website. **SELF-LEARNING**: The command reads your [portfolio-style-guide.md](../../../01-areas/business/mokhouse/website/portfolio-style-guide.md) to understand your writing preferences and learns from your selections over time. It generates catchy taglines, detailed project descriptions, and properly formatted credits, then saves everything to your website content folder with proper logging.

## Usage

```bash
/mokhouse-portfolio-blurb [project details or link to project files]
```

## Self-Learning System (Automatic)

This command improves over time **automatically**:

1. **Reading your style guide** (`portfolio-style-guide.md`) before generating any options
2. **Learning from your selections**: Tracks which tagline/description options you choose
3. **Auto-analyzing patterns**: Every 3 blurbs (3rd, 6th, 9th, etc.), automatically analyzes your preferences
4. **Asking permission**: Shows analysis summary and asks if you want to update style guide
5. **Manual refinement**: Edit the style guide anytime to teach new preferences

**Style Guide Location**: `01-areas/business/mokhouse/website/portfolio-style-guide.md`

**Auto-Analysis Triggers**: After blurbs #3, #6, #9, #12, etc. (every 3 blurbs)

## Interactive Process

When you run this command, I will:

1. **Load style guide**: Read `portfolio-style-guide.md` to understand your preferences

2. **Gather project context** by asking you:
   - What type of project is this? (sonic branding, original composition, mixing, sound design, etc.)
   - Who was the client and what was their core need/brief?
   - What was your creative approach or unique angle?
   - What impact did your work have on the final campaign/product?
   - Any specific sonic elements or techniques worth highlighting?
   - Credits: Client name, Agency/Production company (if applicable)

3. **Reference existing blurbs** by checking `01-areas/business/mokhouse/website/project-blurbs/` for additional examples

4. **Generate options following style guide rules**:
   - 3 catchy one-sentence tagline variations (following tagline formula)
   - 3 complete project description drafts (technical, creative, impact angles)
   - All options apply style guide preferences: tone, word choice, structure

5. **Track your selection**: Record which options you choose (tagline + description)

6. **Iterate with you** until you're happy with the final version

7. **Save and log**:
   - Create `[project-name]-blurb.md` in project-blurbs folder with selection metadata
   - Add log entry to `CLAUDE.md` with date, client, and link
   - Update style guide's selection count

8. **Auto-analysis (if triggered)**:
   - Every 3 blurbs (3rd, 6th, 9th, etc.), automatically analyze patterns
   - Show brief summary of discovered preferences
   - Ask: "Update style guide with these patterns?"
   - Apply updates if you confirm

## Input Requirements

You can provide project details by:
- Describing the project in your own words
- Linking to existing project files/notes in your vault (e.g., `[[Project Brief]]`)
- Pasting reference materials (briefs, emails, client feedback)
- Combining any of the above

## Process

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I'll help you create the perfect portfolio blurb by:

1. **Load style guide**: Read `01-areas/business/mokhouse/website/portfolio-style-guide.md` to understand:
   - Preferred tone and voice patterns
   - Word choice guidelines (preferred terms, words to avoid)
   - Tagline formula and patterns
   - Description structure (4-part flow)
   - Length guidelines and pacing rules
   - Learned patterns from past selections (if available)

2. **Analyze context**: Review your project details and any linked files to understand scope, client, creative direction

3. **Check existing blurbs**: Search `01-areas/business/mokhouse/website/project-blurbs/` for additional examples

4. **Ask clarifying questions**: Get specific details about creative approach, impact, and technical highlights

5. **Generate tagline options following style guide**: Create 3 catchy one-sentence hooks that:
   - Follow the tagline formula: `[Project] — [Verb]ing [Client Mission] with [medium]`
   - Use action-oriented verbs (not descriptive)
   - Keep under 12 words
   - Connect to client's industry/mission

6. **Draft descriptions following style guide**: Write 3 full project descriptions with different angles:
   - **Option A**: Technical/process-focused (the "how")
   - **Option B**: Creative direction-focused (the "why")
   - **Option C**: Impact/results-focused (the "what")
   - All options follow 4-part structure: Partnership → Challenge → Approach → Impact
   - Apply word choice preferences from style guide
   - **STRICT LIMIT: Maximum 50 words per description**
   - Use "Harry" instead of "Harry Sayers" throughout

7. **Format credits**: Structure the "Appreciation" section with your role, client, and agency

8. **Track selection**: When you choose options, record in metadata:
   - Which tagline chosen (1, 2, or 3)
   - Which description chosen (A, B, or C)
   - Any manual edits you made

9. **Iterate**: Refine based on your feedback until you approve

10. **Save file**: Create `[project-name]-blurb.md` with frontmatter containing:
    - Date and client
    - Project type
    - Selection tracking: `selected_tagline`, `selected_description`, `manual_edits`

11. **Update style guide**: Increment `blurbs_analyzed` count in `portfolio-style-guide.md`

12. **Log creation**: Add entry to `CLAUDE.md`

## Output Format

### Final Blurb File Structure

```markdown
---
date: "YYYY-MM-DD HH:MM"
client: "[Client Name]"
project_type: "[sonic branding/composition/mixing/etc.]"
selected_tagline: 1  # Which tagline option (1-3) was chosen
selected_description: "B"  # Which description (A, B, C) was chosen
manual_edits: false  # Whether user made manual edits after selection
---

# [Project Name]
[Selected catchy tagline]

## Project Information
[Selected project description - third person, **MAXIMUM 50 WORDS** following:
1. Partnership context (Harry + Client + Project type)
2. Creative challenge/brief
3. Harry's approach and specific sonic choices
4. Impact on final campaign/product]

## Appreciation
Audio Producer / Composer — Harry Sayers
Client — [Client Name]
Agency / Production — [Agency Name if applicable]
```

**Selection Tracking**: The metadata tracks which options you preferred for future pattern analysis.

### Context Log Entry Format

```markdown
- [YYYY-MM-DD]: Created portfolio blurb for [Client Name] - [Project Name] → [[01-areas/business/mokhouse/website/project-blurbs/[project-name]-blurb]]
```

## Example

### Input
```
Just finished the Repco 100 Years campaign. It was sonic branding for their centenary.
Brief was to honor their 100-year heritage while capturing modern motorsport energy.
I went with gritty guitar tones and cinematic layers to match the adrenaline of the visuals.
Client was Repco, production by Electric Sheep Music.
```

### Tagline Options Generated
1. "Repco 100 Years — Fueling Repco's centenary with sound."
2. "Repco 100 Years — A century of automotive excellence, amplified."
3. "Repco 100 Years — Where heritage meets horsepower through sound."

### Description Options Generated

**Option A (Technical/Process)** (47 words):
Harry partnered with Repco to craft the sonic branding for their 100-year campaign. Working with Electric Sheep Music, Harry developed a driving score built on gritty guitar tones and cinematic orchestration, balancing raw analog warmth with modern production clarity to match the high-octane visuals.

**Option B (Creative Direction)** (45 words):
Harry partnered with Repco to craft the sonic branding for their 100-year campaign. The brief called for music reflecting Repco's heritage while capturing modern motorsport energy. Harry developed a driving score fusing gritty guitar with cinematic layers, amplifying the campaign's momentum.

**Option C (Impact/Results)** (48 words):
Harry partnered with Repco to craft the sonic branding for their 100-year campaign. The score became the emotional backbone of Repco's centenary celebration, driving viewer engagement. Harry's fusion of heritage-inspired guitar with cinematic production gave Repco a sonic identity honoring its legacy.

### User Selects
- Tagline: Option 1
- Description: Option B (with minor tweaks)
- Confirmed credits

### Final Output
File saved to: `01-areas/business/mokhouse/website/project-blurbs/repco-100-years-blurb.md`
Log entry added to: `01-areas/business/mokhouse/CLAUDE.md`

## Evaluation Criteria

A successful MOK HOUSE portfolio blurb should:

1. **Capture attention immediately** with a punchy, memorable tagline
2. **Establish partnership context** (Harry + Client + Project type)
3. **Highlight creative direction** and artistic choices made
4. **Emphasize impact** on the final campaign/product
5. **Maintain third-person perspective** and professional tone
6. **Include specific sonic/technical details** without overwhelming non-technical readers
7. **Credit all parties** accurately and consistently
8. **Match existing blurb style** for portfolio consistency
9. **Be concise** (**MAXIMUM 50 words** for main description)
10. **Sound confident and impactful** without overselling

## Related Resources

- **Style guide**: `01-areas/business/mokhouse/website/portfolio-style-guide.md` (edit to teach preferences)
- **Example blurb**: Repco 100 Years in style guide
- **Portfolio blurbs folder**: `01-areas/business/mokhouse/website/project-blurbs/`
- **Context log**: `01-areas/business/mokhouse/CLAUDE.md`
- **Pattern analysis**: `/analyze-portfolio-style` command (run after 3+ blurbs)
- **MOK HOUSE agent**: `.claude/agents/agent-mokhouse.md`

## Tips for Best Results

- Provide as much creative context as possible (what was unique about this project?)
- Mention any client feedback or campaign results if available
- Note any specific techniques or sonic signature elements used
- Reference the visual style if it informed your audio direction
- Include the project timeline if it was noteworthy (tight deadline, long-term collaboration, etc.)

---

## Command Execution

**ARGUMENTS**: [project details or link to project files]

### Steps:

1. **Load style guide**: Read `01-areas/business/mokhouse/website/portfolio-style-guide.md` to understand all preferences

2. **Acknowledge receipt** of project details

3. **Ask clarifying questions** about creative approach, impact, and credits

4. **Search existing blurbs** in `01-areas/business/mokhouse/website/project-blurbs/` for additional examples

5. **Generate 3 tagline options** following style guide formula and present them

6. **Generate 3 description options** (technical, creative, impact angles) following style guide structure and present them

7. **Iterate** based on your feedback until approved

8. **Track selection**: Note which tagline (1-3) and description (A-C) you chose

9. **Format final blurb** with frontmatter including selection tracking metadata

10. **Save to** `01-areas/business/mokhouse/website/project-blurbs/[project-name]-blurb.md`

11. **Append to master blurbs file**: Add the blurb (WITHOUT Appreciation section) to `01-areas/business/mokhouse/website/project-blurbs/01-blurbs-master.md` with separator `---`

12. **Update style guide**: Increment `blurbs_analyzed` count in `portfolio-style-guide.md`

13. **Check for auto-analysis trigger**:
    - If `total_selections_tracked` is now divisible by 3 (3, 6, 9, etc.)
    - Automatically run pattern analysis
    - Show brief analysis summary
    - Ask: "Would you like me to update the style guide with these patterns?"
    - If yes, update style guide; if no, skip but save analysis for later

14. **Log creation** in `01-areas/business/mokhouse/CLAUDE.md` with format:
    - `[YYYY-MM-DD]: Created portfolio blurb for [Client] - [Project] → [[link-to-file]]`

15. **Confirm completion** with file paths, master file update, and auto-analysis status (if triggered)

Now execute the command with the provided arguments (if any).
