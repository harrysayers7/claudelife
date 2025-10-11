# /generate-mokai-flashcards [file-path]

Generate spaced repetition flashcards from Mokai deep research files using proper multi-line `?` separator syntax.

## Purpose

Extract key concepts from deep research markdown files and convert them into spaced repetition flashcards that can be reviewed using the Obsidian Spaced Repetition plugin.

## Arguments

- `$ARGUMENTS` (optional): Path to specific research file to process
  - If provided: Process only that file
  - If empty: Prompt user to select from available research files

## Steps

1. **Identify Source File**
   - If `$ARGUMENTS` provided: Use that file path
   - If no arguments: List available files and prompt for selection
   - Available research locations:
     - `/01-areas/business/mokai/docs/research/`
     - Any file with `research-type: Deep research` in frontmatter

2. **Find Existing Flashcard Files**
   - Search `/01-areas/business/mokai/learn/flashcards/` for files with `type: flash-card` in frontmatter
   - Use Glob tool to find all `.md` files in flashcards directory
   - Read frontmatter of each to identify flash-card files
   - Present list of existing flashcard files to user

3. **Ask User for Destination**
   - Present options:
     1. **Add to existing file**: Show list of files with `type: flash-card`
     2. **Create new file**: Prompt for filename (auto-save to `/01-areas/business/mokai/learn/flashcards/[name].md`)
   - Wait for user selection

4. **Load Existing Flashcards (if appending)**
   - Read selected existing flashcard file
   - Extract all existing questions (text before `;;` separator)
   - Store in memory for duplicate checking
   - Note: Questions are case-insensitive and whitespace-normalized for comparison

5. **Read and Analyze Research Content**
   - Use Read tool to load the source research file
   - Identify key concepts, definitions, frameworks, and critical facts
   - Look for:
     - Important terminology and definitions
     - Key statistics and numbers
     - Framework names and their purposes
     - Critical business concepts
     - Regulatory requirements (IPP, IRAP, Essential Eight, etc.)
     - Competitor information
     - Procurement rules and thresholds

