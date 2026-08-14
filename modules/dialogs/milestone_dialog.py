"""
Milestone Dialog - Celebration popup when user achieves a milestone.
"""

import customtkinter as ctk


class MilestoneDialog(ctk.CTkToplevel):
    """Dialog for celebrating milestone achievements."""

    def __init__(self, parent, milestone):
        super().__init__(parent)
        self.milestone = milestone
        self.title("🎉 Milestone Achieved!")
        self.geometry("400x300")

        # Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Make it modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        # Create content
        self.create_content()

    def create_content(self):
        """Create dialog content."""
        # Icon/Title
        icon_frame = ctk.CTkFrame(self, fg_color="transparent")
        icon_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        icon_label = ctk.CTkLabel(
            icon_frame,
            text=self.milestone.get('icon', '🎯'),
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack()

        # Milestone name
        name_label = ctk.CTkLabel(
            self,
            text=self.milestone.get('name', 'Achievement Unlocked!'),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#FFD700", "#FFD700")  # Gold color
        )
        name_label.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        # Description based on milestone type
        description = self._get_description()
        desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=ctk.CTkFont(size=12),
            wraplength=350
        )
        desc_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))

        # Celebration button
        celebrate_btn = ctk.CTkButton(
            self,
            text="🎉 Celebrate!",
            command=self.destroy,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        celebrate_btn.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))

    def _get_description(self):
        """Get description text based on milestone type."""
        milestone_type = self.milestone.get('type', '')

        if milestone_type == 'cards_studied':
            threshold = self.milestone.get('threshold', 0)
            return f"You've studied {threshold} cards! Keep up the momentum! 💪"

        elif milestone_type == 'objectives_mastered':
            objective = self.milestone.get('objective', '')
            if objective == 'all':
                return "You've mastered all objectives! You're exam-ready! 🏆"
            else:
                return f"You've mastered Objective {objective}! Great work! 🎯"

        elif milestone_type == 'study_streak':
            days = self.milestone.get('days', 0)
            return f"You've studied {days} days in a row! Amazing dedication! 🔥"

        else:
            return "You've achieved a milestone! Congratulations! 🌟"
