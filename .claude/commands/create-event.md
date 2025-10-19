---
created: "2025-10-17 16:30"
updated: "2025-10-17 20:15"
version_history:
  - version: "1.4"
    date: "2025-10-17 20:15"
    changes: "Fixed DataviewJS checkbox parsing for recurrence - now properly extracts checked pattern from list"
  - version: "1.3"
    date: "2025-10-17 19:45"
    changes: "Added recurring event support with checkbox-based recurrence patterns"
  - version: "1.2"
    date: "2025-10-17 19:15"
    changes: "Added automatic emoji prefix based on keyword detection (21 emoji categories)"
  - version: "1.1"
    date: "2025-10-17 18:45"
    changes: "Fixed wikilink YAML compatibility, added optional description body support"
  - version: "1.0"
    date: "2025-10-17 16:30"
    changes: "Initial creation"
description: |
  Create Event - Quickly create structured event files in your vault using the event.md template.

  Capabilities:
    - Interactive prompts for event details (title, date, time, category)
    - Automatic emoji prefix based on keyword detection (21 categories)
    - Recurring event support (daily/weekly/biweekly/monthly/yearly)
    - Quick mode for minimal input (just title + when + time if needed)
    - Auto-validates relation tags against 97-tags folder
    - YAML-safe wikilink formatting for relation field
    - Optional in-depth description in markdown body
    - Saves to 00-inbox/events/ with consistent naming
    - Integrates with daily notes "Today's Events" table

  Outputs:
    - Properly formatted event file with YAML frontmatter
    - Optional description content below frontmatter
    - Single file creates multiple occurrences (for recurring events)
    - Automatically appears in daily notes when `when` matches today
    - Clean filename: "Event Name.md"
examples:
  - /create-event
  - /create-event --quick "Team Meeting" "2025-10-20" "2:00 PM"
  - /create-event "Client Call" "2025-10-21"
---

# Create Event

This command helps you quickly create structured event files in your claudelife vault using the event.md template. Events automatically appear in your daily notes "Today's Events" table when the date matches.

## Usage

```bash
/create-event                    # Interactive mode
/create-event --quick           # Quick mode with prompts
```

## Interactive Process

When you run this command, I will:

1. Ask for the event title (this becomes the filename)
2. Ask for the date (`when`) in YYYY-MM-DD format (becomes start date for recurring events)
3. Ask if a time is needed (optional)
4. **Ask if this is a recurring event** (optional)
   - If yes: Ask for pattern (daily/weekly/biweekly/monthly/yearly)
   - If yes: Optionally set end date (`recurrence_end`)
5. Ask for category (optional: personal, work, health, etc.)
6. Ask if this relates to specific areas (mokai, mokhouse, p-dev, etc.)
7. Ask if you want to add a note (optional)
8. Ask if you need an in-depth description in the body (optional, only when relevant)
9. **Auto-detect emoji prefix** based on keywords in title, category, relation, and note
10. Validate relation tags against 97-tags folder
11. Create the event file in `00-inbox/events/` with string-based recurrence and YAML-safe wikilinks

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

## Input Requirements

**Required:**
- Event title (becomes filename)
- `when` date (YYYY-MM-DD format)

**Optional:**
- `time` (e.g., "2:00 PM", "14:00")
- `recurrence` (string: daily, weekly, biweekly, monthly, yearly)
- `recurrence_end` (YYYY-MM-DD format, when recurrence stops)
- `category` (freeform text: personal, work, health, etc.)
- `relation` (must exist in 97-tags: mokai, mokhouse, p-dev, etc.)
- `note` (brief context for frontmatter)
- `description` (in-depth details in markdown body, only when necessary)

## Recurrence Patterns

Create recurring events without creating thousands of markdown files. One file generates multiple occurrences automatically.

### Available Patterns

Events use a simple string value for recurrence in frontmatter:

```yaml
recurrence: yearly
```

Valid values: `daily`, `weekly`, `biweekly`, `monthly`, `yearly`

### Recurrence Fields

**`recurrence`** (optional): String value (daily/weekly/biweekly/monthly/yearly)
**`recurrence_end`** (optional): YYYY-MM-DD format, when to stop recurring
- If not provided, events recur indefinitely (shows next 90 days in daily notes)

### How It Works

1. **Start date**: The `when` field becomes the first occurrence
2. **Pattern**: The `recurrence` string value determines frequency
3. **End date**: Optional `recurrence_end` field stops repetition
4. **Single file**: One markdown file creates all occurrences
5. **DataviewJS**: Daily notes automatically show matching occurrences

**Technical Implementation**: The `occursOn()` function in daily-note.md reads the recurrence string value and applies date math to determine if the event occurs on a specific date.

### Examples

**Weekly Team Meeting** (every Monday):
```yaml
when: 2025-10-20          # First Monday
recurrence: weekly
recurrence_end: 2025-12-31
```
Result: Shows every Monday until Dec 31, 2025

