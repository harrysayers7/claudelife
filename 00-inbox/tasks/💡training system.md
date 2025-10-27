---
Done: false
today: false
follow up: false
this week: false
back burner: false
ASAP: false
type: Task
status:
relation:
description:
effort:
ai-assigned: false
ai-ignore: false
ai-ask: false
priority:
agent:
slash-command:
sub-type:
  - idea
---
# OBSIDIA Training System: Complete Implementation Plan

## Project Overview

**Timeline:** 3-week phased rollout (with optional Week 4 for advanced features)
**Architecture:** Obsidian vault + Python automation scripts + Raycast integration
**Core Philosophy:** Start minimal, validate each phase, add complexity only after proven value

---

## System Architecture

```
obsidian-vault/
├── 00-templates/
│   ├── daily-note.md (modified with training section)
│   ├── workout-log.md (detailed session template)
│   └── weekly-summary.md (auto-generated)
├── 02-training/
│   ├── programs/
│   │   ├── current-program.yaml (editable program structure)
│   │   └── program-archive/ (past programs)
│   ├── workouts/
│   │   └── YYYY-MM-DD-session-name.md (individual logs)
│   ├── progress/
│   │   ├── weekly-summaries/
│   │   └── monthly-reports/
│   └── config/
│       ├── exercises-library.yaml (all exercises + metadata)
│       ├── xp-config.yaml (XP calculation rules)
│       └── injury-keywords.yaml (watch patterns)
├── scripts/
│   ├── obsidia/
│   │   ├── __init__.py
│   │   ├── planner.py (session planning logic)
│   │   ├── analyzer.py (progress analysis)
│   │   ├── xp_calculator.py (XP/achievements)
│   │   ├── injury_watch.py (pattern detection)
│   │   ├── voice_parser.py (audio transcription)
│   │   └── utils.py (helper functions)
│   ├── plan_next_session.py (main planning script)
│   ├── analyze_progress.py (weekly analysis)
│   ├── parse_workout_voice.py (voice note handler)
│   └── update_dashboard.py (generate Dataview data)
└── .obsidia/
    ├── cache/ (performance data)
    ├── logs/ (script execution logs)
    └── state.json (current level, XP, streaks)
```

---

## Phase 1: Foundation (Week 1)

**Goal:** Core data structure + manual workflow that feels natural

### 1.1 Obsidian Setup

**Daily Note Template Enhancement**

```markdown
---
date: {{date}}
day: {{date:dddd}}
energy_morning:
sleep_quality:
---

# {{date:YYYY-MM-DD}} {{date:dddd}}

## Morning
- [ ] Meditation
- [ ] 10km walk
- [ ] Cold swim
- [ ] Gym

## Training
<!-- OBSIDIA_PLAN_START -->
**Session:** [Planned/Rest/Adapted]
**Focus:** [Upper Push/Lower Pull/etc]
**Status:** [ ] Not started | [ ] In progress | [ ] Complete

### Workout Log
*Fill in during session:*

**Energy Check-in:**
- Pre-workout: /10
- Post-workout: /10

**Exercises:**
<!-- Exercise logs will go here -->

### Post-Workout Notes
*Record voice note or write quick reflection*
- How did the session feel overall?
- Any exercises that felt off?
- Form concerns or wins?
- Energy trajectory?

<!-- OBSIDIA_PLAN_END -->

## Evening
- [[Daily Reflection]]

---
**Daily Identity:** Today I proved I'm someone who...
```

**Workout Log Template** (`00-templates/workout-log.md`)

```markdown
---
date: {{date}}
session_type: [upper-push/upper-pull/lower-push/lower-pull]
status: [planned/completed/skipped]
program_week:
xp_earned:
---

# {{date:YYYY-MM-DD}} - {{session_type}}

## Pre-Workout
- Energy: /10
- Sleep (last night): /10
- Readiness: [yes/no]
- Notes:

## Exercises

### Exercise 1: [Exercise Name]
**Target:** 4 sets x 8-10 reps @ RPE 8
**Actual:**
- Set 1: kg x reps @ RPE
- Set 2: kg x reps @ RPE
- Set 3: kg x reps @ RPE
- Set 4: kg x reps @ RPE

**Form Quality:** /10
**Pump Rating:** /10
**Notes:**

### Exercise 2: [Exercise Name]
[Repeat structure]

## Post-Workout
- Energy now: /10
- Overall session rating: /10
- Voice note: [[audio-YYYY-MM-DD]]
- Quick reflection:

## XP Calculation
<!-- Auto-calculated by script -->
- Base XP:
- Multipliers:
- **Total XP: **
- **Cumulative XP: **
- **Current Level: **
```

### 1.2 Program Configuration

**`current-program.yaml`**

```yaml
---
program_info:
  name: "Hypertrophy Block - Upper/Lower"
  phase: "Muscle Building"
  start_date: "2025-10-21"
  duration_weeks: 8
  current_week: 1

schedule:
  weekly_frequency: 4
  rest_days: [3, 7]  # Wednesday is active, Sunday is full rest
  preferred_days:
    upper_push: [1, 5]  # Monday, Friday
    lower_push: [2, 6]  # Tuesday, Saturday
    upper_pull: [4]     # Thursday
    lower_pull: [3]     # Wednesday (if training) or reschedule

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

      - name: "Incline Dumbbell Press"
        sets: 3
        reps: "10-12"
        rpe_target: 8
        rest_seconds: 120

      - name: "Cable Flyes"
        sets: 3
        reps: "12-15"
        rpe_target: 9
        rest_seconds: 90

      - name: "Overhead Press"
        sets: 3
        reps: "8-10"
        rpe_target: 8
        rest_seconds: 120

      - name: "Lateral Raises"
        sets: 3
        reps: "12-15"
        rpe_target: 9
        rest_seconds: 60

      - name: "Tricep Pushdowns"
        sets: 3
        reps: "12-15"
        rpe_target: 9
        rest_seconds: 60

  upper_pull:
    focus: "Back, Biceps, Rear Delts"
    exercises:
      - name: "Weighted Pullups"
        sets: 4
        reps: "6-8"
        rpe_target: 8
        primary: true
        rest_seconds: 180

      - name: "Barbell Row"
        sets: 3
        reps: "8-10"
        rpe_target: 8
        rest_seconds: 120

      - name: "Lat Pulldown"
        sets: 3
        reps: "10-12"
        rpe_target: 8
        rest_seconds: 90

      - name: "Face Pulls"
        sets: 3
        reps: "15-20"
        rpe_target: 9
        rest_seconds: 60

      - name: "Barbell Curls"
        sets: 3
        reps: "10-12"
        rpe_target: 8
        rest_seconds: 90

  lower_push:
    focus: "Quads, Glutes, Calves"
    exercises:
      - name: "Back Squat"
        sets: 4
        reps: "6-8"
        rpe_target: 8
        primary: true
        rest_seconds: 240

      - name: "Romanian Deadlift"
        sets: 3
        reps: "8-10"
        rpe_target: 8
        rest_seconds: 180

      - name: "Leg Press"
        sets: 3
        reps: "10-12"
        rpe_target: 9
        rest_seconds: 120

      - name: "Walking Lunges"
        sets: 3
        reps: "12 per leg"
        rpe_target: 8
        rest_seconds: 90

      - name: "Leg Curl"
        sets: 3
        reps: "12-15"
        rpe_target: 9
        rest_seconds: 60

      - name: "Calf Raises"
        sets: 4
        reps: "15-20"
        rpe_target: 9
        rest_seconds: 60

  lower_pull:
    focus: "Hamstrings, Glutes, Lower Back"
    exercises:
      - name: "Deadlift"
        sets: 3
        reps: "5-6"
        rpe_target: 8
        primary: true
        rest_seconds: 240

      - name: "Bulgarian Split Squat"
        sets: 3
        reps: "10 per leg"
        rpe_target: 8
        rest_seconds: 120

      - name: "Leg Curl"
        sets: 3
        reps: "10-12"
        rpe_target: 9
        rest_seconds: 90

      - name: "Hip Thrust"
        sets: 3
        reps: "12-15"
        rpe_target: 9
        rest_seconds: 90

      - name: "Back Extension"
        sets: 3
        reps: "15-20"
        rpe_target: 8
        rest_seconds: 60

progression_rules:
  weight_increase_kg: 2.5
  trigger: "hit_top_of_rep_range_2_weeks"
  deload_week: 8
  deload_multiplier: 0.7
```

