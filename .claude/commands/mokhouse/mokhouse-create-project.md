---
created: "2025-10-16 11:45"
updated: "2025-10-17 14:30"
version_history:
  - version: "1.1"
    date: "2025-10-17 14:30"
    changes: "Added explicit Google Doc extraction instructions using Bash + curl (Step 3b)"
  - version: "1.0"
    date: "2025-10-16 11:45"
    changes: "Initial command creation"
description: |
  Automates MOK HOUSE project creation from client brief emails. Searches Gmail for brief emails,
  extracts Google Doc links, fetches brief content using Bash + curl, creates formatted Obsidian
  project files with complete frontmatter, generates AI creative suggestions, and creates SUNO
  prompts (<1000 chars).

  Outputs:
    - Formatted project file in /02-projects/mokhouse/ with proper callouts and structure
    - AI-generated creative direction, melody suggestions, and sound design ideas
    - SUNO AI prompt optimized for music generation (character-limited)
    - Complete project metadata with due dates, customer info, and deliverables
examples:
  - /mokhouse-create-project "I received a brief email for a new Repco project from Electric Sheep"
  - /mokhouse-create-project "Create project from the latest Panda Candy brief in Gmail"
  - /mokhouse-create-project "New Nintendo project brief arrived, please create the project file"
---

# Create MOK HOUSE Project from Brief

**Voice Transcription Note**: When Harry says "mock house" or "mok house", he means **MOK HOUSE** (all caps, two words).

This command automates the complete process of creating a new MOK HOUSE music project from a client brief email, including AI-powered creative suggestions and production-ready prompts.

## Usage

```bash
/mokhouse-create-project "Brief context or customer name"
```

## What This Command Does

**Phase 1: Project Creation Pipeline**

1. **Gmail Search** → Locate client brief email
2. **Google Doc Extraction** → Fetch brief content from linked document
3. **Obsidian File Creation** → Generate formatted project file with proper structure
4. **AI Creative Generation** → Produce composer-level suggestions for jingles/sonic branding
5. **SUNO Prompt Creation** → Generate optimized music AI prompt (≤1000 characters)

## Interactive Process

When you run this command, I will:

1. **Clarify the brief source:**
   - Which client/customer is this for?
   - Do you have the Gmail thread or Google Doc link?
   - Any specific subject line or sender to search for?

2. **Search and validate:**
   - Search Gmail for matching brief emails
   - Present candidates if multiple matches found
   - Confirm the correct brief before proceeding

3. **Extract brief details:**
   - Customer/brand name
   - Project name and campaign details
   - Due dates and timeline
   - Creative requirements (platform, duration, tone)
   - Budget/fee information

4. **Generate creative content:**
   - AI suggestions for jingle concepts and melody direction
   - Sound design and production ideas
   - SUNO prompt optimized for music generation

5. **Create project file:**
   - Formatted Obsidian markdown in `/02-projects/mokhouse/`
   - Complete frontmatter with all metadata
   - Properly structured sections with callouts

## Input Requirements

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

Before running, prepare:

1. **Customer information:**
   - Customer name (e.g., "Electric Sheep Music", "Panda Candy")
   - Known email addresses or Gmail search terms

2. **Brief source:**
   - Gmail subject line keywords OR
   - Direct Google Doc URL OR
   - Approximate date range for search

3. **Project context (if known):**
   - Campaign name or job number
   - Platform (TV, digital, social media)
   - Rough timeline or urgency

## Process

### Step 1: Identify Brief Email

**Use:** `mcp__gmail__search_emails`

Search for:
- Emails from known clients (Electric Sheep Music, Panda Candy, etc.)
- Subject lines containing "brief", "project", or client names
- Recent emails with Google Docs links
- Emails mentioning project deadlines

**If multiple matches:**
- Present list with subject, sender, date
- Ask user to select the correct brief

### Step 2: Extract Google Doc Link

From the identified email:
- Extract Google Docs URL (`https://docs.google.com/document/d/...`)
- Parse document ID from URL
- Note any contextual information from email body
- Check sender details and urgency indicators

