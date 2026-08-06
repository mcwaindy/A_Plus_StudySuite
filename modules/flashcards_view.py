import json
from pathlib import Path
import customtkinter as ctk
import random

class FlashcardView(ctk.CTkFrame):
    """
    Interactive Flashcard View for CompTIA A+ study terms.
    """

    def __init__(self, parent, config=None):
        super().__init__(parent)

        # Load configuration from setup screen or use defaults
        if config:
            self.selected_exam = config.get("exam", "All")
            self.selected_objectives = config.get("objectives", ["All"])
            self.card_limit = config.get("card_limit", None)
        else:
            self.selected_exam = "All"
            self.selected_objectives = ["All"]
            self.card_limit = None

        # State variables
        self.all_cards = self.load_data()
        self.cards = self.all_cards[:]  # Make a copy for filtering

        # Filter by exam and objectives from config
        self.cards = self.filter_cards_by_exam_and_objective(self.selected_exam, self.selected_objectives)
        random.shuffle(self.cards)  # Shuffle on initial load

        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.start_with_definition = False # Toggle for term vs definition start

        # Card limit and review tracking
        self.reviewed_cards = []  # List of cards marked as "needs review"
        self.cards_studied = []  # List of all cards studied in this session
        self.session_active = False  # Track if currently in a study session
        self._in_review_mode = False  # Track if currently displaying review screen
        self._objective_dialog = None  # Track objective selector dialog to prevent multiples

        # Configure Grid Layout (Row 1 expands to hold the card)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Build UI Elements (order matters)
        self.create_header()
        self.create_card_widget()
        self.create_controls()

        # Display First Card
        self.update_card_display()

    def load_data(self):
        """
        Loads flashcard data from JSON file.
        :return: flashcard data as <LIST>
        """
        json_path = Path("data/flashcards.json")
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error: flashcards.json is improperly formatted.")
        else:
            return None
        return [
            {
                "id": "err",
                "objective": "Error",
                "term": "No Flashcards Found",
                "definition": "Check that data/flashcards.json exists and contains valid JSON."
            }
        ]

    def save_review(self):
        """
        Save the current review session to persistent storage.
        """
        review_data = {
            "timestamp": str(Path("data").cwd()),  # Will use current time
            "exam": self.selected_exam,
            "objectives": self.selected_objectives,  # Changed to list
            "cards_studied": len(self.cards_studied),
            "cards_reviewed": [
                {
                    "id": card.get("id"),
                    "term": card.get("term"),
                    "objective": card.get("objective")
                }
                for card in self.reviewed_cards
            ]
        }

        # Load existing reviews
        review_path = Path("data/review_history.json")
        reviews = []
        if review_path.exists():
            try:
                with open(review_path, "r", encoding="utf-8") as f:
                    reviews = json.load(f)
            except:
                reviews = []

        # Add new review
        reviews.append(review_data)

        # Save back
        with open(review_path, "w", encoding="utf-8") as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)

    def load_reviews(self):
        """
        Load all past review sessions.
        :return: list of review data
        """
        review_path = Path("data/review_history.json")
        if review_path.exists():
            try:
                with open(review_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def show_review_history_dialog(self):
        """
        Display a dialog showing past review sessions in a collapsible format.
        """
        reviews = self.load_reviews()

        if not reviews:
            # Show simple message if no reviews
            dialog = ctk.CTkToplevel(self)
            dialog.title("Review History")
            dialog.geometry("400x200")
            dialog.resizable(False, False)

            label = ctk.CTkLabel(
                dialog,
                text="No past reviews yet.\n\nComplete a flashcard session with\na card limit to create your first review!",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            )
            label.pack(pady=20)
            return

        # Create main dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("Review History")
        dialog.geometry("600x500")
        dialog.resizable(True, True)

        # Main scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Display each review session
        for idx, review in enumerate(reversed(reviews)):  # Newest first
            session_frame = ctk.CTkFrame(scrollable_frame, fg_color=("gray85", "gray20"))
            session_frame.pack(fill="x", pady=5)

            # Header with session info
            exam = review.get("exam", "All")
            objectives = review.get("objectives", review.get("objective", ["All"]))  # Handle both old and new format
            if isinstance(objectives, str):  # For backwards compatibility with old single-objective format
                objectives = [objectives]
            objectives_str = ", ".join(objectives) if objectives != ["All"] else "All"
            cards_studied = review.get("cards_studied", 0)
            cards_reviewed = len(review.get("cards_reviewed", []))

            header_text = f"Session {len(reviews) - idx} - {exam} | Obj: {objectives_str} | Studied: {cards_studied} | Needs Review: {cards_reviewed}"
            header_label = ctk.CTkLabel(
                session_frame,
                text=header_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("gray10", "gray90")
            )
            header_label.pack(fill="x", padx=10, pady=(8, 4))

            # Cards to review list
            if review.get("cards_reviewed"):
                by_objective = {}
                for card in review["cards_reviewed"]:
                    obj = card.get("objective", "Unknown")
                    if obj not in by_objective:
                        by_objective[obj] = []
                    by_objective[obj].append(card.get("term", "Unknown"))

                cards_text = ""
                for obj in sorted(by_objective.keys()):
                    cards_text += f"{obj}: {', '.join(by_objective[obj][:3])}"
                    if len(by_objective[obj]) > 3:
                        cards_text += f" (+{len(by_objective[obj]) - 3} more)"
                    cards_text += "\n"

                cards_label = ctk.CTkLabel(
                    session_frame,
                    text=cards_text,
                    font=ctk.CTkFont(size=10),
                    text_color=("gray30", "gray70"),
                    justify="left"
                )
                cards_label.pack(fill="x", padx=15, pady=(0, 8))

        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            width=100
        )
        close_btn.pack(pady=10)

    def get_available_objectives(self):
        """
        Extract unique main objectives (1, 2, 3, etc.) from flashcards.
        :return: sorted list of main objective numbers
        """
        objectives = set()
        for card in self.all_cards:
            obj_str = card.get("objective", "")
            # Extract the main objective number (e.g., "2" from "2.5 - Network Cables")
            if obj_str:
                main_obj = obj_str.split(".")[0].strip()
                if main_obj and main_obj[0].isdigit():
                    objectives.add(main_obj)
        return sorted(list(objectives))

    def get_available_exams(self):
        """
        Extract unique exams from flashcards (Core 1, Core 2, etc.).
        :return: sorted list of exam names
        """
        exams = set()
        for card in self.all_cards:
            exam = card.get("exam", "")
            if exam:
                exams.add(exam)
        return sorted(list(exams))

    def filter_cards_by_objective(self, objective):
        """
        Filter flashcards by main objective number.
        :param objective: main objective number (e.g., "2") or "All"
        :return: filtered list of cards
        """
        if objective == "All":
            return self.all_cards

        filtered = []
        for card in self.all_cards:
            obj_str = card.get("objective", "")
            if obj_str:
                main_obj = obj_str.split(".")[0].strip()
                if main_obj == objective:
                    filtered.append(card)
        return filtered

    def filter_cards_by_exam(self, exam):
        """
        Filter flashcards by exam name.
        :param exam: exam name (e.g., "Core 1", "Core 2") or "All"
        :return: filtered list of cards
        """
        if exam == "All":
            return self.all_cards

        filtered = []
        for card in self.all_cards:
            card_exam = card.get("exam", "")
            if card_exam == exam:
                filtered.append(card)
        return filtered

    def filter_cards_by_exam_and_objective(self, exam, objectives):
        """
        Filter flashcards by both exam and objectives.
        :param exam: exam name or "All"
        :param objectives: list of objective strings (full names) or ["All"]
        :return: filtered list of cards
        """
        filtered = self.filter_cards_by_exam(exam)

        if "All" in objectives or objectives == ["All"]:
            return filtered

        result = []
        for card in filtered:
            obj_str = card.get("objective", "")
            # Match exact objective string
            if obj_str in objectives:
                result.append(card)
        return result
    def create_header(self):
        """
        Top section showing progress, card limit, and settings toggle.
        """
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))
        header_frame.grid_columnconfigure(2, weight=1)

        # Current Selection Display (Left)
        selection_text = f"{self.selected_exam} | Obj: {', '.join(self.selected_objectives)}"
        if self.selected_objectives == ["All"]:
            selection_text = f"{self.selected_exam} | All Objectives"

        self.lbl_selection = ctk.CTkLabel(
            header_frame,
            text=selection_text,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.lbl_selection.grid(row=0, column=0, sticky="w", padx=(0, 15))

        # Card Limit Label
        lbl_card_limit = ctk.CTkLabel(
            header_frame,
            text="Card Limit:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray",
        )
        lbl_card_limit.grid(row=0, column=1, sticky="w", padx=(0, 5))

        # Card Limit Dropdown Menu
        card_limit_options = ["All", "10", "20", "30", "50"]
        self.card_limit_menu = ctk.CTkOptionMenu(
            header_frame,
            values=card_limit_options,
            command=self.on_card_limit_change,
            width=70,
        )
        if self.card_limit:
            self.card_limit_menu.set(str(self.card_limit))
        else:
            self.card_limit_menu.set("All")
        self.card_limit_menu.grid(row=0, column=2, sticky="w", padx=(0, 15))

        # Objective Label (shows current subset info)
        self.lbl_objective = ctk.CTkLabel(
            header_frame,
            text="Cards: --",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray",
        )
        self.lbl_objective.grid(row=0, column=3, sticky="w")

        # Start Mode Switch (Term vs Definition)
        self.switch_start_side = ctk.CTkSwitch(
            header_frame,
            text="Start with Definition",
            command=self.toggle_start_side,
        )
        self.switch_start_side.grid(row=0, column=4, sticky="e", padx=(15, 0))

    def create_card_widget(self):
        """Main Flashcard display box with responsive text wrapping."""
        # Create main card container frame
        self.card_container = ctk.CTkFrame(
            self,
            fg_color=("gray85", "gray20"),
            corner_radius=15,
        )
        self.card_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.card_container.grid_rowconfigure(0, weight=0)
        self.card_container.grid_rowconfigure(1, weight=1)  # Center row expands
        self.card_container.grid_rowconfigure(2, weight=0)
        self.card_container.grid_columnconfigure(0, weight=1)

        # Bind click to card container itself
        self.card_container.bind("<Button-1>", lambda e: self.flip_card())

        # Side indicator label (top)
        self.lbl_card_side = ctk.CTkLabel(
            self.card_container,
            text="[ Loading... ]",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray30", "gray70"),
        )
        self.lbl_card_side.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        self.lbl_card_side.bind("<Button-1>", lambda e: self.flip_card())

        # Main text display using CTkTextbox for better wrapping
        # This will be vertically centered due to row weight=1
        self.text_card = ctk.CTkTextbox(
            self.card_container,
            font=ctk.CTkFont(size=32, weight="bold"),
            fg_color=("gray85", "gray20"),
            text_color=("gray10", "gray90"),
            border_width=0,
            wrap="word",
            state="disabled",
        )
        self.text_card.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.text_card.bind("<Button-1>", lambda e: self.flip_card())

        # Configure tag for center alignment
        self.text_card.tag_config("center", justify="center")

        # Bottom frame for objective reference and click prompt
        bottom_frame = ctk.CTkFrame(self.card_container, fg_color=("gray85", "gray20"))
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))
        bottom_frame.grid_columnconfigure(0, weight=1)

        # Objective reference label (bottom-left)
        self.lbl_objective_ref = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=ctk.CTkFont(size=9),
            text_color=("gray50", "gray50"),
        )
        self.lbl_objective_ref.grid(row=0, column=0, sticky="w")
        self.lbl_objective_ref.bind("<Button-1>", lambda e: self.flip_card())

        # Click prompt (bottom-right)
        self.lbl_click_prompt = ctk.CTkLabel(
            bottom_frame,
            text="(Click to flip)",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        )
        self.lbl_click_prompt.grid(row=0, column=0, sticky="e")
        self.lbl_click_prompt.bind("<Button-1>", lambda e: self.flip_card())

        # Bind resize event to update wrap length
        self.card_container.bind("<Configure>", self._on_card_configure)

    def create_controls(self):
        """Bottom navigation controls and score tracking."""
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 10))
        controls_frame.grid_columnconfigure(1, weight=1)

        # Left: Score counter
        self.lbl_score = ctk.CTkLabel(
            controls_frame,
            text="Mastered: 0 | Needs Review: 0",
            font=ctk.CTkFont(size=13),
        )
        self.lbl_score.grid(row=0, column=0, sticky="w")

        # Center: Shuffle and Sort buttons
        shuffle_box = ctk.CTkFrame(controls_frame, fg_color="transparent")
        shuffle_box.grid(row=0, column=1, sticky="ew")
        shuffle_box.grid_columnconfigure(0, weight=1)

        self.btn_shuffle = ctk.CTkButton(
            shuffle_box,
            text="🔀 Reshuffle",
            fg_color="#F57C00",
            hover_color="#E65100",
            width=120,
            command=self.reshuffle_cards,
        )
        self.btn_shuffle.pack(side="left", padx=5)

        self.btn_sort = ctk.CTkButton(
            shuffle_box,
            text="↑↓ Sort by Objective",
            fg_color="#00897B",
            hover_color="#00695C",
            width=140,
            command=self.sort_cards,
        )
        self.btn_sort.pack(side="left", padx=5)

        # Right: Self-Assessment Action Buttons
        btn_box = ctk.CTkFrame(controls_frame, fg_color="transparent")
        btn_box.grid(row=0, column=2, sticky="e")

        self.btn_review = ctk.CTkButton(
            btn_box,
            text="Needs Review ✗",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            width=120,
            command=self.on_btn_review_click,
        )
        self.btn_review.pack(side="left", padx=5)

        self.btn_know = ctk.CTkButton(
            btn_box,
            text="Know It ✓",
            fg_color="#388E3C",
            hover_color="#1B5E20",
            width=120,
            command=self.on_btn_know_click,
        )
        self.btn_know.pack(side="left", padx=5)

        # Back to Setup Button
        back_btn = ctk.CTkButton(
            controls_frame,
            text="⚙️ Back to Setup",
            fg_color=("gray60", "gray40"),
            hover_color=("gray70", "gray50"),
            width=120,
            command=self.on_back_to_setup,
        )
        back_btn.grid(row=0, column=3, sticky="e", padx=(5, 0))

    def update_card_display(self):
        """Refreshes text and status labels for the current card with responsive wrapping."""
        if not self.cards:
            self.text_card.configure(state="normal")
            self.text_card.delete("1.0", "end")
            empty_message = "\n\n\nNo flashcards available for this objective.\n\nSelect a different objective.\n\n\n"
            self.text_card.insert("1.0", empty_message, "center")
            self.text_card.configure(state="disabled")
            self.lbl_objective.configure(text="Cards: 0")
            self.lbl_card_side.configure(text="")
            return

        card = self.cards[self.current_index]

        # Update progress header
        total = len(self.cards)
        if self.selected_objectives == ["All"]:
            obj_label = "All Objectives"
        else:
            obj_label = f"Objectives: {', '.join(self.selected_objectives)}"

        self.lbl_objective.configure(
            text=f"Card {self.current_index + 1} of {total} | {obj_label}"
        )

        # Show Term or Definition depending on flipped state and toggle
        front = card.get("term", "")
        back = card.get("definition", "")
        objective = card.get("objective", "")

        if self.start_with_definition:
            display_text = back if not self.is_flipped else front
            sub_label = "[ Definition Side ]" if not self.is_flipped else "[ Term Side ]"
            show_objective_ref = self.is_flipped  # Show objective ref on term side only
        else:
            display_text = front if not self.is_flipped else back
            sub_label = "[ Term Side ]" if not self.is_flipped else "[ Definition Side ]"
            show_objective_ref = not self.is_flipped  # Show objective ref on term side only

        # Update card text in textbox with center alignment
        self.text_card.configure(state="normal")
        self.text_card.delete("1.0", "end")

        # Add newlines before and after text for vertical centering
        centered_text = f"\n\n\n{display_text}\n\n\n"
        self.text_card.insert("1.0", centered_text, "center")
        self.text_card.configure(state="disabled")

        # Update objective reference at bottom (only show on term side)
        if show_objective_ref and objective:
            self.lbl_objective_ref.configure(text=f"Objective: {objective}")
        else:
            self.lbl_objective_ref.configure(text="")

        # Update side indicator
        self.lbl_card_side.configure(text=sub_label)

    def _on_card_configure(self, event):
        """Handle card container resize events."""
        # No need to adjust wrapping - CTkTextbox handles it automatically
        pass

    def _update_wrap_length(self):
        """No longer needed with CTkTextbox - it wraps automatically."""
        pass

    def flip_card(self):
        """Toggles card state between front and back."""
        self.is_flipped = not self.is_flipped
        self.update_card_display()

    def toggle_start_side(self):
        """Handler for 'Start with Definition' switch."""
        self.start_with_definition = self.switch_start_side.get() == 1
        self.is_flipped = False
        self.update_card_display()

    def on_exam_change(self, choice):
        """
        Handler for exam dropdown menu selection.
        :param choice: selected exam (e.g., "All", "Core 1", "Core 2")
        """
        self.selected_exam = choice if choice != "All" else "All"

        # Re-filter cards and reset to first card
        self.cards = self.filter_cards_by_exam_and_objective(self.selected_exam, self.selected_objectives)
        random.shuffle(self.cards)
        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.update_card_display()

    def show_objective_selector(self):
        """
        Display a modal dialog for selecting multiple objectives.
        """
        # Prevent multiple dialogs from opening
        if hasattr(self, '_objective_dialog') and self._objective_dialog is not None:
            try:
                self._objective_dialog.lift()  # Bring to front if already open
                return
            except:
                self._objective_dialog = None

        available_objs = self.get_available_objectives()

        # Create modal dialog window
        dialog = ctk.CTkToplevel(self)
        self._objective_dialog = dialog  # Store reference to prevent multiple openings
        dialog.title("Select Objectives")
        dialog.geometry("350x400")
        dialog.resizable(False, False)

        # Make dialog modal and always on top
        dialog.attributes('-topmost', True)
        dialog.grab_set()

        # Reduce UI artifacts by deferring rendering
        dialog.update_idletasks()

        # Header
        header_label = ctk.CTkLabel(
            dialog,
            text="Select one or more objectives:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        header_label.pack(pady=(10, 5), padx=10)

        # Scrollable frame for checkboxes
        scrollable_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create checkbox for "All"
        var_all = ctk.BooleanVar(value=self.selected_objectives == ["All"])
        checkbox_all = ctk.CTkCheckBox(
            scrollable_frame,
            text="All Objectives",
            variable=var_all,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        checkbox_all.pack(anchor="w", pady=3)

        # Create checkboxes for each objective
        checkbox_vars = {}
        for obj in available_objs:
            is_selected = obj in self.selected_objectives
            var = ctk.BooleanVar(value=is_selected)
            checkbox_vars[obj] = var

            checkbox = ctk.CTkCheckBox(
                scrollable_frame,
                text=f"Objective {obj}",
                variable=var,
                font=ctk.CTkFont(size=11)
            )
            checkbox.pack(anchor="w", pady=2)

        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=10)

        # Apply and Cancel buttons
        apply_btn = ctk.CTkButton(
            button_frame,
            text="Apply",
            command=lambda: self.apply_objective_selection(checkbox_vars, var_all, dialog),
            width=100
        )
        apply_btn.pack(side="left", padx=5)

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color=("gray60", "gray40"),
            hover_color=("gray70", "gray50"),
            command=lambda: self.close_objective_dialog(dialog),
            width=100
        )
        cancel_btn.pack(side="left", padx=5)

        # Handle dialog close
        def on_dialog_close():
            self._objective_dialog = None

        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)

    def close_objective_dialog(self, dialog):
        """Close the objective dialog and clean up reference."""
        self._objective_dialog = None
        dialog.destroy()

    def apply_objective_selection(self, checkbox_vars, var_all, dialog):
        """
        Apply the selected objectives and close dialog.
        """
        if var_all.get():
            self.selected_objectives = ["All"]
        else:
            selected = [obj for obj, var in checkbox_vars.items() if var.get()]
            if not selected:
                selected = ["All"]
            self.selected_objectives = sorted(selected)

        # Update button text
        if self.selected_objectives == ["All"]:
            self.obj_button.configure(text="All Objectives")
        else:
            button_text = "Obj: " + ", ".join(self.selected_objectives)
            self.obj_button.configure(text=button_text)

        # Re-filter cards
        self.cards = self.filter_cards_by_exam_and_objective(self.selected_exam, self.selected_objectives)
        random.shuffle(self.cards)
        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.reviewed_cards = []
        self.cards_studied = []
        self.update_card_display()

        # Close dialog
        self.close_objective_dialog(dialog)

    def on_card_limit_change(self, choice):
        """
        Handler for card limit selection.
        :param choice: selected limit (e.g., "All", "10", "20", etc.)
        """
        if choice == "All":
            self.card_limit = None
        else:
            self.card_limit = int(choice)

        # Reset current session
        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.reviewed_cards = []
        self.cards_studied = []
        self.update_card_display()

    def on_back_to_setup(self):
        """Go back to setup screen."""
        # Get reference to main app window
        root = self.winfo_toplevel()
        # Call the app's start_flashcards_setup method
        if hasattr(root, 'start_flashcards_setup'):
            root.start_flashcards_setup()

    def on_btn_review_click(self):
        """Handle 'Needs Review' button - context aware."""
        if hasattr(self, '_in_review_mode') and self._in_review_mode:
            # On review screen: start new session
            self.start_new_session()
        else:
            # During study: mark card as needs review
            self.record_answer(known=False)

    def on_btn_know_click(self):
        """Handle 'Know It' button - context aware."""
        if hasattr(self, '_in_review_mode') and self._in_review_mode:
            # On review screen: done studying
            self.exit_review_screen()
        else:
            # During study: mark card as known
            self.record_answer(known=True)

    def start_new_session(self):
        """Start a fresh study session."""
        self._in_review_mode = False
        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.reviewed_cards = []
        self.cards_studied = []
        self.cards = self.filter_cards_by_exam_and_objective(self.selected_exam, self.selected_objectives)
        random.shuffle(self.cards)
        self.btn_review.configure(text="Needs Review ✗")
        self.btn_know.configure(text="Know It ✓")
        self.update_card_display()

    def exit_review_screen(self):
        """Exit the review screen and return to normal state."""
        self._in_review_mode = False
        self.btn_review.configure(text="Needs Review ✗")
        self.btn_know.configure(text="Know It ✓")
        self.start_new_session()

    def record_answer(self, known: bool):
        """Tracks mastery score, cards reviewed, and advances to next card."""
        current_card = self.cards[self.current_index]
        self.cards_studied.append(current_card)

        if known:
            self.score_known += 1
        else:
            self.score_review += 1
            self.reviewed_cards.append(current_card)  # Track for review

        self.lbl_score.configure(
            text=f"Mastered: {self.score_known} | Needs Review: {self.score_review}"
        )

        # Check if card limit reached
        total_answered = self.score_known + self.score_review
        if self.card_limit and total_answered >= self.card_limit:
            # Show review screen instead of next card
            self.show_review_screen()
            return

        # Advance to next card or loop back
        self.current_index += 1
        if self.current_index >= len(self.cards):
            self.current_index = 0  # Loop back to beginning

        self.is_flipped = False
        self.update_card_display()

    def show_review_screen(self):
        """
        Display review summary screen with collapsible objectives showing reviewed cards.
        """
        self._in_review_mode = True

        # Save this review to history
        self.save_review()

        # Clear the card content area
        self.text_card.configure(state="normal")
        self.text_card.delete("1.0", "end")

        # Create review summary
        review_text = f"\n✓ REVIEW COMPLETE!\n\n"
        review_text += f"Cards Studied: {len(self.cards_studied)}\n"
        review_text += f"Mastered: {self.score_known}\n"
        review_text += f"Needs Review: {self.score_review}\n\n"

        if self.reviewed_cards:
            review_text += "Cards to Review:\n"
            review_text += "-" * 40 + "\n\n"

            # Group by objective
            by_objective = {}
            for card in self.reviewed_cards:
                obj = card.get("objective", "Unknown")
                if obj not in by_objective:
                    by_objective[obj] = []
                by_objective[obj].append(card.get("term", "Unknown"))

            for obj in sorted(by_objective.keys()):
                review_text += f"\n[{obj}]\n"
                for term in by_objective[obj]:
                    review_text += f"  • {term}\n"

        review_text += "\n\n" + "=" * 40
        review_text += "\nClick 'New Review' to study again"
        review_text += "\nor 'Done' to exit.\n"

        self.text_card.insert("1.0", review_text)
        self.text_card.configure(state="disabled")

        # Hide progress label
        self.lbl_objective.configure(text="")
        self.lbl_card_side.configure(text="")

        # Change button labels
        self.btn_review.configure(text="New Review")
        self.btn_know.configure(text="Done")

    def reshuffle_cards(self):
        """Reshuffle the current card deck."""
        random.shuffle(self.cards)
        self.current_index = 0
        self.is_flipped = False
        self.update_card_display()

    def sort_cards(self):
        """Sort cards by objective number."""
        self.cards.sort(key=lambda card: card.get("objective", ""))
        self.current_index = 0
        self.is_flipped = False
        self.update_card_display()
        self.update_card_display()