**`exercises-library.yaml`**

```yaml
exercises:
  - name: "Barbell Bench Press"
    category: "Upper Push"
    primary_muscles: ["Chest", "Triceps", "Shoulders"]
    equipment: ["Barbell", "Bench"]
    difficulty: "Intermediate"
    injury_risks: ["Shoulder", "Wrist"]
    alternatives: ["Dumbbell Bench Press", "Machine Press"]

  - name: "Back Squat"
    category: "Lower Push"
    primary_muscles: ["Quads", "Glutes"]
    equipment: ["Barbell", "Rack"]
    difficulty: "Advanced"
    injury_risks: ["Lower Back", "Knee"]
    alternatives: ["Front Squat", "Leg Press", "Goblet Squat"]

  # [Continue for all exercises in program + alternatives]
```

**`xp-config.yaml`**

```yaml
xp_calculation:
  base_formula: "weight_kg * reps_completed"

  multipliers:
    rpe_9_plus: 1.2
    rpe_8_to_9: 1.0
    rpe_below_8: 0.9

    form_excellent: 1.1  # 9-10/10
    form_good: 1.0       # 7-8/10
    form_poor: 0.8       # <7/10

    primary_exercise: 1.3
    accessory_exercise: 1.0

    first_time_exercise: 1.5
    pr_achieved: 2.0

  level_system:
    xp_per_level: 10000
    level_titles:
      1-3: "Beginner"
      4-7: "Intermediate"
      8-12: "Advanced"
      13+: "Elite"

achievements:
  consistency:
    - name: "Week Warrior"
      condition: "4_sessions_in_7_days"
      xp_bonus: 500

    - name: "Monthly Streak"
      condition: "16_sessions_in_30_days"
      xp_bonus: 2000

  performance:
    - name: "Century Club"
      condition: "any_exercise_100kg"
      xp_bonus: 1000

    - name: "Volume King"
      condition: "50000_kg_total_volume_week"
      xp_bonus: 1500
```

**`injury-keywords.yaml`**

```yaml
injury_watch:
  pain_keywords:
    high_alert: ["sharp pain", "shooting pain", "severe", "can't move"]
    moderate: ["pain", "hurts", "sore", "tight", "stiff"]
    low: ["uncomfortable", "odd feeling", "slightly sore"]

  body_regions:
    - name: "Lower Back"
      exercises_to_monitor: ["Back Squat", "Deadlift", "RDL"]
      threshold: "2 mentions in 7 days"
      action: "suggest_deload"

    - name: "Shoulder"
      exercises_to_monitor: ["Bench Press", "Overhead Press", "Pullups"]
      threshold: "2 mentions in 7 days"
      action: "suggest_exercise_swap"

    - name: "Knee"
      exercises_to_monitor: ["Back Squat", "Leg Press", "Lunges"]
      threshold: "3 mentions in 14 days"
      action: "flag_for_physio"

  pattern_detection:
    check_frequency: "daily"
    lookback_period_days: 30
    correlation_threshold: 0.7
```

### 1.3 Manual Workflow Testing

