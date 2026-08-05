import json
import random
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk
from modules.diagram.canvas_widget import DiagramCanvasWidget
from utils import image_library
from utils.paths import project_path


class GameView(ctk.CTkFrame):
    """Rapid-fire Hardware Identification Mini-Game supporting both interactive

    motherboard clicking and stand-alone hardware image identification (cables, printers, connectors).
    """

    MIXED_CATEGORY = "All Hardware Mix"
    BOARD_CATEGORY = "Motherboard Layout"

    def __init__(self, parent):
        super().__init__(parent)

        self.nodes_file = project_path("data", "motherboard", "motherboard_nodes.json")

        self.all_boards_data = {}
        # Maps the dropdown's display label back to its catalog category key.
        self.category_keys = {}

        # Game Settings Defaults
        self.sec_per_question = 10
        self.selected_category = self.MIXED_CATEGORY

        # Game State
        self.round_deck = []  # Mix of items/components
        self.current_round_idx = 0
        self.current_item = None
        self.score = 0
        self.streak = 0
        self.time_left_ms = 0
        self.timer_job = None
        self.game_active = False

        # Grid Setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Load Data
        self.load_all_data()

        # Show Setup Menu First
        self.show_setup_screen()

    # --- SETUP SCREEN --- #
    def show_setup_screen(self):
        """Displays customizable mini-game setup menu."""
        self.stop_timer()
        self.game_active = False

        for child in self.winfo_children():
            child.destroy()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Title Header
        lbl_title = ctk.CTkLabel(
            self,
            text="⚡ Hardware Identification Sprint",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        lbl_title.pack(padx=20, pady=(25, 5))

        lbl_subtitle = ctk.CTkLabel(
            self,
            text="Identify motherboard components, network cables, printer parts, and connectors under time pressure!",
            font=ctk.CTkFont(size=13),
            text_color="gray60",
        )
        lbl_subtitle.pack(padx=20, pady=(0, 20))

        # Setup Card
        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(expand=True, fill="both", padx=60, pady=(0, 20))
        card.grid_columnconfigure((0, 1), weight=1)

        # Option 1: Category Selection
        lbl_cat = ctk.CTkLabel(
            card,
            text="1. Hardware Category:",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        lbl_cat.grid(row=0, column=0, sticky="w", padx=25, pady=(20, 10))

        self.category_menu = ctk.CTkOptionMenu(
            card,
            values=self.build_category_options(),
            width=250,
        )
        self.category_menu.set(self.MIXED_CATEGORY)
        self.category_menu.grid(
            row=0, column=1, sticky="e", padx=25, pady=(20, 10)
        )

        # Option 2: Round Speed
        lbl_speed = ctk.CTkLabel(
            card,
            text="2. Time Limit Per Round:",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        lbl_speed.grid(row=1, column=0, sticky="w", padx=25, pady=15)

        self.speed_menu = ctk.CTkOptionMenu(
            card,
            values=[
                "5 Seconds (Expert)",
                "10 Seconds (Standard)",
                "15 Seconds (Relaxed)",
                "30 Seconds (Practice)",
            ],
            width=250,
        )
        self.speed_menu.set("10 Seconds (Standard)")
        self.speed_menu.grid(row=1, column=1, sticky="e", padx=25, pady=15)

        # Start Game Button
        btn_start = ctk.CTkButton(
            card,
            text="🎮 Start Game",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#10B981",
            hover_color="#059669",
            command=self.start_game,
        )
        btn_start.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=25, pady=(25, 20)
        )

    # --- ACTIVE GAME ENGINE --- #
    def start_game(self):
        """Builds round deck based on chosen category and launches view."""
        self.selected_category = self.category_menu.get()
        self.sec_per_question = int(self.speed_menu.get().split()[0])

        self.build_round_deck()

        if not self.round_deck:
            self.show_setup_screen()
            return

        self.current_round_idx = 0
        self.score = 0
        self.streak = 0
        self.game_active = True

        for child in self.winfo_children():
            child.destroy()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Header Info Bar
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        self.lbl_target = ctk.CTkLabel(
            self.header_frame,
            text="Identify Hardware Component",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3B82F6",
        )
        self.lbl_target.pack(side="left")

        self.lbl_score = ctk.CTkLabel(
            self.header_frame,
            text="Score: 0  |  Streak: 0🔥",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_score.pack(side="right")

        # Timer Bar
        self.timer_bar = ctk.CTkProgressBar(self.header_frame, height=8)
        self.timer_bar.pack(fill="x", pady=(8, 0), side="bottom")

        # Main Display Viewport
        self.viewport_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.viewport_frame.grid(
            row=1, column=0, sticky="nsew", padx=20, pady=(0, 15)
        )
        self.viewport_frame.grid_rowconfigure(0, weight=1)
        self.viewport_frame.grid_columnconfigure(0, weight=1)

        self.next_round()

    def build_category_options(self):
        """Builds the dropdown values from the shared image catalog.

        Only categories that currently hold a playable item are offered, so adding
        a new category is purely a data change: create the folder, drop in the
        image, add its catalog entry. No code edit required.
        """
        options = [self.MIXED_CATEGORY, self.BOARD_CATEGORY]
        self.category_keys = {}

        for category in image_library.categories(with_quiz_items=True):
            options.append(category["label"])
            self.category_keys[category["label"]] = category["key"]

        return options

    def build_round_deck(self):
        """Combines motherboard nodes and standalone hardware images into a shuffled game deck."""
        self.round_deck = []

        # 1. Add Motherboard Components (from ALL available boards, excluding IO boards)
        if self.selected_category in (self.MIXED_CATEGORY, self.BOARD_CATEGORY):
            # Iterate through all available boards, skip IO cluster boards (rendering issues)
            for board_id, mb_info in self.all_boards_data.items():
                # Skip IO boards (they render too large)
                if "_io" in board_id.lower():
                    continue
                for comp in mb_info.get("components", []):
                    # Include board_id in the data so we know which board to render
                    comp_data = comp.copy()
                    comp_data["board_id"] = board_id
                    self.round_deck.append({"type": "motherboard", "data": comp_data})

        # 2. Add Standalone Image Items (Cables, Printers, etc.)
        if self.selected_category != self.BOARD_CATEGORY:
            category_key = self.category_keys.get(self.selected_category)
            for item in image_library.quiz_items(category_key=category_key):
                self.round_deck.append({"type": "image_item", "data": item})

        random.shuffle(self.round_deck)

    def next_round(self):
        """Renders either Motherboard Canvas or Standalone Image UI depending on deck item type."""
        if self.current_round_idx >= len(self.round_deck):
            self.end_game()
            return

        for child in self.viewport_frame.winfo_children():
            child.destroy()

        self.current_item = self.round_deck[self.current_round_idx]
        item_type = self.current_item["type"]
        data = self.current_item["data"]

        if item_type == "motherboard":
            self.render_motherboard_round(data)
        else:
            self.render_standalone_image_round(data)

        # Reset Timer
        self.time_left_ms = self.sec_per_question * 1000
        self.timer_bar.set(1.0)
        self.timer_bar.configure(progress_color="#3B82F6")
        self.start_round_timer()

    # --- RENDERER 1: MOTHERBOARD CANVAS ROUND --- #
    def render_motherboard_round(self, comp_data):
        self.lbl_target.configure(
            text=f"🎯 CLICK ON THE BOARD: {comp_data.get('name', 'Unknown')}"
        )

        # Get the board_id from component data (added during build_round_deck)
        board_id = comp_data.get("board_id", "modern_atx")
        board_info = self.all_boards_data.get(board_id, {})
        canvas_widget = DiagramCanvasWidget(
            self.viewport_frame,
            on_component_selected=self.on_board_click_answer,
        )
        canvas_widget.pack(fill="both", expand=True)
        canvas_widget.debug_mode = False
        # Game view should show boards at full size (no display_scale)
        canvas_widget.load_board(board_info, zoom_level=1.0, apply_display_scale=False)

    # --- RENDERER 2: STANDALONE HARDWARE IMAGE ROUND --- #
    def render_standalone_image_round(self, item_data):
        self.lbl_target.configure(
            text=f"🎯 WHAT COMPONENT IS THIS? ({item_data.get('category', 'Hardware')})"
        )

        container = ctk.CTkFrame(self.viewport_frame, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Load & Scale Image
        img_path = Path(item_data.get("image_path", ""))
        if img_path.exists():
            pil_img = Image.open(img_path)
            # Scale image to max ~350px viewport
            max_size = 350
            pil_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(
                light_image=pil_img, dark_image=pil_img, size=pil_img.size
            )

            lbl_img = ctk.CTkLabel(container, image=ctk_img, text="")
            lbl_img.pack(pady=(10, 15))

        # 4 Multiple Choice Option Buttons
        btn_grid = ctk.CTkFrame(container, fg_color="transparent")
        btn_grid.pack(fill="x", padx=40, pady=10)
        btn_grid.grid_columnconfigure((0, 1), weight=1)

        options = item_data.get("options", [])
        for i, opt_text in enumerate(options):
            r = i // 2
            c = i % 2
            btn = ctk.CTkButton(
                btn_grid,
                text=opt_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                height=40,
                command=lambda choice_idx=i: self.on_image_option_selected(
                    choice_idx
                ),
            )
            btn.grid(row=r, column=c, padx=10, pady=6, sticky="ew")

    # --- TIMER & SCORING HANDLERS --- #
    def start_round_timer(self):
        self.stop_timer()
        self.update_round_timer()

    def stop_timer(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None

    def update_round_timer(self):
        if not self.game_active:
            return

        self.time_left_ms -= 50
        ratio = max(0.0, self.time_left_ms / (self.sec_per_question * 1000))
        self.timer_bar.set(ratio)

        if ratio <= 0.3:
            self.timer_bar.configure(progress_color="#EF4444")

        if self.time_left_ms <= 0:
            self.register_wrong_answer()
            return

        self.timer_job = self.after(50, self.update_round_timer)

    def on_board_click_answer(self, clicked_comp):
        target_id = self.current_item["data"].get("id")
        if clicked_comp.get("id") == target_id:
            self.register_correct_answer()
        else:
            self.register_wrong_answer()

    def on_image_option_selected(self, choice_idx):
        correct_idx = self.current_item["data"].get("correct_index", 0)
        if choice_idx == correct_idx:
            self.register_correct_answer()
        else:
            self.register_wrong_answer()

    def register_correct_answer(self):
        self.stop_timer()
        self.streak += 1
        speed_bonus = int((self.time_left_ms / 1000) * 10)
        round_points = 100 + (self.streak * 20) + speed_bonus
        self.score += round_points

        self.lbl_score.configure(
            text=f"Score: {self.score} (+{round_points}) | Streak: {self.streak}🔥"
        )
        self.current_round_idx += 1
        self.next_round()

    def register_wrong_answer(self):
        self.stop_timer()
        self.streak = 0
        self.lbl_score.configure(text=f"Score: {self.score}  |  Streak: 0🔥")
        self.current_round_idx += 1
        self.next_round()

    def end_game(self):
        self.stop_timer()
        self.game_active = False

        for child in self.winfo_children():
            child.destroy()

        card = ctk.CTkFrame(self, corner_radius=15)
        card.pack(expand=True, fill="both", padx=80, pady=40)

        lbl_done = ctk.CTkLabel(
            card, text="🏆 Sprint Complete!", font=ctk.CTkFont(size=24, weight="bold")
        )
        lbl_done.pack(pady=(30, 10))

        lbl_final = ctk.CTkLabel(
            card,
            text=f"Final Score: {self.score} Points\nItems Identified: {len(self.round_deck)}",
            font=ctk.CTkFont(size=16),
            text_color="gray70",
        )
        lbl_final.pack(pady=10)

        btn_replay = ctk.CTkButton(
            card,
            text="Play Again",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.show_setup_screen,
        )
        btn_replay.pack(pady=(20, 30))

    # --- DATA LOADING --- #
    def load_all_data(self):
        if self.nodes_file.exists():
            try:
                with open(self.nodes_file, "r", encoding="utf-8") as f:
                    self.all_boards_data = json.load(f)
            except Exception as e:
                print(f"Error loading motherboard JSON: {e}")

        # Standalone hardware images come from the catalog shared with NotesView.
        # force=True so images added while the app is running are picked up.
        catalog = image_library.load_catalog(force=True)
        for warning in catalog["warnings"]:
            print(f"Image catalog: {warning}")

    def destroy(self):
        self.stop_timer()
        super().destroy()