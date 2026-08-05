"""
Diagram View - Interactive motherboard diagram viewer with component details.

Displays motherboard images with clickable component hotspots, zoom/pan controls,
and component information panels.
"""

import customtkinter as ctk
from pathlib import Path
from typing import Optional, Dict, Any

from modules.diagram.canvas_widget import DiagramCanvasWidget
from utils.board_registry import BoardRegistry


class DiagramView(ctk.CTkFrame):
    """Main view for interactive motherboard diagram display."""

    def __init__(self, parent):
        super().__init__(parent)

        # State
        self.registry = BoardRegistry()
        self.current_board_key: str = "micro_atx"
        self.selected_component: Optional[Dict[str, Any]] = None
        self.zoom_level: float = 1.0

        # Magnifier state
        self.magnifier_zoom = 2.5
        self.magnifier_size = 250
        self.pil_original_img = None
        self.current_board_info = None

        # Get available boards
        board_keys = self.registry.get_board_keys()
        if not board_keys:
            print("❌ No boards available in registry")
            return

        if self.current_board_key not in board_keys:
            self.current_board_key = board_keys[0]

        # Grid Configuration
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # Build UI
        self.create_header()
        self.create_canvas_widget()
        self.create_info_panel()

        # Load and display initial board
        self.refresh_display()

    def create_header(self) -> None:
        """Create the top action bar with board selection and zoom controls."""
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

        board_names = [self.registry.get_board_display_name(key) for key in self.registry.get_board_keys()]
        self.board_menu = ctk.CTkOptionMenu(
            header_frame,
            values=board_names,
            command=self.on_board_changed,
        )
        self.board_menu.pack(side="left", padx=(0, 20))
        if board_names:
            self.board_menu.set(board_names[0])

        # Zoom controls
        zoom_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        zoom_frame.pack(side="left", padx=10)

        btn_zoom_out = ctk.CTkButton(
            zoom_frame,
            text="−",
            width=35,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: self.adjust_zoom(-0.05),
        )
        btn_zoom_out.pack(side="left", padx=2)

        self.lbl_zoom = ctk.CTkLabel(
            zoom_frame,
            text=f"{self.zoom_level:.0%}",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.lbl_zoom.pack(side="left", padx=5)

        btn_zoom_in = ctk.CTkButton(
            zoom_frame,
            text="+",
            width=35,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: self.adjust_zoom(0.05),
        )
        btn_zoom_in.pack(side="left", padx=2)

        btn_fit = ctk.CTkButton(
            zoom_frame, text="Fit Window", width=80, command=self.fit_to_window
        )
        btn_fit.pack(side="left", padx=(5, 0))

        # Highlights toggle
        highlight_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        highlight_frame.pack(side="left", padx=10)

        lbl_highlights = ctk.CTkLabel(highlight_frame, text="Show Highlights:")
        lbl_highlights.pack(side="left", padx=(0, 5))

        self.switch_highlights = ctk.CTkSwitch(
            highlight_frame,
            text="",
            command=self.toggle_highlights,
        )
        self.switch_highlights.pack(side="left")
        self.switch_highlights.select()

        # Spacer to push admin tools to the right
        spacer = ctk.CTkLabel(header_frame, text="", fg_color="transparent")
        spacer.pack(side="left", expand=True)

        # Admin tools (right side)
        admin_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        admin_frame.pack(side="right", padx=10)

        btn_coord_picker = ctk.CTkButton(
            admin_frame,
            text="🔧 Edit Coordinates",
            command=self.open_coordinate_picker,
            fg_color="#FF9800",
            hover_color="#F57C00",
            font=ctk.CTkFont(size=11),
        )
        btn_coord_picker.pack(side="left", padx=5)

    def create_canvas_widget(self) -> None:
        """Create the canvas widget for displaying the motherboard image."""
        self.canvas_widget = DiagramCanvasWidget(
            self, on_component_selected=self.on_component_selected
        )
        self.canvas_widget.grid(
            row=1, column=0, sticky="nsew", padx=15, pady=15
        )

    def create_info_panel(self) -> None:
        """Create the right-hand details panel."""
        self.info_panel = ctk.CTkFrame(self, corner_radius=10)
        self.info_panel.grid(
            row=1, column=1, sticky="nsew", padx=(0, 15), pady=15
        )
        self.info_panel.grid_columnconfigure(0, weight=1)
        self.info_panel.grid_rowconfigure(2, weight=1)

        # Summary Section
        self.lbl_comp_name = ctk.CTkLabel(
            self.info_panel,
            text="Select a Component",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_comp_name.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))

        self.txt_summary = ctk.CTkTextbox(self.info_panel, height=150)
        self.txt_summary.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 15))
        self.txt_summary.insert("1.0", "No component selected.")
        self.txt_summary.configure(state="disabled")

    def on_board_changed(self, display_name: str) -> None:
        """Handle board selection change."""
        # Find board key from display name
        for key in self.registry.get_board_keys():
            if self.registry.get_board_display_name(key) == display_name:
                self.current_board_key = key
                self.selected_component = None
                self.refresh_display()
                break

    def refresh_display(self) -> None:
        """Refresh the canvas with the current board."""
        board = self.registry.get_board(self.current_board_key)
        if not board:
            print(f"❌ Board '{self.current_board_key}' not found")
            return

        self.current_board_info = board
        self.canvas_widget.load_board(
            board, self.zoom_level, self.selected_component
        )

    def on_component_selected(self, comp: Dict[str, Any]) -> None:
        """Callback when a component hotspot is clicked."""
        self.selected_component = comp
        self.lbl_comp_name.configure(text=comp.get("name", "Unknown"))

        self.txt_summary.configure(state="normal")
        self.txt_summary.delete("1.0", "end")
        self.txt_summary.insert(
            "1.0", comp.get("summary", "No details available.")
        )
        self.txt_summary.configure(state="disabled")

    def toggle_highlights(self) -> None:
        """Toggle component highlights on/off."""
        is_enabled = bool(self.switch_highlights.get())
        self.canvas_widget.show_highlights = is_enabled
        self.refresh_display()

    def adjust_zoom(self, delta: float) -> None:
        """Adjust zoom level by percentage increment (typically ±0.05 = ±5%)."""
        self.zoom_level = max(0.1, min(3.0, self.zoom_level + delta))
        self.lbl_zoom.configure(text=f"{self.zoom_level:.0%}")
        self.refresh_display()

    def fit_to_window(self) -> None:
        """Reset zoom to 1.0 (fit the image to available container space)."""
        self.zoom_level = 1.0
        self.lbl_zoom.configure(text="100%")
        self.refresh_display()

    def on_magnifier_resize(self, event=None) -> None:
        """Handle magnifier canvas resize."""
        self.magnifier_size = min(event.width, event.height) if event else 250

    def open_coordinate_picker(self) -> None:
        """Open the coordinate picker in a modal window."""
        import subprocess
        import sys
        from pathlib import Path

        # Launch standalone picker in a separate process
        try:
            picker_script = Path(__file__).parent.parent / "tools" / "coordinate_picker.py"
            subprocess.Popen(
                [sys.executable, str(picker_script)],
                cwd=Path(__file__).parent.parent
            )
        except Exception as e:
            print(f"Error opening coordinate picker: {e}")
