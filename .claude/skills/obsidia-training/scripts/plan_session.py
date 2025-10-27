#!/usr/bin/env python3
"""
OBSIDIA Session Planner
Context-aware workout session planning based on daily note data, recent training history, and current program.
"""

import yaml
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class SessionPlanner:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.training_path = self.vault_path / "01-areas/health-fitness/training"
        self.program = self._load_program()

    def _load_program(self) -> Dict:
        """Load current training program configuration."""
        program_file = self.vault_path / ".claude/skills/obsidia-training/programs/current-program.yaml"
        with open(program_file, 'r') as f:
            return yaml.safe_load(f)

    def _load_exercises_library(self) -> Dict:
        """Load exercise library."""
        exercises_file = self.vault_path / ".claude/skills/obsidia-training/config/exercises.yaml"
        with open(exercises_file, 'r') as f:
            return yaml.safe_load(f)

    def _get_daily_note_path(self, date: Optional[datetime] = None) -> Path:
        """Get path to today's or specified date's daily note."""
        if date is None:
            date = datetime.now()

        # Format: "YY-MM-DD - Day.md" (e.g., "25-10-21 - Mon.md")
        day_name = date.strftime("%a")
        filename = f"{date.strftime('%y-%m-%d')} - {day_name}.md"
        return self.vault_path / "00 - Daily" / filename

    def _get_recent_workouts(self, days: int = 7) -> List[Dict]:
        """Get recent workout logs."""
        workouts = []
        workout_dir = self.training_path / "workouts"

        if not workout_dir.exists():
            return workouts

        # Get workout files from last N days
        cutoff_date = datetime.now() - timedelta(days=days)

        for workout_file in sorted(workout_dir.glob("*.md"), reverse=True):
            # Parse date from filename (supports both formats):
            # - 🏋️YYYY-MM-DD.md
            # - YYYY-MM-DD-workout.md
            filename = workout_file.stem

            # Try emoji format first (🏋️YYYY-MM-DD)
            emoji_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
            if emoji_match:
                date_str = emoji_match.group(1)
            else:
                # Fallback to old format
                date_str = filename.split('-workout')[0]

            try:
                workout_date = datetime.strptime(date_str, "%Y-%m-%d")
                if workout_date >= cutoff_date:
                    workouts.append(self._parse_workout_file(workout_file))
            except ValueError:
                continue

        return workouts

    def _parse_workout_file(self, filepath: Path) -> Dict:
        """Parse a workout markdown file."""
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        else:
            frontmatter = {}

        return {
            'date': frontmatter.get('date'),
            'session_type': frontmatter.get('session_type'),
            'status': frontmatter.get('status'),
            'total_xp': frontmatter.get('total_xp', 0),
            'duration': frontmatter.get('session_duration_min', 0)
        }

    def _parse_daily_note_context(self, date: Optional[datetime] = None) -> Dict:
        """Extract relevant context from daily note."""
        daily_note = self._get_daily_note_path(date)

        if not daily_note.exists():
            return {
                'energy': 7,
                'sleep': 7,
                'stress': 5,
                'soreness': 'None',
                'readiness': 7
            }

        with open(daily_note, 'r') as f:
            content = f.read()

        context = {}

        # Extract frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
            context['energy'] = frontmatter.get('energy_morning', 7)
            context['sleep'] = frontmatter.get('sleep_quality', 7)

        # Extract from body if not in frontmatter
        if 'energy' not in context:
            energy_match = re.search(r'\*\*Energy Level:\*\*\s*(\d+)', content)
            context['energy'] = int(energy_match.group(1)) if energy_match else 7

        if 'sleep' not in context:
            sleep_match = re.search(r'\*\*Sleep Quality.*?:\*\*\s*(\d+)', content)
            context['sleep'] = int(sleep_match.group(1)) if sleep_match else 7

        stress_match = re.search(r'\*\*Stress Level:\*\*\s*(\d+)', content)
        context['stress'] = int(stress_match.group(1)) if stress_match else 5

        soreness_match = re.search(r'\*\*Soreness/Pain:\*\*\s*(None|Mild|Moderate|Severe)', content)
        context['soreness'] = soreness_match.group(1) if soreness_match else 'None'

        readiness_match = re.search(r'\*\*Readiness to Train:\*\*\s*(\d+)', content)
        context['readiness'] = int(readiness_match.group(1)) if readiness_match else 7

        return context

    def _determine_session_type(self, date: Optional[datetime] = None) -> str:
        """Determine which workout type is due based on schedule and recent history."""
        if date is None:
            date = datetime.now()

        day_of_week = date.isoweekday()  # 1=Monday, 7=Sunday

        # Check if it's a scheduled rest day
        if day_of_week in self.program['schedule']['rest_days']:
            return 'rest'

        # Get recent workouts to see what was last trained
        recent_workouts = self._get_recent_workouts(days=7)
        recent_types = [w['session_type'] for w in recent_workouts if w['session_type']]

        # Determine next session based on preferred schedule
        schedule = self.program['schedule']['preferred_days']

        # Check which session types are due today
        for session_type, days in schedule.items():
            if day_of_week in days:
                # Check if this type was recently done
                if session_type not in recent_types[-2:]:  # Not in last 2 sessions
                    return session_type

        # Fallback: rotate through types that haven't been done recently
        workout_types = list(self.program['workouts'].keys())
        for wtype in workout_types:
            if wtype not in recent_types[-3:]:
                return wtype

        return workout_types[0]  # Default to first type

    def _generate_standard_session(self, session_type: str) -> Dict:
        """Generate standard session from program."""
        workout = self.program['workouts'][session_type]

        return {
            'type': 'standard',
            'session_type': session_type,
            'focus': workout['focus'],
            'exercises': workout['exercises'],
            'notes': "Standard program session - follow as written"
        }

    def _generate_adapted_session(self, session_type: str, context: Dict, recent_workouts: List[Dict]) -> Dict:
        """Generate adapted session based on context."""
        workout = self.program['workouts'][session_type].copy()
        adaptations = []

        # Apply adaptation rules
        rules = self.program['recovery_protocols']['adaptation_rules']

        energy = context.get('energy', 7)
        sleep = context.get('sleep', 7)
        stress = context.get('stress', 5)
        soreness = context.get('soreness', 'None')

        # Tired but ok - reduce volume
        if energy < 7 and sleep > 5:
            adaptations.append("Reduced volume by 10% (remove 1 set from accessories)")
            # Remove last set from accessory exercises
            for ex in workout['exercises']:
                if not ex.get('primary', False):
                    ex['sets'] = max(2, ex['sets'] - 1)

        # Very tired - switch to recovery
        if energy < 6 or sleep < 5:
            return self._generate_recovery_session(context)

        # High stress - reduce intensity
        if stress > 7:
            adaptations.append("Reduced intensity to RPE 7 (high stress)")
            for ex in workout['exercises']:
                ex['rpe_target'] = 7

        # Significant soreness - lighter work
        if soreness in ['Moderate', 'Severe']:
            adaptations.append("Lighter loads due to soreness - focus on pump and form")
            for ex in workout['exercises']:
                ex['rpe_target'] = max(6, ex['rpe_target'] - 2)
                ex['reps'] = f"{int(ex['reps'].split('-')[0]) + 2}-{int(ex['reps'].split('-')[1]) + 3}"

        return {
            'type': 'adapted',
            'session_type': session_type,
            'focus': workout['focus'],
            'exercises': workout['exercises'],
            'adaptations': adaptations,
            'notes': f"Adapted session based on: Energy={energy}/10, Sleep={sleep}/10, Stress={stress}/10"
        }

    def _generate_recovery_session(self, context: Dict) -> Dict:
        """Generate light recovery session."""
        return {
            'type': 'recovery',
            'session_type': 'recovery',
            'focus': 'Active recovery and movement quality',
            'exercises': [
                {
                    'name': 'Light cardio (walk, bike)',
                    'duration': '20-30 min',
                    'intensity': 'Very easy, conversational pace'
                },
                {
                    'name': 'Dynamic stretching',
                    'duration': '10 min',
                    'focus': 'Major muscle groups'
                },
                {
                    'name': 'Foam rolling',
                    'duration': '10 min',
                    'focus': 'Sore areas'
                }
            ],
            'notes': f"Recovery session due to low energy ({context.get('energy', 'unknown')}/10) or poor sleep ({context.get('sleep', 'unknown')}/10)"
        }

    def plan_next_session(self, date: Optional[datetime] = None) -> Dict:
        """
        Generate 3 session options: Standard, Adapted, Recovery.

        Returns:
            Dict with keys: standard, adapted, recovery, recommendation, context
        """
        if date is None:
            date = datetime.now()

        # Get context
        context = self._parse_daily_note_context(date)
        recent_workouts = self._get_recent_workouts()
        session_type = self._determine_session_type(date)

        # Generate options
        standard = self._generate_standard_session(session_type)
        adapted = self._generate_adapted_session(session_type, context, recent_workouts)
        recovery = self._generate_recovery_session(context)

        # Determine recommendation
        if context['energy'] < 6 or context['sleep'] < 5:
            recommendation = 'recovery'
        elif context['energy'] < 7 or context['stress'] > 7 or context['soreness'] in ['Moderate', 'Severe']:
            recommendation = 'adapted'
        else:
            recommendation = 'standard'

        return {
            'date': date.strftime('%Y-%m-%d'),
            'standard': standard,
            'adapted': adapted,
            'recovery': recovery,
            'recommendation': recommendation,
            'context': context
        }

def main():
    """CLI interface for session planning."""
    import sys

    vault_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/harrysayers/Developer/claudelife"

    planner = SessionPlanner(vault_path)
    plan = planner.plan_next_session()

    print(yaml.dump(plan, default_flow_style=False, sort_keys=False))

if __name__ == "__main__":
    main()
