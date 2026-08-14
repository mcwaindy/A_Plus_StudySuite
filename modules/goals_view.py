"""
Goals View - Main dashboard for study goals and progress tracking.
Displays exam countdown, readiness progress, daily recommendations,
study streak, recent milestones, and spaced repetition statistics.
"""

import customtkinter as ctk
from utils.goals_manager import GoalsManager
from utils.spaced_repetition_manager import SpacedRepetitionManager
from datetime import datetime
import json
from pathlib import Path


class GoalsView(ctk.CTkFrame):
    """Main goals and progress dashboard."""

    def __init__(self, parent):
        super().__init__(parent)
        self.gm = GoalsManager()

        # Initialize SR manager (if data available)
        self.sr_manager = None
        try:
            flashcards_path = Path("data/flashcards.json")
            if flashcards_path.exists():
                with open(flashcards_path, "r", encoding="utf-8") as f:
                    flashcards = json.load(f)
                self.sr_manager = SpacedRepetitionManager(flashcards)
        except Exception:
            pass

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Scrollable content

        # Create header
        self.create_header()

        # Create scrollable content area
        self.create_scrollable_content()

        # Initial refresh
        self.refresh_display()

    def create_header(self):
        """Create the header section."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="📊 GOALS & PROGRESS",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")

    def create_scrollable_content(self):
        """Create scrollable content area."""
        # Main scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Exam countdown section
        self.create_countdown_section()

        # Readiness section
        self.create_readiness_section()

        # Recommendation section
        self.create_recommendation_section()

        # Streak section
        self.create_streak_section()

        # Milestones section
        self.create_milestones_section()

        # Spaced Repetition statistics section
        self.create_sr_stats_section()

        # Buttons section
        self.create_buttons_section()

    def create_countdown_section(self):
        """Create exam countdown display."""
        section = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        section.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        section.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            section,
            text="📅 EXAM TARGET",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

        self.countdown_label = ctk.CTkLabel(
            section,
            text="No exam date set",
            font=ctk.CTkFont(size=12)
        )
        self.countdown_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 15))

    def create_readiness_section(self):
        """Create readiness progress bar section."""
        section = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        section.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        section.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            section,
            text="📊 EXAM READINESS",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(section, height=25)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 5))
        self.progress_bar.set(0)

        # Percentage label
        self.readiness_label = ctk.CTkLabel(
            section,
            text="0% Ready • Target: 90%",
            font=ctk.CTkFont(size=11)
        )
        self.readiness_label.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 15))

    def create_recommendation_section(self):
        """Create daily recommendation section."""
        section = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        section.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        section.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            section,
            text="💡 DAILY RECOMMENDATION",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

        self.recommendation_label = ctk.CTkLabel(
            section,
            text="Set a target exam date to get personalized recommendations",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
            wraplength=500
        )
        self.recommendation_label.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))

    def create_streak_section(self):
        """Create study streak section."""
        section = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        section.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        section.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            section,
            text="🔥 STUDY STREAK",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

        # Current streak
        self.current_streak_label = ctk.CTkLabel(
            section,
            text="Current: 0 days",
            font=ctk.CTkFont(size=11)
        )
        self.current_streak_label.grid(row=1, column=0, sticky="w", padx=15, pady=2)

        # Best streak
        self.best_streak_label = ctk.CTkLabel(
            section,
            text="Best: 0 days",
            font=ctk.CTkFont(size=11)
        )
        self.best_streak_label.grid(row=2, column=0, sticky="w", padx=15, pady=2)

        # Cards studied
        self.cards_studied_label = ctk.CTkLabel(
            section,
            text="Total cards studied: 0",
            font=ctk.CTkFont(size=11)
        )
        self.cards_studied_label.grid(row=3, column=0, sticky="w", padx=15, pady=(2, 15))

    def create_milestones_section(self):
        """Create recent milestones section."""
        section = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        section.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        section.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            section,
            text="🎉 RECENT MILESTONES",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

        # Milestones container
        self.milestones_container = ctk.CTkFrame(section, fg_color="transparent")
        self.milestones_container.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.milestones_container.grid_columnconfigure(0, weight=1)

        self.no_milestones_label = ctk.CTkLabel(
            self.milestones_container,
            text="No milestones achieved yet. Keep studying!",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50")
        )
        self.no_milestones_label.grid(row=0, column=0, sticky="ew")

    def create_sr_stats_section(self):
        """Create spaced repetition statistics section."""
        section = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        section.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        section.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            section,
            text="🧠 SMART STUDY STATS",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

        # Container for SR stats
        self.sr_stats_container = ctk.CTkFrame(section, fg_color="transparent")
        self.sr_stats_container.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.sr_stats_container.grid_columnconfigure((0, 1), weight=1)

    def update_sr_stats_display(self):
        """Update spaced repetition statistics."""
        if not self.sr_manager:
            return

        # Clear existing stats
        for widget in self.sr_stats_container.winfo_children():
            widget.destroy()

        try:
            stats = self.sr_manager.get_learning_statistics()

            # Due today
            due_today = ctk.CTkLabel(
                self.sr_stats_container,
                text=f"📋 Due Today: {stats['cards_due_today']}",
                font=ctk.CTkFont(size=11),
                text_color=("gray10", "gray90")
            )
            due_today.grid(row=0, column=0, sticky="w", pady=2)

            # Overdue cards
            overdue = ctk.CTkLabel(
                self.sr_stats_container,
                text=f"🔴 Overdue: {stats['overdue_cards']}",
                font=ctk.CTkFont(size=11),
                text_color=("gray10", "gray90")
            )
            overdue.grid(row=0, column=1, sticky="w", pady=2)

            # Learning efficiency
            efficiency = ctk.CTkLabel(
                self.sr_stats_container,
                text=f"📈 Efficiency: {stats['learning_efficiency']}%",
                font=ctk.CTkFont(size=11),
                text_color=("gray10", "gray90")
            )
            efficiency.grid(row=1, column=0, sticky="w", pady=2)

            # Mastery estimate
            mastery_date = stats.get('estimated_mastery_date', 'N/A')
            mastery = ctk.CTkLabel(
                self.sr_stats_container,
                text=f"✅ Mastery by: {mastery_date}",
                font=ctk.CTkFont(size=11),
                text_color=("gray10", "gray90")
            )
            mastery.grid(row=1, column=1, sticky="w", pady=2)

        except Exception:
            # If SR data not available, show placeholder
            placeholder = ctk.CTkLabel(
                self.sr_stats_container,
                text="Start Smart Study sessions to see stats",
                font=ctk.CTkFont(size=11),
                text_color=("gray50", "gray50")
            )
            placeholder.grid(row=0, column=0, columnspan=2, sticky="w", pady=2)

    def create_buttons_section(self):
        """Create action buttons."""
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        button_frame.grid(row=6, column=0, sticky="ew", pady=(10, 0))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Set Goal button
        set_goal_btn = ctk.CTkButton(
            button_frame,
            text="📝 Set Goal",
            command=self.open_goal_dialog
        )
        set_goal_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # View All Milestones button
        all_milestones_btn = ctk.CTkButton(
            button_frame,
            text="🏆 All Milestones",
            command=self.show_all_milestones
        )
        all_milestones_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def refresh_display(self):
        """Refresh all display elements with current data."""
        summary = self.gm.get_progress_summary()

        # Update countdown
        if summary['days_until_exam'] is not None:
            exam_date = self.gm.get_exam_date()
            self.countdown_label.configure(
                text=f"📅 {exam_date} • ⏱️ {summary['days_until_exam']} days remaining"
            )
        else:
            self.countdown_label.configure(text="No exam date set")

        # Update readiness
        readiness = summary['readiness_percentage']
        self.progress_bar.set(readiness / 100)
        target = summary['target_readiness']
        self.readiness_label.configure(
            text=f"{readiness:.1f}% Ready • Target: {target}%"
        )

        # Update recommendation
        self.recommendation_label.configure(
            text=summary['daily_recommendation'],
            text_color=("gray10", "gray90")
        )

        # Update streak
        streak = summary['study_streak_current']
        best_streak = summary['study_streak_longest']
        cards = summary['total_cards_studied']

        self.current_streak_label.configure(text=f"Current: {streak} days 🔥" if streak > 0 else "Current: 0 days")
        self.best_streak_label.configure(text=f"Best: {best_streak} days" if best_streak > 0 else "Best: 0 days")
        self.cards_studied_label.configure(text=f"Total cards studied: {cards}")

        # Update milestones
        self.update_milestones_display(summary['recent_milestones'])

        # Update SR stats
        self.update_sr_stats_display()

    def update_milestones_display(self, milestones):
        """Update the milestones display."""
        # Clear existing milestones
        for widget in self.milestones_container.winfo_children():
            widget.destroy()

        if not milestones:
            no_milestones_label = ctk.CTkLabel(
                self.milestones_container,
                text="No milestones achieved yet. Keep studying!",
                font=ctk.CTkFont(size=11),
                text_color=("gray50", "gray50")
            )
            no_milestones_label.grid(row=0, column=0, sticky="ew")
        else:
            for idx, milestone in enumerate(milestones):
                milestone_text = f"{milestone['icon']} {milestone['name']}"
                label = ctk.CTkLabel(
                    self.milestones_container,
                    text=milestone_text,
                    font=ctk.CTkFont(size=11)
                )
                label.grid(row=idx, column=0, sticky="w", pady=3)

    def open_goal_dialog(self):
        """Open the goal setting dialog."""
        from modules.dialogs.goals_dialog import GoalsDialog

        def on_save(date_str, readiness):
            self.gm.set_exam_date(date_str)
            self.gm.goals_data['target_readiness_percentage'] = readiness
            self.gm._save_goals()
            self.refresh_display()

        dialog = GoalsDialog(self.master, callback=on_save)
        dialog.wait_window()

    def show_all_milestones(self):
        """Show dialog with all milestones."""
        all_milestones = self.gm.get_all_milestones()

        # Create dialog
        dialog = ctk.CTkToplevel(self.master)
        dialog.title("All Milestones")
        dialog.geometry("500x400")
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkLabel(
            dialog,
            text="🏆 All Milestones Achieved",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Milestones list
        list_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        list_frame.grid_columnconfigure(0, weight=1)

        if not all_milestones:
            empty_label = ctk.CTkLabel(
                list_frame,
                text="No milestones yet. Start studying to unlock achievements!",
                text_color=("gray50", "gray50")
            )
            empty_label.grid(row=0, column=0)
        else:
            for idx, milestone in enumerate(all_milestones):
                milestone_frame = ctk.CTkFrame(
                    list_frame,
                    corner_radius=8,
                    fg_color=("gray85", "gray15")
                )
                milestone_frame.grid(row=idx, column=0, sticky="ew", pady=5)
                milestone_frame.grid_columnconfigure(1, weight=1)

                icon_label = ctk.CTkLabel(
                    milestone_frame,
                    text=milestone.get('icon', '🎯'),
                    font=ctk.CTkFont(size=14)
                )
                icon_label.grid(row=0, column=0, padx=(10, 5), pady=10)

                name_label = ctk.CTkLabel(
                    milestone_frame,
                    text=milestone.get('name', 'Unknown'),
                    font=ctk.CTkFont(size=11, weight="bold")
                )
                name_label.grid(row=0, column=1, sticky="w", padx=5, pady=10)

                date_str = milestone.get('achieved_date', '')
                if date_str:
                    try:
                        date_obj = datetime.fromisoformat(date_str)
                        date_display = date_obj.strftime("%b %d, %Y")
                    except:
                        date_display = date_str
                else:
                    date_display = "Unknown date"

                date_label = ctk.CTkLabel(
                    milestone_frame,
                    text=date_display,
                    font=ctk.CTkFont(size=9),
                    text_color=("gray50", "gray50")
                )
                date_label.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 10))

        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy
        )
        close_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
