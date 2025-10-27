---
date: "2025-10-21"
system_type: "claude-skill"
status: "active"
auto_generated: true
generated_by: "/report:document-system"
---

# OBSIDIA Training System

**Obsidian Second Brain Architect for Intelligent Data-driven Auto-regulation**

## Overview

### What It Does

OBSIDIA is an intelligent training assistance system that provides:
- **Context-Aware Session Planning**: Generates workout plans based on daily note data (energy, sleep, stress, soreness)
- **Workout Logging**: Structured templates for comprehensive exercise tracking
- **XP Gamification**: Motivational system with multipliers for intensity, form quality, exercise type, and achievements
- **Injury Pattern Detection**: NLP-based scanning for pain keywords and temporal correlation tracking
- **Progress Analysis**: Tracks volume, intensity, frequency, and recovery metrics over time

### Why It Exists

Built to solve the problem of rigid training programs that don't adapt to daily readiness. OBSIDIA implements auto-regulation principles from evidence-based strength training methodology, combining RPE-based intensity prescription with progressive overload tracking.

**Key Philosophy**:
- Train hard when you can, back off when you should
- Progressive disclosure - load context only when needed
- Gamify adherence without sacrificing training quality

### Integration Pattern

OBSIDIA uses the **Claude Skills** architecture for:
- **Auto-activation** on training-related keywords (gym, workout, exercise, training, lift)
- **Progressive disclosure** - loads config/scripts from filesystem instead of dumping everything in context
- **Bundled intelligence** - Python scripts for session planning and XP calculation
- **Daily note integration** - reads frontmatter (energy_morning, sleep_quality) to inform workout recommendations

---

## Location

### File Structure

```
.claude/skills/obsidia-training/          # Skill root
├── SKILL.md                              # Main orchestrator (265 lines)
│
├── programs/
│   └── current-program.yaml              # 8-week hypertrophy block (218 lines)
│
├── config/
│   ├── xp-config.yaml                    # XP calculation rules (134 lines)
│   ├── exercises.yaml                    # Exercise library (289 lines)
│   └── injury-keywords.yaml              # Pain detection keywords (206 lines)
│
├── scripts/
│   ├── plan_session.py                   # Session planner (230 lines)
│   └── calculate_xp.py                   # XP calculator (206 lines)
│
└── reference/
    ├── progression.md                    # Progressive overload guide (205 lines)
    └── recovery.md                       # Recovery protocols (308 lines)

01-areas/health-fitness/training/         # User training data
├── programs/                             # Historical programs
├── workouts/                             # Daily workout logs
├── config/                               # User overrides
├── progress/                             # Analytics outputs
└── injuries/                             # Injury tracking reports

98-templates/workout.md                   # Workout log template (177 lines)
```

### Key Entry Points

- **SKILL.md**: Main orchestrator loaded by Claude when training keywords detected
- **plan_session.py**: CLI script for generating session options (`python scripts/plan_session.py`)
- **calculate_xp.py**: CLI script for XP calculation (`python scripts/calculate_xp.py <workout-file>`)
- **workout.md template**: Used to create daily workout logs via Templater

---

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      OBSIDIA Skill                          │
│                    (SKILL.md orchestrator)                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐   ┌──────────┐
    │ Session │    │    XP    │   │  Injury  │
    │ Planner │    │Calculator│   │ Detector │
    └────┬────┘    └────┬─────┘   └────┬─────┘
         │              │              │
         │              │              │
         ▼              ▼              ▼
    ┌────────────────────────────────────┐
    │         Config Files               │
    │  • current-program.yaml            │
    │  • xp-config.yaml                  │
    │  • exercises.yaml                  │
    │  • injury-keywords.yaml            │
    └────────────────────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────┐
    │      User Training Data            │
    │  • Daily workout logs              │
    │  • Progress analytics              │
    │  • Injury reports                  │
    └────────────────────────────────────┘
