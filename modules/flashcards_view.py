import json
from pathlib import Path
import customtkinter as ctk
import random

class FlashcardView(ctk.CTkFrame):
    """
    Interactive Flashcard View for CompTIA A+ study terms.
    """

    def __init__(self, parent):
        super().__init__(parent)

        # State variables
        self.all_cards = self.load_data()
        self.cards = self.all_cards[:]  # Make a copy for filtering
        random.shuffle(self.cards)  # Shuffle on initial load
        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.start_with_definition = False # Toggle for term vs definition start
        self.selected_objective = "All"  # Track selected objective

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
    def create_header(self):
        """
        Top section showing Objective selector, progress, and settings toggle.
        """
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))
        header_frame.grid_columnconfigure(2, weight=1)

        # Objective Selector Label
        lbl_select_obj = ctk.CTkLabel(
            header_frame,
            text="Select Objective:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray",
        )
        lbl_select_obj.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Objective Dropdown Menu
        available_objs = ["All"] + [f"Objective {obj}" for obj in self.get_available_objectives()]
        self.objective_menu = ctk.CTkOptionMenu(
            header_frame,
            values=available_objs,
            command=self.on_objective_change,
            width=150,
        )
        self.objective_menu.set("All")
        self.objective_menu.grid(row=0, column=1, sticky="w", padx=(0, 15))

        # Objective Label (shows current subset info)
        self.lbl_objective = ctk.CTkLabel(
            header_frame,
            text="Cards: --",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray",
        )
        self.lbl_objective.grid(row=0, column=2, sticky="w")

        # Start Mode Switch (Term vs Definition)
        self.switch_start_side = ctk.CTkSwitch(
            header_frame,
            text="Start with Definition",
            command=self.toggle_start_side,
        )
        self.switch_start_side.grid(row=0, column=3, sticky="e", padx=(15, 0))

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
            command=lambda: self.record_answer(known=False),
        )
        self.btn_review.pack(side="left", padx=5)

        self.btn_know = ctk.CTkButton(
            btn_box,
            text="Know It ✓",
            fg_color="#388E3C",
            hover_color="#1B5E20",
            width=120,
            command=lambda: self.record_answer(known=True),
        )
        self.btn_know.pack(side="left", padx=5)

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
        if self.selected_objective == "All":
            obj_label = "All Objectives"
        else:
            obj_label = f"Objective {self.selected_objective}"

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

    def on_objective_change(self, choice):
        """
        Handler for objective dropdown menu selection.
        :param choice: selected choice (e.g., "All" or "Objective 2")
        """
        if choice == "All":
            self.selected_objective = "All"
        else:
            # Extract just the number from "Objective 2"
            self.selected_objective = choice.split()[-1]

        # Re-filter cards and reset to first card
        self.cards = self.filter_cards_by_objective(self.selected_objective)
        random.shuffle(self.cards)  # Shuffle the filtered cards
        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.update_card_display()

    def record_answer(self, known: bool):
        """Tracks mastery score and advances to the next card."""
        if known:
            self.score_known += 1
        else:
            self.score_review += 1

        self.lbl_score.configure(
            text=f"Mastered: {self.score_known} | Needs Review: {self.score_review}"
        )

        # Advance to next card or loop back
        self.current_index += 1
        if self.current_index >= len(self.cards):
            self.current_index = 0  # Loop back to beginning (or present summary screen)

        self.is_flipped = False
        self.update_card_display()

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