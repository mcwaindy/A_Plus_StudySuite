from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk
from utils.coordinate_translator import CoordinateTranslator


class DiagramCanvasWidget(ctk.CTkFrame):
    """Reusable interactive Motherboard Canvas widget managing image scaling,

    hotspot rendering, drag-panning, and coordinate picker debug actions.
    """

    def __init__(self, parent, on_component_selected=None):
        super().__init__(parent, fg_color=("gray90", "gray15"))

        self.on_component_selected = on_component_selected

        # State
        self.board_info = {}
        self.selected_component = None
        self.zoom_level = 1.0
        self.debug_mode = True

        # Debug drag tracking
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.temp_rect = None

        # Translator helper
        self.translator = CoordinateTranslator()

        # Layout Setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_canvas()

    def create_canvas(self):
        """Builds Tkinter canvas and attaches scrollbars + mouse bindings."""
        self.v_scrollbar = ctk.CTkScrollbar(self, orientation="vertical")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        self.h_scrollbar = ctk.CTkScrollbar(self, orientation="horizontal")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas = ctk.CTkCanvas(
            self,
            bg="#1E1E1E",
            highlightthickness=0,
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.v_scrollbar.configure(command=self.canvas.yview)
        self.h_scrollbar.configure(command=self.canvas.xview)

        # Mouse Bindings
        self.canvas.bind("<ButtonPress-1>", self._on_left_press)
        self.canvas.bind("<B1-Motion>", self._on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_left_release)

        # Right-click drag to pan
        self.canvas.bind(
            "<ButtonPress-3>", lambda e: self.canvas.scan_mark(e.x, e.y)
        )
        self.canvas.bind(
            "<B3-Motion>", lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1)
        )

    def load_board(self, board_info, zoom_level=1.0, selected_comp=None):
        """Renders motherboard image and scales hotspots for given board_info."""
        self.board_info = board_info
        self.zoom_level = zoom_level
        self.selected_component = selected_comp

        if not board_info:
            return

        img_path = Path(board_info.get("image_path", ""))
        resolution = board_info.get("resolution", [908, 871])
        self.translator.orig_w, self.translator.orig_h = resolution

        if not img_path.exists():
            self.canvas.delete("all")
            self.canvas.create_text(
                200,
                200,
                text=f"Image not found:\n{img_path}",
                fill="#D32F2F",
                font=("Arial", 14),
            )
            return

        disp_w, disp_h = self.translator.get_display_dimensions(zoom_level)

        # Resize Image
        pil_img = Image.open(img_path)
        pil_resized = pil_img.resize(
            (disp_w, disp_h), Image.Resampling.LANCZOS
        )
        self.tk_img = ImageTk.PhotoImage(pil_resized)

        self.canvas.delete("all")
        self.canvas.create_image(10, 10, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=(0, 0, disp_w + 20, disp_h + 20))

        # Render Hotspots
        self.render_hotspots(board_info.get("components", []))

    def render_hotspots(self, components):
        """Draws bounding boxes over components."""
        for comp in components:
            coords = comp.get("coords", [0, 0, 0, 0])
            x1, y1, x2, y2 = self.translator.native_to_canvas(
                coords, self.zoom_level
            )

            is_selected = (
                self.selected_component
                and self.selected_component["id"] == comp["id"]
            )
            outline_color = "#10B981" if is_selected else "#3B82F6"
            width = 3 if is_selected else 2

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                outline=outline_color,
                width=width,
                tags=(comp["id"], "hotspot"),
            )

    # --- EVENT HANDLERS --- #
    def _on_left_press(self, event):
        click_x = self.canvas.canvasx(event.x)
        click_y = self.canvas.canvasy(event.y)

        if self.debug_mode:
            self.drag_start_x = click_x
            self.drag_start_y = click_y
            if self.temp_rect:
                self.canvas.delete(self.temp_rect)
            self.temp_rect = self.canvas.create_rectangle(
                click_x,
                click_y,
                click_x,
                click_y,
                outline="#EF4444",
                width=2,
                dash=(4, 4),
            )
        else:
            self._check_hotspot_click(click_x, click_y)

    def _on_left_drag(self, event):
        if self.debug_mode and self.temp_rect:
            current_x = self.canvas.canvasx(event.x)
            current_y = self.canvas.canvasy(event.y)
            self.canvas.coords(
                self.temp_rect,
                self.drag_start_x,
                self.drag_start_y,
                current_x,
                current_y,
            )

    def _on_left_release(self, event):
        if self.debug_mode and self.temp_rect:
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)

            x1_canvas = min(self.drag_start_x, end_x)
            y1_canvas = min(self.drag_start_y, end_y)
            x2_canvas = max(self.drag_start_x, end_x)
            y2_canvas = max(self.drag_start_y, end_y)

            if (x2_canvas - x1_canvas) < 5 or (y2_canvas - y1_canvas) < 5:
                return

            native_coords = self.translator.canvas_to_native(
                [x1_canvas, y1_canvas, x2_canvas, y2_canvas], self.zoom_level
            )

            print("\n🎯 --- NEW HOTSPOT COORDINATES ---")
            print(f'"coords": {native_coords}')
            print("------------------------------------\n")

    def _check_hotspot_click(self, click_x, click_y):
        components = self.board_info.get("components", [])

        for comp in components:
            coords = comp.get("coords", [0, 0, 0, 0])
            x1, y1, x2, y2 = self.translator.native_to_canvas(
                coords, self.zoom_level
            )

            if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                self.selected_component = comp
                if self.on_component_selected:
                    self.on_component_selected(comp)
                self.load_board(
                    self.board_info, self.zoom_level, self.selected_component
                )
                return