```

### Data Flow

1. **User Trigger**: Mentions "gym", "workout", etc. in conversation
2. **SKILL.md Activation**: Claude loads orchestrator, displays available actions
3. **Session Planning Path**:
   - Read daily note frontmatter (energy, sleep, stress)
   - Load `current-program.yaml` to determine scheduled workout type
   - Query recent workout history from `01-areas/health-fitness/training/workouts/`
   - Generate 3 options: Standard, Adapted, Recovery
   - Apply adaptation rules based on context
4. **Workout Logging Path**:
   - Use Templater to create workout file from `98-templates/workout.md`
   - User fills in exercise data (sets, reps, weight, RPE, form)
   - Run `calculate_xp.py` to compute session XP
5. **Injury Detection Path**:
   - Scan workout logs and daily notes for pain keywords
   - Categorize by severity (mild/moderate/severe) and body region
   - Track temporal patterns (frequency, progression)
   - Alert if patterns exceed thresholds

### Integration Points

**Daily Notes Integration**:
```yaml
# Daily note frontmatter (read by plan_session.py)
energy_morning: 7    # /10
sleep_quality: 8     # /10
stress_level: 5      # /10
soreness: "mild"     # none/mild/moderate/severe
```

**Workout Template Integration**:
```yaml
# Workout log frontmatter (written by user)
session_type: "upper_push"
program_week: 2
day_number: 5
status: "completed"
total_xp: 4250
```

**Templater Variables**:
- `{{date:YYYY-MM-DD}}` - Auto-fills workout date
- Template creates structured tables for exercise tracking

---

## Configuration

### Program Configuration

**File**: `.claude/skills/obsidia-training/programs/current-program.yaml`

**Structure**:
```yaml
program_info:
  name: "Hypertrophy Block - Upper/Lower Split"
  phase: "Muscle Building"
  duration_weeks: 8
  current_week: 1

schedule:
  weekly_frequency: 4
  rest_days: [3, 7]  # Wednesday, Sunday
  preferred_days:
    upper_push: [1, 5]    # Mon, Fri
    lower_push: [2, 6]    # Tue, Sat
    upper_pull: [4]       # Thu

workouts:
  upper_push:
    focus: "Chest, Shoulders, Triceps"
    exercises:
      - name: "Barbell Bench Press"
        sets: 4
        reps: "8-10"
        rpe_target: 8
        primary: true
        rest_seconds: 180
        progression: "Add 2.5kg when hit 4x10 at RPE 8"
```

**Key Fields**:
- `primary: true` - Compound exercises get 1.3x XP multiplier
- `rpe_target` - Target intensity (1-10 scale, based on reps in reserve)
- `progression` - When to increase load

**Adaptation Rules**:
```yaml
recovery_protocols:
  adaptation_rules:
    tired_but_ok:
      condition: "energy < 7 AND sleep > 5"
      action: "Reduce volume by 10%, keep intensity"

    very_tired:
      condition: "energy < 6 OR sleep < 5"
      action: "Switch to recovery session"

    high_stress:
      condition: "stress > 7"
      action: "Reduce RPE targets by 1 point"
```

### XP Configuration

**File**: `.claude/skills/obsidia-training/config/xp-config.yaml`

**Base Formula**:
```
XP = weight_kg × reps × (RPE_mult × form_mult × exercise_mult × achievement_mult)
```

**Multipliers**:
```yaml
multipliers:
  # Intensity
  rpe_9_plus: 1.2        # High effort bonus
  rpe_8_to_9: 1.0        # Target zone
  rpe_below_8: 0.9       # Penalty for going too easy

  # Form Quality
  form_excellent: 1.1    # 9-10/10
  form_good: 1.0         # 7-8/10
  form_poor: 0.8         # <7/10 (penalty)

  # Exercise Type
  primary_exercise: 1.3  # Compound lifts
  accessory_exercise: 1.0

  # Achievements
  pr_achieved: 2.0       # 100% bonus for PRs
  first_time_exercise: 1.5
  all_sets_hit_target: 1.1