### Step 3: Fetch Brief Content

**Step 3a: Get email content with Google Doc link**

**Use:** `mcp__gmail__read_email` to get full email content

From the email, extract:
- Google Doc URL (format: `https://docs.google.com/document/d/{DOCUMENT_ID}/edit`)
- Document ID from the URL
- Any context from email body (demo fees, due dates, etc.)

**Step 3b: Extract Google Doc content using Bash + curl**

**CRITICAL**: Use the Bash tool with curl to fetch the document as plain text:

```bash
curl -L "https://docs.google.com/document/d/{DOCUMENT_ID}/export?format=txt" 2>/dev/null
```

**Example:**
```bash
curl -L "https://docs.google.com/document/d/1z4tfRJkL7BBvsfCURLGCFs5vztHT5suhEmKk9ECtiZU/export?format=txt" 2>/dev/null
```

**Important notes:**
- DO NOT use WebFetch tool - it cannot access Google Docs export URLs properly
- The `/export?format=txt` endpoint returns plain text content
- The `-L` flag follows redirects (Google Docs redirects to content delivery URL)
- `2>/dev/null` suppresses curl progress output

**Step 3c: Parse extracted brief content**

From the fetched text, extract these critical details:
- **Job number** (if present)
- **Project name/campaign name**
- **Agency name**
- **Client/brand name**
- **Product name**
- **Brief description/summary**
- **Target audience**
- **Platform** (TV, digital, social media)
- **Duration requirements** (15s, 30s, 60s, 3min)
- **Demo due date** and **Final mix due date**
- **Demo fee** and **Award/usage fee**
- **Creative direction**
- **Tone & emotion**
- **Instrumentation ideas**
- **Structure notes**
- **Reference tracks**
- **Client feedback/quotes**
- **Technical requirements** (file format, naming convention, FOS, APRA)
- **Special requirements** (12 FOS, APRA, etc.)

### Step 4: Create Obsidian Project File

**Use:** `mcp__claudelife-obsidian__write_note`

**File naming:** Use the exact `project name` field value as the filename (e.g., `Nintendo - EM.md`)
**Location:** `/02-projects/mokhouse/` (or in a numbered subdirectory like `/02-projects/mokhouse/036-nintendo/`)
**Important:** The filename should match the `project name` field exactly, NOT a date-prefixed slug

**Frontmatter template:**
```yaml
---
relation:
  - "[[mokhouse]]"
type: project
project name: "[Extracted project name]"
customer: "[Client name]"
status: "Brief Received"
demo fee: [Amount or leave blank]
award fee: [Amount or leave blank]
due date: "YYYY-MM-DD"
date received: "YYYY-MM-DD"
internal review: ""
Date Paid: ""
PO: ""
"Invoice #": ""
submitted date: ""
paid: false
awarded: false
APRA: false
12 FOS: [true/false - based on brief requirements]
---
```

### Step 5: Structure Brief Summary

**Use proper callouts and formatting:**

```markdown
> [!NOTE]
> ## Details:
>
> **JOB NUMBER:** [number]
> **AGENCY:** [agency]
> **CLIENT:** [client]
> **PRODUCT:** [product]
> **LENGTH:** [duration]

> [!DELIVERABLES]
>
> - [List all deliverables from brief]
> - [Each on separate line]

> [!TRACK LENGTH]
>
> [Track length requirements and details]
```YYMMDD_[JobNumber]_[Client]_3A_Mus.wav```

---

## [Project Name] Brief

**CREATIVE DIRECTION:**

[Brief content with proper line breaks and spacing]


**TONE & EMOTION:**

[Content with proper spacing between paragraphs]


**INSTRUMENTATION:**

[Content with proper spacing between paragraphs]


**STRUCTURE:**

[Content with proper spacing between paragraphs]


**CLIENT FEEDBACK:**

[Content with proper spacing between paragraphs]

---
```

### Step 6: Generate AI Creative Suggestions

**Execute this AI prompt with brief context:**

