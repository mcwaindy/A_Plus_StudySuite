import customtkinter as ctk
from customtkinter import CTkFont

# --- MODULES --- #
from modules.flashcards_view import FlashcardView
from modules.flashcard_setup_view import FlashcardSetupView
from modules.notes_view import NotesView
from modules.diagram_view import DiagramView
from modules.exam_view import ExamView
from modules.custom_exam_view import CustomExamView
from modules.game_view import GameView
from modules.goals_view import GoalsView
from modules.dev_tools_view import DevToolsView
from modules.settings_view import SettingsView
from utils.session_manager import SessionManager

# Set dark mode theme and default color scheme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    """
    Main Application Window setup and screen manager.
    Supports session recovery for interrupted flashcard/exam sessions.
    """

    def __init__(self):
        super().__init__()

        # Configure Window Properties
        self.title("CompTIA A+ Study Suite")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # Configure 1x2 Grid Layout
        # (Column 0 = Sidebar, Coloumn 1 = Main View)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Initialize session manager
        self.session_manager = SessionManager()

        # Build UI Elements
        self.create_sidebar()

        # Content Area Container
        self.current_frame = None

        # Check for interrupted sessions at startup
        self.check_for_session_recovery()

    def check_for_session_recovery(self):
        """
        Check for saved session state at app startup.
        If a flashcard session was interrupted, prompt user to resume.
        """
        session = self.session_manager.load_session()
        if not session:
            # No saved session, show welcome screen
            self.show_placeholder_screen(
                "Welcome to CompTIA A+ Study Suite!\nSelect an option from the sidebar to begin.",
            )
            return

        session_type = session.get("session_type")
        session_info = self.session_manager.get_session_info()

        if session_type == "flashcard" and session_info:
            # Show recovery dialog
            self.show_session_recovery_dialog(session)
        else:
            # Unknown session type or error, clear it
            self.session_manager.clear_session()
            self.show_placeholder_screen(
                "Welcome to CompTIA A+ Study Suite!\nSelect an option from the sidebar to begin.",
            )

    def show_session_recovery_dialog(self, session):
        """
        Display a dialog asking user if they want to resume the interrupted session.
        """
        session_info = self.session_manager.get_session_info()
        session_data = session.get("data", {})

        dialog = ctk.CTkToplevel(self)
        dialog.title("Resume Session?")
        dialog.geometry("400x220")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Message
        msg_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        msg_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            msg_frame,
            text="📚 Flashcard Session Found",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 10))

        desc_text = (
            f"You had an interrupted study session\n"
            f"from {session_info['time']}.\n\n"
            f"Study Mode: {session_data.get('study_mode', 'unknown').title()}\n"
            f"Cards Studied: {len(session_data.get('cards_studied', []))}\n"
            f"Score: {session_data.get('score_known', 0)} known"
        )
        desc_label = ctk.CTkLabel(
            msg_frame,
            text=desc_text,
            text_color="gray",
            wraplength=360,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 20))

        # Buttons
        btn_frame = ctk.CTkFrame(msg_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))

        def resume():
            self.start_flashcard_session(None, recovered_session=session)
            dialog.destroy()

        def skip():
            self.session_manager.clear_session()
            self.show_placeholder_screen(
                "Welcome to CompTIA A+ Study Suite!\nSelect an option from the sidebar to begin.",
            )
            dialog.destroy()

        btn_resume = ctk.CTkButton(
            btn_frame,
            text="Resume Session",
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=resume
        )
        btn_resume.pack(side="right", padx=(5, 0))

        btn_skip = ctk.CTkButton(
            btn_frame,
            text="Start Fresh",
            fg_color="#555",
            hover_color="#444",
            command=skip
        )
        btn_skip.pack(side="right", padx=5)

    def create_sidebar(self):
        """
        Creates the persistent left navigation menu
        :param self: PARAMETER UNDEFINED
        :return:
        """
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")

        # App Title Header
        title_label = ctk.CTkLabel(
            sidebar,
            text="A+ Study Suite",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")

        # --- SECTION 1: STUDY MENU --- #
        study_label = ctk.CTkLabel(
            sidebar,
            text="1. STUDY",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        study_label.grid(row=1, column=0, padx=20, pady=(15,5), sticky="w")

        btn_goals = ctk.CTkButton(
            sidebar,
            text="  📊 Goals & Progress",
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(GoalsView)
        )
        btn_goals.grid(row=2, column=0, padx=10, pady=2, sticky="ew")

        btn_notes = ctk.CTkButton(
            sidebar, text="  💠 Select Objectives", anchor="w", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(NotesView)
        )
        btn_notes.grid(row=3, column=0, padx=10, pady=2, sticky="ew")

        btn_flashcards = ctk.CTkButton(
            sidebar,
            text="  💠 Flash Cards",
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.start_flashcards_setup
        )
        btn_flashcards.grid(row=4, column=0, padx=10, pady=2, sticky="ew")

        btn_diagram = ctk.CTkButton(
            sidebar, text="  💠 Motherboard Diagram", anchor="w", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(DiagramView)
        )
        btn_diagram.grid(row=5, column=0, padx=10, pady=2, sticky="ew")

        # --- SECTION 2: PRACTICE MENU ---
        practice_label = ctk.CTkLabel(
            sidebar,
            text="2. PRACTICE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        practice_label.grid(row=6, column=0, padx=20, pady=(20, 5), sticky="w")

        btn_select_exam = ctk.CTkButton(
            sidebar,
            text="  💠 Select Exam",
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(ExamView)
        )
        btn_select_exam.grid(row=7, column=0, padx=10, pady=2, sticky="ew")

        btn_custom_exam = ctk.CTkButton(
            sidebar, text="  💠 Custom Objectives", anchor="w", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(CustomExamView)
        )
        btn_custom_exam.grid(row=8, column=0, padx=10, pady=2, sticky="ew")

        btn_guessing = ctk.CTkButton(
            sidebar,
            text="  💠 Hardware Game",
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(GameView)
        )
        btn_guessing.grid(row=9, column=0, padx=10, pady=2, sticky="ew")

        # --- SECTION 3: DEV TOOLS ---
        dev_tools_label = ctk.CTkLabel(
            sidebar,
            text="3. DEV TOOLS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        dev_tools_label.grid(row=10, column=0, padx=20, pady=(20, 5), sticky="w")

        btn_dev_notes = ctk.CTkButton(
            sidebar,
            text="  📝 Notes",
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(DevToolsView)
        )
        btn_dev_notes.grid(row=11, column=0, padx=10, pady=2, sticky="ew")

        # --- SECTION 4: SETTINGS ---
        settings_label = ctk.CTkLabel(
            sidebar,
            text="4. SETTINGS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        settings_label.grid(row=12, column=0, padx=20, pady=(20, 5), sticky="w")

        btn_settings = ctk.CTkButton(
            sidebar,
            text="  ⚙️ Options",
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=lambda: self.switch_frame(SettingsView)
        )
        btn_settings.grid(row=13, column=0, padx=10, pady=2, sticky="ew")

    def start_flashcards_setup(self):
        """
        Display the flashcard setup screen instead of directly loading flashcards.
        """
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = FlashcardSetupView(
            self,
            on_start_callback=self.start_flashcard_session
        )
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def start_flashcard_session(self, config, recovered_session=None):
        """
        Start the actual flashcard session with the provided configuration.
        :param config: dict with 'exam', 'objectives', 'card_limit' keys
        :param recovered_session: optional dict of recovered session state for resume
        """
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = FlashcardView(self, config=config, recovered_session=recovered_session)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def switch_frame(self, new_frame_class, *args, **kwargs):
        """
        Swaps the current center view with a new CTkFrame view.
        :param self:
        :param new_frame_class:
        :param args:
        :param kwargs:
        """
        if self.current_frame is not None:
            self.current_frame.destroy() # Clear existing view

        self.current_frame = new_frame_class(self, *args, **kwargs)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_placeholder_screen(self, title_text):
        """
        Temporary helper to display placeholder content when menu items are clicked.
        :param self:
        :param title_text:
        """

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        label = ctk.CTkLabel(
            self.current_frame,
            text=title_text,
            font=CTkFont(size=22, weight="bold")
        )
        label.pack(expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