```

**Level System**:
```yaml
level_system:
  xp_per_level: 10000

  level_milestones:
    5: "Novice Lifter - Unlock advanced exercise variations"
    10: "Intermediate Lifter - Unlock periodization templates"
    15: "Advanced Lifter - Unlock custom program builder"
    20: "Elite Lifter - Unlock competition prep protocols"
```

**Streak Bonuses**:
```yaml
streaks_and_bonuses:
  weekly_consistency:
    description: "Hit all planned sessions in a week"
    bonus_xp: 500

  perfect_week:
    description: "All sessions + no missed exercises"
    bonus_xp: 1000

  monthly_milestone:
    description: "16+ sessions in a month"
    bonus_xp: 2000
```

### Exercise Library

**File**: `.claude/skills/obsidia-training/config/exercises.yaml`

**Organization**: Exercises grouped by movement pattern (upper_push, upper_pull, lower_push, lower_pull)

**Example Entry**:
```yaml
upper_push:
  chest_primary:
    - name: "Barbell Bench Press"
      muscle_groups: ["chest", "triceps", "front_delts"]
      equipment: ["barbell", "bench"]
      difficulty: "intermediate"
      form_cues:
        - "Retract scapula, chest up"
        - "Bar touches mid-chest"
        - "Drive through feet"
        - "Elbows 45-degree angle"
```

**Substitution Matrix**:
```yaml
substitution_matrix:
  "Barbell Bench Press":
    alternatives: ["Dumbbell Bench Press", "Incline Barbell Bench Press"]
    reason: "Equipment availability, injury, variety"

  "Back Squat":
    alternatives: ["Front Squat", "Leg Press", "Bulgarian Split Squat"]
    reason: "Mobility issues, lower back strain, equipment"
```

### Injury Detection Configuration

**File**: `.claude/skills/obsidia-training/config/injury-keywords.yaml`

**Pain Severity Levels**:
```yaml
pain_keywords:
  severity_high:
    keywords: ["sharp", "stabbing", "intense", "severe"]
    alert_level: "critical"
    action: "Stop training this body region immediately"

  severity_moderate:
    keywords: ["aching", "sore", "tender", "painful"]
    alert_level: "warning"
    action: "Reduce load, monitor closely, consider deload"
```

**Body Region Mapping**:
```yaml
body_regions:
  upper_body:
    shoulder:
      keywords: ["shoulder", "rotator cuff", "deltoid"]
      common_exercises: ["Overhead Press", "Bench Press", "Lateral Raises"]

  lower_body:
    lower_back:
      keywords: ["lower back", "lumbar", "spine"]
      common_exercises: ["Deadlifts", "Squats", "Romanian Deadlifts"]
      high_risk: true
```

**Alert Thresholds**:
```yaml
alert_thresholds:
  immediate_alert:
    conditions:
      - "severity_high keyword detected"
      - "Same body region mentioned 3+ days in a row"
      - "Pain during warm-up (not just work sets)"

  warning_alert:
    conditions:
      - "severity_moderate keyword detected"
      - "Same body region mentioned 5+ times in 2 weeks"
```

---

## Usage

### Planning a Session

**Workflow**:
1. User says: "What should I train today?" or "Plan my workout"
2. OBSIDIA activates and displays available actions
3. User selects: "Plan next workout session"
4. System executes:

**What OBSIDIA Does**:
```python
# 1. Read daily note context
energy = daily_note.frontmatter.energy_morning       # e.g., 7/10
sleep = daily_note.frontmatter.sleep_quality         # e.g., 8/10
stress = daily_note.frontmatter.stress_level         # e.g., 5/10
soreness = daily_note.frontmatter.soreness           # e.g., "mild"

# 2. Determine which workout type is due
today = datetime.now().isoweekday()  # 1=Mon, 7=Sun
if today in [1, 5]:  # Monday or Friday
    session_type = "upper_push"

# 3. Generate 3 options
standard = load_program_as_written(session_type)

adapted = apply_adaptation_rules(standard, {
    'energy': energy,
    'sleep': sleep,
    'stress': stress,
    'soreness': soreness
})

recovery = generate_recovery_session({
    'energy': energy,
    'sleep': sleep
})

