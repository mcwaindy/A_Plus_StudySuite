import customtkinter as ctk
from customtkinter import CTkFont

# --- MODULES --- #
from modules.flashcards_view import FlashcardView
from modules.notes_view import NotesView
from modules.diagram_view import DiagramView
from modules.exam_view import ExamView
from modules.custom_exam_view import CustomExamView
from modules.game_view import GameView

# Set dark mode theme and default color scheme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    """
    Main Application Window setup and screen manager
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

        # Build UI Elements
        self.create_sidebar()

        # Content Area Container
        self.current_frame = None
        self.show_placeholder_screen(
            "Welcome to CompTIA A+ Study Suite!\nSelect an option from the sidebar to begin.",
        )

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
            command=lambda: self.switch_frame(FlashcardView)
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