> Act as a world-class composer, vocalist, and sonic branding strategist for memorable, emotional, and brand-driven jingles and sonic identities across TV, digital, and social media.
>
> Given the creative brief above (brand, audience, platform, messaging, tone, duration, and key campaign goals), generate:
>
> - Catchy, emotionally resonant jingle lyrics and concepts (≤30s) tailored to platform and audience
> - Melody style & feel (describe musical genre, tempo, instrumentation, and overall mood)
> - Sound design/production ideas (instruments, FX, mnemonic motifs, and transitions)
> - A short, reusable sonic logo/audio mnemonic if appropriate
> - Concise creative intent paragraph connecting concept to the brand's goals

**Format as:**
```markdown
## AI Suggestions

> [!NOTE]
> **Creative Concept:**
>
> [Generated creative direction with proper spacing]
>
>
> **Musical Direction:**
>
> - **Genre:** [genre]
> - **Tempo:** [tempo with reasoning]
> - **Key Elements:** [elements]
>
>
> **Sound Design Ideas:**
>
> - Opening: [description]
> - Drop: [description]
> - Texture: [description]
> - [Special moments]: [description]
>
>
> **Sonic Logo/Audio Mnemonic:**
>
> [Description of memorable audio element]
>
>
> **Creative Intent:**
>
> [Paragraph connecting concept to brand goals]
```

### Step 7: Generate SUNO Prompt

**Critical constraint:** Maximum 1000 characters (not words)

**Execute this prompt:**

> You are a music prompt assistant. Given a jingle project brief, generate a detailed SUNO AI prompt using the following format - ensure the output is less than 1000 characters:
>
> [Title: {Project or Track Name}] [Genre: {Main genre or hybrid style}] [Mood: {3–5 emotional descriptors}] [Instruments: {Primary + supporting instruments}] [Structure: {Overall flow, e.g. Intro → Build → Climax → Outro}] [Tempo: {Approx BPM or feel: slow, mid-tempo, fast}]

**Format as code block:**
```markdown
## SUNO prompt
```

[Title: Project Name] [Genre: Style] [Mood: 3-5 descriptors] [Instruments: List] [Structure: Flow] [Tempo: BPM/feel]

[Intro 00:00-00:XX] Description [Build 00:XX-00:XX] Description
[Drop 00:XX-00:XX] Description [Main 00:XX-00:XX] Description [Outro 00:XX-end] Description

Requirements: [Key requirements]

**Character count verification:** [X/1000 characters]
```
```

### Step 8: Complete File Structure

Add these sections:

```markdown
---

## Creative References

- **Reference Tracks:** [tracks from brief]

- **Client Notes:** [specific notes]

- **Mood/Style:** [style direction]

---

> [!NOTE]
> ## Other relevant info:
>
> **Original Reference:** [if replacing existing track]
>
> **Key Challenge:** [main creative challenge]
>
> **Sync Points:** [timing requirements]
>
> **Special Moments:** [specific requirements]

## Links & Files

- **Ref Folder:** /references/[project-name]/

- **Google Doc:** [original brief URL]

- **Obsidian Links:** [[mokhouse-projects]]

- **Video Links:**
	- [link] <if required>
```

### Step 9: Provide Success Summary

```
✅ Project Created from Brief
────────────────────────────
Project: [project name]
Client: [customer]
Due Date: [due date]
Brief Source: [Google Doc URL]
File Created: [filename].md
Location: /Users/harrysayers/Developer/claudelife/02-projects/mokhouse/
Status: Brief Received

AI Suggestions: ✓ Generated
SUNO Prompt: ✓ Generated ([X]/1000 chars)
Next: Create demo, then mark as submitted
────────────────────────────
```

## Technical Requirements

### File Naming Convention

**Extract from brief:** `YYMMDD_[JobNumber]_[Client]_3A_Mus.wav`
**Harrison's composer number:** Always use "3"
**Format:** Code block with backticks

### YAML Frontmatter Rules

- **Dates:** YYYY-MM-DD format only
- **Booleans:** `true`/`false` (not quoted)
- **Numbers:** Unquoted (500 not "500")
- **12 FOS:** Boolean based on brief requirements
- **Composer number:** Always "3" for Harrison

