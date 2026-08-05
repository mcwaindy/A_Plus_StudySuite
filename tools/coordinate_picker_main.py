"""
Coordinate Picker UI - Admin tool for measuring and mapping component hotspots.

This tool allows you to click on motherboard images to define rectangular
regions for each component. Used to generate/update the board definitions JSON.
"""

import json
import sys
from pathlib import Path
from typing import Optional, Tuple, Dict
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

# Add parent directory to path so we can import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.board_registry import BoardRegistry


class CoordinatePickerUI(ctk.CTk):
    """Interactive UI for measuring component coordinates on motherboard images."""

    def __init__(self):
        super().__init__()

        self.title("Motherboard Coordinate Picker - Admin Tool")
        self.geometry("1400x900")
        self.minsize(1200, 800)

        # State
        self.registry = BoardRegistry()
        self.current_board_key: Optional[str] = None
        self.current_board: Optional[Dict] = None
        self.current_image_path: Optional[Path] = None
        self.pil_image: Optional[Image.Image] = None
        self.pil_image_display: Optional[Image.Image] = None
        self.tk_image: Optional[ImageTk.PhotoImage] = None

        self.picking_active = False
        self.start_point: Optional[Tuple[int, int]] = None
        self.current_point: Optional[Tuple[int, int]] = None
        self.measuring_rect: Optional[Tuple[int, int, int, int]] = None

        self.selected_component_idx: Optional[int] = None
        self.scale_factor = 1.0  # Scale between image pixels and canvas pixels

        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Build UI - Create main view FIRST so canvas and labels exist
        # when sidebar calls _on_board_selected
        self._create_main_view()
        self._create_sidebar()

    def _create_sidebar(self) -> None:
        """Create the left sidebar with board selection and component list."""
        sidebar = ctk.CTkFrame(self, width=350, fg_color="#1a1a1a")
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        sidebar.grid_rowconfigure(5, weight=1)

        # Board Selection
        lbl_board = ctk.CTkLabel(sidebar, text="Board Selection", font=("Arial", 14, "bold"))
        lbl_board.pack(padx=10, pady=(10, 5))

        board_keys = self.registry.get_board_keys()
        self.board_menu = ctk.CTkOptionMenu(
            sidebar,
            values=board_keys,
            command=self._on_board_selected
        )
        self.board_menu.pack(padx=10, pady=(0, 10), fill="x")

        # Display Scale Section (must be created BEFORE board selection callback)
        lbl_scale = ctk.CTkLabel(sidebar, text="Display Scale", font=("Arial", 12, "bold"))
        lbl_scale.pack(padx=10, pady=(10, 5))

        scale_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        scale_frame.pack(padx=10, pady=(0, 10), fill="x")

        self.scale_slider = ctk.CTkSlider(
            scale_frame,
            from_=0.25,
            to=2.0,
            command=self._on_scale_changed
        )
        self.scale_slider.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.lbl_scale_value = ctk.CTkLabel(scale_frame, text="100%", width=40, font=("Arial", 10))
        self.lbl_scale_value.pack(side="left")

        # Now set the board selection AFTER slider is created
        if board_keys:
            self.board_menu.set(board_keys[0])
            self._on_board_selected(board_keys[0])

        # Component List
        lbl_components = ctk.CTkLabel(sidebar, text="Components", font=("Arial", 14, "bold"))
        lbl_components.pack(padx=10, pady=(10, 5))

        # Scrollable frame for components
        components_frame = ctk.CTkScrollableFrame(sidebar)
        components_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.components_frame = components_frame

        # Input area for new component
        lbl_new_comp = ctk.CTkLabel(sidebar, text="Add Component", font=("Arial", 12, "bold"))
        lbl_new_comp.pack(padx=10, pady=(10, 5))

        self.entry_comp_id = ctk.CTkEntry(sidebar, placeholder_text="Component ID (e.g., cpu_socket)")
        self.entry_comp_id.pack(padx=10, pady=(0, 5), fill="x")

        self.entry_comp_name = ctk.CTkEntry(sidebar, placeholder_text="Display Name")
        self.entry_comp_name.pack(padx=10, pady=(0, 5), fill="x")

        self.entry_comp_summary = ctk.CTkTextbox(sidebar, height=60)
        self.entry_comp_summary.pack(padx=10, pady=(0, 5), fill="x")

        btn_pick = ctk.CTkButton(
            sidebar,
            text="Click to Pick Coordinates",
            command=self._start_picking,
            fg_color="#FF6B35",
            hover_color="#FF5722"
        )
        btn_pick.pack(padx=10, pady=(0, 5), fill="x")

        # Action buttons
        btn_add = ctk.CTkButton(sidebar, text="Add Component", command=self._add_component)
        btn_add.pack(padx=10, pady=(0, 10), fill="x")

        btn_save = ctk.CTkButton(
            sidebar,
            text="Save Board Data",
            command=self._save_board,
            fg_color="#28a745",
            hover_color="#218838"
        )
        btn_save.pack(padx=10, pady=(0, 5), fill="x")

        btn_new_board = ctk.CTkButton(
            sidebar,
            text="➕ Add New Diagram",
            command=self._create_new_board_dialog,
            fg_color="#17A2B8",
            hover_color="#138496"
        )
        btn_new_board.pack(padx=10, pady=(0, 10), fill="x")

        btn_export = ctk.CTkButton(
            sidebar,
            text="Export All Boards",
            command=self._export_all,
            fg_color="#6610f2",
            hover_color="#5a04d4"
        )
        btn_export.pack(padx=10, pady=(0, 10), fill="x")

    def _create_main_view(self) -> None:
        """Create the main canvas area for viewing and picking coordinates."""
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Image display
        self.canvas = ctk.CTkCanvas(main_frame, bg="#2a2a2a", cursor="crosshair")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)

        # Status bar
        status_frame = ctk.CTkFrame(self)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.lbl_status = ctk.CTkLabel(
            status_frame,
            text="Ready. Select a board to begin.",
            text_color="#888888"
        )
        self.lbl_status.pack(side="left", padx=10)

    def _on_board_selected(self, board_key: str) -> None:
        """Handle board selection."""
        self.current_board_key = board_key
        board = self.registry.get_board(board_key)

        if not board:
            self._update_status(f"❌ Board '{board_key}' not found")
            return

        self.current_board = board
        self.current_image_path = Path(board.get("image_path", ""))

        if not self.current_image_path.exists():
            self._update_status(f"❌ Image not found: {self.current_image_path}")
            return

        # Load the board's display scale
        display_scale = board.get("display_scale", 1.0)
        self.scale_slider.set(display_scale)
        self.lbl_scale_value.configure(text=f"{int(display_scale * 100)}%")

        # Load image
        try:
            self.pil_image = Image.open(self.current_image_path)
            self._refresh_canvas()
            self._refresh_components_list()
            self._update_status(f"✅ Loaded board: {board_key}")
        except Exception as e:
            self._update_status(f"❌ Error loading image: {e}")

    def _on_scale_changed(self, value: float) -> None:
        """Handle display scale slider change."""
        scale_val = float(value)

        # Update label
        self.lbl_scale_value.configure(text=f"{int(scale_val * 100)}%")

        # Update board's display_scale
        if self.current_board:
            self.current_board["display_scale"] = scale_val
            # Save to registry
            self.registry.update_board(self.current_board_key, self.current_board)

        # Refresh canvas with new scale
        self._refresh_canvas()

    def _refresh_canvas(self) -> None:
        """Refresh the canvas display with the current image."""
        if not self.pil_image:
            return

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 2 or canvas_height < 2:
            # Canvas not fully initialized yet
            self.after(100, self._refresh_canvas)
            return

        # Calculate scale to fit image in canvas
        img_w, img_h = self.pil_image.size
        scale_w = canvas_width / img_w
        scale_h = canvas_height / img_h
        base_scale = min(scale_w, scale_h, 1.0)  # Don't upscale

        # Apply the board's display scale setting
        display_scale = self.current_board.get("display_scale", 1.0) if self.current_board else 1.0
        self.scale_factor = base_scale * display_scale

        # Resize for display - always create a fresh copy
        display_w = int(img_w * self.scale_factor)
        display_h = int(img_h * self.scale_factor)

        # Create a fresh copy to draw on
        self.pil_image_display = self.pil_image.copy().resize(
            (display_w, display_h),
            Image.Resampling.LANCZOS
        )

        # Draw existing components on preview
        self._draw_components_on_preview()

        # Convert to PhotoImage
        self.tk_image = ImageTk.PhotoImage(self.pil_image_display)

        # Display
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

    def _draw_components_on_preview(self) -> None:
        """Draw existing component boxes on the preview image."""
        if not self.pil_image_display:
            return

        draw = ImageDraw.Draw(self.pil_image_display)
        components = self.registry.get_components(self.current_board_key)

        for comp in components:
            coords = comp.get("coords", [])
            if len(coords) == 4:
                x1, y1, x2, y2 = coords

                # Scale to canvas display
                x1 = int(x1 * self.scale_factor)
                y1 = int(y1 * self.scale_factor)
                x2 = int(x2 * self.scale_factor)
                y2 = int(y2 * self.scale_factor)

                draw.rectangle([x1, y1, x2, y2], outline="#00FF00", width=2)

    def _refresh_components_list(self) -> None:
        """Refresh the components list in the sidebar."""
        # Clear existing
        for widget in self.components_frame.winfo_children():
            widget.destroy()

        components = self.registry.get_components(self.current_board_key)

        for idx, comp in enumerate(components):
            frame = self._create_component_item(comp, idx)
            frame.pack(padx=5, pady=5, fill="x")

    def _create_component_item(self, comp: dict, idx: int) -> ctk.CTkFrame:
        """Create a UI element for a component in the list."""
        frame = ctk.CTkFrame(self.components_frame, fg_color="#2a2a2a")

        # Component name and ID
        text = f"{comp.get('name', 'Unknown')} ({comp.get('id', 'N/A')})"
        lbl = ctk.CTkLabel(frame, text=text, wraplength=300, justify="left")
        lbl.pack(anchor="w", padx=10, pady=(5, 0))

        # Coordinates
        coords = comp.get("coords", [])
        coords_text = f"Coords: {coords}"
        lbl_coords = ctk.CTkLabel(frame, text=coords_text, text_color="#888888", font=("Arial", 9))
        lbl_coords.pack(anchor="w", padx=10)

        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(anchor="w", padx=10, pady=(0, 5), fill="x")

        btn_pick = ctk.CTkButton(
            btn_frame,
            text="Pick Coords",
            width=70,
            height=25,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=lambda: self._start_picking_for_component(idx)
        )
        btn_pick.pack(side="left", padx=(0, 5))

        btn_edit = ctk.CTkButton(
            btn_frame,
            text="Edit",
            width=50,
            height=25,
            command=lambda: self._edit_component(idx)
        )
        btn_edit.pack(side="left", padx=(0, 5))

        btn_delete = ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=50,
            height=25,
            fg_color="#DC3545",
            hover_color="#C82333",
            command=lambda: self._delete_component(idx)
        )
        btn_delete.pack(side="left")

        return frame

    def _start_picking(self) -> None:
        """Start coordinate picking mode."""
        if not self.current_board_key:
            self._update_status("⚠️  Select a board first")
            return

        if self.picking_active:
            self._update_status("Already picking coordinates")
            return

        self.picking_active = True
        self.start_point = None
        self.current_point = None
        self.measuring_rect = None
        self._update_status("🎯 Click and drag to select coordinates")

    def _start_picking_for_component(self, idx: int) -> None:
        """Start picking coordinates to update an existing component."""
        self._edit_component(idx)
        self._start_picking()
        self._update_status(f"🎯 Pick new coordinates for component (index {idx})")


    def _on_canvas_click(self, event) -> None:
        """Handle canvas click."""
        if not self.picking_active or not self.pil_image_display:
            return

        # Convert canvas coordinates to image coordinates
        img_x = int(event.x / self.scale_factor)
        img_y = int(event.y / self.scale_factor)

        self.start_point = (img_x, img_y)
        self.current_point = (img_x, img_y)

    def _on_canvas_drag(self, event) -> None:
        """Handle canvas drag to show preview rectangle."""
        if not self.picking_active or not self.start_point:
            return

        img_x = int(event.x / self.scale_factor)
        img_y = int(event.y / self.scale_factor)
        self.current_point = (img_x, img_y)

        # Redraw canvas with preview rectangle
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        # Draw preview rectangle
        x1 = int(self.start_point[0] * self.scale_factor)
        y1 = int(self.start_point[1] * self.scale_factor)
        x2 = int(self.current_point[0] * self.scale_factor)
        y2 = int(self.current_point[1] * self.scale_factor)

        self.canvas.create_rectangle(x1, y1, x2, y2, outline="#00FF00", width=2)

    def _on_canvas_release(self, event) -> None:
        """Handle canvas release - confirm coordinates."""
        if not self.picking_active or not self.start_point or not self.current_point:
            return

        x1, y1 = self.start_point
        x2, y2 = self.current_point

        # Normalize coordinates
        min_x = min(x1, x2)
        min_y = min(y1, y2)
        max_x = max(x1, x2)
        max_y = max(y1, y2)

        self.measuring_rect = (min_x, min_y, max_x, max_y)
        self.picking_active = False

        self._update_status(f"✅ Coordinates picked: {self.measuring_rect}")

    def _add_component(self) -> None:
        """Add a new component or update an existing one with picked coordinates."""
        if not self.current_board_key:
            self._update_status("❌ Select a board first")
            return

        if not self.measuring_rect:
            self._update_status("❌ Pick coordinates first")
            return

        comp_id = self.entry_comp_id.get().strip()
        comp_name = self.entry_comp_name.get().strip()
        comp_summary = self.entry_comp_summary.get("1.0", "end").strip()

        if not comp_id or not comp_name:
            self._update_status("❌ Component ID and Name are required")
            return

        component = {
            "id": comp_id,
            "name": comp_name,
            "coords": list(self.measuring_rect),
            "summary": comp_summary
        }

        # Get a fresh copy of the board from registry
        board = self.registry.get_board(self.current_board_key)
        if not board:
            self._update_status("❌ Board not found")
            return

        # Ensure components list exists
        if "components" not in board:
            board["components"] = []

        # Check if updating or adding
        if self.selected_component_idx is not None:
            # Update existing component
            board["components"][self.selected_component_idx] = component
            action_text = f"✅ Updated component: {comp_name}"
            self.selected_component_idx = None
        else:
            # Add new component
            board["components"].append(component)
            action_text = f"✅ Added component: {comp_name}"

        # Explicitly update the board in registry and save
        if self.registry.update_board(self.current_board_key, board):
            # Clear the cached images so they get reloaded
            self.pil_image = None
            self.pil_image_display = None
            self.tk_image = None

            # Reload the board to ensure fresh data
            self.registry.reload()
            self._on_board_selected(self.current_board_key)
        else:
            self._update_status("❌ Failed to save component")
            return

        # Clear inputs
        self.entry_comp_id.delete(0, "end")
        self.entry_comp_name.delete(0, "end")
        self.entry_comp_summary.delete("1.0", "end")
        self.measuring_rect = None
        self.selected_component_idx = None

        self._update_status(action_text)

    def _edit_component(self, idx: int) -> None:
        """Edit an existing component."""
        board = self.registry.get_board(self.current_board_key)
        if not board or idx >= len(board.get("components", [])):
            return

        comp = board["components"][idx]

        # Populate fields
        self.entry_comp_id.delete(0, "end")
        self.entry_comp_id.insert(0, comp.get("id", ""))

        self.entry_comp_name.delete(0, "end")
        self.entry_comp_name.insert(0, comp.get("name", ""))

        self.entry_comp_summary.delete("1.0", "end")
        self.entry_comp_summary.insert("1.0", comp.get("summary", ""))

        self.measuring_rect = tuple(comp.get("coords", []))
        self.selected_component_idx = idx

        self._update_status(f"Editing component: {comp.get('name')}")

    def _delete_component(self, idx: int) -> None:
        """Delete a component."""
        board = self.registry.get_board(self.current_board_key)
        if not board or idx >= len(board.get("components", [])):
            return

        del board["components"][idx]
        self.registry.update_board(self.current_board_key, board)

        self._refresh_components_list()
        self._refresh_canvas()
        self._update_status("✅ Component deleted")

    def _save_board(self) -> None:
        """Save the current board (it auto-saves on component changes, but this forces a save)."""
        if not self.current_board_key:
            self._update_status("❌ No board selected")
            return

        if self.registry.save_boards():
            self._update_status(f"✅ Board '{self.current_board_key}' saved")
        else:
            self._update_status(f"❌ Error saving board")

    def _export_all(self) -> None:
        """Export all boards to JSON."""
        if self.registry.save_boards():
            self._update_status("✅ All boards exported to JSON")
        else:
            self._update_status("❌ Error exporting boards")

    def _create_new_board_dialog(self) -> None:
        """Open a dialog to create a new board with a PNG image."""
        from tkinter import filedialog
        import shutil
        from pathlib import Path

        # Ask user to select an image file
        file_path = filedialog.askopenfilename(
            title="Select Motherboard Image",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if not file_path:
            self._update_status("❌ No image selected")
            return

        # Create a dialog for board details
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Diagram")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Labels and entries
        frame = ctk.CTkFrame(dialog)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Board Key (ID):", font=("Arial", 11)).pack(anchor="w", pady=(0, 5))
        entry_key = ctk.CTkEntry(frame, placeholder_text="e.g., my_atx_board")
        entry_key.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Display Name:", font=("Arial", 11)).pack(anchor="w", pady=(0, 5))
        entry_name = ctk.CTkEntry(frame, placeholder_text="e.g., My ATX Motherboard")
        entry_name.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Image Path (relative):", font=("Arial", 11)).pack(anchor="w", pady=(0, 5))
        entry_image = ctk.CTkEntry(frame, placeholder_text="e.g., data/motherboard/my_board.png")
        entry_image.pack(fill="x", pady=(0, 10))

        # Info label
        info_label = ctk.CTkLabel(
            frame,
            text=f"Selected: {Path(file_path).name}",
            text_color="#888888",
            font=("Arial", 9),
            wraplength=350
        )
        info_label.pack(anchor="w", pady=(0, 15))

        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))

        def on_create():
            key = entry_key.get().strip()
            name = entry_name.get().strip()
            image_path = entry_image.get().strip()

            if not key or not name or not image_path:
                self._update_status("❌ All fields are required")
                return

            # Check if board key already exists
            if key in self.registry.get_board_keys():
                self._update_status(f"❌ Board key '{key}' already exists")
                return

            try:
                # Copy image to destination
                dest_path = Path(image_path)
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(file_path, dest_path)

                # Create new board entry
                new_board = {
                    "key": key,
                    "name": name,
                    "image_path": image_path,
                    "resolution": [1920, 1080],  # Default, user can edit
                    "flipped": False,
                    "components": []
                }

                # Add to registry
                self.registry.update_board(key, new_board)
                self.registry.save_boards()

                # Refresh UI
                board_keys = self.registry.get_board_keys()
                self.board_menu.configure(values=board_keys)
                self.board_menu.set(key)
                self._on_board_selected(key)

                self._update_status(f"✅ Created new board: {name}")
                dialog.destroy()

            except Exception as e:
                self._update_status(f"❌ Error creating board: {e}")

        btn_create = ctk.CTkButton(
            btn_frame,
            text="Create Board",
            command=on_create,
            fg_color="#28a745",
            hover_color="#218838"
        )
        btn_create.pack(side="left", padx=(0, 5))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        btn_cancel.pack(side="left")


    def _update_status(self, message: str) -> None:
        """Update the status bar."""
        self.lbl_status.configure(text=message)


if __name__ == "__main__":
    app = CoordinatePickerUI()
    app.mainloop()