**Daily Standup**:
```yaml
when: 2025-10-20
time: 9:00 AM
recurrence: daily
recurrence_end: 2025-10-24  # Mon-Fri only for this week
```

**Monthly Invoice Due**:
```yaml
when: 2025-10-15          # 15th of month
recurrence: monthly
# No end date = continues indefinitely
```

**Yearly Birthday**:
```yaml
when: 2025-12-25
recurrence: yearly
# No end date = every year
```

## Emoji Detection Logic

Events are automatically prefixed with emojis based on keyword detection (case-insensitive) across **title**, **category**, **relation**, and **note** fields. The system prioritizes predefined mappings but can **get creative with emoji selection** when a more fitting emoji would better represent the event.

### Creative Emoji Selection

Beyond the predefined keywords below, use judgment to select emojis that best represent the event:
- **Sports events**: 🏈 (football), ⚽ (soccer), 🏀 (basketball), 🏉 (rugby), ⚾ (baseball), 🎾 (tennis), 🏐 (volleyball)
- **Seasonal/Nature**: 🌸 (spring), ☀️ (summer), 🍂 (autumn), ❄️ (winter), 🌺 (tropical)
- **Cultural**: 🎭 (theatre), 🎬 (cinema), 📚 (reading), 🎨 (art)
- **Food/Drinks**: ☕ (coffee), 🍕 (pizza), 🍔 (burger), 🍰 (cake), 🍻 (drinks)
- **Special occasions**: 💍 (engagement/wedding), 🎓 (graduation), 🏆 (awards)

**Use creative emojis when:**
- The event title suggests a specific activity (e.g., "Super Bowl" → 🏈, "Art Gallery Opening" → 🎨)
- A more specific emoji exists than the category default (e.g., "Coffee with Client" → ☕ instead of 💼)
- The emoji adds clarity or personality to the calendar view

### Priority Order (Predefined Keywords, Specific → General):

**Business Entities:**
- ⛰️ MOKAI - Keywords: `mokai`
- 🎹 Mok House/ESM - Keywords: `mokhouse`, `mok house`, `esm`, `music production`
- 🎧 SAFIA - Keywords: `safia`

**Appointments & Maintenance:**
- 🏥 Medical - Keywords: `doctor`, `medical`, `appointment`, `dentist`, `hospital`
- 🚘 Car Registration - Keywords: `car`, `rego`, `registration`, `vehicle`

**Special Dates:**
- 🎂 Birthday - Keywords: `birthday`, `bday`
- 📅 Key Dates - Keywords: `christmas`, `halloween`, `easter`, `anzac`, `kings birthday`, `public holiday`
- 🔆 Daylight Savings - Keywords: `daylight`, `savings`, `dst`
- 🌴 Holiday/Vacation - Keywords: `holiday`, `vacation`, `travel`, `trip`

**Travel & Logistics:**
- ✈️ Flight - Keywords: `flight`, `plane`, `airport`, `airline`

**Financial:**
- 🏦 Accounting - Keywords: `accounting`, `accountant`, `tax`, `ato`, `bookkeeper`

**Activities:**
- 🏋️ Gym/Workout - Keywords: `gym`, `workout`, `exercise`, `fitness`, `training session`
- 🍽️ Meal - Keywords: `dinner`, `lunch`, `breakfast`, `meal`, `restaurant`, `brunch`
- 🎵 Music Event - Keywords: `concert`, `gig`, `show`, `performance`, `festival`
- 🎓 Training/Education - Keywords: `training`, `course`, `workshop`, `seminar`, `class`, `lesson`
- 🎉 Celebration - Keywords: `party`, `celebration`, `anniversary`, `engagement`

**Work-Related:**
- 📞 Remote Meeting - Keywords: `call`, `phone`, `zoom`, `teams`, `video call`
- 💻 Tech/Dev - Keywords: `dev`, `development`, `coding`, `tech`, `programming`, `hackathon`
- 🏠 Home Tasks - Keywords: `home`, `house`, `maintenance`, `repair`, `plumber`
- 💼 General Business - Keywords: `meeting`, `work`, `business`, `conference`, `client`

**Flags:**
- 🔴 Important - Keywords: `important`, `urgent`, `critical`, `priority`

**Default:** No emoji if no keywords match

### Examples (Predefined):
- "MOKAI Strategy Meeting" → "⛰️ MOKAI Strategy Meeting"
- "Doctor Appointment" → "🏥 Doctor Appointment"
- "Mok House Recording Session" → "🎹 Mok House Recording Session"
- "Christmas Day" → "📅 Christmas Day"
- "Team Zoom Call" → "📞 Team Zoom Call"
- "Gym Session" → "🏋️ Gym Session"