**Week 1 Tasks:**
1. Create program file with your actual exercises
2. Use daily note template for 7 days
3. Manually log 3-4 workouts using workout-log template
4. Test voice note recording (just record, don't parse yet)
5. Weekend: Manually review your logs, validate data structure works

**Success Criteria:**
- [ ] Can fill in workout logs in <2 minutes per exercise
- [ ] Daily note training section feels natural
- [ ] Have 3-4 completed workout logs with all fields filled
- [ ] Program structure reflects your actual training plan

---

## Phase 2: Automation Core (Week 2)

**Goal:** Scripts that plan sessions + calculate XP automatically

### 2.1 Core Scripts Development

**`scripts/obsidia/planner.py`**

```python
"""
Session planning logic
"""
import yaml
from datetime import datetime, timedelta
from pathlib import Path

class SessionPlanner:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.program = self._load_program()
        self.state = self._load_state()

    def _load_program(self):
        """Load current program from YAML"""
        program_path = self.vault_path / "02-training/programs/current-program.yaml"
        with open(program_path) as f:
            return yaml.safe_load(f)

    def _load_state(self):
        """Load current training state"""
        state_path = self.vault_path / ".obsidia/state.json"
        if state_path.exists():
            with open(state_path) as f:
                return json.load(f)
        return {"xp": 0, "level": 1, "streak": 0}

    def _get_recent_daily_notes(self, days=3):
        """Parse recent daily notes for context"""
        notes = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            note_path = self.vault_path / f"{date.strftime('%Y-%m-%d')}.md"
            if note_path.exists():
                notes.append(self._parse_daily_note(note_path))
        return notes

    def _parse_daily_note(self, path):
        """Extract energy, sleep, stress indicators"""
        with open(path) as f:
            content = f.read()

        # Extract YAML frontmatter
        import re
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        else:
            frontmatter = {}

        # Look for stress indicators
        stress_keywords = ['late call', 'busy', 'stressed', 'chaotic', 'deadline']
        stress_score = sum(1 for kw in stress_keywords if kw in content.lower())

        return {
            'energy': frontmatter.get('energy_morning'),
            'sleep': frontmatter.get('sleep_quality'),
            'stress_indicators': stress_score,
            'content': content
        }

    def _get_last_workouts(self):
        """Get last 5 workout logs"""
        workout_dir = self.vault_path / "02-training/workouts"
        workouts = sorted(workout_dir.glob("*.md"), reverse=True)[:5]
        return [self._parse_workout(w) for w in workouts]

    def _parse_workout(self, path):
        """Extract workout data from markdown file"""
        with open(path) as f:
            content = f.read()

        # Parse frontmatter
        import re
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            data = yaml.safe_load(frontmatter_match.group(1))
        else:
            data = {}

        return data

    def plan_next_session(self, date=None):
        """
        Generate session plan with 3 options:
        1. Standard (from program)
        2. Adapted (context-adjusted)
        3. Recovery (if needed)
        """
        if date is None:
            date = datetime.now()

        # Get context
        recent_notes = self._get_recent_daily_notes()
        last_workouts = self._get_last_workouts()

        # Determine which workout type is due
        program_week = self.program['program_info']['current_week']
        day_of_week = date.weekday() + 1  # 1=Monday

        # Match day to workout type
        session_type = self._determine_session_type(day_of_week, last_workouts)

        if session_type is None:
            return self._format_rest_day()

        # Get workout template
        workout_template = self.program['workouts'][session_type]

        # Generate options
        standard = self._generate_standard_session(workout_template, session_type)
        adapted = self._generate_adapted_session(
            workout_template,
            session_type,
            recent_notes,
            last_workouts
        )
        recovery = self._generate_recovery_option(recent_notes, last_workouts)

        return {
            'date': date.strftime('%Y-%m-%d'),
            'session_type': session_type,
            'options': {
                'standard': standard,
                'adapted': adapted,
                'recovery': recovery
            },
            'recommendation': self._recommend_option(recent_notes, last_workouts)
        }

    def _determine_session_type(self, day_of_week, last_workouts):
        """Figure out which workout type is due based on schedule and recovery"""
        # Get last trained muscle groups
        last_upper = self._days_since_last(last_workouts, 'upper')
        last_lower = self._days_since_last(last_workouts, 'lower')

        # Minimum rest days between same muscle group
        min_rest = 48  # hours

        schedule = self.program['schedule']

        # Check preferred days
        for session_type, preferred_days in schedule.get('preferred_days', {}).items():
            if day_of_week in preferred_days:
                # Check if adequate rest
                if 'upper' in session_type and last_upper >= 2:
                    return session_type
                elif 'lower' in session_type and last_lower >= 2:
                    return session_type

        # If no preferred day match, return next due workout
        if last_upper >= last_lower:
            return 'upper_push' if last_upper >= 3 else None
        else:
            return 'lower_push' if last_lower >= 3 else None

    def _days_since_last(self, workouts, muscle_group):
        """Calculate days since last training of muscle group"""
        for i, workout in enumerate(workouts):
            if muscle_group in workout.get('session_type', ''):
                return i
        return 999  # Not trained recently

    def _generate_standard_session(self, template, session_type):
        """Generate standard session from program template"""
        exercises = []
        total_time = 0

        for exercise in template['exercises']:
            sets = exercise['sets']
            reps = exercise['reps']
            rest = exercise.get('rest_seconds', 90)

            # Estimate time: sets * (work time + rest time)
            # Assume ~30 sec per set on average
            exercise_time = sets * (30 + rest) / 60
            total_time += exercise_time

            exercises.append({
                'name': exercise['name'],
                'sets': sets,
                'reps': reps,
                'rpe_target': exercise['rpe_target'],
                'primary': exercise.get('primary', False)
            })

        return {
            'type': 'standard',
            'session_name': template['focus'],
            'exercises': exercises,
            'estimated_time': int(total_time),
            'xp_target': self._estimate_xp(exercises)
        }

    def _generate_adapted_session(self, template, session_type, recent_notes, last_workouts):
        """Generate adapted session based on context"""
        # Calculate adaptation factors
        avg_energy = self._avg_metric(recent_notes, 'energy')
        avg_sleep = self._avg_metric(recent_notes, 'sleep')
        stress_level = sum(n.get('stress_indicators', 0) for n in recent_notes)

        # Determine volume reduction
        reduction_factor = 1.0

        if avg_energy and avg_energy < 6:
            reduction_factor *= 0.75
        if avg_sleep and avg_sleep < 6:
            reduction_factor *= 0.85
        if stress_level > 3:
            reduction_factor *= 0.85

        # Modify template
        exercises = []
        for exercise in template['exercises'][:int(len(template['exercises']) * reduction_factor)]:
            adapted_sets = max(2, int(exercise['sets'] * reduction_factor))

            exercises.append({
                'name': exercise['name'],
                'sets': adapted_sets,
                'reps': exercise['reps'],
                'rpe_target': max(7, exercise['rpe_target'] - 1),  # Reduce intensity slightly
                'primary': exercise.get('primary', False)
            })

        return {
            'type': 'adapted',
            'session_name': template['focus'] + " (Reduced)",
            'exercises': exercises,
            'estimated_time': int(len(exercises) * 8),  # ~8 min per exercise
            'xp_target': self._estimate_xp(exercises),
            'adaptation_reason': self._explain_adaptation(avg_energy, avg_sleep, stress_level)
        }

    def _generate_recovery_option(self, recent_notes, last_workouts):
        """Generate active recovery session"""
        # Check if recovery is actually needed
        recent_volume = self._calculate_recent_volume(last_workouts)
        avg_energy = self._avg_metric(recent_notes, 'energy')

        return {
            'type': 'recovery',
            'session_name': 'Active Recovery',
            'activities': [
                '20min zone 2 cardio (incline walk or bike)',
                '10min mobility work (focus on tight areas)',
                '10min light stretching'
            ],
            'estimated_time': 40,
            'xp_target': 200,  # Recovery bonus
            'reason': self._explain_recovery_need(recent_volume, avg_energy)
        }

    def _recommend_option(self, recent_notes, last_workouts):
        """Recommend which option to take"""
        avg_energy = self._avg_metric(recent_notes, 'energy')
        recent_volume = self._calculate_recent_volume(last_workouts)

        if avg_energy and avg_energy < 5:
            return 'recovery'
        elif avg_energy and avg_energy < 7:
            return 'adapted'
        else:
            return 'standard'

    def _avg_metric(self, notes, metric):
        """Calculate average of a metric from recent notes"""
        values = [n[metric] for n in notes if n.get(metric)]
        return sum(values) / len(values) if values else None

    def _calculate_recent_volume(self, workouts):
        """Calculate total volume from recent workouts"""
        # Simplified - would need full workout parsing
        return len(workouts) * 1000  # Placeholder

    def _estimate_xp(self, exercises):
        """Estimate XP for a session"""
        # Rough estimate based on exercises
        return len(exercises) * 250

    def _explain_adaptation(self, energy, sleep, stress):
        """Generate human-readable adaptation explanation"""
        reasons = []
        if energy and energy < 6:
            reasons.append(f"low energy ({energy}/10)")
        if sleep and sleep < 6:
            reasons.append(f"poor sleep ({sleep}/10)")
        if stress > 3:
            reasons.append("high stress indicators")

        return " + ".join(reasons) if reasons else "optimal recovery strategy"

    def _explain_recovery_need(self, volume, energy):
        """Explain why recovery is suggested"""
        if energy and energy < 5:
            return f"Energy very low ({energy}/10) - body needs recovery"
        return "Proactive recovery to prevent overreaching"

    def _format_rest_day(self):
        """Format rest day message"""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'session_type': 'rest',
            'message': '🔄 Rest day - recovery is training'
        }
```

**`scripts/plan_next_session.py`** (Main entry point)

```python
#!/usr/bin/env python3
"""
Generate tomorrow's training session plan
Run via cron or Raycast
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import yaml

# Add obsidia module to path
sys.path.insert(0, str(Path(__file__).parent))
from obsidia.planner import SessionPlanner

VAULT_PATH = Path.home() / "Documents/Obsidian/HarrysVault"  # Adjust to your path

def generate_session_markdown(plan):
    """Convert plan to markdown for daily note"""

    if plan.get('session_type') == 'rest':
        return f"## Training\n\n{plan['message']}\n"

    options = plan['options']
    recommendation = plan['recommendation']

    md = f"""## Training: {plan['date']}

🤖 **OBSIDIA Analysis**
- Recommendation: **{recommendation.upper()}**

"""

    # Standard option
    std = options['standard']
    md += f"""### 1. ✅ Standard: {std['session_name']}
*Est. time: {std['estimated_time']}min | XP target: {std['xp_target']}*

"""
    for ex in std['exercises']:
        primary = "🔥 " if ex.get('primary') else ""
        md += f"- {primary}{ex['name']}: {ex['sets']}x{ex['reps']} @ RPE {ex['rpe_target']}\n"

    md += "\n"

    # Adapted option
    adapted = options['adapted']
    md += f"""### 2. ⚡ Adapted: {adapted['session_name']}
*Est. time: {adapted['estimated_time']}min | XP target: {adapted['xp_target']}*
*Reason: {adapted.get('adaptation_reason', 'Context-based adjustment')}*

"""
    for ex in adapted['exercises']:
        md += f"- {ex['name']}: {ex['sets']}x{ex['reps']} @ RPE {ex['rpe_target']}\n"

    md += "\n"

    # Recovery option
    recovery = options['recovery']
    md += f"""### 3. 🔄 Recovery: {recovery['session_name']}
*Est. time: {recovery['estimated_time']}min | XP: {recovery['xp_target']}*
*{recovery['reason']}*

"""
    for activity in recovery['activities']:
        md += f"- {activity}\n"

    md += "\n**Your choice:** [ ] Standard | [ ] Adapted | [ ] Recovery\n"

    return md

def inject_into_daily_note(date, session_markdown):
    """Insert session plan into daily note"""
    note_path = VAULT_PATH / f"{date.strftime('%Y-%m-%d')}.md"

    if not note_path.exists():
        print(f"Creating daily note for {date.strftime('%Y-%m-%d')}")
        # Create from template
        template_path = VAULT_PATH / "00-templates/daily-note.md"
        with open(template_path) as f:
            template = f.read()

        # Replace template variables
        content = template.replace("{{date}}", date.strftime("%Y-%m-%d"))
        content = content.replace("{{date:dddd}}", date.strftime("%A"))
        content = content.replace("{{date:YYYY-MM-DD}}", date.strftime("%Y-%m-%d"))
    else:
        with open(note_path) as f:
            content = f.read()

    # Find OBSIDIA section and replace/inject
    import re
    pattern = r'<!-- OBSIDIA_PLAN_START -->.*?<!-- OBSIDIA_PLAN_END -->'

    if re.search(pattern, content, re.DOTALL):
        # Replace existing
        new_section = f"<!-- OBSIDIA_PLAN_START -->\n{session_markdown}\n<!-- OBSIDIA_PLAN_END -->"
        content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    else:
        # Append to training section
        training_marker = "## Training"
        if training_marker in content:
            content = content.replace(
                training_marker,
                f"{training_marker}\n<!-- OBSIDIA_PLAN_START -->\n{session_markdown}\n<!-- OBSIDIA_PLAN_END -->"
            )

    # Write back
    with open(note_path, 'w') as f:
        f.write(content)

    print(f"✅ Session plan injected into {note_path.name}")

def main():
    # Default: plan for tomorrow
    target_date = datetime.now() + timedelta(days=1)

    # Override if date provided as argument
    if len(sys.argv) > 1:
        target_date = datetime.strptime(sys.argv[1], '%Y-%m-%d')

    print(f"Planning session for {target_date.strftime('%Y-%m-%d %A')}")

    # Initialize planner
    planner = SessionPlanner(VAULT_PATH)

    # Generate plan
    plan = planner.plan_next_session(target_date)

    # Convert to markdown
    session_md = generate_session_markdown(plan)

    # Inject into daily note
    inject_into_daily_note(target_date, session_md)

    print(f"\n🎯 Recommendation: {plan.get('recommendation', 'N/A').upper()}")

if __name__ == "__main__":
    main()
```

### 2.2 XP Calculator

**`scripts/obsidia/xp_calculator.py`**

```python
"""
XP calculation and achievement system
"""
import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
import re

class XPCalculator:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.config = self._load_xp_config()
        self.state = self._load_state()

    def _load_xp_config(self):
        config_path = self.vault_path / "02-training/config/xp-config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def _load_state(self):
        state_path = self.vault_path / ".obsidia/state.json"
        if state_path.exists():
            with open(state_path) as f:
                return json.load(f)
        return {
            "total_xp": 0,
            "level": 1,
            "current_level_xp": 0,
            "streak_days": 0,
            "last_workout": None,
            "achievements_unlocked": []
        }

    def _save_state(self):
        state_path = self.vault_path / ".obsidia/state.json"
        state_path.parent.mkdir(exist_ok=True)
        with open(state_path, 'w') as f:
            json.dump(self.state, f, indent=2)

    def calculate_workout_xp(self, workout_path):
        """
        Parse workout markdown file and calculate XP
        """
        with open(workout_path) as f:
            content = f.read()

        # Parse exercises from markdown
        exercises = self._parse_exercises(content)

        total_xp = 0
        breakdown = []

        for exercise in exercises:
            exercise_xp = self._calculate_exercise_xp(exercise)
            total_xp += exercise_xp
            breakdown.append({
                'exercise': exercise['name'],
                'xp': exercise_xp
            })

        # Check for achievements
        new_achievements = self._check_achievements(workout_path, exercises)

        for achievement in new_achievements:
            total_xp += achievement['xp_bonus']
            breakdown.append({
                'exercise': f"🏆 {achievement['name']}",
                'xp': achievement['xp_bonus']
            })

        return {
            'total_xp': int(total_xp),
            'breakdown': breakdown,
            'achievements': new_achievements
        }

    def _parse_exercises(self, markdown_content):
        """
        Extract exercise data from markdown workout log
        """
        exercises = []

        # Find all exercise blocks
        exercise_pattern = r'### Exercise \d+: (.+?)\n\*\*Target:\*\*.*?\n\*\*Actual:\*\*\n(.*?)\n\n\*\*Form Quality:\*\* (\d+)/10'

        for match in re.finditer(exercise_pattern, markdown_content, re.DOTALL):
            exercise_name = match.group(1).strip()
            sets_text = match.group(2)
            form_quality = int(match.group(3))

            # Parse sets
            sets = []
            set_pattern = r'- Set \d+: ([\d.]+)kg x (\d+) @ RPE (\d+)'
            for set_match in re.finditer(set_pattern, sets_text):
                sets.append({
                    'weight': float(set_match.group(1)),
                    'reps': int(set_match.group(2)),
                    'rpe': int(set_match.group(3))
                })

            exercises.append({
                'name': exercise_name,
                'sets': sets,
                'form_quality': form_quality
            })

        return exercises

    def _calculate_exercise_xp(self, exercise):
        """Calculate XP for a single exercise"""
        config = self.config['xp_calculation']
        exercise_xp = 0

        for set_data in exercise['sets']:
            # Base XP
            base_xp = set_data['weight'] * set_data['reps']

            # RPE multiplier
            rpe = set_data['rpe']
            if rpe >= 9:
                base_xp *= config['multipliers']['rpe_9_plus']
            elif rpe >= 8:
                base_xp *= config['multipliers']['rpe_8_to_9']
            else:
                base_xp *= config['multipliers']['rpe_below_8']

            # Form multiplier
            form = exercise['form_quality']
            if form >= 9:
                base_xp *= config['multipliers']['form_excellent']
            elif form >= 7:
                base_xp *= config['multipliers']['form_good']
            else:
                base_xp *= config['multipliers']['form_poor']

            exercise_xp += base_xp

        return exercise_xp

    def _check_achievements(self, workout_path, exercises):
        """Check if new achievements were unlocked"""
        achievements = []
        achievement_config = self.config['achievements']

        # Check consistency achievements
        workout_date = self._extract_date_from_path(workout_path)
        recent_workouts = self._count_recent_workouts(workout_date)

        for achievement in achievement_config['consistency']:
            if achievement['name'] in self.state['achievements_unlocked']:
                continue

            if achievement['condition'] == "4_sessions_in_7_days" and recent_workouts['last_7_days'] >= 4:
                achievements.append(achievement)
                self.state['achievements_unlocked'].append(achievement['name'])

            elif achievement['condition'] == "16_sessions_in_30_days" and recent_workouts['last_30_days'] >= 16:
                achievements.append(achievement)
                self.state['achievements_unlocked'].append(achievement['name'])

        # Check performance achievements
        for achievement in achievement_config['performance']:
            if achievement['name'] in self.state['achievements_unlocked']:
                continue

            if achievement['condition'] == "any_exercise_100kg":
                if any(any(s['weight'] >= 100 for s in ex['sets']) for ex in exercises):
                    achievements.append(achievement)
                    self.state['achievements_unlocked'].append(achievement['name'])

        return achievements

    def _extract_date_from_path(self, path):
        """Extract date from workout file path"""
        filename = Path(path).stem
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if date_match:
            return datetime.strptime(date_match.group(1), '%Y-%m-%d')
        return datetime.now()

    def _count_recent_workouts(self, reference_date):
        """Count workouts in recent time windows"""
        workout_dir = self.vault_path / "02-training/workouts"

        last_7_days = 0
        last_30_days = 0

        for workout_file in workout_dir.glob("*.md"):
            workout_date = self._extract_date_from_path(workout_file)
            days_ago = (reference_date - workout_date).days

            if 0 <= days_ago <= 7:
                last_7_days += 1
            if 0 <= days_ago <= 30:
                last_30_days += 1

        return {
            'last_7_days': last_7_days,
            'last_30_days': last_30_days
        }

    def update_state(self, xp_earned):
        """Update global state with new XP"""
        self.state['total_xp'] += xp_earned
        self.state['current_level_xp'] += xp_earned

        # Check for level up
        xp_per_level = self.config['xp_calculation']['level_system']['xp_per_level']

        while self.state['current_level_xp'] >= xp_per_level:
            self.state['level'] += 1
            self.state['current_level_xp'] -= xp_per_level
            print(f"🎉 LEVEL UP! You are now Level {self.state['level']}")

        self._save_state()

        return self.state

    def get_progress_summary(self):
        """Get current progress statistics"""
        xp_per_level = self.config['xp_calculation']['level_system']['xp_per_level']
        xp_to_next = xp_per_level - self.state['current_level_xp']
        progress_pct = (self.state['current_level_xp'] / xp_per_level) * 100

        # Determine title
        level_titles = self.config['xp_calculation']['level_system']['level_titles']
        title = "Beginner"
        for range_str, title_name in level_titles.items():
            if '-' in range_str:
                low, high = map(int, range_str.split('-'))
                if low <= self.state['level'] <= high:
                    title = title_name
                    break
            elif '+' in range_str:
                low = int(range_str.replace('+', ''))
                if self.state['level'] >= low:
                    title = title_name

        return {
            'total_xp': self.state['total_xp'],
            'level': self.state['level'],
            'title': title,
            'current_level_xp': self.state['current_level_xp'],
            'xp_to_next_level': xp_to_next,
            'progress_percentage': progress_pct,
            'achievements': len(self.state['achievements_unlocked'])
        }
```

**`scripts/calculate_workout_xp.py`** (Entry point)

```python
#!/usr/bin/env python3
"""
Calculate XP for completed workout
Called after workout is logged
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from obsidia.xp_calculator import XPCalculator

VAULT_PATH = Path.home() / "Documents/Obsidian/HarrysVault"

def inject_xp_into_workout(workout_path, xp_data):
    """Add XP calculation to workout markdown"""
    with open(workout_path) as f:
        content = f.read()

    xp_section = f"""
## XP Calculation

**Total XP Earned:** {xp_data['total_xp']}

### Breakdown:
"""
    for item in xp_data['breakdown']:
        xp_section += f"- {item['exercise']}: {item['xp']} XP\n"

    if xp_data['achievements']:
        xp_section += "\n### 🏆 Achievements Unlocked:\n"
        for achievement in xp_data['achievements']:
            xp_section += f"- **{achievement['name']}** (+{achievement['xp_bonus']} XP)\n"

    # Append to file if not already there
    if "## XP Calculation" not in content:
        content += "\n" + xp_section

    with open(workout_path, 'w') as f:
        f.write(content)

def main():
    if len(sys.argv) < 2:
        print("Usage: calculate_workout_xp.py <workout-file-path>")
        sys.exit(1)

    workout_path = Path(sys.argv[1])

    if not workout_path.exists():
        print(f"Error: Workout file not found: {workout_path}")
        sys.exit(1)

    print(f"Calculating XP for {workout_path.name}")

    calculator = XPCalculator(VAULT_PATH)

    # Calculate XP
    xp_data = calculator.calculate_workout_xp(workout_path)

    # Update global state
    new_state = calculator.update_state(xp_data['total_xp'])

    # Inject back into workout file
    inject_xp_into_workout(workout_path, xp_data)

    # Print summary
    progress = calculator.get_progress_summary()
    print(f"\n✅ Workout logged!")
    print(f"XP Earned: {xp_data['total_xp']}")
    print(f"Total XP: {progress['total_xp']}")
    print(f"Level: {progress['level']} ({progress['title']})")
    print(f"Progress to next level: {progress['progress_percentage']:.1f}%")

    if xp_data['achievements']:
        print(f"\n🏆 New achievements:")
        for achievement in xp_data['achievements']:
            print(f"  - {achievement['name']}")

if __name__ == "__main__":
    main()
```

### 2.3 Cron Job Setup (macOS)

**Create `~/Library/LaunchAgents/com.obsidia.plan-session.plist`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.obsidia.plan-session</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/harry/Documents/Obsidian/scripts/plan_next_session.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>20</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/obsidia-plan.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/obsidia-plan-error.log</string>
</dict>
</plist>
```

**Load cron job:**
```bash
launchctl load ~/Library/LaunchAgents/com.obsidia.plan-session.plist
```

**Week 2 Tasks:**
1. Build and test planner.py locally
2. Build and test xp_calculator.py
3. Manually run `plan_next_session.py` for 3 days
4. Manually run `calculate_workout_xp.py` after 2 workouts
5. Set up cron job for evening planning
6. Validate XP calculations match expectations

**Success Criteria:**
- [ ] Session plans generate correctly with 3 options
- [ ] XP calculations match manual calculations
- [ ] Cron job runs successfully (check logs)
- [ ] State persists between script runs
- [ ] Achieved at least 1 "achievement"

---

## Phase 3: Intelligence Layer (Week 3)

**Goal:** Add adaptive intelligence + injury watch + analysis

### 3.1 Progress Analyzer

**`scripts/obsidia/analyzer.py`**

```python
"""
Workout progress analysis and insights
"""
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import re

class ProgressAnalyzer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)

    def analyze_weekly_progress(self, start_date=None):
        """
        Generate weekly summary with insights
        """
        if start_date is None:
            # Default: analyze last 7 days
            start_date = datetime.now() - timedelta(days=7)

        end_date = start_date + timedelta(days=7)

        # Collect all workouts in range
        workouts = self._collect_workouts(start_date, end_date)

        if not workouts:
            return {
                'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                'workouts_completed': 0,
                'message': "No workouts logged this week"
            }

        # Calculate metrics
        total_volume = self._calculate_total_volume(workouts)
        avg_rpe = self._calculate_avg_rpe(workouts)
        exercise_progress = self._track_exercise_progress(workouts)
        energy_trends = self._analyze_energy_trends(workouts)

        # Identify patterns
        insights = self._generate_insights(workouts, exercise_progress, energy_trends)

        # Recommendations
        recommendations = self._generate_recommendations(workouts, exercise_progress, insights)

        return {
            'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            'workouts_completed': len(workouts),
            'total_volume_kg': total_volume,
            'avg_rpe': avg_rpe,
            'exercise_progress': exercise_progress,
            'insights': insights,
            'recommendations': recommendations
        }

    def _collect_workouts(self, start_date, end_date):
        """Collect all workout files in date range"""
        workout_dir = self.vault_path / "02-training/workouts"
        workouts = []

        for workout_file in workout_dir.glob("*.md"):
            workout_date = self._extract_date_from_filename(workout_file.name)
            if start_date <= workout_date <= end_date:
                workouts.append({
                    'date': workout_date,
                    'path': workout_file,
                    'data': self._parse_workout_file(workout_file)
                })

        return sorted(workouts, key=lambda x: x['date'])

    def _extract_date_from_filename(self, filename):
        """Extract date from workout filename"""
        match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if match:
            return datetime.strptime(match.group(1), '%Y-%m-%d')
        return datetime.now()

    def _parse_workout_file(self, path):
        """Parse workout markdown into structured data"""
        with open(path) as f:
            content = f.read()

        # Extract frontmatter
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        frontmatter = yaml.safe_load(frontmatter_match.group(1)) if frontmatter_match else {}

        # Parse exercises
        exercises = []
        exercise_pattern = r'### Exercise \d+: (.+?)\n.*?\n\*\*Actual:\*\*\n(.*?)\n\n\*\*Form Quality:\*\* (\d+)/10'

        for match in re.finditer(exercise_pattern, content, re.DOTALL):
            exercise_name = match.group(1).strip()
            sets_text = match.group(2)
            form_quality = int(match.group(3))

            sets = []
            set_pattern = r'- Set \d+: ([\d.]+)kg x (\d+) @ RPE (\d+)'
            for set_match in re.finditer(set_pattern, sets_text):
                sets.append({
                    'weight': float(set_match.group(1)),
                    'reps': int(set_match.group(2)),
                    'rpe': int(set_match.group(3))
                })

            exercises.append({
                'name': exercise_name,
                'sets': sets,
                'form_quality': form_quality,
                'total_volume': sum(s['weight'] * s['reps'] for s in sets)
            })

        return {
            'frontmatter': frontmatter,
            'exercises': exercises,
            'pre_energy': self._extract_metric(content, 'Pre-workout:.*?Energy: (\d+)/10'),
            'post_energy': self._extract_metric(content, 'Energy now: (\d+)/10'),
        }

    def _extract_metric(self, content, pattern):
        """Extract numeric metric from content"""
        match = re.search(pattern, content)
        return int(match.group(1)) if match else None

    def _calculate_total_volume(self, workouts):
        """Calculate total volume across all workouts"""
        total = 0
        for workout in workouts:
            for exercise in workout['data']['exercises']:
                total += exercise['total_volume']
        return int(total)

    def _calculate_avg_rpe(self, workouts):
        """Calculate average RPE across all sets"""
        all_rpes = []
        for workout in workouts:
            for exercise in workout['data']['exercises']:
                for set_data in exercise['sets']:
                    all_rpes.append(set_data['rpe'])

        return round(sum(all_rpes) / len(all_rpes), 1) if all_rpes else 0

    def _track_exercise_progress(self, workouts):
        """Track progress for key exercises"""
        # Group by exercise name
        exercise_history = {}

        for workout in workouts:
            for exercise in workout['data']['exercises']:
                name = exercise['name']
                if name not in exercise_history:
                    exercise_history[name] = []

                # Track max weight and volume
                max_weight = max(s['weight'] for s in exercise['sets'])
                total_volume = exercise['total_volume']

                exercise_history[name].append({
                    'date': workout['date'],
                    'max_weight': max_weight,
                    'volume': total_volume
                })

        # Analyze trends
        progress = {}
        for exercise_name, history in exercise_history.items():
            if len(history) >= 2:
                first = history[0]
                last = history[-1]

                weight_change = last['max_weight'] - first['max_weight']
                volume_change = last['volume'] - first['volume']

                progress[exercise_name] = {
                    'sessions': len(history),
                    'weight_change_kg': round(weight_change, 1),
                    'volume_change_pct': round((volume_change / first['volume']) * 100, 1) if first['volume'] > 0 else 0,
                    'trend': 'improving' if weight_change > 0 or volume_change > 0 else 'plateau'
                }

        return progress

    def _analyze_energy_trends(self, workouts):
        """Analyze energy patterns"""
        energy_data = []

        for workout in workouts:
            pre = workout['data'].get('pre_energy')
            post = workout['data'].get('post_energy')

            if pre and post:
                energy_data.append({
                    'date': workout['date'],
                    'day_of_week': workout['date'].strftime('%A'),
                    'pre': pre,
                    'post': post,
                    'delta': post - pre
                })

        if not energy_data:
            return {}

        df = pd.DataFrame(energy_data)

        return {
            'avg_pre': round(df['pre'].mean(), 1),
            'avg_post': round(df['post'].mean(), 1),
            'avg_delta': round(df['delta'].mean(), 1),
            'best_day': df.groupby('day_of_week')['delta'].mean().idxmax() if len(df) > 0 else None
        }

    def _generate_insights(self, workouts, exercise_progress, energy_trends):
        """Generate human-readable insights"""
        insights = []

        # Volume trend
        if len(workouts) >= 2:
            total_volumes = [sum(e['total_volume'] for e in w['data']['exercises']) for w in workouts]
            if total_volumes[-1] > total_volumes[0] * 1.1:
                insights.append("📈 Volume increased 10%+ this week - strength gains incoming")
            elif total_volumes[-1] < total_volumes[0] * 0.9:
                insights.append("📉 Volume dropped 10%+ - check recovery or consider deload")

        # Exercise plateaus
        plateaus = [name for name, prog in exercise_progress.items() if prog['trend'] == 'plateau']
        if plateaus:
            insights.append(f"⚠️ Plateaus detected: {', '.join(plateaus[:2])}")

        # Energy insights
        if energy_trends.get('avg_pre', 0) < 6:
            insights.append("🔋 Low pre-workout energy averaging <6/10 - review sleep/nutrition")

        if energy_trends.get('avg_delta', 0) > 2:
            insights.append("✨ Training consistently boosts energy (+2 points avg) - great sign")

        return insights

    def _generate_recommendations(self, workouts, exercise_progress, insights):
        """Generate actionable recommendations"""
        recs = []

        # Progression opportunities
        improving = [name for name, prog in exercise_progress.items() if prog['trend'] == 'improving']
        if improving:
            recs.append(f"💪 Keep pushing: {improving[0]} is trending up")

        # Plateau solutions
        plateaus = [name for name, prog in exercise_progress.items() if prog['trend'] == 'plateau']
        if plateaus and len(plateaus) > 0:
            recs.append(f"🔄 {plateaus[0]}: Try adding 1 set or swapping to a variation next week")

        # Volume management
        if len(workouts) >= 4:
            recs.append("✅ 4+ sessions this week - consider scheduling a deload week 2-3 weeks out")

        return recs
