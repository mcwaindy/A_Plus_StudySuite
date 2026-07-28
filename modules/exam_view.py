import json
import random
from pathlib import Path
import customtkinter as ctk


class ExamView(ctk.CTkFrame):
    """Interactive Practice Exam module supporting Core 1 / Core 2 selection,

    a 90-minute countdown timer, question navigation, scoring, and review mode.
    """

    def __init__(self, parent, objective_filter=None):
        super().__init__(parent)

        self.questions_file = Path("data/questions.json")
        self.objective_filter = objective_filter
        self.selected_core = None  # "core1" or "core2"

        self.questions = []
        self.current_index = 0
        self.user_answers = {}  # {question_id: selected_index}
        self.exam_submitted = False

        # Timer State (90 minutes = 5400 seconds)
        self.time_left_seconds = 5400
        self.timer_running = False
        self.timer_job = None

        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Show Selection Menu First
        self.show_exam_selection_screen()

    # --- SCREEN 1: EXAM SELECTION MENU --- #
    def show_exam_selection_screen(self):
        """Displays Core 1 vs Core 2 launcher cards."""
        self.stop_timer()

        for child in self.winfo_children():
            child.destroy()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        lbl_title = ctk.CTkLabel(
            self,
            text="Select Practice Exam Mode",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        lbl_title.pack(padx=20, pady=(30, 5))

        lbl_subtitle = ctk.CTkLabel(
            self,
            text="Choose an exam domain to generate your 90-question, 90-minute test session.",
            font=ctk.CTkFont(size=13),
            text_color="gray60",
        )
        lbl_subtitle.pack(padx=20, pady=(0, 25))

        # Cards Container Frame
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(expand=True, fill="both", padx=40, pady=20)
        cards_frame.grid_columnconfigure((0, 1), weight=1)
        cards_frame.grid_rowconfigure(0, weight=1)

        # Card 1: Core 1
        card_core1 = ctk.CTkFrame(cards_frame, corner_radius=15)
        card_core1.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        lbl_c1_title = ctk.CTkLabel(
            card_core1,
            text="CompTIA A+ Core 1",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_c1_title.pack(padx=20, pady=(20, 5))

        lbl_c1_sub = ctk.CTkLabel(
            card_core1,
            text="Exam 220-1101\n\n• Max 90 Questions | 90 Minutes\n• Mobile Devices & Networking\n• Hardware & Storage\n• Virtualization & Cloud Computing",
            font=ctk.CTkFont(size=13),
            justify="left",
            text_color="gray70",
        )
        lbl_c1_sub.pack(padx=20, pady=10, expand=True)

        btn_start_c1 = ctk.CTkButton(
            card_core1,
            text="Start Core 1 Exam",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=lambda: self.start_exam_session("core1"),
        )
        btn_start_c1.pack(padx=20, pady=(10, 20), fill="x")

        # Card 2: Core 2
        card_core2 = ctk.CTkFrame(cards_frame, corner_radius=15)
        card_core2.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        lbl_c2_title = ctk.CTkLabel(
            card_core2,
            text="CompTIA A+ Core 2",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_c2_title.pack(padx=20, pady=(20, 5))

        lbl_c2_sub = ctk.CTkLabel(
            card_core2,
            text="Exam 220-1102\n\n• Max 90 Questions | 90 Minutes\n• Operating Systems & CLI\n• Security & Operational Procedures\n• Software Troubleshooting",
            font=ctk.CTkFont(size=13),
            justify="left",
            text_color="gray70",
        )
        lbl_c2_sub.pack(padx=20, pady=10, expand=True)

        btn_start_c2 = ctk.CTkButton(
            card_core2,
            text="Start Core 2 Exam",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=lambda: self.start_exam_session("core2"),
        )
        btn_start_c2.pack(padx=20, pady=(10, 20), fill="x")

    # --- SCREEN 2: ACTIVE EXAM INTERFACE --- #
    def start_exam_session(self, core_key):
        """Initializes questions, resets timer, and transitions UI to active exam mode."""
        self.selected_core = core_key
        self.exam_submitted = False
        self.user_answers = {}
        self.time_left_seconds = 5400  # 90 minutes

        self.load_questions(max_questions=90)

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
        self.start_timer()

    def create_header(self):
        """Top progress header with question tracker and live countdown timer."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(
            row=0, column=0, sticky="ew", padx=20, pady=(15, 10)
        )

        core_name = "Core 1 (220-1101)" if self.selected_core == "core1" else "Core 2 (220-1102)"
        title_text = f"Practice Exam — {core_name}"

        self.lbl_title = ctk.CTkLabel(
            self.header_frame,
            text=title_text,
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.lbl_title.pack(side="left")

        # Live Timer Label
        self.lbl_timer = ctk.CTkLabel(
            self.header_frame,
            text="⏱️ 90:00",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6",
        )
        self.lbl_timer.pack(side="right", padx=(15, 0))

        # Question Counter Label
        self.lbl_progress = ctk.CTkLabel(
            self.header_frame,
            text="Question 0 / 0",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="gray60",
        )
        self.lbl_progress.pack(side="right")

    def create_question_area(self):
        """Scrollable main area for question prompt, options, and explanation box."""
        self.scroll_area = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.scroll_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scroll_area.grid_columnconfigure(0, weight=1)

        self.lbl_question = ctk.CTkLabel(
            self.scroll_area,
            text="Loading Question...",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            justify="left",
            wraplength=650,
        )
        self.lbl_question.pack(fill="x", padx=15, pady=(15, 10))

        self.selected_option_var = ctk.IntVar(value=-1)
        self.option_buttons = []

        self.options_container = ctk.CTkFrame(
            self.scroll_area, fg_color="transparent"
        )
        self.options_container.pack(fill="x", padx=15, pady=10)

        for i in range(4):
            btn = ctk.CTkRadioButton(
                self.options_container,
                text=f"Option {i+1}",
                variable=self.selected_option_var,
                value=i,
                command=self.on_option_selected,
                font=ctk.CTkFont(size=14),
            )
            btn.pack(fill="x", pady=6, anchor="w")
            self.option_buttons.append(btn)

        self.explanation_frame = ctk.CTkFrame(
            self.scroll_area, fg_color=("gray85", "gray20")
        )
        self.lbl_explanation = ctk.CTkLabel(
            self.explanation_frame,
            text="",
            font=ctk.CTkFont(size=13),
            justify="left",
            wraplength=650,
        )
        self.lbl_explanation.pack(padx=15, pady=15, fill="x")

    def create_footer_navigation(self):
        """Bottom bar with Navigation and Submit Exam buttons."""
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(
            row=2, column=0, sticky="ew", padx=20, pady=(10, 15)
        )

        self.btn_prev = ctk.CTkButton(
            self.footer_frame,
            text="← Previous",
            width=110,
            command=self.prev_question,
        )
        self.btn_prev.pack(side="left")

        self.btn_submit = ctk.CTkButton(
            self.footer_frame,
            text="Submit Exam",
            fg_color="#10B981",
            hover_color="#059669",
            width=120,
            command=self.submit_exam,
        )
        self.btn_submit.pack(side="left", expand=True)

        self.btn_next = ctk.CTkButton(
            self.footer_frame,
            text="Next →",
            width=110,
            command=self.next_question,
        )
        self.btn_next.pack(side="right")

    # --- TIMER LOGIC --- #
    def start_timer(self):
        """Starts countdown loop."""
        self.stop_timer()
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        """Cancels scheduled timer update."""
        self.timer_running = False
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None

    def update_timer(self):
        """Updates timer display every second and checks for expiration."""
        if not self.timer_running or self.exam_submitted:
            return

        minutes = self.time_left_seconds // 60
        seconds = self.time_left_seconds % 60
        self.lbl_timer.configure(text=f"⏱️ {minutes:02d}:{seconds:02d}")

        # Warning color when under 10 minutes
        if self.time_left_seconds <= 600:
            self.lbl_timer.configure(text_color="#EF4444")

        if self.time_left_seconds <= 0:
            self.submit_exam()
            self.lbl_timer.configure(text="⏱️ TIME EXPIRED")
            return

        self.time_left_seconds -= 1
        self.timer_job = self.after(1000, self.update_timer)

    # --- EXAM ENGINE LOGIC --- #
    def load_questions(self, max_questions=90):
        """Reads questions JSON, filters by selected Core, shuffles,

        and caps at max 90 questions.
        """
        if not self.questions_file.exists():
            return

        try:
            with open(self.questions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_q = data.get("questions", [])

                filtered = [
                    q for q in all_q if q.get("core") == self.selected_core
                ]

                if self.objective_filter:
                    filtered = [
                        q
                        for q in filtered
                        if q.get("objective") == self.objective_filter
                    ]

                random.shuffle(filtered)

                if max_questions and len(filtered) > max_questions:
                    self.questions = filtered[:max_questions]
                else:
                    self.questions = filtered
        except Exception as e:
            print(f"Error loading questions: {e}")

    def show_question(self, index):
        """Displays target question by index."""
        if not self.questions or index < 0 or index >= len(self.questions):
            return

        self.current_index = index
        q = self.questions[index]

        self.lbl_progress.configure(
            text=f"Question {index + 1} / {len(self.questions)}"
        )
        self.lbl_question.configure(text=q.get("question", ""))

        options = q.get("options", [])
        saved_answer = self.user_answers.get(q["id"], -1)
        self.selected_option_var.set(saved_answer)

        for i, btn in enumerate(self.option_buttons):
            if i < len(options):
                btn.configure(text=options[i], state="normal")
                btn.pack(fill="x", pady=6, anchor="w")
            else:
                btn.pack_forget()

        if not self.exam_submitted:
            self.explanation_frame.pack_forget()
        else:
            self.reveal_explanation(q)

        self.btn_prev.configure(state="normal" if index > 0 else "disabled")
        self.btn_next.configure(
            state="normal" if index < len(self.questions) - 1 else "disabled"
        )

    def show_empty_state(self):
        """Fallback display if no questions exist for chosen core."""
        for child in self.winfo_children():
            child.destroy()

        lbl_msg = ctk.CTkLabel(
            self,
            text=f"No questions found for {self.selected_core.upper()}.\nAdd questions to data/questions.json to begin!",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        lbl_msg.pack(expand=True)

        btn_back = ctk.CTkButton(
            self, text="← Back to Menu", command=self.show_exam_selection_screen
        )
        btn_back.pack(pady=20)

    def on_option_selected(self):
        """Saves user choice when radio button clicked."""
        if not self.questions:
            return
        q_id = self.questions[self.current_index]["id"]
        self.user_answers[q_id] = self.selected_option_var.get()

    def prev_question(self):
        self.show_question(self.current_index - 1)

    def next_question(self):
        self.show_question(self.current_index + 1)

    def reveal_explanation(self, q):
        """Shows answer explanation card after exam submission."""
        correct_idx = q.get("correct_index", 0)
        user_idx = self.user_answers.get(q["id"], -1)
        is_correct = user_idx == correct_idx

        status_text = "✅ Correct!" if is_correct else "❌ Incorrect"
        color = "#10B981" if is_correct else "#EF4444"

        exp_text = f"{status_text}\n\nExplanation:\n{q.get('explanation', '')}"
        self.lbl_explanation.configure(text=exp_text, text_color=color)
        self.explanation_frame.pack(fill="x", padx=15, pady=15)

    def submit_exam(self):
        """Calculates final score, stops timer, and enables review mode."""
        if not self.questions or self.exam_submitted:
            return

        self.exam_submitted = True
        self.stop_timer()

        correct_count = 0
        for q in self.questions:
            if self.user_answers.get(q["id"]) == q.get("correct_index"):
                correct_count += 1

        percentage = int((correct_count / len(self.questions)) * 100)
        self.lbl_title.configure(
            text=f"Results: {percentage}% ({correct_count}/{len(self.questions)} Correct)"
        )
        self.btn_submit.configure(state="disabled", text="Submitted")

        self.show_question(self.current_index)

    def destroy(self):
        """Clean up timer job when switching frames."""
        self.stop_timer()
        super().destroy()