### Formatting Standards

**Use these elements:**
- **Callouts:** `> [!NOTE]` for important information
- **Code blocks:** For file names and SUNO prompts
- **H2 headings:** `##` (not H3 `###`)
- **Line breaks:** Double spacing between paragraphs
- **Bold text:** For emphasis on key terms

## Examples

### Example 1: Electric Sheep Music Brief

**User request:**
```
"I received a brief email for a new Repco project from Electric Sheep Music"
```

**Command execution:**

1. Search Gmail for "Electric Sheep Music" + "Repco" + "brief"
2. Find email with subject "Repco Automotive - Q4 Campaign Brief"
3. Extract Google Doc link from email body
4. Fetch brief content showing:
   - Project: Repco Automotive Q4 Campaign
   - Duration: 15s and 30s versions
   - Platform: TV + digital
   - Due: 2025-11-15
5. Create file: `Repco Automotive Q4.md` (using project name as filename)
6. Generate AI suggestions for automotive-themed jingle
7. Create SUNO prompt (verified <1000 chars)
8. Confirm creation with summary

### Example 2: Panda Candy Brief

**User request:**
```
"New Panda Candy brief for Nintendo campaign arrived, create project"
```

**Command execution:**

1. Search Gmail for "Panda Candy" + "Nintendo"
2. Find recent brief email
3. Extract Google Doc and fetch content
4. Identify 30s social media spot requirement
5. Create project file with:
   - Gaming-focused creative direction
   - Upbeat, energetic AI suggestions
   - SUNO prompt optimized for gaming vibes
6. Mark `12 FOS: false` (social media platform)
7. Provide complete success report

## Error Handling

**Gmail issues:**
- No matching emails found → Ask for more search details
- Multiple matches → Present list for user selection
- Missing Google Doc link → Ask user to provide URL directly

**Google Doc extraction issues:**
- curl fails → Verify document ID is correct
- Empty content returned → Document may require authentication (ask user to copy/paste content)
- Malformed text → Document may have special formatting (ask user to provide clean version)
- Permission denied → Document is private (ask user to make publicly accessible or share link)

**Obsidian issues:**
- File creation error → Verify path exists
- Duplicate filename → Suggest alternative name

**AI generation issues:**
- SUNO prompt exceeds 1000 chars → Regenerate with shorter content
- Missing brief details → Ask user to provide missing information

## Evaluation Criteria

A successful project creation should:

1. ✅ **Complete frontmatter** with all required fields (dates, customer, status, booleans)
2. ✅ **Proper formatting** with callouts, code blocks, H2 headings, double spacing
3. ✅ **Accurate brief extraction** capturing all deliverables, requirements, creative direction
4. ✅ **High-quality AI suggestions** providing actionable creative direction for Harrison
5. ✅ **Valid SUNO prompt** under 1000 characters with complete structure and timing
6. ✅ **Correct file naming** using exact project name as filename (e.g., `Nintendo - EM.md`)
7. ✅ **Proper file location** in /02-projects/mokhouse/ directory
8. ✅ **Harrison's composer number** correctly set as "3" in file naming template

## Related Commands

- `/mokhouse-update-status` - Mark project as submitted, awarded, etc.
- `/mokhouse-create-invoice` - Create invoice when PO is received
- `/mokhouse-mark-paid` - Track payment completion

## Known Customers

Quick reference for Gmail searches:

**Electric Sheep Music Pty Ltd**
- Email: esmusic@dext.cc, accounts@electricsheepmusic.com
- Common subjects: Job numbers, client campaign names

**Panda Candy Pty Ltd**
- Email: accounts@pandacandy.com.au
- Common subjects: Brand names, PO references

---

**Version:** 1.1
**Integration:** Gmail + Google Docs (curl export) + Obsidian
**File Location:** `/02-projects/mokhouse/`
**Harrison's Composer Number:** 3
**Updated:** 2025-10-17 - Added explicit Bash + curl instructions for Google Doc extraction