```

**`scripts/analyze_progress.py`** (Entry point)

```python
#!/usr/bin/env python3
"""
Generate weekly progress report
Run on Sundays or on-demand
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))
from obsidia.analyzer import ProgressAnalyzer

VAULT_PATH = Path.home() / "Documents/Obsidian/HarrysVault"

def generate_summary_markdown(analysis):
    """Convert analysis to markdown report"""
    md = f"""# Training Summary: {analysis['period']}

## Overview
- **Workouts Completed:** {analysis['workouts_completed']}
- **Total Volume:** {analysis['total_volume_kg']:,} kg
- **Average RPE:** {analysis['avg_rpe']}

## Exercise Progress

"""

    for exercise, progress in analysis['exercise_progress'].items():
        trend_emoji = "📈" if progress['trend'] == 'improving' else "➡️"
        md += f"### {trend_emoji} {exercise}\n"
        md += f"- Sessions: {progress['sessions']}\n"
        md += f"- Weight change: {progress['weight_change_kg']:+.1f} kg\n"
        md += f"- Volume change: {progress['volume_change_pct']:+.1f}%\n\n"

    if analysis.get('insights'):
        md += "## 🧠 Insights\n\n"
        for insight in analysis['insights']:
            md += f"- {insight}\n"
        md += "\n"

    if analysis.get('recommendations'):
        md += "## 🎯 Recommendations\n\n"
        for rec in analysis['recommendations']:
            md += f"- {rec}\n"
        md += "\n"

    return md

def save_summary(analysis, output_dir):
    """Save summary to file"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    end_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"weekly-summary-{end_date}.md"
    output_path = output_dir / filename

    # Generate markdown
    md = generate_summary_markdown(analysis)

    # Write file
    with open(output_path, 'w') as f:
        f.write(md)

    print(f"✅ Weekly summary saved: {output_path}")
    return output_path

