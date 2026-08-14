"""
Session Manager - Handles auto-save and recovery of interrupted sessions.

Supports:
- Flashcard session state persistence
- Exam session recovery
- Auto-save during active study
- Session recovery on app startup
- Clean session management (clear after resume, data expiration)
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class SessionManager:
    """Manages session auto-save and recovery functionality."""

    SESSION_FILE = Path("data/session_state.json")
    SESSION_TIMEOUT_DAYS = 7  # Auto-clear sessions older than 7 days

    def __init__(self):
        """Initialize the session manager."""
        self.current_session = None
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        Path("data").mkdir(exist_ok=True)

    def save_flashcard_session(self, session_data: Dict[str, Any]) -> bool:
        """
        Save current flashcard session state to disk.

        Args:
            session_data: Dictionary containing:
                - selected_exam: str
                - selected_objectives: list
                - card_limit: int or None
                - study_mode: str ("standard" or "smart")
                - current_index: int
                - cards_studied: list
                - reviewed_cards: list
                - score_known: int
                - score_review: int
                - is_flipped: bool
                - timestamp: str (ISO format)

        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            state = {
                "session_type": "flashcard",
                "timestamp": datetime.now().isoformat(),
                "data": session_data
            }

            with open(self.SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error saving session: {e}")
            return False

    def save_exam_session(self, session_data: Dict[str, Any]) -> bool:
        """
        Save current exam session state to disk.

        Args:
            session_data: Dictionary containing exam state details

        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            state = {
                "session_type": "exam",
                "timestamp": datetime.now().isoformat(),
                "data": session_data
            }

            with open(self.SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error saving exam session: {e}")
            return False

    def load_session(self) -> Optional[Dict[str, Any]]:
        """
        Load the most recent session state from disk.

        Returns:
            dict: Session state if valid and not expired, None otherwise
        """
        if not self.SESSION_FILE.exists():
            return None

        try:
            with open(self.SESSION_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)

            # Check if session has expired
            if self._is_session_expired(state.get("timestamp")):
                self.clear_session()
                return None

            self.current_session = state
            return state
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading session: {e}")
            return None

    def _is_session_expired(self, timestamp_str: str) -> bool:
        """
        Check if session is older than SESSION_TIMEOUT_DAYS.

        Args:
            timestamp_str: ISO format timestamp string

        Returns:
            bool: True if session is expired, False otherwise
        """
        try:
            saved_time = datetime.fromisoformat(timestamp_str)
            age = datetime.now() - saved_time
            return age.days >= self.SESSION_TIMEOUT_DAYS
        except (ValueError, TypeError):
            return True

    def clear_session(self) -> bool:
        """
        Clear the saved session state.

        Returns:
            bool: True if cleared successfully, False otherwise
        """
        try:
            if self.SESSION_FILE.exists():
                self.SESSION_FILE.unlink()
            self.current_session = None
            return True
        except OSError as e:
            print(f"Error clearing session: {e}")
            return False

    def has_session(self) -> bool:
        """
        Check if there's a valid saved session available.

        Returns:
            bool: True if valid session exists, False otherwise
        """
        return self.load_session() is not None

    def get_session_info(self) -> Optional[Dict[str, str]]:
        """
        Get human-readable info about the saved session.

        Returns:
            dict with 'type' and 'time' keys, or None if no session
        """
        session = self.load_session()
        if not session:
            return None

        try:
            saved_time = datetime.fromisoformat(session.get("timestamp", ""))
            time_ago = datetime.now() - saved_time

            if time_ago.total_seconds() < 60:
                time_str = "moments ago"
            elif time_ago.total_seconds() < 3600:
                minutes = int(time_ago.total_seconds() / 60)
                time_str = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            elif time_ago.total_seconds() < 86400:
                hours = int(time_ago.total_seconds() / 3600)
                time_str = f"{hours} hour{'s' if hours > 1 else ''} ago"
            else:
                days = time_ago.days
                time_str = f"{days} day{'s' if days > 1 else ''} ago"

            return {
                "type": session.get("session_type", "unknown"),
                "time": time_str,
                "timestamp": session.get("timestamp", "")
            }
        except (ValueError, KeyError):
            return None
