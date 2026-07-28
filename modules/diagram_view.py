import json
from pathlib import Path
import customtkinter as ctk
from modules.diagram.canvas_widget import DiagramCanvasWidget


class DiagramView(ctk.CTkFrame):
    """Main view orchestrator for the Interactive Motherboard Diagram module."""

    def __init__(self, parent):
        super().__init__(parent)

        self.nodes_file = Path("data/motherboard/motherboard_nodes.json")
        self.all_boards_data = {}
        self.current_board_key = "modern_atx"
        self.selected_component = None
        self.zoom_level = 1.0

        # Grid Configuration
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # Build UI
        self.create_header()
        self.create_canvas_widget()
        self.create_info_panel()

        # Load Data
        self.load_all_data()
        self.refresh_display()

    def create_header(self):
        """Top action bar containing dropdown, debug toggle, and zoom controls."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5)
        )

        lbl_select = ctk.CTkLabel(
            header_frame,
            text="Select Motherboard:",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        lbl_select.pack(side="left", padx=(0, 10))

        self.board_menu = ctk.CTkOptionMenu(
            header_frame,
            values=["Modern ATX Board"],
            command=self.on_board_change,
            width=200,
        )
        self.board_menu.pack(side="left")

        # Debug Toggle
        self.switch_debug = ctk.CTkSwitch(
            header_frame,
            text="Coordinate Picker",
            command=self.toggle_debug_mode,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.switch_debug.select()
        self.switch_debug.pack(side="left", padx=15)

        # Zoom Controls
        zoom_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        zoom_frame.pack(side="right")

        btn_zoom_out = ctk.CTkButton(
            zoom_frame,
            text="-",
            width=35,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: self.adjust_zoom(-0.15),
        )
        btn_zoom_out.pack(side="left", padx=2)

        self.lbl_zoom = ctk.CTkLabel(
            zoom_frame,
            text="100%",
            width=50,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.lbl_zoom.pack(side="left", padx=5)

        btn_zoom_in = ctk.CTkButton(
            zoom_frame,
            text="+",
            width=35,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: self.adjust_zoom(0.15),
        )
        btn_zoom_in.pack(side="left", padx=2)

        btn_reset = ctk.CTkButton(
            zoom_frame, text="Reset", width=60, command=self.reset_zoom
        )
        btn_reset.pack(side="left", padx=(5, 0))

    def create_canvas_widget(self):
        """Instantiates the modular canvas widget."""
        self.canvas_widget = DiagramCanvasWidget(
            self, on_component_selected=self.on_component_selected
        )
        self.canvas_widget.grid(
            row=1, column=0, sticky="nsew", padx=15, pady=15
        )

    def create_info_panel(self):
        """Creates the right-hand details panel."""
        self.info_panel = ctk.CTkFrame(self, corner_radius=10)
        self.info_panel.grid(
            row=1, column=1, sticky="nsew", padx=(0, 15), pady=15
        )
        self.info_panel.grid_columnconfigure(0, weight=1)

        self.lbl_comp_name = ctk.CTkLabel(
            self.info_panel,
            text="Select a Component",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.lbl_comp_name.pack(fill="x", padx=20, pady=(20, 5))

        ctk.CTkFrame(self.info_panel, height=2, fg_color="gray30").pack(
            fill="x", padx=20, pady=5
        )

        self.txt_summary = ctk.CTkTextbox(
            self.info_panel,
            fg_color="transparent",
            font=ctk.CTkFont(size=13),
            wrap="word",
        )
        self.txt_summary.pack(fill="both", expand=True, padx=15, pady=10)
        self.txt_summary.insert(
            "1.0",
            "Click any highlighted box on the board to view component descriptions.",
        )
        self.txt_summary.configure(state="disabled")

    # --- CONTROLLER LOGIC --- #
    def load_all_data(self):
        """Loads JSON board configuration store."""
        if self.nodes_file.exists():
            try:
                with open(self.nodes_file, "r", encoding="utf-8") as f:
                    self.all_boards_data = json.load(f)
                    print(
                        f"✅ Loaded boards: {list(self.all_boards_data.keys())}"
                    )
            except Exception as e:
                print(f"❌ Error loading motherboard JSON: {e}")

    def refresh_display(self):
        """Passes active board data to the canvas widget."""
        board_info = self.all_boards_data.get(self.current_board_key, {})
        self.canvas_widget.load_board(
            board_info, self.zoom_level, self.selected_component
        )

    def on_component_selected(self, comp):
        """Callback triggered when a hotspot is clicked on the canvas."""
        self.selected_component = comp
        self.lbl_comp_name.configure(text=comp.get("name", "Unknown"))

        self.txt_summary.configure(state="normal")
        self.txt_summary.delete("1.0", "end")
        self.txt_summary.insert(
            "1.0", comp.get("summary", "No details available.")
        )
        self.txt_summary.configure(state="disabled")

    def toggle_debug_mode(self):
        """Toggles coordinate picker mode inside canvas widget."""
        is_enabled = bool(self.switch_debug.get())
        self.canvas_widget.debug_mode = is_enabled
        status = "ENABLED" if is_enabled else "DISABLED"
        print(f"🔧 Coordinate Picker Mode: {status}")

    def adjust_zoom(self, delta):
        """Adjusts zoom level between 70% and 200%."""
        new_zoom = round(self.zoom_level + delta, 2)
        if 0.70 <= new_zoom <= 2.0:
            self.zoom_level = new_zoom
            self.lbl_zoom.configure(text=f"{int(self.zoom_level * 100)}%")
            self.refresh_display()

    def reset_zoom(self):
        """Resets zoom back to baseline 100%."""
        self.zoom_level = 1.0
        self.lbl_zoom.configure(text="100%")
        self.refresh_display()

    def on_board_change(self, choice):
        """Dropdown handler for switching motherboard models."""
        if choice == "Modern ATX Board":
            self.current_board_key = "modern_atx"
        self.selected_component = None
        self.refresh_display()