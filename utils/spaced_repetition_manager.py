"""
SpacedRepetitionManager - Implements SM-2 Spaced Repetition Algorithm

Intelligently schedules card reviews based on:
- Difficulty (how often marked "needs review")
- Performance history
- Time since last review
- Scientifically proven intervals

Using adapted SM-2 algorithm (SuperMemo 2) - proven to improve retention by 25%+
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import math


class SpacedRepetitionManager:
    """Manages spaced repetition scheduling and metrics for flashcards."""

    # SM-2 Algorithm Constants
    MIN_EASINESS = 1.3  # Minimum difficulty factor
    MAX_EASINESS = 2.5  # Maximum difficulty factor
    DEFAULT_EASINESS = 2.0  # Default starting factor

    # Interval progression (days)
    FIRST_INTERVAL = 1  # After first correct: 1 day
    SECOND_INTERVAL = 3  # After second correct: 3 days

    def __init__(self, flashcards_data: List[Dict] = None):
        """
        Initialize SR Manager.

        Args:
            flashcards_data: List of all flashcards from flashcards.json
        """
        self.metrics_path = Path("data/card_metrics.json")
        self.flashcards_data = flashcards_data or []
        self.card_metrics = self._load_or_create_metrics()

    def _load_or_create_metrics(self) -> Dict:
        """Load metrics from file or create defaults for all cards."""
        if self.metrics_path.exists():
            try:
                with open(self.metrics_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_default_metrics()

        return self._create_default_metrics()

    def _create_default_metrics(self) -> Dict:
        """Create default metrics for all flashcards."""
        metrics = {}
        today = datetime.now().date().isoformat()

        for card in self.flashcards_data:
            card_id = card.get("id", "unknown")
            metrics[card_id] = {
                "easiness_factor": self.DEFAULT_EASINESS,
                "interval": 0,  # Days until next review
                "repetitions": 0,  # Number of successful repetitions
                "next_review_date": today,  # When to review next
                "difficulty_score": 0.0,  # % of times marked "needs review"
                "last_review_date": None,  # When last reviewed
                "first_seen_date": today,  # When first encountered
                "total_reviews": 0,  # Total times reviewed
                "correct_reviews": 0,  # Times marked "know it"
                "incorrect_reviews": 0,  # Times marked "needs review"
                "learning_stage": "new"  # new, learning, review, mastered
            }

        self._save_metrics(metrics)
        return metrics

    def _save_metrics(self, metrics: Dict = None) -> None:
        """Save metrics to file."""
        if metrics is None:
            metrics = self.card_metrics

        try:
            with open(self.metrics_path, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2)
        except IOError as e:
            print(f"Error saving card metrics: {e}")

    def get_study_cards(
        self, 
        cards: List[Dict], 
        max_cards: int = None,
        objectives_filter: List[str] = None
    ) -> List[Dict]:
        """
        Get cards prioritized for study using SR algorithm.

        Args:
            cards: List of cards to prioritize
            max_cards: Maximum cards to return (None = all)
            objectives_filter: Filter by objectives

        Returns:
            List of cards sorted by priority (most urgent first)
        """
        today = datetime.now().date()

        # Score each card
        scored_cards = []
        for card in cards:
            card_id = card.get("id")
            if not card_id or card_id not in self.card_metrics:
                continue

            # Filter by objectives if provided
            if objectives_filter and "All" not in objectives_filter:
                if card.get("objective") not in objectives_filter:
                    continue

            metrics = self.card_metrics[card_id]
            score = self._calculate_priority_score(metrics, today)

            scored_cards.append({
                "card": card,
                "score": score,
                "metrics": metrics,
                "days_overdue": self._days_overdue(metrics, today),
                "status": self._get_card_status(metrics, today)
            })

        # Sort by priority score (highest first = most urgent)
        scored_cards.sort(key=lambda x: x["score"], reverse=True)

        # Limit if requested
        if max_cards:
            scored_cards = scored_cards[:max_cards]

        return scored_cards

    def _calculate_priority_score(self, metrics: Dict, today) -> float:
        """
        Calculate priority score for a card.
        Higher score = more urgent to study.

        Formula considers:
        - Days overdue (highest priority)
        - Difficulty (harder cards more urgent)
        - Interval (shorter intervals = more urgent)
        """
        try:
            next_review = datetime.fromisoformat(metrics["next_review_date"]).date()
        except (ValueError, TypeError):
            return 100.0  # Default high priority if date invalid

        days_overdue = max(0, (today - next_review).days)
        difficulty = metrics["difficulty_score"]
        interval = max(1, metrics["interval"])

        # Scoring formula (weighted)
        score = (
            days_overdue * 10.0 +  # Overdue cards are highest priority
            difficulty * 2.0 +      # Harder cards are secondary priority
            (1.0 / interval) * 5.0  # Shorter intervals are moderately urgent
        )

        return score

    def _days_overdue(self, metrics: Dict, today) -> int:
        """Calculate how many days overdue a card is."""
        try:
            next_review = datetime.fromisoformat(metrics["next_review_date"]).date()
            return max(0, (today - next_review).days)
        except (ValueError, TypeError):
            return 0

    def _get_card_status(self, metrics: Dict, today) -> str:
        """
        Determine card status for UI display.

        Returns: "overdue", "due_soon", "current", "new", or "mastered"
        """
        if metrics["learning_stage"] == "mastered":
            return "mastered"

        if metrics["repetitions"] == 0:
            return "new"

        try:
            next_review = datetime.fromisoformat(metrics["next_review_date"]).date()
        except (ValueError, TypeError):
            return "new"

        days_until = (next_review - today).days

        if days_until < 0:
            return "overdue"
        elif days_until <= 2:
            return "due_soon"
        else:
            return "current"

    def record_review(
        self,
        card_id: str,
        was_correct: bool,
        session_timestamp: str = None
    ) -> None:
        """
        Record a card review and update metrics using SM-2 algorithm.

        Args:
            card_id: ID of card reviewed
            was_correct: True if marked "Know It", False if "Needs Review"
            session_timestamp: ISO format timestamp of review
        """
        if card_id not in self.card_metrics:
            return

        metrics = self.card_metrics[card_id]
        today = datetime.now().date()

        # Update basic stats
        metrics["total_reviews"] += 1
        metrics["last_review_date"] = today.isoformat()

        if was_correct:
            metrics["correct_reviews"] += 1
            quality = 5  # SM-2 quality grade (0-5)
        else:
            metrics["incorrect_reviews"] += 1
            quality = 0  # Wrong answer

        # Update difficulty score (% of times marked incorrect)
        if metrics["total_reviews"] > 0:
            metrics["difficulty_score"] = (
                metrics["incorrect_reviews"] / metrics["total_reviews"] * 100
            )

        # SM-2 Algorithm Update
        if was_correct:
            metrics["repetitions"] += 1

            # Calculate new easiness factor
            old_ef = metrics["easiness_factor"]
            new_ef = old_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            metrics["easiness_factor"] = max(
                self.MIN_EASINESS,
                min(self.MAX_EASINESS, new_ef)
            )

            # Calculate new interval
            if metrics["repetitions"] == 1:
                interval = self.FIRST_INTERVAL
            elif metrics["repetitions"] == 2:
                interval = self.SECOND_INTERVAL
            else:
                interval = math.ceil(metrics["interval"] * metrics["easiness_factor"])

            # Cap interval at 30 days (beyond that, diminishing returns)
            metrics["interval"] = min(30, interval)
        else:
            # Reset on incorrect answer
            metrics["repetitions"] = 0
            metrics["interval"] = 1
            metrics["easiness_factor"] = max(
                self.MIN_EASINESS,
                metrics["easiness_factor"] - 0.2  # Penalty for wrong answer
            )

        # Calculate next review date
        next_review = today + timedelta(days=metrics["interval"])
        metrics["next_review_date"] = next_review.isoformat()

        # Update learning stage
        self._update_learning_stage(metrics)

        # Save immediately
        self._save_metrics()

    def _update_learning_stage(self, metrics: Dict) -> None:
        """Update learning stage based on progress."""
        if metrics["total_reviews"] == 0:
            metrics["learning_stage"] = "new"
        elif metrics["repetitions"] < 2:
            metrics["learning_stage"] = "learning"
        elif metrics["interval"] >= 14:
            metrics["learning_stage"] = "mastered"
        else:
            metrics["learning_stage"] = "review"

    def get_learning_statistics(self) -> Dict:
        """Get overall learning statistics."""
        if not self.card_metrics:
            return {
                "total_cards": 0,
                "new_cards": 0,
                "learning_cards": 0,
                "review_cards": 0,
                "mastered_cards": 0,
                "cards_due_today": 0,
                "overdue_cards": 0,
                "average_difficulty": 0,
                "average_easiness": 2.0,
                "estimated_mastery_date": None,
                "learning_efficiency": 0
            }

        today = datetime.now().date()

        stages = {
            "new": 0,
            "learning": 0,
            "review": 0,
            "mastered": 0
        }

        cards_due = 0
        overdue = 0
        total_difficulty = 0
        total_easiness = 0
        count = 0

        for card_id, metrics in self.card_metrics.items():
            stage = metrics.get("learning_stage", "new")
            stages[stage] = stages.get(stage, 0) + 1

            # Count due cards
            try:
                next_review = datetime.fromisoformat(
                    metrics["next_review_date"]
                ).date()
                if next_review <= today:
                    cards_due += 1
                    if next_review < today:
                        overdue += 1
            except (ValueError, TypeError):
                pass

            total_difficulty += metrics.get("difficulty_score", 0)
            total_easiness += metrics.get("easiness_factor", 2.0)
            count += 1

        # Calculate metrics
        total_cards = count
        avg_difficulty = (
            total_difficulty / count if count > 0 else 0
        )
        avg_easiness = (
            total_easiness / count if count > 0 else 2.0
        )

        # Learning efficiency: % of cards mastered
        learning_efficiency = (
            (stages["mastered"] / total_cards * 100)
            if total_cards > 0 else 0
        )

        # Estimate mastery date (simple linear projection - inline to avoid recursion)
        mastery_date = None
        if total_cards > 0 and stages["mastered"] < total_cards:
            mastery_rate = 0.5  # Default: ~0.5 cards mastered per day
            if avg_difficulty > 50:
                mastery_rate = 0.3
            elif avg_difficulty < 25:
                mastery_rate = 0.7

            remaining = total_cards - stages["mastered"]
            days_needed = int(remaining / mastery_rate)
            estimated_date = today + timedelta(days=days_needed)
            mastery_date = estimated_date.isoformat()
        elif total_cards > 0:
            mastery_date = today.isoformat()

        return {
            "total_cards": total_cards,
            "new_cards": stages["new"],
            "learning_cards": stages["learning"],
            "review_cards": stages["review"],
            "mastered_cards": stages["mastered"],
            "cards_due_today": cards_due,
            "overdue_cards": overdue,
            "average_difficulty": round(avg_difficulty, 1),
            "average_easiness": round(avg_easiness, 2),
            "estimated_mastery_date": mastery_date,
            "learning_efficiency": round(learning_efficiency, 1)
        }

    def _estimate_mastery_date(self) -> Optional[str]:
        """Estimate when user will master all cards (deprecated - inlined to avoid recursion)."""
        return None

    def get_card_stats(self, card_id: str) -> Dict:
        """Get statistics for a specific card."""
        if card_id not in self.card_metrics:
            return {}

        metrics = self.card_metrics[card_id]
        today = datetime.now().date()

        return {
            "learning_stage": metrics.get("learning_stage", "new"),
            "total_reviews": metrics.get("total_reviews", 0),
            "correct_reviews": metrics.get("correct_reviews", 0),
            "incorrect_reviews": metrics.get("incorrect_reviews", 0),
            "difficulty_score": round(metrics.get("difficulty_score", 0), 1),
            "easiness_factor": round(metrics.get("easiness_factor", 2.0), 2),
            "interval_days": metrics.get("interval", 0),
            "days_overdue": self._days_overdue(metrics, today),
            "last_review_date": metrics.get("last_review_date"),
            "next_review_date": metrics.get("next_review_date"),
            "status": self._get_card_status(metrics, today)
        }

    def reset_card_metrics(self, card_id: str = None) -> None:
        """Reset metrics for a card or all cards."""
        today = datetime.now().date().isoformat()

        if card_id:
            # Reset single card
            if card_id in self.card_metrics:
                self.card_metrics[card_id] = {
                    "easiness_factor": self.DEFAULT_EASINESS,
                    "interval": 0,
                    "repetitions": 0,
                    "next_review_date": today,
                    "difficulty_score": 0.0,
                    "last_review_date": None,
                    "first_seen_date": today,
                    "total_reviews": 0,
                    "correct_reviews": 0,
                    "incorrect_reviews": 0,
                    "learning_stage": "new"
                }
        else:
            # Reset all cards
            self.card_metrics = self._create_default_metrics()

        self._save_metrics()

    def get_weak_objectives(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Get objectives sorted by difficulty (hardest first).

        Args:
            top_n: Number of objectives to return

        Returns:
            List of (objective_name, average_difficulty) tuples
        """
        objective_stats = {}

        for card in self.flashcards_data:
            objective = card.get("objective", "Unknown")
            card_id = card.get("id")

            if card_id not in self.card_metrics:
                continue

            if objective not in objective_stats:
                objective_stats[objective] = {"sum_difficulty": 0, "count": 0}

            metrics = self.card_metrics[card_id]
            objective_stats[objective]["sum_difficulty"] += metrics["difficulty_score"]
            objective_stats[objective]["count"] += 1

        # Calculate averages and sort
        objectives = [
            (
                obj,
                stats["sum_difficulty"] / stats["count"]
            )
            for obj, stats in objective_stats.items()
            if stats["count"] > 0
        ]

        objectives.sort(key=lambda x: x[1], reverse=True)
        return objectives[:top_n]

    def get_summary(self) -> str:
        """Get human-readable summary of learning progress."""
        stats = self.get_learning_statistics()

        summary = f"""
SPACED REPETITION SUMMARY
{'='*50}
Total Cards: {stats['total_cards']}
  New: {stats['new_cards']} | Learning: {stats['learning_cards']} | Review: {stats['review_cards']} | Mastered: {stats['mastered_cards']}

Study Status:
  Due Today: {stats['cards_due_today']}
  Overdue: {stats['overdue_cards']}

Progress:
  Learning Efficiency: {stats['learning_efficiency']}%
  Average Difficulty: {stats['average_difficulty']}%
  Average Easiness: {stats['average_easiness']}

Projection:
  Estimated Mastery: {stats['estimated_mastery_date']}
{'='*50}
        """

        return summary