# 4. Recommend best option
if energy < 6 or sleep < 5:
    recommendation = "recovery"
elif energy < 7 or stress > 7 or soreness in ["moderate", "severe"]:
    recommendation = "adapted"
else:
    recommendation = "standard"
```

**Example Output**:
```markdown
## Session Plan for 2025-10-21 (Monday)

**Daily Context**:
- Energy: 7/10 ✅
- Sleep: 8/10 ✅
- Stress: 5/10 ✅
- Soreness: Mild (shoulders)

**Session Type**: Upper Push (Chest, Shoulders, Triceps)

### ✅ RECOMMENDED: Standard Program
Follow program as written - you're ready for full intensity.

**Exercises**:
1. Barbell Bench Press - 4x8-10 @ RPE 8 (180s rest)
2. Overhead Press - 4x8-10 @ RPE 8 (180s rest)
3. Incline Dumbbell Press - 3x10-12 @ RPE 7 (90s rest)
4. Lateral Raises - 3x12-15 @ RPE 7 (60s rest)
5. Tricep Pushdowns - 3x12-15 @ RPE 7 (60s rest)

**Focus**: Progressive overload on compound lifts
**Estimated Duration**: 60-75 min
**Target XP**: 3800-4500

---

### 🔀 OPTION 2: Adapted (Volume Reduced)
Use if you want to train but play it safe.

**Changes**:
- Remove 1 set from accessories (exercises 3-5)
- Reduce Bench/OHP to 3 sets instead of 4
- Keep intensity (RPE targets unchanged)

**Estimated Duration**: 45-55 min
**Target XP**: 2800-3400

---

### 🛌 OPTION 3: Recovery
Active recovery and movement quality.

**Protocol**:
- 20-30 min light cardio (walk/bike, conversational pace)
- 10 min dynamic stretching (major muscle groups)
- 10 min foam rolling (focus on shoulders)

