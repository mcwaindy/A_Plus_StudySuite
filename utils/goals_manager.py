"""
GoalsManager - Manages study goals, milestones, and progress tracking.

Handles:
- Exam target date management
- Readiness percentage calculation
- Daily study recommendations
- Milestone tracking and achievement detection
- Study streak calculation
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class GoalsManager:
    """Central manager for all goals and milestones functionality."""

    MILESTONES_CONFIG = {
        'cards_studied': [
            {'threshold': 10, 'name': 'First 10 Cards', 'icon': '🎉'},
            {'threshold': 25, 'name': 'Keep It Up - 25 Cards Studied!', 'icon': '🎉'},
            {'threshold': 50, 'name': '50 Cards Down!', 'icon': '🎉'},
            {'threshold': 100, 'name': 'Century! 100 Cards Studied!', 'icon': '🎉'},
            {'threshold': 250, 'name': 'Super Grind - 250 Cards!', 'icon': '🎉'},
            {'threshold': 500, 'name': 'Halfway There - 500 Cards!', 'icon': '🎉'},
            {'threshold': 1000, 'name': 'Legendary Grind - 1000 Cards!', 'icon': '🎉'},
        ],
        'objectives_mastered': [
            {'objective': '1', 'name': 'Objective 1 Mastered!', 'icon': '🎯'},
            {'objective': '2', 'name': 'Objective 2 Mastered!', 'icon': '🎯'},
            {'objective': '3', 'name': 'Objective 3 Mastered!', 'icon': '🎯'},
            {'objective': 'all', 'name': 'All Objectives Mastered!', 'icon': '🏆'},
        ],
        'study_streak': [
            {'days': 3, 'name': '3-Day Streak!', 'icon': '🔥'},
            {'days': 7, 'name': 'Week-Long Streak!', 'icon': '🔥'},
            {'days': 14, 'name': 'Two-Week Grind!', 'icon': '🔥'},
            {'days': 30, 'name': 'Monthly Commitment!', 'icon': '🔥'},
        ],
        'perfect_scores': [
            {'type': 'single_perfect', 'name': 'Perfect Practice Exam!', 'icon': '💯'},
            {'type': 'week_perfect', 'name': 'Perfect Week!', 'icon': '💯'},
        ]
    }

    def __init__(self):
        """Initialize GoalsManager and load existing goals data."""
        self.goals_path = Path('data/goals.json')
        self.review_history_path = Path('data/review_history.json')
        self.goals_data = self._load_goals()

    def _load_goals(self) -> Dict:
        """Load goals from data file, create if doesn't exist."""
        if self.goals_path.exists():
            try:
                with open(self.goals_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading goals: {e}. Using defaults.")
                return self._get_default_goals()
        return self._get_default_goals()

    def _get_default_goals(self) -> Dict:
        """Return default goals structure."""
        return {
            'exam_target_date': None,
            'target_readiness_percentage': 90,
            'milestones_achieved': [],
            'daily_goals': {
                'target_cards_per_day': 20,
                'target_exams_per_week': 2,
                'target_minutes_per_day': 45
            },
            'study_streak': {
                'current_days': 0,
                'longest_streak': 0,
                'last_study_date': None
            }
        }

    def _save_goals(self) -> None:
        """Save goals data to file."""
        try:
            with open(self.goals_path, 'w', encoding='utf-8') as f:
                json.dump(self.goals_data, f, indent=2)
        except IOError as e:
            print(f"Error saving goals: {e}")

    def _load_review_history(self) -> List[Dict]:
        """Load review history from file."""
        if self.review_history_path.exists():
            try:
                with open(self.review_history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    # ==================== EXAM DATE MANAGEMENT ====================

    def set_exam_date(self, date_str: str) -> bool:
        """
        Set the target exam date.

        Args:
            date_str: Date string in format 'YYYY-MM-DD'

        Returns:
            bool: True if successful, False if invalid format
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            self.goals_data['exam_target_date'] = date_str
            self._save_goals()
            return True
        except ValueError:
            print(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
            return False

    def get_exam_date(self) -> Optional[str]:
        """Get the target exam date."""
        return self.goals_data.get('exam_target_date')

    def get_days_until_exam(self) -> Optional[int]:
        """
        Calculate days until exam.

        Returns:
            int: Days remaining, or None if no exam date set
        """
        exam_date_str = self.goals_data.get('exam_target_date')
        if not exam_date_str:
            return None

        try:
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
            today = datetime.now().date()
            delta = (exam_date - today).days
            return max(delta, 0)  # Return 0 if past exam date
        except ValueError:
            return None

    # ==================== READINESS CALCULATION ====================

    def calculate_readiness_percentage(self, review_history: Optional[List[Dict]] = None) -> float:
        """
        Calculate exam readiness as percentage (0-100).

        Formula:
        Readiness % = (A × 0.5 + B × 0.3 + C × 0.2) × 100

        Where:
            A = Cards Studied Progress (current / target) — HEAVILY WEIGHTED
            B = Objectives Coverage (objectives_with_cards / 3)
            C = Mastery Score (cards_mastered / cards_studied via spaced repetition)

        Note: cards_reviewed in review history contains cards marked "Needs Review",
        so mastery = total_studied - cards_needing_help.

        Args:
            review_history: Optional review history list. If None, loads from file.

        Returns:
            float: Readiness percentage (0-100)
        """
        if review_history is None:
            review_history = self._load_review_history()

        if not review_history:
            return 0.0

        # A: Cards Studied Progress (DOMINANT FACTOR - 50%)
        # This reflects raw volume of study; must see significant portion of card pool
        total_cards_studied = sum(r.get('cards_studied', 0) for r in review_history)
        target_cards = 500  # Rough target for full readiness; user should study most/all 222+ cards
        cards_progress = min(total_cards_studied / target_cards, 1.0) if target_cards > 0 else 0.0

        # B: Objectives Coverage (30%)
        # Encourages balanced study across all 3 objectives
        objectives_with_cards = set()
        for review in review_history:
            for objective in review.get('objectives', []):
                if objective != 'All':
                    objectives_with_cards.add(objective)
        objectives_coverage = len(objectives_with_cards) / 3.0  # 3 objectives total

        # C: Mastery Score (20%)
        # Based on spaced repetition when available; otherwise estimate from review data
        # cards_reviewed contains cards marked "Needs Review", so:
        # mastery = (total_studied - cards_needing_help) / total_studied
        cards_needing_help = sum(len(r.get('cards_reviewed', [])) for r in review_history)
        total_attempts = total_cards_studied
        cards_mastered = max(0, total_attempts - cards_needing_help)
        mastery_score = (cards_mastered / total_attempts) if total_attempts > 0 else 0.0

        # Calculate weighted readiness
        # Heavy emphasis on cards_progress to reflect that readiness is primarily volume-based
        readiness = (cards_progress * 0.5 + objectives_coverage * 0.3 + mastery_score * 0.2) * 100
        return min(readiness, 100.0)  # Cap at 100%

    # ==================== DAILY RECOMMENDATIONS ====================

    def get_daily_recommendation(self) -> str:
        """
        Calculate recommended daily study load based on progress and time to exam.

        Returns:
            str: Personalized recommendation text
        """
        review_history = self._load_review_history()
        readiness = self.calculate_readiness_percentage(review_history)
        days_until = self.get_days_until_exam()

        if days_until is None:
            return "⏰ Set a target exam date to get personalized study recommendations!"

        if days_until <= 0:
            return "🎓 Exam day! Good luck and go get that A+!"

        if readiness >= 90:
            return "✅ You're exam-ready! Light review recommended (15 mins/day)"

        if readiness >= 75:
            daily_cards = 20
            return f"📚 Review unfamiliar cards ({daily_cards} cards/day)"

        # Scale recommendations based on readiness deficit
        deficit = 90 - readiness
        intensity_factor = min(deficit / 15, 2.0)  # Cap at 2x normal intensity
        daily_cards = int(20 * intensity_factor)
        daily_minutes = int(45 * intensity_factor)

        return f"💪 Study {daily_cards} new cards + 10 reviews ({daily_minutes} mins/day)"

    # ==================== STUDY STREAK ====================

    def update_study_streak(self, review_entry: Dict) -> None:
        """
        Update study streak based on a new review entry.

        Args:
            review_entry: Review history entry from flashcard session
        """
        review_date_str = review_entry.get('timestamp', '')
        if not review_date_str:
            return

        try:
            # Parse timestamp (format: "2026-08-11T14:30:00")
            review_date = datetime.fromisoformat(review_date_str).date()
        except (ValueError, AttributeError):
            return

        last_study_str = self.goals_data['study_streak'].get('last_study_date')
        today = datetime.now().date()

        if last_study_str:
            try:
                last_study_date = datetime.fromisoformat(last_study_str).date()
            except ValueError:
                last_study_date = None
        else:
            last_study_date = None

        # If studied today already, don't increment
        if last_study_date == today:
            return

        # If studied yesterday, continue streak
        if last_study_date and (today - last_study_date).days == 1:
            self.goals_data['study_streak']['current_days'] += 1
        # If gap of 2+ days, reset streak
        elif not last_study_date or (today - last_study_date).days > 1:
            self.goals_data['study_streak']['current_days'] = 1

        # Update longest streak if current is longer
        if self.goals_data['study_streak']['current_days'] > self.goals_data['study_streak']['longest_streak']:
            self.goals_data['study_streak']['longest_streak'] = self.goals_data['study_streak']['current_days']

        # Update last study date
        self.goals_data['study_streak']['last_study_date'] = today.isoformat()
        self._save_goals()

    def get_study_streak(self) -> Dict:
        """Get current study streak information."""
        return self.goals_data['study_streak'].copy()

    # ==================== MILESTONES ====================

    def check_for_milestone_achievement(self, review_history: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Check if any new milestones have been achieved.

        Args:
            review_history: Optional review history. If None, loads from file.

        Returns:
            List of newly achieved milestones with details
        """
        if review_history is None:
            review_history = self._load_review_history()

        new_milestones = []

        # Check cards studied milestones
        total_cards_studied = sum(r.get('cards_studied', 0) for r in review_history)
        for milestone_config in self.MILESTONES_CONFIG['cards_studied']:
            if self._is_milestone_new(
                'cards_studied',
                str(milestone_config['threshold']),
                total_cards_studied >= milestone_config['threshold']
            ):
                new_milestones.append({
                    'type': 'cards_studied',
                    'name': milestone_config['name'],
                    'icon': milestone_config['icon'],
                    'threshold': milestone_config['threshold'],
                    'achieved_date': datetime.now().isoformat(),
                    'celebrated': False
                })

        # Check objectives mastered milestones
        objectives_with_cards = {}
        for review in review_history:
            for objective in review.get('objectives', []):
                if objective != 'All':
                    objectives_with_cards[objective] = objectives_with_cards.get(objective, 0) + review.get('cards_studied', 0)

        for milestone_config in self.MILESTONES_CONFIG['objectives_mastered']:
            objective = milestone_config.get('objective')
            if objective == 'all':
                # All objectives mastered if all 3 have been studied
                if len(objectives_with_cards) >= 3:
                    if self._is_milestone_new('all_objectives_mastered', 'achieved', True):
                        new_milestones.append({
                            'type': 'objectives_mastered',
                            'name': milestone_config['name'],
                            'icon': milestone_config['icon'],
                            'objective': 'all',
                            'achieved_date': datetime.now().isoformat(),
                            'celebrated': False
                        })
            else:
                # Individual objective mastered if 30+ cards studied
                if objectives_with_cards.get(objective, 0) >= 30:
                    if self._is_milestone_new('objective_mastered', objective, True):
                        new_milestones.append({
                            'type': 'objectives_mastered',
                            'name': milestone_config['name'],
                            'icon': milestone_config['icon'],
                            'objective': objective,
                            'achieved_date': datetime.now().isoformat(),
                            'celebrated': False
                        })

        # Check study streak milestones
        current_streak = self.goals_data['study_streak']['current_days']
        for milestone_config in self.MILESTONES_CONFIG['study_streak']:
            days = milestone_config['days']
            if current_streak >= days:
                if self._is_milestone_new('study_streak', str(days), True):
                    new_milestones.append({
                        'type': 'study_streak',
                        'name': milestone_config['name'],
                        'icon': milestone_config['icon'],
                        'days': days,
                        'achieved_date': datetime.now().isoformat(),
                        'celebrated': False
                    })

        # Add new milestones to history and save
        for milestone in new_milestones:
            self.goals_data['milestones_achieved'].append(milestone)

        if new_milestones:
            self._save_goals()

        return new_milestones

    def _is_milestone_new(self, milestone_type: str, identifier: str, condition_met: bool) -> bool:
        """
        Check if a milestone is newly achieved (not already recorded).

        Args:
            milestone_type: Type of milestone ('cards_studied', 'objective_mastered', etc.)
            identifier: Specific identifier (threshold, objective ID, etc.)
            condition_met: Whether condition for milestone is currently true

        Returns:
            bool: True if this is a new achievement
        """
        if not condition_met:
            return False

        for achieved in self.goals_data['milestones_achieved']:
            if achieved.get('type') == milestone_type and str(achieved.get('threshold') or achieved.get('objective') or achieved.get('days')) == identifier:
                return False  # Already achieved

        return True

    def mark_milestone_celebrated(self, milestone_index: int) -> None:
        """Mark a milestone as celebrated (notification shown)."""
        if 0 <= milestone_index < len(self.goals_data['milestones_achieved']):
            self.goals_data['milestones_achieved'][milestone_index]['celebrated'] = True
            self._save_goals()

    def get_recent_milestones(self, count: int = 5) -> List[Dict]:
        """Get most recent achieved milestones."""
        return sorted(
            self.goals_data['milestones_achieved'],
            key=lambda x: x.get('achieved_date', ''),
            reverse=True
        )[:count]

    def get_all_milestones(self) -> List[Dict]:
        """Get all achieved milestones."""
        return sorted(
            self.goals_data['milestones_achieved'],
            key=lambda x: x.get('achieved_date', ''),
            reverse=True
        )

    # ==================== PROGRESS SUMMARY ====================

    def get_progress_summary(self) -> Dict:
        """
        Get comprehensive progress summary for dashboard display.

        Returns:
            Dict with all key progress metrics
        """
        review_history = self._load_review_history()

        total_cards = sum(r.get('cards_studied', 0) for r in review_history)
        readiness = self.calculate_readiness_percentage(review_history)
        days_until = self.get_days_until_exam()
        streak = self.goals_data['study_streak']

        objectives_studied = set()
        for review in review_history:
            objectives_studied.update(review.get('objectives', []))

        total_study_time = sum(r.get('study_duration_minutes', 0) for r in review_history)

        return {
            'exam_target_date': self.goals_data.get('exam_target_date'),
            'days_until_exam': days_until,
            'readiness_percentage': round(readiness, 1),
            'total_cards_studied': total_cards,
            'objectives_studied': sorted(list(objectives_studied)),
            'objectives_count': len([o for o in objectives_studied if o != 'All']),
            'daily_recommendation': self.get_daily_recommendation(),
            'study_streak_current': streak['current_days'],
            'study_streak_longest': streak['longest_streak'],
            'total_study_time_minutes': total_study_time,
            'sessions_completed': len(review_history),
            'recent_milestones': self.get_recent_milestones(5),
            'target_readiness': self.goals_data.get('target_readiness_percentage', 90),
        }

    def reset_goals(self) -> None:
        """Reset all goals to defaults."""
        self.goals_data = self._get_default_goals()
        self._save_goals()