6. **Generate Flashcards (with Duplicate Prevention)**
   - **CRITICAL**: Use `?` separator on its own line (NOT `;;`)
   - **Format**:
     ```markdown
     Question text
     ?
     Answer text (no blank line after ?)
     <br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> [text]
     <br><br><span style="color: #10b981;">**Key Terms:**</span>
     - **[Technical word]**: [Simple definition]
     <br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
     - **[ABBR]**: [Full name] - [What it does/means]
     ```
   - **Before adding each card**:
     - Normalize question (lowercase, trim whitespace)
     - Check against existing questions
     - Skip if duplicate found
     - Log skipped duplicates for user report
   - Focus on:
     - **Definitions**: "What is [term]?"
     - **Applications**: "When would you use [concept]?"
     - **Comparisons**: "What's the difference between X and Y?"
     - **Numbers/Facts**: "What is the IPP threshold for direct procurement?"
     - **Processes**: "What are the steps in [process]?"

   - **Enhanced Format Requirements**:
     - **NO** blank line after `?` separator
     - **NO** `---` separators between flashcards
     - **NO** Obsidian callouts (`> [!note]`) - use plain bold markdown
     - Use `<br><br>` before each section header for visual spacing
     - Color code sections:
       - Blue (#3b82f6) for Simple Explanation
       - Green (#10b981) for Key Terms
       - Orange (#f59e0b) for Abbreviations

7. **Write Flashcard File**
   - **If creating new file**:
     - Create in `/01-areas/business/mokai/learn/flashcards/[filename].md`
     - Add frontmatter with `type: flash-card` property
     - **IMPORTANT**: Use single unique tag matching filename (e.g., `financial-business-development-flashcards`)
   - **If appending to existing**:
     - Read existing file content
     - Append new flashcards to end (maintaining structure)
     - Update `date modified` in frontmatter
   - Structure:
     ```markdown
     ---
     type: flash-card
     tags:
       - [filename-without-extension]
     source: [research file name]
     date created: [date]
     date modified: [date]
     ---

     # [Research Topic] - Flashcards

     Question 1
     ?
     Answer 1
     <br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> [explanation]
     <br><br><span style="color: #10b981;">**Key Terms:**</span>
     - **[Term]**: [Definition]
     <br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
     - **[ABBR]**: [Full name] - [What it does]

     Question 2
     ?
     Answer 2
     <br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> [explanation]
     <br><br><span style="color: #10b981;">**Key Terms:**</span>
     - **[Term]**: [Definition]
     <br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
     - **[ABBR]**: [Full name] - [What it does]
     ```

8. **Organize by Topic**
   - Group flashcards by logical sections:
     - ## Procurement & Policy
     - ## Competitors & Market
     - ## Technical Requirements
     - ## Business Model
     - ## Frameworks & Standards

9. **Quality Checks**
   - Ensure questions are clear and specific
   - Answers should be concise (1-3 sentences ideal)
   - Avoid ambiguous questions
   - Include context where needed
   - Use consistent terminology from research
   - **For Simple Explanations**:
     - Use everyday language (avoid jargon)
     - Use relatable analogies where possible
     - Break complex concepts into familiar comparisons
     - Aim for 1-2 sentence maximum
   - **For Key Terms**:
     - Identify words unlikely known by 15-year-olds
     - Words like: procurement, compliance, maturity, remediation, accreditation, etc.
     - Provide plain-English definitions
   - **For Abbreviations**:
     - Expand all acronyms (IPP, IRAP, GRC, SOC, etc.)
     - Include 1-sentence explanation of what it does/means
     - Format: "**IRAP**: Information Security Registered Assessors Program - Government security checkers"

10. **Report Summary**
    - Count of flashcards generated (new cards only)
    - Count of duplicates skipped
    - List of skipped duplicate questions
    - Topics covered
    - Source file processed
    - Destination file location
    - Action taken (created new / appended to existing)

## Example Flashcards

From **AUS GOV CYBER LANDSCAPE**:

```markdown
What is the IPP (Indigenous Procurement Policy)?
?
A mandatory policy requiring federal agencies to consider Indigenous businesses for contracts, with direct procurement available under $80,000 and set-asides for larger contracts.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> Think of it like a rule that says government must shop from Indigenous-owned businesses first for smaller purchases, kind of like a "locals first" policy at your school canteen.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Procurement**: The process of buying goods or services (like shopping for the government)
- **Federal agencies**: Government departments (like departments of health, defense, etc.)
- **Set-asides**: Reserving contracts specifically for certain groups
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **IPP**: Indigenous Procurement Policy - Government rule to buy from Indigenous businesses first

What does IRAP stand for and what is it?
?
Information Security Registered Assessors Program - Australian government security assessment framework requiring certified assessors to evaluate systems handling government data.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> It's like having qualified inspectors check if a computer system is safe enough to store government secrets - only specially trained security experts can do these checks.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Assessment framework**: A structured way to check and evaluate something (like a marking rubric for a test)
- **Certified assessors**: Officially qualified people who check systems (like licensed driving instructors)
- **Evaluate**: To carefully examine and judge something
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **IRAP**: Information Security Registered Assessors Program - Official government security checkers

What are the Essential Eight maturity levels?
?
Maturity Level 1 (basic), Level 2 (managed), Level 3 (robust) - progressive cybersecurity controls defined by Australian Cyber Security Centre.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> It's like levels in a video game for cybersecurity - Level 1 is beginner protection, Level 2 is intermediate, and Level 3 is expert level security. Each level gets harder but protects you better.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Maturity levels**: Stages showing how advanced or developed something is (like belt colors in martial arts)
- **Progressive**: Getting more advanced step by step
- **Cybersecurity controls**: Security measures to protect computers and data (like locks on doors)
- **Robust**: Strong and difficult to break or bypass
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **ACSC**: Australian Cyber Security Centre - Government's main cybersecurity advice agency
```

From **COMPETITIVE LANDSCAPE**:

```markdown
Who are Mokai's main Indigenous cybersecurity competitors?
?
Baidam Solutions, Willyama Services, Arrpwere - all Supply Nation certified with government client bases.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> These are other Aboriginal-owned cybersecurity companies that compete for the same government contracts - they're all officially recognized Indigenous businesses.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Competitors**: Other businesses offering similar services
- **Certified**: Officially approved or verified (like being an accredited school)
- **Client bases**: Groups of customers they regularly work with
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **N/A**: No abbreviations in this answer

What is Baidam Solutions' unique differentiator?
?
Australia's first Indigenous-run Security Operations Centre (SOC) launched in 2023, with Google partnership and 50%+ profit to Indigenous training.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> They run Australia's first Aboriginal-owned cybersecurity monitoring center, partnered with Google, and give over half their profits to training Aboriginal people - making them stand out from competitors.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Differentiator**: What makes a business special or different from others (your unique selling point)
- **Partnership**: Working together with another company in an official agreement
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **SOC**: Security Operations Centre - 24/7 cybersecurity monitoring center (like a control room watching for hackers)

What revenue did Willyama Services achieve by ~2021?
?
Estimated $5-6M annual revenue, growing from startup in 2016 to multi-million by year 5.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> They started from scratch in 2016 and within 5 years were making $5-6 million per year - that's fast growth for a new business.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Revenue**: Total money a business earns (before expenses, like your total pay before tax)
- **Annual**: Per year or yearly
- **Startup**: A newly created company
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **M**: Million (in money context)
```

From **Operating Model & Business Architecture**:

```markdown
What are the three main service delivery models for cyber consulting?
?
1. Staff augmentation (contractor placement), 2. Project-based delivery (fixed scope), 3. Managed services (ongoing retainer).
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> There are three ways to sell cybersecurity services: 1) Rent out experts by the day, 2) Get paid for completing specific projects, 3) Get monthly payments for ongoing protection (like a Netflix subscription for security).
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Service delivery models**: Different ways a business can provide its services to customers
- **Staff augmentation**: Lending skilled workers to clients temporarily (like a substitute teacher)
- **Fixed scope**: Clearly defined project with set deliverables (like a homework assignment with specific requirements)
- **Retainer**: Regular ongoing payment for continuous services (like a monthly subscription)
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **N/A**: No abbreviations in this answer

What is a realistic gross margin for contractor-based consulting?
?
50-100% markup on contractor cost, typically resulting in 30-40% net profit after overhead.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> If you pay a contractor $100/day, you charge the client $150-200/day, and after paying all business expenses, you keep about $30-40 as profit - that's healthy for this business.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Gross margin**: Difference between what you charge and what you pay (before other expenses)
- **Markup**: How much extra you charge on top of your cost (like a store's price vs wholesale cost)
- **Net profit**: Money left after paying ALL expenses (what you actually keep)
- **Overhead**: Ongoing business costs like rent, insurance, software (costs not directly tied to one project)
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **N/A**: No abbreviations in this answer

What does SOP stand for in business operations?
?
Standard Operating Procedures - documented processes ensuring consistency and quality in service delivery.
<br><br><span style="color: #3b82f6;">**Simple Explanation:**</span> SOPs are like recipe cards for business tasks - step-by-step instructions so everyone does the job the same correct way every time, ensuring quality doesn't vary.
<br><br><span style="color: #10b981;">**Key Terms:**</span>
- **Documented processes**: Written instructions for how to do tasks (like an instruction manual)
- **Consistency**: Doing things the same way every time (not randomly different)
- **Service delivery**: How you provide your services to customers
<br><br><span style="color: #f59e0b;">**Abbreviations:**</span>
- **SOP**: Standard Operating Procedures - Step-by-step business instructions (like a recipe book for work tasks)
```

## Usage

```bash
# Generate flashcards from specific file (with path argument)
/generate-mokai-flashcards /00-inbox/OPERATIONS GUIDE📘.md

# Or let command prompt you to select a file
/generate-mokai-flashcards

# Examples with full paths
/generate-mokai-flashcards /01-areas/business/mokai/docs/research/AUS GOV CYBER LANDSCAPE...md
/generate-mokai-flashcards /01-areas/business/mokai/docs/research/COMPETITIVE LANDSCAPE.md
```

## Interactive Flow

1. **If `$ARGUMENTS` provided**: Directly process that file
2. **If no arguments**: Show list of available research files for selection
3. **Find existing flashcard files**: Scan `/01-areas/business/mokai/learn/flashcards/`
4. **Ask destination**:
   - "Add to existing file?" → Show list of `type: flash-card` files
   - "Create new file?" → Prompt for filename
5. **Generate cards**: Extract concepts, check for duplicates
6. **Report**: Show new cards added, duplicates skipped, final location

## Configuration

**Spaced Repetition Settings** (for Obsidian plugin):
- **Separator**: `?` on its own line (NOT `;;`)
- **Tag**: Use unique tag per file (e.g., `#financial-business-development-flashcards`)
- **Review schedule**: Default SR algorithm (or customize)
- **Multi-line format**: Question\n?\nAnswer (continuous block, no blank lines)

## Tips

- **Atomic cards**: One concept per card
- **Context**: Include enough context in question to stand alone
- **Active recall**: Frame as questions, not fill-in-blanks when possible
- **Progressive detail**: Create both basic and advanced cards for same topic
- **Interleaving**: Mix topics rather than grouping all similar cards together

### Enhanced Learning Features

- **Simple Explanations**: Use color-coded bold text (NOT callouts)
  - Color: `<span style="color: #3b82f6;">**Simple Explanation:**</span>`
  - Use analogies (like Netflix subscriptions, recipe cards, school examples)
  - Break complex ideas into relatable comparisons
  - Keep to 1-2 sentences maximum
  - Add `<br><br>` before section for visual spacing

- **Key Terms Detection**: Identify complex vocabulary automatically
  - Color: `<span style="color: #10b981;">**Key Terms:**</span>`
  - Business jargon: procurement, compliance, remediation, accreditation
  - Technical terms: maturity, robust, progressive, evaluate
  - Industry-specific: retainer, markup, overhead, margin
  - Add `<br><br>` before section for visual spacing

- **Abbreviation Expansion**: Always expand and explain acronyms
  - Color: `<span style="color: #f59e0b;">**Abbreviations:**</span>`
  - Format: "**[ABBR]**: Full Name - Simple explanation"
  - Examples: IPP, IRAP, SOC, GRC, ACSC, SOP
  - Include what they do/mean in plain language
  - Add `<br><br>` before section for visual spacing

## Output Location

**All flashcards are saved to:**
- `/01-areas/business/mokai/learn/flashcards/` directory

**File structure:**
```
/01-areas/business/mokai/learn/flashcards/
├── operations-guide.md          # type: flash-card
├── procurement-policy.md         # type: flash-card
├── competitive-landscape.md      # type: flash-card
├── irap-essentials.md           # type: flash-card
└── [custom-name].md             # type: flash-card
```

**Each file includes:**
- `type: flash-card` in frontmatter (for filtering)
- Single unique tag matching filename (e.g., `growth-strategy-flashcards`)
- `source: [research file]` (tracks origin)
- `date created` and `date modified` timestamps
- Organized sections with `##` headings
- Spaced repetition `?` separator format (multi-line)
- Color-coded sections with HTML spans

## Duplicate Prevention Logic

**How duplicates are detected:**
1. Extract all questions from existing flashcard file (text before `?` separator)
2. Normalize each question:
   - Convert to lowercase
   - Trim leading/trailing whitespace
   - Remove extra spaces
3. Compare new questions against normalized existing questions
4. Skip if match found (case-insensitive)
5. Report skipped duplicates to user

**Example:**
- Existing: "What is the IPP threshold?\n?\nUnder $80,000..."
- New attempt: "What is the IPP threshold?\n?\nDifferent answer..."
- Result: **Skipped** (question already exists)

## Notes

- Use this command after updating deep research files
- Review and edit generated cards before using
- Can regenerate cards as research evolves - duplicates will be automatically skipped
- Combine with Obsidian Spaced Repetition plugin for learning
- Files with `type: flash-card` are searchable via Dataview queries