**XP**: 0 (recovery doesn't count toward XP, but preserves readiness)
```

### Logging a Workout

**Workflow**:
1. Use Templater hotkey to create workout log from `98-templates/workout.md`
2. Fill in frontmatter (session_type, program_week, day_number)
3. Complete Pre-Workout Check-in section
4. Log each exercise in tables during workout
5. Complete Post-Workout Summary
6. Run XP calculation

**Exercise Logging Format**:
```markdown
### Exercise 1: Barbell Bench Press
**Type:** Primary
**Target:** Chest, Triceps, Front Delts
**Setup Notes:** 80kg starting weight, standard grip width

| Set | Weight (kg) | Reps | RPE | Form (/10) | Rest (sec) | Notes |
|-----|-------------|------|-----|------------|------------|-------|
| 1   | 80          | 10   | 7   | 9          | 180        | Warmup set, felt good |
| 2   | 85          | 9    | 8   | 8          | 180        | Target weight |
| 3   | 85          | 8    | 9   | 8          | 180        | Grinder on last rep |
| 4   | 85          | 8    | 9   | 7          | 180        | Form broke slightly |

**Set XP:** (Auto-calculated by script)
**Exercise Notes:** Shoulders felt tight, might need more warmup next time
```

**XP Calculation**:
```bash
# Run from vault root
python .claude/skills/obsidia-training/scripts/calculate_xp.py \
  01-areas/health-fitness/training/workouts/🏋️2025-10-21.md

# Output:
# Set 1: 80kg × 10 reps × 1.0 (RPE 7) × 1.1 (form 9) × 1.3 (primary) = 1144 XP
# Set 2: 85kg × 9 reps × 1.0 (RPE 8) × 1.0 (form 8) × 1.3 (primary) = 994 XP
# Set 3: 85kg × 8 reps × 1.2 (RPE 9) × 1.0 (form 8) × 1.3 (primary) = 1061 XP
# Set 4: 85kg × 8 reps × 1.2 (RPE 9) × 0.8 (form 7) × 1.3 (primary) = 849 XP
# Exercise Total: 4048 XP
```

### Tracking Progress

**Weekly Summary Query**:
```markdown
You: "Analyze my training week"

OBSIDIA:
1. Scans workout logs from last 7 days
2. Aggregates volume metrics (total sets, reps, tonnage)
3. Calculates average RPE and form quality
4. Checks for missed sessions
5. Runs injury pattern detection
6. Compares to program prescription
```

**Example Output**:
```markdown
## Training Week: Oct 14-20, 2025

### Session Adherence
✅ 4/4 planned sessions completed
- Mon: Upper Push (4250 XP)
- Tue: Lower Push (3890 XP)
- Thu: Upper Pull (4100 XP)
- Sat: Lower Pull (3750 XP)

**Weekly XP**: 15,990 (Level 1 → 16% progress to Level 2)

### Volume Metrics
- Total sets: 92
- Total reps: 1,048
- Total tonnage: 24,560 kg
- Average RPE: 8.1
- Average form quality: 8.3/10

### Progressive Overload Check
✅ Bench Press: 80kg → 82.5kg (+2.5kg)
✅ Squat: 100kg → 102.5kg (+2.5kg)
⚠️ Deadlift: No progression (held at 120kg, form concerns)

### Injury Scan
⚠️ Warning: "Lower back" mentioned 3 times this week
- Mon: "Lower back tight after deadlifts"
- Thu: "Lower back sore during warm-up"
- Sat: "Lower back aching"

**Recommendation**: Deload deadlifts next week, add McGill Big 3 core work

### Recovery Status
Sleep average: 7.8/10 ✅
Energy average: 7.2/10 ✅
No major red flags
```

### Injury Pattern Detection

**Automatic Scanning**:
OBSIDIA continuously scans:
1. **Workout logs**: Exercise notes, set notes, post-workout feedback
2. **Daily notes**: Body section, health mentions, pain descriptions

**Detection Example**:
```markdown
# Workout log entry
**Exercise Notes:** "Shoulder felt sharp pain on last set of overhead press"

# Daily note entry
**Body**: "Shoulder still sore from yesterday's workout, pain when reaching overhead"

# OBSIDIA Alert
⚠️ INJURY PATTERN DETECTED

**Body Region**: Shoulder (right)
**Severity**: High ("sharp pain" keyword)
**Frequency**: 2 mentions in 2 days
**Related Exercises**: Overhead Press, Lateral Raises

**Recommendation**:
1. Stop training overhead pressing movements immediately
2. Focus on horizontal pressing only (bench, push-ups)
3. Add rotator cuff rehab exercises
4. Monitor for 7 days before reintroducing overhead work
5. Consider medical consultation if pain persists >1 week
```

---

## Examples

### Example 1: Standard Session (Optimal Readiness)

**Context**:
```yaml
# Daily note frontmatter
energy_morning: 8
sleep_quality: 9
stress_level: 4
soreness: "none"
```

**User**: "What should I train today?"

**OBSIDIA Response**:
```markdown
## Session Plan - Upper Push (Monday)

**Your Readiness**: ✅ Excellent
- Energy: 8/10
- Sleep: 9/10
- Stress: 4/10
- Soreness: None

**Recommendation**: STANDARD PROGRAM

You're firing on all cylinders - hit the program as written and push for PRs!

**Workout**:
1. Barbell Bench Press - 4x8-10 @ RPE 8
   - **Progression Opportunity**: Last week you hit 3x10 @ 80kg. Try 82.5kg today.
2. Overhead Press - 4x8-10 @ RPE 8
3. Incline Dumbbell Press - 3x10-12 @ RPE 7
4. Lateral Raises - 3x12-15 @ RPE 7
5. Tricep Pushdowns - 3x12-15 @ RPE 7

**Target XP**: 4200-4800 (potential for bonus if you hit PRs!)
**Duration**: 60-75 min
```

### Example 2: Adapted Session (Suboptimal Readiness)

**Context**:
```yaml
# Daily note frontmatter
energy_morning: 6
sleep_quality: 6
stress_level: 7
soreness: "moderate"  # shoulders
```

**User**: "Plan my workout"

**OBSIDIA Response**:
```markdown
## Session Plan - Upper Push (Monday)

**Your Readiness**: ⚠️ Suboptimal
- Energy: 6/10 (below threshold)
- Sleep: 6/10 (below threshold)
- Stress: 7/10 (borderline high)
- Soreness: Moderate (shoulders)

**Recommendation**: ADAPTED PROGRAM

Not your best day - let's train smart and protect your shoulders.

**Adaptations Applied**:
1. ✂️ Volume reduced by 20% (remove 1 set from all exercises)
2. 🎚️ RPE targets lowered to 7 (from 8)
3. 🔀 Replaced Overhead Press with Incline Bench (shoulder-friendly)
4. ➕ Added extra warmup sets

**Modified Workout**:
1. Barbell Bench Press - 3x8-10 @ RPE 7 (down from 4 sets)
2. Incline Barbell Press - 3x8-10 @ RPE 7 (replaces OHP)
3. Incline Dumbbell Press - 2x10-12 @ RPE 6
4. Lateral Raises - 2x12-15 @ RPE 6 (lighter, focus on pump)
5. Tricep Pushdowns - 2x12-15 @ RPE 6

**Target XP**: 2400-2800 (reduced, but preserves stimulus)
**Duration**: 40-50 min

**Recovery Focus**:
- Extra shoulder mobility work pre-workout
- Foam roll upper back and lats
- Ice shoulders post-workout
- Aim for 8+ hours sleep tonight
```

### Example 3: Recovery Session (Poor Readiness)

**Context**:
```yaml
# Daily note frontmatter
energy_morning: 4
sleep_quality: 4
stress_level: 8
soreness: "severe"  # full body
```

**User**: "Should I train today?"

**OBSIDIA Response**:
```markdown
## Session Plan - Recovery Recommended

**Your Readiness**: ❌ Poor
- Energy: 4/10 (critically low)
- Sleep: 4/10 (critically low)
- Stress: 8/10 (high)
- Soreness: Severe (full body)

**Recommendation**: SKIP TRAINING, DO RECOVERY

Your body is sending clear signals - pushing through would be counterproductive.

**Recovery Session Protocol**:

1. **Light Movement** (20-30 min)
   - Walk at conversational pace
   - OR easy bike ride
   - Keep heart rate <120 bpm
   - Focus: Blood flow, feel-good endorphins

2. **Mobility Work** (10 min)
   - Cat-cow stretches
   - World's greatest stretch
   - Hip 90/90 rotations
   - Shoulder dislocations with band

3. **Foam Rolling** (10 min)
   - Focus on sore areas
   - Slow, controlled passes
   - Breathe deeply

4. **Optional**: Contrast shower (hot 3 min / cold 1 min × 3 rounds)

**XP**: 0 (recovery doesn't count, but preserves long-term gains)
**Duration**: 30-40 min total

**Action Items**:
- Aim for 9+ hours sleep tonight
- Increase water intake (3L+ today)
- Consider Epsom salt bath
- Reassess tomorrow morning
- If still feeling poor, take full rest day
```

### Example 4: Injury Detection Alert

**Trigger**: Automated scan finds pattern

**OBSIDIA Alert**:
```markdown
🚨 INJURY PATTERN DETECTED

**Detection Summary**:
- Body region: Lower back
- Severity: Moderate → High (escalating)
- Timeline: 6 mentions over 8 days
- Related exercises: Deadlift, Back Squat

**Pattern Analysis**:

**Oct 14** (Workout log):
"Lower back tight during deadlift warmups" [Moderate]

**Oct 16** (Daily note):
"Lower back sore, hard to bend over" [Moderate]

**Oct 17** (Workout log):
"Sharp pain in lower back on set 3 of squats, stopped early" [HIGH]

**Oct 18** (Daily note):
"Lower back pain worse, can't sit comfortably" [HIGH]

**Oct 20** (Daily note):
"Lower back still painful, spreading to right hip" [HIGH + SPREADING]

**Oct 21** (Today - Daily note):
"Woke up with severe lower back pain, took ibuprofen" [SEVERE]

---

**⚠️ IMMEDIATE ACTION REQUIRED**:

1. **Stop all lower back-loaded exercises**:
   - ❌ Deadlifts (all variations)
   - ❌ Back Squats
   - ❌ Good Mornings
   - ❌ Bent-over Rows

2. **Safe alternatives**:
   - ✅ Leg Press (instead of squats)
   - ✅ Machine Rows (instead of barbell rows)
   - ✅ Single-leg exercises (lunges, split squats)

3. **Rehab protocol**:
   - McGill Big 3 daily (bird dog, side plank, curl-up)
   - Gentle cat-cow stretches
   - Hip flexor stretches
   - Avoid flexion under load

4. **Medical consultation recommended**:
   - Pain escalating over 8 days
   - "Sharp" and "severe" descriptors
   - Spreading to hip (nerve involvement?)
   - Affecting daily activities (sitting, bending)

5. **Return-to-training criteria**:
   - Pain-free for 7 consecutive days
   - Can perform bodyweight movements without discomfort
   - Cleared by physio/doctor (recommended)
   - Start with 50% previous loads

**Would you like me to generate a rehab-focused program?**
```

---

## Troubleshooting

### XP Calculation Not Updating

**Symptom**: Running `calculate_xp.py` doesn't update workout file frontmatter

**Cause**: Script reads from file but doesn't write back (by design - requires manual copy)

**Fix**:
1. Run script: `python scripts/calculate_xp.py workouts/🏋️2025-10-21.md`
2. Copy XP values from terminal output
3. Manually paste into workout file frontmatter: `total_xp: 4250`

**Future Enhancement**: Add `--write-back` flag to script for auto-update

### Session Planning Shows Wrong Workout Type

**Symptom**: OBSIDIA recommends Upper Push when you expected Lower Pull

**Cause 1**: Program schedule doesn't match actual training days

**Fix**:
```yaml
# In current-program.yaml, update preferred_days
schedule:
  preferred_days:
    upper_push: [1, 5]    # Your actual Mon/Fri
    lower_push: [2, 6]    # Your actual Tue/Sat
    upper_pull: [4]       # Your actual Thu
    lower_pull: [7]       # Your actual Sun (not in schedule)
```

**Cause 2**: Recent workout history not detected

**Fix**:
- Ensure workout files follow naming convention: `YYYY-MM-DD-workout.md`
- Verify files are in `01-areas/health-fitness/training/workouts/`
- Check frontmatter has `session_type: "upper_push"` etc.

### Daily Note Context Not Loading

**Symptom**: Session planner defaults to average values (7/10 energy, 7/10 sleep)

**Cause**: Daily note frontmatter missing or incorrectly formatted

**Fix**:
```yaml
# Add to daily note frontmatter
---
energy_morning: 8
sleep_quality: 7
stress_level: 5
soreness: "none"  # or "mild", "moderate", "severe"
---
```

**Note**: Field names must match exactly (case-sensitive, underscores required)

### Injury Detection Missed Pain Mention

**Symptom**: You mentioned shoulder pain but no alert triggered

**Cause 1**: Keyword not in detection library

**Fix**:
```yaml
# Add to injury-keywords.yaml
pain_keywords:
  severity_moderate:
    keywords: [... , "your-specific-phrase"]
```

**Cause 2**: Mention was in a section not scanned

**Current Scan Locations**:
- Workout log: Exercise notes, set notes, post-workout summary
- Daily note: Body section, health sections

**Not Currently Scanned**:
- Thoughts/notes sections (too much noise)
- Non-health related areas

**Fix**: Add pain mentions to explicit health sections

### Skill Not Auto-Activating

**Symptom**: Mention "workout" but OBSIDIA doesn't load

**Cause**: Trigger keyword not in auto-activation list

**Current Triggers** (from SKILL.md):
```yaml
auto_activate:
  keywords: ["gym", "workout", "training", "exercise", "lift"]
  phrases: ["plan my workout", "log my workout", "analyze progress"]
```

**Fix**: Either:
1. Use exact trigger words: "Help me plan my **workout**"
2. Manually invoke: "Load the OBSIDIA training skill"
3. Add custom triggers to SKILL.md frontmatter

### Python Scripts Fail to Run

**Symptom**: `FileNotFoundError` or import errors

**Cause 1**: Running from wrong directory

**Fix**: Always run from vault root:
```bash
# Wrong
cd .claude/skills/obsidia-training/scripts
python plan_session.py  # ❌

# Correct
cd /Users/harrysayers/Developer/claudelife
python .claude/skills/obsidia-training/scripts/plan_session.py  # ✅
```

**Cause 2**: Missing dependencies

**Fix**:
```bash
# Install required packages
pip install pyyaml  # For YAML parsing
```

**Cause 3**: Hardcoded vault path doesn't match your system

**Fix**: Pass vault path as argument:
```bash
python scripts/plan_session.py /path/to/your/vault
```

---

## Related Systems

### Daily Notes Integration

**File**: `00 - Daily/*.md`

**Frontmatter Fields Used**:
```yaml
energy_morning: 8        # Read by plan_session.py
sleep_quality: 7         # Read by plan_session.py
stress_level: 5          # Used for adaptation rules
```

**Body Sections Scanned**:
- `## 🏃 Body` - Injury detection scans here
- `## 🧠 Health` - Pain mentions tracked

**Bi-directional Flow**:
- OBSIDIA reads daily notes for context
- Workout logs can reference daily note for pre-workout state
- Injury alerts suggest updates to daily health tracking

### Templater Integration

**Template**: `98-templates/workout.md`

**Variables Used**:
```
{{date:YYYY-MM-DD}}     # Auto-fills workout date
```

**Workflow**:
1. Hit Templater hotkey in daily note or training folder
2. Select "workout" template
3. File created with today's date
4. Frontmatter pre-filled with date, empty fields for user

**Future**: Could auto-fill `session_type` from OBSIDIA session plan

### Serena MCP Memory

**Memory File**: `.serena/memories/project_structure.md`

**What Serena Knows**:
- OBSIDIA system exists at `.claude/skills/obsidia-training/`
- Auto-activation triggers
- Purpose: training intelligence and auto-regulation
- Integration with daily notes

**Why This Matters**:
- Future sessions can ask Serena "where is the training system?"
- Serena can suggest using OBSIDIA when user asks training questions
- Memory persists across Claude Code restarts

### Future Integrations (Planned)

**Task Master AI**:
- Create tasks for each workout in program
- Track completion and check off as done
- Alert if missing sessions

**Graphiti Knowledge Graph** (Phase 3):
- Long-term pattern analysis across months
- "Show me how my bench press progressed in 2025"
- Correlate injury patterns with exercise selection over time

**n8n Automation**:
- Auto-generate weekly summary emails
- Sync workout logs to Google Sheets for visualization
- Send reminder notifications for rest day vs training day

---

## Version History

**v1.0** (2025-10-21):
- Initial system implementation
- Core features: Session planning, XP tracking, injury detection
- 8-week hypertrophy program template
- Complete exercise library (289 lines)
- Python scripts for automation
- Integration with daily notes via frontmatter

---

## Future Enhancements

**Phase 2** (Short-term):
- Auto-fill session type in workout template from session plan
- `--write-back` flag for XP calculator to auto-update files
- Weekly email summaries via n8n
- Mobile-friendly workout logging (Obsidian mobile optimizations)

**Phase 3** (Medium-term):
- Graphiti integration for long-term pattern analysis
- Deload week auto-detection and recommendation
- Exercise substitution AI (suggest alternatives based on equipment/injuries)
- Volume/intensity analytics with charts

**Phase 4** (Long-term):
- AI-generated program design based on goals and history
- Video form analysis integration
- Social features (share PRs, compete with friends)
- Wearable integration (HRV, sleep tracking from Whoop/Oura)

---

*Auto-generated by `/report:document-system` on 2025-10-21*
*Skill version: 1.0*
*Documentation maintained by: Serena MCP + Claude Skills*
