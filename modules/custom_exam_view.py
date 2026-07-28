import json
from pathlib import Path
import customtkinter as ctk
from modules.exam_view import ExamView


class CustomExamView(ExamView):
    """Custom Exam Module allowing users to filter by multiple CompTIA objectives,

    set custom timers, and select question limits before starting.
    """

    def __init__(self, parent):
        self.selected_objectives = set()
        self.custom_time_limit_mins = 30  # Default 30 mins
        self.custom_max_questions = 20  # Default 20 questions

        # Call parent constructor
        super().__init__(parent)

    # --- OVERRIDE SELECTION SCREEN --- #
    def show_exam_selection_screen(self):
        """Displays Custom Exam configuration panel with objective dropdown,

        badge tags, timer selection, and question limit controls.
        """
        self.stop_timer()

        for child in self.winfo_children():
            child.destroy()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Header Title
        lbl_title = ctk.CTkLabel(
            self,
            text="Build Custom Objective Practice Session",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        lbl_title.pack(padx=20, pady=(25, 5))

        lbl_subtitle = ctk.CTkLabel(
            self,
            text="Select specific objectives, set a time limit, and choose question length.",
            font=ctk.CTkFont(size=13),
            text_color="gray60",
        )
        lbl_subtitle.pack(padx=20, pady=(0, 15))

        # Main Settings Container (Scrollable)
        container = ctk.CTkScrollableFrame(self, corner_radius=12)
        container.pack(expand=True, fill="both", padx=30, pady=(0, 15))
        container.grid_columnconfigure(0, weight=1)

        # --- SECTION 1: OBJECTIVES SELECTOR --- #
        sec_obj = ctk.CTkFrame(container, fg_color="transparent")
        sec_obj.pack(fill="x", padx=15, pady=10)

        lbl_obj = ctk.CTkLabel(
            sec_obj,
            text="1. Target Objectives",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        lbl_obj.pack(anchor="w", pady=(0, 5))

        # Dropdown + Add Button Row
        selector_row = ctk.CTkFrame(sec_obj, fg_color="transparent")
        selector_row.pack(fill="x", pady=5)

        available_objs = self.get_available_objectives()
        self.obj_dropdown = ctk.CTkOptionMenu(
            selector_row,
            values=(
                available_objs
                if available_objs
                else ["No Objectives Found in JSON"]
            ),
            width=380,
        )
        self.obj_dropdown.pack(side="left", padx=(0, 10))

        btn_add = ctk.CTkButton(
            selector_row,
            text="+ Add Objective",
            width=130,
            command=self.add_selected_objective,
        )
        btn_add.pack(side="left")

        # Container for objective tags/badges
        self.tags_frame = ctk.CTkFrame(sec_obj, fg_color=("gray90", "gray15"))
        self.tags_frame.pack(fill="x", pady=10, ipady=5)
        self.render_objective_tags()

        # --- SECTION 2: EXAM CONFIGURATION (TIMER & LENGTH) --- #
        sec_config = ctk.CTkFrame(container, fg_color="transparent")
        sec_config.pack(fill="x", padx=15, pady=10)
        sec_config.grid_columnconfigure((0, 1), weight=1)

        # Timer Selection Card
        card_timer = ctk.CTkFrame(sec_config, corner_radius=10)
        card_timer.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

        lbl_timer_title = ctk.CTkLabel(
            card_timer,
            text="2. Time Limit",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        lbl_timer_title.pack(anchor="w", padx=15, pady=(15, 5))

        self.time_option_menu = ctk.CTkOptionMenu(
            card_timer,
            values=[
                "15 Minutes",
                "30 Minutes",
                "45 Minutes",
                "60 Minutes",
                "90 Minutes",
                "Untimed (No Timer)",
            ],
            command=self.on_timer_change,
        )
        self.time_option_menu.set("30 Minutes")
        self.time_option_menu.pack(padx=15, pady=(5, 15), fill="x")

        # Question Limit Selection Card
        card_length = ctk.CTkFrame(sec_config, corner_radius=10)
        card_length.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

        lbl_length_title = ctk.CTkLabel(
            card_length,
            text="3. Question Count",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        lbl_length_title.pack(anchor="w", padx=15, pady=(15, 5))

        self.length_option_menu = ctk.CTkOptionMenu(
            card_length,
            values=[
                "5 Questions",
                "10 Questions",
                "20 Questions",
                "50 Questions",
                "All Matching Questions",
            ],
            command=self.on_length_change,
        )
        self.length_option_menu.set("20 Questions")
        self.length_option_menu.pack(padx=15, pady=(5, 15), fill="x")

        # --- START BUTTON --- #
        btn_start_custom = ctk.CTkButton(
            self,
            text="🚀 Start Custom Practice Session",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            fg_color="#10B981",
            hover_color="#059669",
            command=self.start_custom_exam_session,
        )
        btn_start_custom.pack(padx=40, pady=(0, 20), fill="x")

    # --- OBJECTIVE TAG HELPERS --- #
    def get_available_objectives(self):
        """Reads questions.json and returns a sorted list of unique objectives."""
        if not self.questions_file.exists():
            return []
        try:
            with open(self.questions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_q = data.get("questions", [])
                objs = {
                    q.get("objective")
                    for q in all_q
                    if q.get("objective") is not None
                }
                return sorted(list(objs))
        except Exception:
            return []

    def add_selected_objective(self):
        """Adds chosen objective to active target set."""
        val = self.obj_dropdown.get()
        if val and val != "No Objectives Found in JSON":
            self.selected_objectives.add(val)
            self.render_objective_tags()

    def remove_objective(self, obj_name):
        """Removes objective from active target set."""
        self.selected_objectives.discard(obj_name)
        self.render_objective_tags()

    def render_objective_tags(self):
        """Draws badge widgets for all currently added target objectives."""
        for child in self.tags_frame.winfo_children():
            child.destroy()

        if not self.selected_objectives:
            lbl_empty = ctk.CTkLabel(
                self.tags_frame,
                text="No objectives selected. (Will include all objectives if left empty)",
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color="gray60",
            )
            lbl_empty.pack(padx=10, pady=8)
            return

        for obj in sorted(list(self.selected_objectives)):
            badge = ctk.CTkFrame(self.tags_frame, fg_color="#3B82F6")
            badge.pack(side="left", padx=5, pady=5)

            lbl_tag = ctk.CTkLabel(
                badge,
                text=obj,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
            )
            lbl_tag.pack(side="left", padx=(8, 4), pady=2)

            btn_del = ctk.CTkButton(
                badge,
                text="✕",
                width=18,
                height=18,
                fg_color="transparent",
                hover_color="#1D4ED8",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda target=obj: self.remove_objective(target),
            )
            btn_del.pack(side="left", padx=(0, 4), pady=2)

    # --- CONFIGURATION HANDLERS --- #
    def on_timer_change(self, choice):
        """Maps user dropdown selection to time limit in minutes."""
        if choice == "Untimed (No Timer)":
            self.custom_time_limit_mins = None
        else:
            self.custom_time_limit_mins = int(choice.split()[0])

    def on_length_change(self, choice):
        """Maps user dropdown selection to maximum question count."""
        if choice == "All Matching Questions":
            self.custom_max_questions = None
        else:
            self.custom_max_questions = int(choice.split()[0])

    # --- START CUSTOM SESSION --- #
    def start_custom_exam_session(self):
        """Initializes questions filtered by target objectives and starts session."""
        self.exam_submitted = False
        self.user_answers = {}

        # Set time limit in seconds
        if self.custom_time_limit_mins is not None:
            self.time_left_seconds = self.custom_time_limit_mins * 60
        else:
            self.time_left_seconds = None

        self.load_custom_questions()

        if not self.questions:
            self.show_empty_state()
            return

        for child in self.winfo_children():
            child.destroy()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.create_header()
        self.create_question_area()
        self.create_footer_navigation()

        self.show_question(0)

        # Start timer if time limit set
        if self.custom_time_limit_mins is not None:
            self.start_timer()
        else:
            self.lbl_timer.configure(text="⏱️ Untimed Mode")

    def load_custom_questions(self):
        """Loads and filters questions by set of selected objectives."""
        if not self.questions_file.exists():
            return

        try:
            with open(self.questions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_q = data.get("questions", [])

                # Filter by objective set if objectives were selected
                if self.selected_objectives:
                    filtered = [
                        q
                        for q in all_q
                        if q.get("objective") in self.selected_objectives
                    ]
                else:
                    filtered = all_q

                import random

                random.shuffle(filtered)

                # Cap max questions if limit set
                if (
                    self.custom_max_questions
                    and len(filtered) > self.custom_max_questions
                ):
                    self.questions = filtered[: self.custom_max_questions]
                else:
                    self.questions = filtered
        except Exception as e:
            print(f"Error loading custom questions: {e}")