def main():
    print("Analyzing training progress...")

    analyzer = ProgressAnalyzer(VAULT_PATH)

    # Analyze last 7 days by default
    analysis = analyzer.analyze_weekly_progress()

    # Print to console
    print(f"\n{'='*50}")
    print(f"Training Summary: {analysis['period']}")
    print(f"{'='*50}")
    print(f"Workouts: {analysis['workouts_completed']}")
    print(f"Volume: {analysis['total_volume_kg']:,} kg")
    print(f"Avg RPE: {analysis['avg_rpe']}")

    if analysis.get('insights'):
        print(f"\n🧠 Insights:")
        for insight in analysis['insights']:
            print(f"  {insight}")

    if analysis.get('recommendations'):
        print(f"\n🎯 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"  {rec}")

    # Save to file
    summary_dir = VAULT_PATH / "02-training/progress/weekly-summaries"
    save_summary(analysis, summary_dir)

if __name__ == "__main__":
    main()
```

### 3.2 Injury Watch System

**`scripts/obsidia/injury_watch.py`**

```python
"""
Monitor workout logs and daily notes for injury risk patterns
"""
import yaml
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class InjuryWatch:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.config = self._load_config()

    def _load_config(self):
        config_path = self.vault_path / "02-training/config/injury-keywords.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def scan_for_risks(self, lookback_days=30):
        """Scan recent logs for injury risk patterns"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)

        # Collect mentions
        mentions = self._collect_pain_mentions(start_date, end_date)

        # Analyze patterns
        alerts = []

        for body_region_config in self.config['injury_watch']['body_regions']:
            region = body_region_config['name']
            region_mentions = mentions.get(region, [])

            if len(region_mentions) >= self._parse_threshold(body_region_config['threshold']):
                alert = {
                    'region': region,
                    'severity': self._assess_severity(region_mentions),
                    'mentions': len(region_mentions),
                    'affected_exercises': self._identify_affected_exercises(
                        region_mentions,
                        body_region_config['exercises_to_monitor']
                    ),
                    'action': body_region_config['action'],
                    'details': region_mentions
                }
                alerts.append(alert)

        return alerts

    def _collect_pain_mentions(self, start_date, end_date):
        """Scan workout logs and daily notes for pain keywords"""
        mentions = defaultdict(list)
        pain_keywords = self.config['injury_watch']['pain_keywords']

        # Scan workout logs
        workout_dir = self.vault_path / "02-training/workouts"
        for workout_file in workout_dir.glob("*.md"):
            workout_date = self._extract_date(workout_file.name)
            if start_date <= workout_date <= end_date:
                content = workout_file.read_text()

                # Check for pain keywords
                for severity, keywords in pain_keywords.items():
                    for keyword in keywords:
                        if keyword.lower() in content.lower():
                            # Extract context
                            context = self._extract_context(content, keyword)

                            # Determine body region
                            region = self._identify_body_region(context)
                            if region:
                                mentions[region].append({
                                    'date': workout_date,
                                    'source': 'workout',
                                    'severity': severity,
                                    'keyword': keyword,
                                    'context': context
                                })

        # Scan daily notes
        for i in range((end_date - start_date).days + 1):
            date = start_date + timedelta(days=i)
            note_path = self.vault_path / f"{date.strftime('%Y-%m-%d')}.md"

            if note_path.exists():
                content = note_path.read_text()

                for severity, keywords in pain_keywords.items():
                    for keyword in keywords:
                        if keyword.lower() in content.lower():
                            context = self._extract_context(content, keyword)
                            region = self._identify_body_region(context)
                            if region:
                                mentions[region].append({
                                    'date': date,
                                    'source': 'daily_note',
                                    'severity': severity,
                                    'keyword': keyword,
                                    'context': context
                                })

        return mentions

    def _extract_date(self, filename):
        """Extract date from filename"""
        match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        return datetime.strptime(match.group(1), '%Y-%m-%d') if match else datetime.now()

    def _extract_context(self, content, keyword, window=100):
        """Extract text around keyword"""
        idx = content.lower().find(keyword.lower())
        if idx == -1:
            return ""

        start = max(0, idx - window)
        end = min(len(content), idx + len(keyword) + window)

        return content[start:end].strip()

    def _identify_body_region(self, context):
        """Identify which body region is mentioned"""
        context_lower = context.lower()

        region_keywords = {
            'Lower Back': ['lower back', 'lumbar', 'back', 'spine'],
            'Shoulder': ['shoulder', 'rotator', 'deltoid'],
            'Knee': ['knee', 'patella'],
            'Elbow': ['elbow', 'forearm'],
            'Wrist': ['wrist'],
            'Hip': ['hip', 'groin'],
            'Ankle': ['ankle']
        }

        for region, keywords in region_keywords.items():
            if any(kw in context_lower for kw in keywords):
                return region

        return None

    def _parse_threshold(self, threshold_str):
        """Parse threshold string like '2 mentions in 7 days'"""
        match = re.search(r'(\d+) mentions', threshold_str)
        return int(match.group(1)) if match else 2

    def _assess_severity(self, mentions):
        """Assess overall severity based on mentions"""
        high_count = sum(1 for m in mentions if m['severity'] == 'high_alert')
        moderate_count = sum(1 for m in mentions if m['severity'] == 'moderate')

        if high_count > 0:
            return 'high'
        elif moderate_count >= 3:
            return 'moderate'
        else:
            return 'low'

    def _identify_affected_exercises(self, mentions, monitored_exercises):
        """Identify which exercises correlate with mentions"""
        affected = set()

        for mention in mentions:
            context = mention['context'].lower()
            for exercise in monitored_exercises:
                if exercise.lower() in context:
                    affected.add(exercise)

        return list(affected)

    def generate_alert_markdown(self, alerts):
        """Generate markdown alert for daily note"""
        if not alerts:
            return ""

        md = "\n## ⚠️ OBSIDIA Injury Watch\n\n"

        for alert in alerts:
            severity_emoji = "🔴" if alert['severity'] == 'high' else "🟡"

            md += f"### {severity_emoji} {alert['region']}\n"
            md += f"- **Mentions:** {alert['mentions']} in last 30 days\n"
            md += f"- **Action:** {alert['action'].replace('_', ' ').title()}\n"

            if alert['affected_exercises']:
                md += f"- **Affected exercises:** {', '.join(alert['affected_exercises'])}\n"

            md += f"\n**Latest mention:** {alert['details'][-1]['date'].strftime('%Y-%m-%d')} - \"{alert['details'][-1]['context'][:80]}...\"\n\n"

        return md
```

**`scripts/check_injury_risk.py`** (Entry point)

```python
#!/usr/bin/env python3
"""
Check for injury risk patterns
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from obsidia.injury_watch import InjuryWatch

VAULT_PATH = Path.home() / "Documents/Obsidian/HarrysVault"

def inject_alert_into_today(alert_markdown):
    """Inject alert into today's daily note"""
    if not alert_markdown:
        return

    today = Path(VAULT_PATH) / f"{datetime.now().strftime('%Y-%m-%d')}.md"

    if not today.exists():
        print("Today's note doesn't exist yet")
        return

    with open(today) as f:
        content = f.read()

    # Check if alert already exists
    if "OBSIDIA Injury Watch" in content:
        # Replace existing
        import re
        pattern = r'## ⚠️ OBSIDIA Injury Watch.*?(?=\n##|\Z)'
        content = re.sub(pattern, alert_markdown.strip(), content, flags=re.DOTALL)
    else:
        # Append
        content += "\n" + alert_markdown

    with open(today, 'w') as f:
        f.write(content)

    print(f"✅ Injury alert added to {today.name}")

def main():
    print("Scanning for injury risks...")

    watcher = InjuryWatch(VAULT_PATH)
    alerts = watcher.scan_for_risks(lookback_days=30)

    if not alerts:
        print("✅ No injury risk patterns detected")
        return

    print(f"\n⚠️ {len(alerts)} potential injury risks detected:\n")

    for alert in alerts:
        print(f"{alert['region']}: {alert['mentions']} mentions ({alert['severity']} severity)")
        if alert['affected_exercises']:
            print(f"  Exercises: {', '.join(alert['affected_exercises'])}")
        print(f"  Action: {alert['action']}\n")

    # Generate markdown alert
    alert_md = watcher.generate_alert_markdown(alerts)

    # Inject into today's note
    from datetime import datetime
    inject_alert_into_today(alert_md)

if __name__ == "__main__":
    main()
```

### 3.3 Raycast Integration

**Create Raycast scripts in `~/Library/Application Support/Raycast/Scripts/`:**

**`obsidia-plan-today.sh`:**
```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Plan Today's Workout
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 💪
# @raycast.packageName OBSIDIA

python3 ~/Documents/Obsidian/scripts/plan_next_session.py $(date +%Y-%m-%d)
```

**`obsidia-weekly-summary.sh`:**
```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Weekly Training Summary
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📊
# @raycast.packageName OBSIDIA

python3 ~/Documents/Obsidian/scripts/analyze_progress.py
```

**`obsidia-injury-check.sh`:**
```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Check Injury Risks
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon ⚠️
# @raycast.packageName OBSIDIA

python3 ~/Documents/Obsidian/scripts/check_injury_risk.py
```

**Week 3 Tasks:**
1. Build analyzer.py and test on real workout data
2. Build injury_watch.py and test pattern detection
3. Set up Raycast scripts
4. Run full analysis on 2+ weeks of data
5. Test injury watch with intentional keywords
6. Add Sunday cron job for weekly analysis

**Success Criteria:**
- [ ] Weekly summaries generate useful insights
- [ ] Exercise progress tracking identifies plateaus
- [ ] Injury watch detects patterns correctly
- [ ] Raycast shortcuts work smoothly
- [ ] All scripts run without errors

---

## Phase 4: Polish & Advanced Features (Week 4 - Optional)

### 4.1 Voice Note Integration

**`scripts/obsidia/voice_parser.py`:**

```python
"""
Parse voice notes for workout reflections
"""
import whisper
import re
from pathlib import Path

class VoiceParser:
    def __init__(self):
        # Load Whisper model (small is good balance)
        self.model = whisper.load_model("small")

    def transcribe_audio(self, audio_path):
        """Transcribe audio file to text"""
        result = self.model.transcribe(str(audio_path))
        return result['text']

    def extract_workout_insights(self, transcript):
        """Extract structured insights from transcript"""
        insights = {
            'overall_feeling': None,
            'exercises_mentioned': [],
            'concerns': [],
            'energy_notes': [],
            'raw_transcript': transcript
        }

        # Detect sentiment
        positive_words = ['great', 'good', 'strong', 'solid', 'felt good', 'felt strong']
        negative_words = ['hard', 'struggle', 'difficult', 'tired', 'weak', 'off']

        transcript_lower = transcript.lower()

        if any(word in transcript_lower for word in positive_words):
            insights['overall_feeling'] = 'positive'
        elif any(word in transcript_lower for word in negative_words):
            insights['overall_feeling'] = 'challenging'
        else:
            insights['overall_feeling'] = 'neutral'

        # Extract exercise names (basic pattern matching)
        common_exercises = [
            'bench', 'squat', 'deadlift', 'pullup', 'row', 'press',
            'curl', 'lunge', 'overhead', 'lateral', 'tricep', 'cable'
        ]

        for exercise in common_exercises:
            if exercise in transcript_lower:
                insights['exercises_mentioned'].append(exercise)

        # Look for concerns
        concern_indicators = ['pain', 'hurt', 'sore', 'tight', 'uncomfortable', 'form']
        for indicator in concern_indicators:
            if indicator in transcript_lower:
                # Extract sentence containing the indicator
                sentences = re.split(r'[.!?]', transcript)
                for sentence in sentences:
                    if indicator in sentence.lower():
                        insights['concerns'].append(sentence.strip())

        # Look for energy mentions
        energy_indicators = ['energy', 'tired', 'fatigue', 'exhausted', 'pump', 'feeling']
        for indicator in energy_indicators:
            if indicator in transcript_lower:
                sentences = re.split(r'[.!?]', transcript)
                for sentence in sentences:
                    if indicator in sentence.lower():
                        insights['energy_notes'].append(sentence.strip())

        return insights
```

**`scripts/parse_workout_voice.py`:**

```python
#!/usr/bin/env python3
"""
Transcribe post-workout voice note and append to workout log
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from obsidia.voice_parser import VoiceParser

def append_to_workout(workout_path, insights):
    """Append parsed insights to workout markdown"""
    with open(workout_path) as f:
        content = f.read()

    voice_section = f"""
## Voice Note Insights

**Overall feeling:** {insights['overall_feeling'].title()}

"""

    if insights['exercises_mentioned']:
        voice_section += f"**Exercises mentioned:** {', '.join(insights['exercises_mentioned'])}\n\n"

    if insights['concerns']:
        voice_section += "**Concerns noted:**\n"
        for concern in insights['concerns']:
            voice_section += f"- {concern}\n"
        voice_section += "\n"

    if insights['energy_notes']:
        voice_section += "**Energy notes:**\n"
        for note in insights['energy_notes']:
            voice_section += f"- {note}\n"
        voice_section += "\n"

    voice_section += f"**Full transcript:**\n> {insights['raw_transcript']}\n"

    # Append
    content += "\n" + voice_section

    with open(workout_path, 'w') as f:
        f.write(content)

def main():
    if len(sys.argv) < 3:
        print("Usage: parse_workout_voice.py <audio-file> <workout-file>")
        sys.exit(1)

    audio_path = Path(sys.argv[1])
    workout_path = Path(sys.argv[2])

    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    if not workout_path.exists():
        print(f"Error: Workout file not found: {workout_path}")
        sys.exit(1)

    print(f"Transcribing {audio_path.name}...")

    parser = VoiceParser()
    transcript = parser.transcribe_audio(audio_path)

    print(f"Extracting insights...")
    insights = parser.extract_workout_insights(transcript)

    print(f"Appending to {workout_path.name}...")
    append_to_workout(workout_path, insights)

    print("✅ Voice note processed!")
    print(f"Overall feeling: {insights['overall_feeling']}")
    if insights['concerns']:
        print(f"⚠️ Concerns detected: {len(insights['concerns'])}")

if __name__ == "__main__":
    main()
```

### 4.2 Dataview Dashboard

**Create `02-training/dashboard.md`:**

````markdown
---
cssclass: dashboard
---

# 💪 OBSIDIA Training Dashboard

## Current Status

```dataview
TABLE WITHOUT ID
  level as "Level",
  title as "Title",
  total_xp as "Total XP",
  current_level_xp as "Progress",
  xp_to_next_level as "To Next Level"
FROM ".obsidia/state.json"
```

## This Week

```dataview
TABLE WITHOUT ID
  date as "Date",
  session_type as "Type",
  xp_earned as "XP",
  status as "Status"
FROM "02-training/workouts"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

## Recent Progress

```dataviewjs
const workouts = dv.pages('"02-training/workouts"')
  .where(p => p.date >= dv.date('today') - dv.duration('30 days'))
  .sort(p => p.date, 'desc');

const volumeByWeek = {};
workouts.forEach(w => {
  const week = dv.date(w.date).weekyear;
  if (!volumeByWeek[week]) volumeByWeek[week] = 0;
  volumeByWeek[week] += w.total_volume || 0;
});

dv.header(3, "Volume Trend (Last 4 Weeks)");
dv.table(
  ["Week", "Total Volume (kg)"],
  Object.entries(volumeByWeek).map(([week, vol]) => [week, Math.round(vol)])
);
```

## Exercise PRs

```dataview
TABLE WITHOUT ID
  exercise as "Exercise",
  max_weight as "Max Weight (kg)",
  date as "Date"
FROM "02-training/workouts"
WHERE max_weight != null
SORT max_weight DESC
LIMIT 10
```

## Achievements

```dataview
LIST
FROM ".obsidia/state.json"
WHERE achievements_unlocked != null
FLATTEN achievements_unlocked
```

## Injury Watch

```dataview
TABLE WITHOUT ID
  region as "Region",
  mentions as "Mentions (30d)",
  action as "Recommended Action"
FROM "02-training/injury-alerts"
WHERE severity IN ["moderate", "high"]
SORT severity DESC
```
````

### 4.3 Advanced Raycast Commands

**`obsidia-log-workout.sh`** (Quick logging):

```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Log Workout
# @raycast.mode silent

# @raycast.argument1 { "type": "text", "placeholder": "Exercise name" }
# @raycast.argument2 { "type": "text", "placeholder": "Weight (kg)" }
# @raycast.argument3 { "type": "text", "placeholder": "Reps" }
# @raycast.argument4 { "type": "text", "placeholder": "RPE" }

# Optional parameters:
# @raycast.icon 📝
# @raycast.packageName OBSIDIA

WORKOUT_FILE=$(ls -t ~/Documents/Obsidian/HarrysVault/02-training/workouts/*.md | head -1)

# Append to latest workout
echo "- $1: $2kg x $3 @ RPE $4" >> "$WORKOUT_FILE"

echo "Logged: $1 - $2kg x $3 @ RPE $4"
```

**Week 4 Tasks:**
1. Install Whisper for voice transcription
2. Test voice note parsing on sample audio
3. Set up Dataview dashboard
4. Build advanced Raycast commands
5. Polish UI/UX elements
6. Full system integration test

---

## Deployment Checklist

### Initial Setup

```bash
# 1. Install dependencies
pip3 install pandas pyyaml openai-whisper

# 2. Create directory structure
cd ~/Documents/Obsidian/HarrysVault
mkdir -p 02-training/{programs,workouts,progress/{weekly-summaries,monthly-reports},config}
mkdir -p scripts/obsidia
mkdir -p .obsidia/{cache,logs}

# 3. Initialize state
echo '{"total_xp": 0, "level": 1, "current_level_xp": 0, "streak_days": 0, "achievements_unlocked": []}' > .obsidia/state.json

# 4. Make scripts executable
chmod +x scripts/*.py

# 5. Set up cron jobs
launchctl load ~/Library/LaunchAgents/com.obsidia.plan-session.plist

# 6. Install Obsidian plugins
# - Dataview
# - Templater
# - Periodic Notes
```

### Testing Protocol

**Day 1:**
- [ ] Create daily note from template
- [ ] Run `plan_next_session.py` manually
- [ ] Verify session options appear correctly

**Day 2:**
- [ ] Complete a workout, log manually
- [ ] Run `calculate_workout_xp.py`
- [ ] Verify XP calculation is correct

**Day 3:**
- [ ] Check cron job ran (look at logs)
- [ ] Complete another workout
- [ ] Test Raycast shortcuts

**Day 7:**
- [ ] Run `analyze_progress.py`
- [ ] Review weekly summary
- [ ] Check injury watch system

---

## Maintenance & Scaling

### Weekly
- Review generated summaries
- Check script logs for errors
- Validate XP calculations

### Monthly
- Review program structure (edit `current-program.yaml`)
- Archive old workout logs
- Update exercise library if needed

### Quarterly
- Analyze long-term trends
- Adjust XP formulas if needed
- Add new achievements

---

## Troubleshooting

**Scripts not running:**
```bash
# Check Python path
which python3

# Check logs
tail -f /tmp/obsidia-plan.log
tail -f /tmp/obsidia-plan-error.log

# Test manually
python3 ~/Documents/Obsidian/scripts/plan_next_session.py
```

**XP calculations seem off:**
```bash
# Check state file
cat ~/Documents/Obsidian/HarrysVault/.obsidia/state.json

# Recalculate from scratch
python3 ~/Documents/Obsidian/scripts/recalculate_all_xp.py
```

**Cron job not triggering:**
```bash
# Check if loaded
launchctl list | grep obsidia

# Reload
launchctl unload ~/Library/LaunchAgents/com.obsidia.plan-session.plist
launchctl load ~/Library/LaunchAgents/com.obsidia.plan-session.plist
```

---

## Success Metrics

After 4 weeks, you should have:
- [ ] 90%+ session planning automation
- [ ] Accurate XP/level tracking
- [ ] At least 3 useful insights from weekly analysis
- [ ] 0 false positives from injury watch
- [ ] <5min manual logging time per workout
- [ ] High engagement (you actually use it consistently)

**The ultimate test:** Does this system make training *easier* and *more motivating*? If yes, keep building. If no, simplify ruthlessly.

---

Want me to start building Phase 1 in Claude Code right now?
