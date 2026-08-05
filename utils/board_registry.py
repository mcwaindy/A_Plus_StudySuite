"""
Board Registry - Centralized management of all motherboard definitions.

Loads board data from JSON files and provides a unified interface for
diagram_view, game_view, and other components to access board configurations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class BoardRegistry:
    """Manages all motherboard and IO cluster definitions."""

    def __init__(self, board_file: str | Path = "data/motherboard/motherboard_nodes.json"):
        """
        Initialize the board registry.

        Args:
            board_file: Path to the JSON file containing all board definitions
        """
        self.board_file = Path(board_file)
        self.boards: Dict[str, Dict[str, Any]] = {}
        self._load_boards()

    def _load_boards(self) -> None:
        """Load all board definitions from JSON file."""
        if not self.board_file.exists():
            print(f"⚠️  Board file not found: {self.board_file}")
            self.boards = {}
            return

        try:
            with open(self.board_file, "r", encoding="utf-8") as f:
                self.boards = json.load(f)
            print(f"✅ Loaded {len(self.boards)} boards from {self.board_file}")
        except Exception as e:
            print(f"❌ Error loading boards: {e}")
            self.boards = {}

    def get_board(self, board_key: str) -> Optional[Dict[str, Any]]:
        """
        Get a board definition by key.

        Args:
            board_key: The board identifier (e.g., 'micro_atx')

        Returns:
            Board configuration dict or None if not found
        """
        return self.boards.get(board_key)

    def get_all_boards(self) -> Dict[str, Dict[str, Any]]:
        """Get all loaded boards."""
        return self.boards.copy()

    def get_board_keys(self) -> List[str]:
        """Get list of all board keys."""
        return list(self.boards.keys())

    def get_board_display_name(self, board_key: str) -> str:
        """Get the display name for a board."""
        board = self.get_board(board_key)
        if board:
            return board.get("title", board_key)
        return board_key

    def get_components(self, board_key: str) -> List[Dict[str, Any]]:
        """
        Get all components for a specific board.

        Args:
            board_key: The board identifier

        Returns:
            List of component configurations
        """
        board = self.get_board(board_key)
        if board:
            return board.get("components", [])
        return []

    def get_component(self, board_key: str, component_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific component from a board.

        Args:
            board_key: The board identifier
            component_id: The component ID

        Returns:
            Component configuration or None if not found
        """
        components = self.get_components(board_key)
        for comp in components:
            if comp.get("id") == component_id:
                return comp
        return None

    def save_boards(self, boards: Dict[str, Dict[str, Any]] | None = None) -> bool:
        """
        Save board definitions to JSON file.

        Args:
            boards: Board definitions to save. If None, uses current self.boards

        Returns:
            True if successful, False otherwise
        """
        try:
            data_to_save = boards if boards is not None else self.boards
            self.board_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.board_file, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=2)

            print(f"✅ Saved board data to {self.board_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving boards: {e}")
            return False

    def update_board(self, board_key: str, board_data: Dict[str, Any]) -> bool:
        """
        Update a board definition and save.

        Args:
            board_key: The board identifier
            board_data: Updated board configuration

        Returns:
            True if successful
        """
        self.boards[board_key] = board_data
        return self.save_boards()

    def update_components(self, board_key: str, components: List[Dict[str, Any]]) -> bool:
        """
        Update components for a board and save.

        Args:
            board_key: The board identifier
            components: List of component configurations

        Returns:
            True if successful
        """
        if board_key in self.boards:
            self.boards[board_key]["components"] = components
            return self.save_boards()
        return False

    def reload(self) -> None:
        """Reload board data from disk."""
        self._load_boards()
