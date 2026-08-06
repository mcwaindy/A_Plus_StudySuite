"""Setup screen for flashcard study sessions with Core 1 and Core 2 objective selection."""
import customtkinter as ctk
from pathlib import Path
import json


class FlashcardSetupView(ctk.CTkFrame):
    def __init__(self, parent, on_start_callback=None):
        super().__init__(parent, fg_color="transparent")

        self.on_start_callback = on_start_callback
        self.selected_objectives = []
        self.selected_card_limit = "All"
        self.checkboxes = {}
        self.show_review_history = False

        # Load objectives by core
        self.load_data()

        # Create setup UI
        self.create_setup_screen()

    def load_data(self):
        """Load flashcards and extract objectives by core."""
        try:
            with open("data/flashcards.json", "r", encoding="utf-8") as f:
                self.cards = json.load(f)
        except FileNotFoundError:
            self.cards = []

        # Group objectives by core
        self.objectives_by_core = {"Core 1": set(), "Core 2": set()}
        for card in self.cards:
            exam = card.get("exam", "")
            objective = card.get("objective", "")
            if exam in self.objectives_by_core and objective:
                self.objectives_by_core[exam].add(objective)

        # Sort objectives
        for core in self.objectives_by_core:
            self.objectives_by_core[core] = sorted(list(self.objectives_by_core[core]))

    def create_setup_screen(self):
        """Main setup screen with two-column objective selection."""
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=0)  # Subtitle
        self.grid_rowconfigure(2, weight=1)  # Columns
        self.grid_rowconfigure(3, weight=0)  # Card limit
        self.grid_rowconfigure(4, weight=0)  # Buttons
        self.grid_rowconfigure(5, weight=1)  # Review history (toggleable)
        self.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(
            self,
            text="?? Flashcard Study Setup",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Subtitle
        subtitle = ctk.CTkLabel(
            self,
            text="Select objectives to study. Unselected = All objectives.",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        subtitle.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Two-column objectives frame
        columns_frame = ctk.CTkFrame(self, fg_color="transparent")
        columns_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)

        # Core 1 column
        self.create_core_column(columns_frame, "Core 1", 0)

        # Core 2 column
        self.create_core_column(columns_frame, "Core 2", 1)

        # Card limit section
        self.create_card_limit_section()

        # Summary and start button
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        bottom_frame.grid_columnconfigure(0, weight=1)

        # Summary label
        self.lbl_summary = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.lbl_summary.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Start button
        btn_start = ctk.CTkButton(
            bottom_frame,
            text="?? Start Study Session",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#388E3C",
            hover_color="#1B5E20",
            height=40,
            command=self.start_session
        )
        btn_start.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # Review History button
        btn_review = ctk.CTkButton(
            bottom_frame,
            text="?? Review History",
            font=ctk.CTkFont(size=12),
            fg_color="#5E35B1",
            hover_color="#4527A0",
            height=40,
            width=150,
            command=self.toggle_review_history
        )
        btn_review.grid(row=1, column=1, sticky="ew")

        # Review history frame (initially hidden)
        self.review_history_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.review_history_frame.grid(row=5, column=0, sticky="nsew", pady=(10, 0))
        self.review_history_frame.grid_columnconfigure(0, weight=1)
        self.review_history_frame.grid_rowconfigure(1, weight=1)

        # Review history header
        hist_header = ctk.CTkLabel(
            self.review_history_frame,
            text="?? Review History",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        hist_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Review history scrollable content
        self.hist_scrollable = ctk.CTkScrollableFrame(
            self.review_history_frame,
            fg_color=("gray90", "gray15")
        )
        self.hist_scrollable.grid(row=1, column=0, sticky="nsew")
        self.hist_scrollable.grid_columnconfigure(0, weight=1)

        # Clear history button at bottom
        btn_clear = ctk.CTkButton(
            self.review_history_frame,
            text="??? Clear History",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            width=120,
            command=self.clear_review_history
        )
        btn_clear.grid(row=2, column=0, sticky="e", pady=(10, 0))

        # Hide review history initially
        self.review_history_frame.grid_remove()

        # Update summary display
        self.update_summary()

    def create_core_column(self, parent, core_name, column):
        """Create a column with checkboxes for a core's objectives."""
        col_frame = ctk.CTkFrame(parent, fg_color="transparent")
        col_frame.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 20))
        col_frame.grid_rowconfigure(1, weight=1)
        col_frame.grid_columnconfigure(0, weight=1)

        # Core header
        header = ctk.CTkLabel(
            col_frame,
            text=core_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#388E3C" if core_name == "Core 1" else "#D32F2F")
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Scrollable frame for checkboxes
        scroll_frame = ctk.CTkScrollableFrame(
            col_frame,
            fg_color=("gray90", "gray15"),
            label_text=None
        )
        scroll_frame.grid(row=1, column=0, sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Create checkbox for each objective
        objectives = self.objectives_by_core.get(core_name, [])

        if not objectives:
            empty_label = ctk.CTkLabel(
                scroll_frame,
                text="No objectives available",
                text_color="gray"
            )
            empty_label.pack(pady=20)
        else:
            for objective in objectives:
                checkbox = ctk.CTkCheckBox(
                    scroll_frame,
                    text=objective,
                    font=ctk.CTkFont(size=11),
                    command=self.update_summary
                )
                checkbox.pack(anchor="w", pady=5, padx=10)

                # Store reference to checkbox
                self.checkboxes[objective] = checkbox

    def create_card_limit_section(self):
        """Card limit selection section."""
        limit_frame = ctk.CTkFrame(self, fg_color="transparent")
        limit_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        limit_frame.grid_columnconfigure(1, weight=1)

        # Label
        lbl = ctk.CTkLabel(
            limit_frame,
            text="Card Limit:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lbl.grid(row=0, column=0, sticky="w", padx=(0, 15))

        # Create variable for radio buttons
        self.card_limit_var = ctk.StringVar(value="All")

        # Radio buttons
        options = ["All", "10", "20", "30", "50"]
        for i, option in enumerate(options):
            radio = ctk.CTkRadioButton(
                limit_frame,
                text=option,
                variable=self.card_limit_var,
                value=option,
                command=self.update_summary
            )
            radio.grid(row=0, column=i+1, sticky="w", padx=5)

    def update_summary(self):
        """Update the summary label with selected objectives and card count."""
        # Get selected objectives
        selected = [obj for obj, cb in self.checkboxes.items() if cb.get()]
        self.selected_objectives = selected if selected else ["All"]
        self.selected_card_limit = self.card_limit_var.get()

        # Count available cards
        card_count = self.count_cards_for_selection()

        # Build summary text
        if self.selected_objectives == ["All"]:
            obj_text = "All Objectives"
        else:
            obj_text = ", ".join(self.selected_objectives)

        limit_text = f"{self.selected_card_limit} cards" if self.selected_card_limit != "All" else "All available cards"

        summary = f"?? {obj_text} | ?? {card_count} cards | {limit_text}"
        self.lbl_summary.configure(text=summary)

    def count_cards_for_selection(self):
        """Count how many cards match the current selection."""
        count = 0
        for card in self.cards:
            # Match by objective
            if self.selected_objectives == ["All"]:
                count += 1
            elif card.get("objective", "") in self.selected_objectives:
                count += 1

        return count

    def start_session(self):
        """Start the flashcard session with current selections."""
        # Build config dict
        config = {
            "exam": "All",  # Both cores selected
            "objectives": self.selected_objectives if self.selected_objectives != ["All"] else ["All"],
            "card_limit": int(self.selected_card_limit) if self.selected_card_limit != "All" else None
        }

        if self.on_start_callback:
            self.on_start_callback(config)

    def toggle_review_history(self):
        """Show/hide review history panel."""
        self.show_review_history = not self.show_review_history
        if self.show_review_history:
            self.review_history_frame.grid()
            self.populate_review_history()
        else:
            self.review_history_frame.grid_remove()

    def load_reviews(self):
        """Load all past review sessions."""
        review_path = Path("data/review_history.json")
        if review_path.exists():
            try:
                with open(review_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def populate_review_history(self):
        """Populate review history display."""
        # Clear existing content
        for widget in self.hist_scrollable.winfo_children():
            widget.destroy()

        reviews = self.load_reviews()

        if not reviews:
            empty_label = ctk.CTkLabel(
                self.hist_scrollable,
                text="No past reviews yet.\n\nComplete a flashcard session to create your first review!",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            empty_label.pack(pady=20)
            return

        # Display each review session
        for idx, review in enumerate(reversed(reviews)):  # Newest first
            session_frame = ctk.CTkFrame(
                self.hist_scrollable,
                fg_color=("gray85", "gray20")
            )
            session_frame.pack(fill="x", pady=5, padx=5)

            # Session info
            exam = review.get("exam", "All")
            objectives = review.get("objectives", review.get("objective", ["All"]))
            if isinstance(objectives, str):
                objectives = [objectives]
            objectives_str = ", ".join(objectives) if objectives != ["All"] else "All"
            cards_studied = review.get("cards_studied", 0)
            cards_reviewed = len(review.get("cards_reviewed", []))

            header_text = f"Session {len(reviews) - idx} | {exam} | Obj: {objectives_str}"
            header_label = ctk.CTkLabel(
                session_frame,
                text=header_text,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("gray10", "gray90")
            )
            header_label.pack(fill="x", padx=10, pady=(8, 4))

            stats_text = f"Studied: {cards_studied} | Needs Review: {cards_reviewed}"
            stats_label = ctk.CTkLabel(
                session_frame,
                text=stats_text,
                font=ctk.CTkFont(size=10),
                text_color=("gray30", "gray70")
            )
            stats_label.pack(fill="x", padx=10, pady=(0, 4))

            # Cards to review
            if review.get("cards_reviewed"):
                by_objective = {}
                for card in review["cards_reviewed"]:
                    obj = card.get("objective", "Unknown")
                    if obj not in by_objective:
                        by_objective[obj] = []
                    by_objective[obj].append(card.get("term", "Unknown"))

                cards_text = ""
                for obj in sorted(by_objective.keys()):
                    cards_text += f"{obj}: {', '.join(by_objective[obj][:2])}"
                    if len(by_objective[obj]) > 2:
                        cards_text += f" (+{len(by_objective[obj]) - 2} more)"
                    cards_text += "\n"

                cards_label = ctk.CTkLabel(
                    session_frame,
                    text=cards_text.strip(),
                    font=ctk.CTkFont(size=9),
                    text_color=("gray40", "gray60"),
                    justify="left"
                )
                cards_label.pack(fill="x", padx=15, pady=(0, 8))

    def clear_review_history(self):
        """Clear all review history with confirmation."""
        # Create confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Clear Review History")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Message
        msg_label = ctk.CTkLabel(
            dialog,
            text="Are you sure you want to clear ALL review history?\n\nThis action cannot be undone.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        msg_label.pack(pady=20)

        # Button frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        # Cancel button
        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color=("gray70", "gray30"),
            command=dialog.destroy
        )
        btn_cancel.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Confirm button
        def do_clear():
            review_path = Path("data/review_history.json")
            if review_path.exists():
                review_path.unlink()
            self.populate_review_history()
            dialog.destroy()

        btn_confirm = ctk.CTkButton(
            btn_frame,
            text="Clear All",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=do_clear
        )
        btn_confirm.grid(row=0, column=1, sticky="ew", padx=(5, 0))
