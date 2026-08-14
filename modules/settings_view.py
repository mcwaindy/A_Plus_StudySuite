import customtkinter as ctk
import json
from pathlib import Path
from utils.goals_manager import GoalsManager
from utils.spaced_repetition_manager import SpacedRepetitionManager


class SettingsView(ctk.CTkFrame):
    """Settings and data management view with reset options."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Inner scrollable frame for settings content
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_reset_section()
        self.create_data_section()

    def create_header(self):
        """Create header section."""
        header_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

    def create_reset_section(self):
        """Create reset options section."""
        section_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Data Management",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="orange"
        )
        section_label.grid(row=1, column=0, sticky="w", pady=(10, 10))

        # Reset all statistics button
        btn_reset_all = ctk.CTkButton(
            self.scrollable_frame,
            text="🔄 Reset All Statistics",
            command=self.confirm_reset_all,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            text_color="white"
        )
        btn_reset_all.grid(row=2, column=0, sticky="ew", pady=5)

        reset_all_desc = ctk.CTkLabel(
            self.scrollable_frame,
            text="Clear all card metrics, review history, and reset goals to defaults.",
            text_color="gray",
            wraplength=500,
            justify="left"
        )
        reset_all_desc.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 15))

        # Reset card metrics only
        btn_reset_cards = ctk.CTkButton(
            self.scrollable_frame,
            text="🔄 Reset Card Metrics Only",
            command=self.confirm_reset_cards,
            fg_color="#f57c00",
            hover_color="#e65100",
            text_color="white"
        )
        btn_reset_cards.grid(row=4, column=0, sticky="ew", pady=5)

        reset_cards_desc = ctk.CTkLabel(
            self.scrollable_frame,
            text="Reset spaced repetition data (intervals, ease factors, etc.) but keep goals and history.",
            text_color="gray",
            wraplength=500,
            justify="left"
        )
        reset_cards_desc.grid(row=5, column=0, sticky="w", padx=10, pady=(0, 15))

        # Reset review history only
        btn_reset_history = ctk.CTkButton(
            self.scrollable_frame,
            text="🔄 Reset Review History",
            command=self.confirm_reset_history,
            fg_color="#f57c00",
            hover_color="#e65100",
            text_color="white"
        )
        btn_reset_history.grid(row=6, column=0, sticky="ew", pady=5)

        reset_history_desc = ctk.CTkLabel(
            self.scrollable_frame,
            text="Clear all study session history and progress statistics.",
            text_color="gray",
            wraplength=500,
            justify="left"
        )
        reset_history_desc.grid(row=7, column=0, sticky="w", padx=10, pady=(0, 15))

        # Reset goals only
        btn_reset_goals = ctk.CTkButton(
            self.scrollable_frame,
            text="🔄 Reset Goals",
            command=self.confirm_reset_goals,
            fg_color="#f57c00",
            hover_color="#e65100",
            text_color="white"
        )
        btn_reset_goals.grid(row=8, column=0, sticky="ew", pady=5)

        reset_goals_desc = ctk.CTkLabel(
            self.scrollable_frame,
            text="Reset all goals, milestones, and streaks to defaults.",
            text_color="gray",
            wraplength=500,
            justify="left"
        )
        reset_goals_desc.grid(row=9, column=0, sticky="w", padx=10, pady=(0, 15))

    def create_data_section(self):
        """Create data info section."""
        section_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Data Files",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="cyan"
        )
        section_label.grid(row=10, column=0, sticky="w", pady=(20, 10))

        data_dir = Path("data")
        files_info = []
        if data_dir.exists():
            for json_file in sorted(data_dir.glob("*.json")):
                size = json_file.stat().st_size
                size_kb = size / 1024
                files_info.append(f"  • {json_file.name}: {size_kb:.1f} KB")

        if files_info:
            info_text = "\n".join(files_info)
        else:
            info_text = "  • No data files found yet"

        info_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=info_text,
            text_color="gray",
            justify="left",
            wraplength=500
        )
        info_label.grid(row=11, column=0, sticky="w", padx=10, pady=(0, 20))

    def confirm_reset_all(self):
        """Show confirmation dialog for reset all."""
        dialog = ConfirmDialog(
            self,
            title="Reset All Statistics?",
            message="This will clear ALL data:\n• Card metrics\n• Review history\n• Goals & milestones\n\nThis action cannot be undone. Continue?",
            confirm_text="Reset All",
            confirm_color="#d32f2f"
        )
        if dialog.get_input():
            self.reset_all_statistics()

    def confirm_reset_cards(self):
        """Show confirmation dialog for reset card metrics."""
        dialog = ConfirmDialog(
            self,
            title="Reset Card Metrics?",
            message="This will reset spaced repetition data:\n• Intervals & ease factors\n• Next review dates\n• Learning stages\n\nReview history will be preserved.",
            confirm_text="Reset Cards",
            confirm_color="#f57c00"
        )
        if dialog.get_input():
            self.reset_card_metrics()

    def confirm_reset_history(self):
        """Show confirmation dialog for reset review history."""
        dialog = ConfirmDialog(
            self,
            title="Reset Review History?",
            message="This will clear:\n• All study sessions\n• Progress statistics\n• Study streaks\n\nCard metrics will be preserved.",
            confirm_text="Reset History",
            confirm_color="#f57c00"
        )
        if dialog.get_input():
            self.reset_review_history()

    def confirm_reset_goals(self):
        """Show confirmation dialog for reset goals."""
        dialog = ConfirmDialog(
            self,
            title="Reset Goals?",
            message="This will reset:\n• Exam target date\n• Readiness target\n• Milestones achieved\n• Daily goals\n• Study streak\n\nData will be set to defaults.",
            confirm_text="Reset Goals",
            confirm_color="#f57c00"
        )
        if dialog.get_input():
            self.reset_goals()

    def reset_all_statistics(self):
        """Reset all data files."""
        self.reset_card_metrics()
        self.reset_review_history()
        self.reset_goals()
        self.show_message("✓ All statistics reset successfully!")

    def reset_card_metrics(self):
        """Reset card metrics file."""
        try:
            sr_manager = SpacedRepetitionManager()
            sr_manager.reset_card_metrics()
            self.show_message("✓ Card metrics reset!")
        except Exception as e:
            self.show_message(f"✗ Error resetting cards: {str(e)}", error=True)

    def reset_review_history(self):
        """Reset review history file."""
        try:
            history_file = Path("data/review_history.json")
            if history_file.exists():
                history_file.write_text(json.dumps([], indent=2))
            self.show_message("✓ Review history cleared!")
        except Exception as e:
            self.show_message(f"✗ Error clearing history: {str(e)}", error=True)

    def reset_goals(self):
        """Reset goals file."""
        try:
            goals_manager = GoalsManager()
            goals_manager.reset_goals()
            self.show_message("✓ Goals reset to defaults!")
        except Exception as e:
            self.show_message(f"✗ Error resetting goals: {str(e)}", error=True)

    def show_message(self, message, error=False):
        """Show a temporary message to the user."""
        # Create a simple message label that appears and disappears
        msg_color = "#d32f2f" if error else "#4caf50"
        msg_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=message,
            text_color=msg_color,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        msg_label.grid(row=100, column=0, sticky="ew", pady=20)

        # Auto-remove after 3 seconds
        def remove_message():
            try:
                msg_label.grid_forget()
            except:
                pass

        self.after(3000, remove_message)


class ConfirmDialog(ctk.CTkToplevel):
    """Simple confirmation dialog."""

    def __init__(self, parent, title, message, confirm_text="Confirm", confirm_color="#1f6aa5"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        self.result = False

        # Message label
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            wraplength=350,
            justify="left",
            text_color="gray85"
        )
        msg_label.pack(padx=20, pady=20)

        # Button frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.cancel,
            fg_color="#444444",
            hover_color="#555555"
        )
        btn_cancel.pack(side="left", padx=5)

        btn_confirm = ctk.CTkButton(
            btn_frame,
            text=confirm_text,
            command=self.confirm,
            fg_color=confirm_color,
            hover_color=confirm_color,
            text_color="white"
        )
        btn_confirm.pack(side="right", padx=5)

    def confirm(self):
        """Confirm action."""
        self.result = True
        self.destroy()

    def cancel(self):
        """Cancel action."""
        self.result = False
        self.destroy()

    def get_input(self):
        """Wait for dialog result."""
        self.wait_window()
        return self.result
