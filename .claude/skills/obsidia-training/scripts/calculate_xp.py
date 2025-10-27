#!/usr/bin/env python3
"""
OBSIDIA XP Calculator
Calculate workout XP based on weight × reps with multipliers for RPE, form, exercise type, and achievements.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional

class XPCalculator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.config = self._load_xp_config()

    def _load_xp_config(self) -> Dict:
        """Load XP configuration from YAML."""
        config_file = self.vault_path / ".claude/skills/obsidia-training/config/xp-config.yaml"
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def calculate_set_xp(
        self,
        weight_kg: float,
        reps: int,
        rpe: float,
        form_quality: int,
        is_primary: bool = False,
        achievements: Optional[List[str]] = None
    ) -> Dict:
        """
        Calculate XP for a single set.

        Args:
            weight_kg: Weight lifted in kilograms
            reps: Number of reps completed
            rpe: Rate of Perceived Exertion (1-10 scale)
            form_quality: Form quality rating (1-10 scale)
            is_primary: Whether this is a primary/compound exercise
            achievements: List of achievement codes ('pr', 'first_time', 'all_sets_complete')

        Returns:
            Dict with 'base_xp', 'multipliers', 'total_xp', 'breakdown'
        """
        if achievements is None:
            achievements = []

        # Base XP = weight × reps
        base_xp = weight_kg * reps

        # Calculate multipliers
        multipliers = {}
        breakdown = []

        # 1. RPE Multiplier
        rpe_mult = self._get_rpe_multiplier(rpe)
        multipliers['rpe'] = rpe_mult
        breakdown.append(f"RPE {rpe}: {rpe_mult}x")

        # 2. Form Quality Multiplier
        form_mult = self._get_form_multiplier(form_quality)
        multipliers['form'] = form_mult
        breakdown.append(f"Form {form_quality}/10: {form_mult}x")

        # 3. Exercise Type Multiplier
        exercise_mult = 1.3 if is_primary else 1.0
        multipliers['exercise_type'] = exercise_mult
        breakdown.append(f"{'Primary' if is_primary else 'Accessory'}: {exercise_mult}x")

        # 4. Achievement Multipliers
        achievement_mults = []
        if 'pr' in achievements:
            achievement_mults.append(('PR', 2.0))
            breakdown.append("PR Achievement: 2.0x")

        if 'first_time' in achievements:
            achievement_mults.append(('First Time', 1.5))
            breakdown.append("First Time: 1.5x")

        if 'all_sets_complete' in achievements:
            achievement_mults.append(('All Sets', 1.1))
            breakdown.append("All Sets Complete: 1.1x")

        # Calculate total multiplier (all multiply together)
        total_mult = rpe_mult * form_mult * exercise_mult
        for _, mult in achievement_mults:
            total_mult *= mult

        # Calculate final XP
        total_xp = round(base_xp * total_mult)

        return {
            'base_xp': base_xp,
            'multipliers': {
                'rpe': rpe_mult,
                'form': form_mult,
                'exercise_type': exercise_mult,
                'achievements': {name: mult for name, mult in achievement_mults},
                'total': total_mult
            },
            'total_xp': total_xp,
            'breakdown': breakdown
        }

    def _get_rpe_multiplier(self, rpe: float) -> float:
        """Get RPE multiplier based on config."""
        if rpe >= 9:
            return self.config['xp_calculation']['multipliers']['rpe_9_plus']['value']
        elif rpe == 8:
            return self.config['xp_calculation']['multipliers']['rpe_8']['value']
        elif rpe == 7:
            return self.config['xp_calculation']['multipliers']['rpe_7']['value']
        else:
            return self.config['xp_calculation']['multipliers']['rpe_below_7']['value']

    def _get_form_multiplier(self, form: int) -> float:
        """Get form quality multiplier based on config."""
        if form >= 9:
            return self.config['xp_calculation']['multipliers']['form_excellent']['value']
        elif form >= 7:
            return self.config['xp_calculation']['multipliers']['form_good']['value']
        else:
            return self.config['xp_calculation']['multipliers']['form_poor']['value']

    def calculate_exercise_xp(self, exercise_data: Dict) -> Dict:
        """
        Calculate total XP for an exercise (all sets combined).

        Args:
            exercise_data: Dict with 'name', 'sets' (list of set data), 'is_primary', 'achievements'

        Returns:
            Dict with 'exercise_name', 'total_xp', 'sets_breakdown'
        """
        sets = exercise_data.get('sets', [])
        is_primary = exercise_data.get('is_primary', False)
        exercise_achievements = exercise_data.get('achievements', [])

        total_exercise_xp = 0
        sets_breakdown = []

        for i, set_data in enumerate(sets, 1):
            set_xp = self.calculate_set_xp(
                weight_kg=set_data['weight_kg'],
                reps=set_data['reps'],
                rpe=set_data['rpe'],
                form_quality=set_data['form'],
                is_primary=is_primary,
                achievements=set_data.get('achievements', [])
            )

            total_exercise_xp += set_xp['total_xp']
            sets_breakdown.append({
                'set_number': i,
                'xp': set_xp['total_xp'],
                'breakdown': set_xp['breakdown']
            })

        # Apply exercise-level achievement bonuses
        if 'all_sets_complete' in exercise_achievements:
            bonus = total_exercise_xp * 0.1
            total_exercise_xp += round(bonus)
            sets_breakdown.append({
                'bonus': 'All Sets Complete',
                'xp': round(bonus)
            })

        return {
            'exercise_name': exercise_data['name'],
            'total_xp': round(total_exercise_xp),
            'sets_breakdown': sets_breakdown
        }

    def calculate_session_xp(self, session_data: Dict) -> Dict:
        """
        Calculate total XP for entire session.

        Args:
            session_data: Dict with 'exercises' (list of exercise data) and optional 'bonuses'

        Returns:
            Dict with 'total_xp', 'exercises_breakdown', 'level_info', 'bonuses'
        """
        exercises = session_data.get('exercises', [])
        total_session_xp = 0
        exercises_breakdown = []

        for exercise in exercises:
            exercise_xp = self.calculate_exercise_xp(exercise)
            total_session_xp += exercise_xp['total_xp']
            exercises_breakdown.append(exercise_xp)

        # Apply session-level bonuses
        bonuses = []
        if session_data.get('weekly_consistency_bonus', False):
            bonus_xp = self.config['xp_calculation'].get('streaks_and_bonuses', {}).get('weekly_consistency', {}).get('bonus_xp', 500)
            bonuses.append({'name': 'Weekly Consistency', 'xp': bonus_xp})
            total_session_xp += bonus_xp

        if session_data.get('perfect_week_bonus', False):
            bonus_xp = self.config['xp_calculation'].get('streaks_and_bonuses', {}).get('perfect_week', {}).get('bonus_xp', 1000)
            bonuses.append({'name': 'Perfect Week', 'xp': bonus_xp})
            total_session_xp += bonus_xp

        # Calculate level information
        xp_per_level = self.config['xp_calculation']['level_system']['xp_per_level']
        current_total_xp = session_data.get('current_total_xp', 0) + total_session_xp
        current_level = current_total_xp // xp_per_level
        xp_to_next_level = xp_per_level - (current_total_xp % xp_per_level)

        return {
            'session_xp': total_session_xp,
            'exercises_breakdown': exercises_breakdown,
            'bonuses': bonuses,
            'level_info': {
                'current_level': current_level,
                'current_total_xp': current_total_xp,
                'xp_to_next_level': xp_to_next_level,
                'progress_percentage': round((current_total_xp % xp_per_level) / xp_per_level * 100, 1)
            }
        }

    def format_xp_summary(self, session_xp_data: Dict) -> str:
        """Format XP calculation into human-readable summary."""
        lines = []
        lines.append("=" * 50)
        lines.append("SESSION XP SUMMARY")
        lines.append("=" * 50)

        for exercise in session_xp_data['exercises_breakdown']:
            lines.append(f"\n{exercise['exercise_name']}: {exercise['total_xp']} XP")
            for set_info in exercise['sets_breakdown']:
                if 'set_number' in set_info:
                    lines.append(f"  Set {set_info['set_number']}: {set_info['xp']} XP")
                    lines.append(f"    ({', '.join(set_info['breakdown'])})")
                elif 'bonus' in set_info:
                    lines.append(f"  Bonus - {set_info['bonus']}: +{set_info['xp']} XP")

        if session_xp_data['bonuses']:
            lines.append("\nSESSION BONUSES:")
            for bonus in session_xp_data['bonuses']:
                lines.append(f"  {bonus['name']}: +{bonus['xp']} XP")

        lines.append("\n" + "=" * 50)
        lines.append(f"TOTAL SESSION XP: {session_xp_data['session_xp']}")
        lines.append("=" * 50)

        level_info = session_xp_data['level_info']
        lines.append(f"\nCurrent Level: {level_info['current_level']}")
        lines.append(f"Total XP: {level_info['current_total_xp']}")
        lines.append(f"Progress to Level {level_info['current_level'] + 1}: {level_info['progress_percentage']}%")
        lines.append(f"XP Needed: {level_info['xp_to_next_level']}")

        return "\n".join(lines)

def main():
    """CLI interface for XP calculation."""
    import sys

    vault_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/harrysayers/Developer/claudelife"

    # Example usage
    calculator = XPCalculator(vault_path)

    # Example session data
    session_data = {
        'current_total_xp': 25000,  # Already at level 2
        'exercises': [
            {
                'name': 'Bench Press',
                'is_primary': True,
                'sets': [
                    {'weight_kg': 80, 'reps': 8, 'rpe': 8, 'form': 8},
                    {'weight_kg': 80, 'reps': 8, 'rpe': 8, 'form': 8},
                    {'weight_kg': 80, 'reps': 7, 'rpe': 9, 'form': 7},
                ],
                'achievements': ['all_sets_complete']
            },
            {
                'name': 'Bicep Curls',
                'is_primary': False,
                'sets': [
                    {'weight_kg': 15, 'reps': 12, 'rpe': 8, 'form': 9, 'achievements': ['pr']},
                    {'weight_kg': 15, 'reps': 11, 'rpe': 9, 'form': 8},
                ],
            }
        ],
        'weekly_consistency_bonus': False
    }

    result = calculator.calculate_session_xp(session_data)
    print(calculator.format_xp_summary(result))
    print("\nJSON Output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