### Examples (Creative):
- "Super Bowl Party" → "🏈 Super Bowl Party"
- "Coffee with Sarah" → "☕ Coffee with Sarah"
- "Art Gallery Opening" → "🎨 Art Gallery Opening"
- "Pizza Night" → "🍕 Pizza Night"
- "Theatre Show" → "🎭 Theatre Show"
- "Book Club Meeting" → "📚 Book Club Meeting"
- "Graduation Ceremony" → "🎓 Graduation Ceremony"

## Process

I'll help you create an event by:

1. **Gather event details** through interactive prompts
2. **Detect appropriate emoji** by scanning for keywords in:
   - Title field (case-insensitive)
   - Category field
   - Relation field (e.g., "mokai" → ⛰️)
   - Note field
   - **Use creative judgment**: If a more specific/fitting emoji exists beyond predefined keywords, use it
   - Priority: Specific creative emoji > Predefined keyword match > No emoji
3. **Validate relation tags** by checking 97-tags folder
   - If relation specified, verify it exists (e.g., `mokai.md`, `mokhouse.md`)
   - Format as YAML-safe wikilink (quoted string): `"[[mokai]]"`
4. **Ask about description** - Only if event needs more context than `note` field
   - Skip for simple events (appointments, meetings)
   - Use for complex events (conferences, multi-day events, detailed agendas)
5. **Create event file** in `00-inbox/events/` using this structure:
   ```yaml
   ---
   type:
     - event
   category: [category if provided]
   when: YYYY-MM-DD
   time: [time if provided]
   recurrence: [pattern if provided: daily/weekly/biweekly/monthly/yearly]
   recurrence_end: [YYYY-MM-DD if provided]
   relation: "[[ tag ]]" # YAML-safe quoted wikilink
   archive:
   note: [note if provided]
   ---

   ## Description (optional, only if provided)

   [Detailed event information, agenda, requirements, etc.]
   ```
6. **Name file** as `Event Name.md` (exact title provided)
7. **Confirm creation** with file path

## Available Relations (from 97-tags)

Common area relations you can use:
- `[[mokai]]` - MOKAI business events
- `[[mokhouse]]` - MOK HOUSE projects
- `[[mok-music]]` - Music production events
- `[[p-dev]]` - Personal development
- `[[business]]` - General business
- `[[admin]]` - Administrative tasks
- `[[tech]]` - Technical/developer events
- `[[ai]]` - AI research events
- `[[health-fitness]]` - Health/fitness events

**Validation**: The command will check if the relation tag exists in `97-tags/` before adding it to the event file.

## Quick Mode Examples

### Minimal Event (just date)
```
You: /create-event
Me: What's the event title?
You: Doctor Appointment
Me: When is this event? (YYYY-MM-DD)
You: 2025-10-20
Me: Does this event have a specific time? (optional)
You: [press enter to skip]
Me: Category? (optional)
You: health
Me: Is this related to any areas? (mokai, mokhouse, p-dev, etc.)
You: [press enter to skip]
Me: Any notes to add? (optional)
You: Bring medical records
```

**Output**: `00-inbox/events/🏥 Doctor Appointment.md`
```yaml
---
type:
  - event
category: health
when: 2025-10-20
time:
relation:
archive:
note: Bring medical records
---
```
*Emoji detected: 🏥 (medical keywords: "doctor", "appointment")*

### Business Event with Time
```
You: /create-event
Me: What's the event title?
You: MOKAI Strategy Meeting
Me: When is this event? (YYYY-MM-DD)
You: 2025-10-22
Me: Does this event have a specific time?
You: 2:00 PM
Me: Category? (optional)
You: business
Me: Is this related to any areas?
You: mokai
Me: Any notes?
You: Discuss Q1 tender pipeline
```

**Output**: `00-inbox/events/⛰️ MOKAI Strategy Meeting.md`
```yaml
---
type:
  - event
category: business
when: 2025-10-22
time: 2:00 PM
relation: "[[mokai]]"
archive:
note: Discuss Q1 tender pipeline
---
```
*Emoji detected: ⛰️ (relation: "mokai")*

### All-Day Event (no time)
```
You: /create-event
Me: What's the event title?
You: Christmas Day
Me: When is this event? (YYYY-MM-DD)
You: 2025-12-25
Me: Does this event have a specific time?
You: [press enter to skip]
Me: Category?
You: personal
Me: Is this related to any areas?
You: [press enter to skip]
Me: Any notes?
You: [press enter to skip]
Me: Need an in-depth description? (optional)
You: [press enter to skip]
```

**Output**: `00-inbox/events/📅 Christmas Day.md`
```yaml
---
type:
  - event
category: personal
when: 2025-12-25
time:
relation:
archive:
note:
---
```
*Emoji detected: 📅 (key date keyword: "christmas")*

