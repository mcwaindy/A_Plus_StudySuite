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

        self.parent = parent
        self.on_component_selected = on_component_selected

        # State
        self.board_info = {}
        self.selected_component = None
        self.zoom_level = 1.0
        self.show_highlights = True
        self.is_destroyed = False  # Flag to prevent callbacks on destroyed widgets

        # Store original image for magnifier
        self.pil_original_img = None

        # Image display dimensions and position (for non-scrollable centered layout)
        self.displayed_image_width = 0
        self.displayed_image_height = 0
        self.image_display_x = 0
        self.image_display_y = 0
        self.image_item = None
        self.tk_img = None

        # Translator helper
        self.translator = CoordinateTranslator()

        # Layout Setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_canvas()

    def destroy(self):
        """Cleanup before widget is destroyed to prevent callback errors."""
        self.is_destroyed = True
        if self.canvas:
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Configure>")
        super().destroy()

    def create_canvas(self):
        """Builds Tkinter canvas with optional scrollbars and centered image."""
        # Scrollbar setup
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

        # Mouse motion for magnifier
        self.canvas.bind("<Motion>", self._on_mouse_motion)

        # Bind canvas resize to recenter image
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def load_board(self, board_info, zoom_level=1.0, selected_comp=None, apply_display_scale=True):
        """Renders motherboard image centered, with scrolling available if image is larger than canvas.

        Args:
            board_info: Board definition dict
            zoom_level: Zoom multiplier (default 1.0)
            selected_comp: Optional component to highlight
            apply_display_scale: If True, applies per-board display_scale; if False, ignores it (default True)
        """
        # Guard: check if widget is still valid before proceeding
        if self.is_destroyed or not self.winfo_exists():
            return

        self.board_info = board_info
        self.zoom_level = zoom_level
        self.selected_component = selected_comp

        if not board_info:
            return

        img_path = Path(board_info.get("image_path", ""))
        resolution = board_info.get("resolution", [908, 871])
        flipped = board_info.get("flipped", False)
        # Only apply display_scale if requested
        display_scale = board_info.get("display_scale", 1.0) if apply_display_scale else 1.0

        self.translator.orig_w, self.translator.orig_h = resolution

        if not img_path.exists():
            if self.canvas and self.winfo_exists():
                self.canvas.delete("all")
                self.canvas.create_text(
                    200,
                    200,
                    text=f"Image not found:\n{img_path}",
                    fill="#D32F2F",
                    font=("Arial", 14),
                )
            return

        # Calculate responsive base height from actual container dimensions
        # Get canvas actual dimensions (after widget layout)
        if not self.canvas or not self.winfo_exists():
            return

        canvas_height = self.canvas.winfo_height()

        # If canvas height not yet initialized (< 2px), use a reasonable default
        # This happens during initial widget creation before geometry manager finishes
        if canvas_height < 2:
            canvas_height = 400  # Fallback for initialization phase

        # Set translator base height to fit the container with padding
        # Leave 20px padding top/bottom for margins
        available_height = max(100, canvas_height - 40)
        self.translator.set_base_height(available_height)

        # Apply combined zoom and display scale
        effective_zoom = zoom_level * display_scale
        disp_w, disp_h = self.translator.get_display_dimensions(effective_zoom)

        # Resize Image
        pil_img = Image.open(img_path)
        self.pil_original_img = pil_img  # Store for magnifier

        # Apply horizontal flip if needed
        if flipped:
            pil_img = pil_img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        pil_resized = pil_img.resize(
            (disp_w, disp_h), Image.Resampling.LANCZOS
        )
        self.tk_img = ImageTk.PhotoImage(pil_resized)

        # Update parent's original image reference
        if hasattr(self.parent, 'pil_original_img'):
            self.parent.pil_original_img = self.pil_original_img
            self.parent.current_board_info = board_info

        self.canvas.delete("all")

        # Store image display dimensions
        self.displayed_image_width = disp_w
        self.displayed_image_height = disp_h

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # If canvas not fully initialized yet, use a reasonable default
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 600
            canvas_height = 500

        # Center image on canvas, creating scroll region that allows panning
        center_x = max(disp_w // 2, canvas_width // 2)
        center_y = max(disp_h // 2, canvas_height // 2)

        # Create image centered in scroll region
        self.image_item = self.canvas.create_image(
            center_x, center_y,
            image=self.tk_img,
            tags="image"
        )

        # Store image position for coordinate calculations
        self.image_display_x = center_x
        self.image_display_y = center_y

        # Set scroll region to allow panning if image is larger than canvas
        scroll_left = center_x - canvas_width // 2
        scroll_top = center_y - canvas_height // 2
        scroll_right = center_x + canvas_width // 2
        scroll_bottom = center_y + canvas_height // 2

        # Expand scroll region to include full image even if smaller than canvas
        scroll_left = min(scroll_left, 0)
        scroll_top = min(scroll_top, 0)
        scroll_right = max(scroll_right, disp_w)
        scroll_bottom = max(scroll_bottom, disp_h)

        self.canvas.config(scrollregion=(scroll_left, scroll_top, scroll_right, scroll_bottom))

        # Render Hotspots
        self.render_hotspots(board_info.get("components", []))

        # If canvas wasn't fully initialized, schedule a refresh after layout completes
        if self.canvas.winfo_height() < 2:
            self.after_idle(lambda: self.load_board(board_info, zoom_level, selected_comp, apply_display_scale))

    def _on_canvas_resize(self, event=None):
        """Handle canvas resize - scroll region needs to be recalculated."""
        # The image position should remain the same, but scroll region might need adjustment
        pass

    def render_hotspots(self, components):
        """Draws bounding boxes over components if highlights are enabled."""
        if not self.show_highlights:
            return

        # Get display scale from current board
        display_scale = self.board_info.get("display_scale", 1.0) if self.board_info else 1.0
        effective_zoom = self.zoom_level * display_scale

        for comp in components:
            coords = comp.get("coords", [0, 0, 0, 0])
            x1, y1, x2, y2 = self.translator.native_to_canvas(
                coords, effective_zoom, offset=(0, 0)
            )

            # Offset coordinates to account for centered image position
            # The image is centered, so we subtract half the image dimensions from center
            x1 += self.image_display_x - self.displayed_image_width // 2
            y1 += self.image_display_y - self.displayed_image_height // 2
            x2 += self.image_display_x - self.displayed_image_width // 2
            y2 += self.image_display_y - self.displayed_image_height // 2

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
        # Guard: check if widget is still valid
        if self.is_destroyed or not self.winfo_exists():
            return
        # Convert event coordinates to canvas coordinates (accounts for scroll)
        click_x = self.canvas.canvasx(event.x)
        click_y = self.canvas.canvasy(event.y)
        self._check_hotspot_click(click_x, click_y)

    def _on_left_drag(self, event):
        pass

    def _on_left_release(self, event):
        pass

    def _check_hotspot_click(self, click_x, click_y):
        # Guard: check if widget is still valid
        if self.is_destroyed or not self.winfo_exists():
            return

        components = self.board_info.get("components", [])

        # Get display scale from current board
        display_scale = self.board_info.get("display_scale", 1.0) if self.board_info else 1.0
        effective_zoom = self.zoom_level * display_scale

        for comp in components:
            coords = comp.get("coords", [0, 0, 0, 0])
            x1, y1, x2, y2 = self.translator.native_to_canvas(
                coords, effective_zoom, offset=(0, 0)
            )

            # Offset coordinates to account for centered image position
            x1 += self.image_display_x - self.displayed_image_width // 2
            y1 += self.image_display_y - self.displayed_image_height // 2
            x2 += self.image_display_x - self.displayed_image_width // 2
            y2 += self.image_display_y - self.displayed_image_height // 2

            if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                self.selected_component = comp
                if self.on_component_selected:
                    self.on_component_selected(comp)
                self.load_board(
                    self.board_info, self.zoom_level, self.selected_component
                )

    def get_magnified_region(self, viewport_x, viewport_y, magnification, output_size):
        """Get a magnified PIL Image of the region around a viewport coordinate.

        viewport_x, viewport_y are event coordinates that need to be converted to canvas coordinates.

        Args:
            viewport_x, viewport_y: Coordinates on the viewport (from event.x, event.y)
            magnification: How much to zoom (e.g., 2.5 = 2.5x magnification)
            output_size: (width, height) tuple for the output image

        Returns:
            PIL Image of the magnified region, or None if out of bounds
        """
        if not self.pil_original_img or not self.board_info:
            return None

        # Convert viewport coordinates to canvas coordinates (accounts for scroll)
        canvas_x = self.canvas.canvasx(viewport_x)
        canvas_y = self.canvas.canvasy(viewport_y)

        # Calculate image bounds on canvas
        img_left = self.image_display_x - self.displayed_image_width // 2
        img_top = self.image_display_y - self.displayed_image_height // 2
        img_right = img_left + self.displayed_image_width
        img_bottom = img_top + self.displayed_image_height

        # Check if cursor is over the image
        if canvas_x < img_left or canvas_x >= img_right or canvas_y < img_top or canvas_y >= img_bottom:
            return None

        # Get position relative to displayed image
        rel_x = canvas_x - img_left
        rel_y = canvas_y - img_top

        # Get the displayed image dimensions
        disp_w = self.displayed_image_width
        disp_h = self.displayed_image_height

        # Calculate crop region size in displayed coordinates
        crop_width = int(output_size[0] / magnification)
        crop_height = int(output_size[1] / magnification)

        # Center crop on cursor position
        crop_left = int(rel_x - crop_width / 2)
        crop_top = int(rel_y - crop_height / 2)
        crop_right = crop_left + crop_width
        crop_bottom = crop_top + crop_height

        # Track where the cursor actually is relative to the ideal crop
        cursor_in_crop_x = crop_width / 2
        cursor_in_crop_y = crop_height / 2

        # Clamp to image bounds and track the offset
        if crop_left < 0:
            cursor_in_crop_x = rel_x  # Cursor is offset from left edge
            crop_left = 0
            crop_right = crop_width
        elif crop_right > disp_w:
            cursor_in_crop_x = rel_x - (disp_w - crop_width)  # Cursor is offset from right edge
            crop_right = disp_w
            crop_left = max(0, crop_right - crop_width)

        if crop_top < 0:
            cursor_in_crop_y = rel_y  # Cursor is offset from top edge
            crop_top = 0
            crop_bottom = crop_height
        elif crop_bottom > disp_h:
            cursor_in_crop_y = rel_y - (disp_h - crop_height)  # Cursor is offset from bottom edge
            crop_bottom = disp_h
            crop_top = max(0, crop_bottom - crop_height)

        # Validate crop
        if crop_right <= crop_left or crop_bottom <= crop_top:
            return None

        try:
            # Scale crop coordinates from displayed to original image
            resolution = self.board_info.get("resolution", [908, 871])
            orig_w, orig_h = resolution
            scale_x = orig_w / disp_w
            scale_y = orig_h / disp_h

            orig_crop_left = int(crop_left * scale_x)
            orig_crop_top = int(crop_top * scale_y)
            orig_crop_right = int(crop_right * scale_x)
            orig_crop_bottom = int(crop_bottom * scale_y)

            # Clamp to original image bounds
            orig_crop_left = max(0, min(orig_crop_left, orig_w - 1))
            orig_crop_top = max(0, min(orig_crop_top, orig_h - 1))
            orig_crop_right = max(orig_crop_left + 1, min(orig_crop_right, orig_w))
            orig_crop_bottom = max(orig_crop_top + 1, min(orig_crop_bottom, orig_h))

            # Crop from original image and resize to output
            cropped = self.pil_original_img.crop((orig_crop_left, orig_crop_top, orig_crop_right, orig_crop_bottom))
            magnified = cropped.resize(output_size, Image.Resampling.LANCZOS)

            # Position crosshair based on cursor location within the cropped region
            # Scale the cursor position from displayed coordinates to output image coordinates
            scale_display_to_output_x = output_size[0] / (crop_right - crop_left)
            scale_display_to_output_y = output_size[1] / (crop_bottom - crop_top)

            cursor_display_x = int(cursor_in_crop_x * scale_display_to_output_x)
            cursor_display_y = int(cursor_in_crop_y * scale_display_to_output_y)

            # Clamp to output bounds to ensure crosshair stays visible
            cursor_display_x = max(0, min(cursor_display_x, output_size[0] - 1))
            cursor_display_y = max(0, min(cursor_display_y, output_size[1] - 1))

            magnified.crosshair_x = cursor_display_x
            magnified.crosshair_y = cursor_display_y

            return magnified
        except Exception as e:
            print(f"Error creating magnified region: {e}")
            return None

    def _on_mouse_motion(self, event):
        """Updates magnifier view on mouse motion."""
        if self.is_destroyed or not self.winfo_exists():
            return
        if hasattr(self.parent, 'update_magnifier'):
            # Pass viewport coordinates; magnifier will convert to canvas coords
            self.parent.update_magnifier(event.x, event.y, self.board_info)