import json
from pathlib import Path
import customtkinter as ctk

class FlashcardView(ctk.CTkFrame):
    """
    Interactive Flashcard View for CompTIA A+ study terms.
    """

    def __init__(self, parent):
        super().__init__(parent)

        # State variables
        self.cards = self.load_data()
        self.current_index = 0
        self.is_flipped = False
        self.score_known = 0
        self.score_review = 0
        self.start_with_definition = False # Toggle for term vs definition start

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
    def create_header(self):
        """
        Top section showing Objective tag, progress, and settings toggle.
        """
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)

        # Objective Label
        self.lbl_objective = ctk.CTkLabel(
            header_frame,
            text="Objective: --",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray",
        )
        self.lbl_objective.grid(row=0, column=0, sticky="w")

        # Start Mode Switch (Term vs Definition)
        self.switch_start_side = ctk.CTkSwitch(
            header_frame,
            text="Start with Definition",
            command=self.toggle_start_side,
        )
        self.switch_start_side.grid(row=0, column=2, sticky="e")

    def create_card_widget(self):
        """Main Flashcard display box (clickable to flip)."""
        self.card_button = ctk.CTkButton(
            self,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("gray85", "gray20"),
            hover_color=("gray75", "gray25"),
            text_color=("gray10", "gray90"),
            corner_radius=15,
            command=self.flip_card,
        )
        self.card_button.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

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
        """Refreshes text and status labels for the current card."""
        if not self.cards:
            return

        card = self.cards[self.current_index]

        # Update Objective Header & Progress
        total = len(self.cards)
        self.lbl_objective.configure(
            text=f"Card {self.current_index + 1} of {total} | {card.get('objective', 'General')}"
        )

        # Show Term or Definition depending on flipped state and toggle
        front = card.get("term", "")
        back = card.get("definition", "")

        if self.start_with_definition:
            display_text = back if not self.is_flipped else front
            sub_label = "[ Definition Side ]" if not self.is_flipped else "[ Term Side ]"
        else:
            display_text = front if not self.is_flipped else back
            sub_label = "[ Term Side ]" if not self.is_flipped else "[ Definition Side ]"

        # Update card button text
        self.card_button.configure(text=f"{display_text}\n\n\n\n(Click to flip)\n{sub_label}")

    def flip_card(self):
        """Toggles card state between front and back."""
        self.is_flipped = not self.is_flipped
        self.update_card_display()

    def toggle_start_side(self):
        """Handler for 'Start with Definition' switch."""
        self.start_with_definition = self.switch_start_side.get() == 1
        self.is_flipped = False
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