### Complex Event with Description Body
```
You: /create-event
Me: What's the event title?
You: Tech Conference 2025
Me: When is this event? (YYYY-MM-DD)
You: 2025-11-15
Me: Does this event have a specific time?
You: 9:00 AM
Me: Category?
You: professional development
Me: Is this related to any areas?
You: tech
Me: Any notes?
You: AI & Cloud Computing focus
Me: Need an in-depth description? (Only if event needs detailed agenda, requirements, etc.)
You: yes
Me: Enter description (can be multi-line):
You: Annual tech conference covering latest in AI, cloud infrastructure, and DevOps.

Key sessions:
- 9:00 AM: Opening keynote on AI advancements
- 11:00 AM: Workshop on cloud-native architectures
- 2:00 PM: Panel discussion on ethical AI
- 4:00 PM: Networking session

Requirements:
- Bring laptop for workshops
- Business casual attire
- Badge pickup at registration desk
```

**Output**: `00-inbox/events/🎓 Tech Conference 2025.md`
```yaml
---
type:
  - event
category: professional development
when: 2025-11-15
time: 9:00 AM
relation: "[[tech]]"
archive:
note: AI & Cloud Computing focus
---

## Description

Annual tech conference covering latest in AI, cloud infrastructure, and DevOps.

Key sessions:
- 9:00 AM: Opening keynote on AI advancements
- 11:00 AM: Workshop on cloud-native architectures
- 2:00 PM: Panel discussion on ethical AI
- 4:00 PM: Networking session

Requirements:
- Bring laptop for workshops
- Business casual attire
- Badge pickup at registration desk
```
*Emoji detected: 🎓 (category keyword: "professional development" → training/education)*

### Recurring Event Example
```
You: /create-event
Me: What's the event title?
You: Weekly Team Standup
Me: When is this event? (YYYY-MM-DD)
You: 2025-10-20
Me: Does this event have a specific time?
You: 9:00 AM
Me: Is this a recurring event? (y/n)
You: y
Me: Choose recurrence pattern:
    - daily
    - weekly
    - biweekly
    - monthly
    - yearly
You: weekly
Me: When should recurrence end? (YYYY-MM-DD, or leave blank for no end)
You: 2025-12-31
Me: Category? (optional)
You: work
Me: Is this related to any areas?
You: mokai
Me: Any notes?
You: Discuss sprint progress
```

**Output**: `00-inbox/events/⛰️ Weekly Team Standup.md`
```yaml
---
type:
  - event
category: work
when: 2025-10-20
time: 9:00 AM
recurrence: weekly
recurrence_end: 2025-12-31
relation: "[[mokai]]"
archive:
note: Discuss sprint progress
---
```
*Emoji detected: ⛰️ (relation: "mokai")*
*Recurrence: Appears every Monday from Oct 20 - Dec 31, 2025*

**Result**: One file creates 11 weekly occurrences. Each Monday's daily note will show this event automatically.

## Integration with Daily Notes

Events automatically appear in your daily note's "Today's Events" table when:
- `type` contains "event"
- `when` date matches today's date

The table displays (with emoji prefixes):
| Event | Time | Note |
|-------|------|------|
| ⛰️ MOKAI Strategy Meeting | 2:00 PM | Discuss Q1 tender pipeline |
| 🏥 Doctor Appointment | 10:00 AM | Bring medical records |
| 📅 Christmas Day | | Family gathering |

## Evaluation Criteria

A successful event file should:

1. ✅ **Be properly located** in `00-inbox/events/` folder
2. ✅ **Have valid YAML frontmatter** with all template fields
3. ✅ **Use correct filename** with emoji prefix (if detected) matching event title
4. ✅ **Have appropriate emoji** based on keyword detection (or none if no match)
5. ✅ **Contain validated relation tags** (only from 97-tags)
6. ✅ **Display in daily notes** with emoji prefix when `when` matches today
7. ✅ **Have required fields filled** (`type: [event]`, `when` date)

## Related Resources

- Event template: `98-templates/event.md`
- Emoji mappings: `00-inbox/Calendar emojis.md` (21 category mappings)
- Events folder: `00-inbox/events/`
- Relations tags: `97-tags/`
- Daily note template: `98-templates/daily-note.md` (Today's Events table)

## Error Handling

**Invalid relation tag:**
```
You: Is this related to any areas?
User: mokai-test
Me: ⚠️ Warning: "mokai-test" doesn't exist in 97-tags.
    Available relations: mokai, mokhouse, mok-music, p-dev, business...
    Would you like to use one of these, or skip the relation field?
```

**Invalid date format:**
```
You: When is this event?
User: Oct 20
Me: ⚠️ Please use YYYY-MM-DD format (e.g., 2025-10-20)
```

**Missing events folder:**
```
Me: Creating 00-inbox/events/ folder...
    ✅ Folder created
    📝 Creating event file...
```
