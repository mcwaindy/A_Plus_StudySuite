"""
Dev Tools View - Developer utilities for notes and quick reference.
Includes a multi-page notes system for tracking ideas, bugs, and notes.
"""

import customtkinter as ctk
from pathlib import Path
import json
from datetime import datetime


class DevToolsView(ctk.CTkFrame):
    """Multi-page notes system for development notes and ideas."""

    def __init__(self, parent):
        super().__init__(parent)

        self.notes_file = Path("data/dev_notes.json")
        self.current_page = "Notes"
        self.notes_data = self.load_notes()

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Tab view
        self.grid_rowconfigure(2, weight=0)  # Footer

        # Create header
        self.create_header()

        # Create tab-based notes system
        self.create_notes_tabs()

        # Create footer with info
        self.create_footer()

    def create_header(self):
        """Create header section."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        title = ctk.CTkLabel(
            header_frame,
            text="📝 DEV NOTES",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")

        # Info label
        info = ctk.CTkLabel(
            header_frame,
            text="Quick notes and ideas · Auto-saved",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        info.grid(row=1, column=0, sticky="w", pady=(5, 0))

    def create_notes_tabs(self):
        """Create tab view for multiple note pages."""
        # Tab view
        self.tab_view = ctk.CTkTabview(self, fg_color=("gray85", "gray15"))
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 0))

        # Get list of pages from notes data
        pages = list(self.notes_data.keys()) if self.notes_data else ["Notes"]

        # Create tabs
        self.text_widgets = {}
        for page_name in pages:
            self.tab_view.add(page_name)
            tab_frame = self.tab_view.tab(page_name)
            tab_frame.grid_columnconfigure(0, weight=1)
            tab_frame.grid_rowconfigure(0, weight=1)

            # Text widget for this page
            text_widget = ctk.CTkTextbox(
                tab_frame,
                wrap="word",
                font=ctk.CTkFont(family="Courier", size=11)
            )
            text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            # Load content from notes_data
            content = self.notes_data.get(page_name, "")
            if content:
                text_widget.insert("1.0", content)

            # Bind save on any change
            text_widget.bind("<KeyRelease>", lambda e, page=page_name: self.auto_save(page))
            text_widget.bind("<FocusOut>", lambda e, page=page_name: self.auto_save(page))

            self.text_widgets[page_name] = text_widget

    def create_footer(self):
        """Create footer section."""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=0)
        footer_frame.grid_columnconfigure(2, weight=0)

        # Info label
        status = ctk.CTkLabel(
            footer_frame,
            text="💡 Tip: Click tabs to switch between note pages",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50")
        )
        status.grid(row=0, column=0, sticky="w")

        # Add page button
        btn_add = ctk.CTkButton(
            footer_frame,
            text="➕ Add Page",
            width=100,
            command=self.add_new_page
        )
        btn_add.grid(row=0, column=1, sticky="e", padx=(10, 5))

        # Delete page button
        btn_delete = ctk.CTkButton(
            footer_frame,
            text="🗑️ Delete",
            width=100,
            command=self.delete_current_page
        )
        btn_delete.grid(row=0, column=2, sticky="e", padx=(0, 0))

    def add_new_page(self):
        """Add a new note page."""
        # Simple dialog to get page name
        dialog = ctk.CTkInputDialog(
            text="Enter page name:",
            title="New Note Page"
        )
        page_name = dialog.get_input()

        if page_name and page_name.strip():
            page_name = page_name.strip()

            # Check if page already exists
            if page_name in self.text_widgets:
                error_dialog = ctk.CTkInputDialog(
                    text="Page already exists!",
                    title="Error"
                )
                return

            # Add to notes_data
            self.notes_data[page_name] = ""
            self.save_notes()

            # Add tab
            self.tab_view.add(page_name)
            tab_frame = self.tab_view.tab(page_name)
            tab_frame.grid_columnconfigure(0, weight=1)
            tab_frame.grid_rowconfigure(0, weight=1)

            # Create text widget
            text_widget = ctk.CTkTextbox(
                tab_frame,
                wrap="word",
                font=ctk.CTkFont(family="Courier", size=11)
            )
            text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            # Bind save
            text_widget.bind("<KeyRelease>", lambda e, page=page_name: self.auto_save(page))
            text_widget.bind("<FocusOut>", lambda e, page=page_name: self.auto_save(page))

            self.text_widgets[page_name] = text_widget

            # Switch to new tab
            self.tab_view.set(page_name)

    def delete_current_page(self):
        """Delete the currently selected page."""
        current_tab = self.tab_view.get()

        # Don't delete if only one page
        if len(self.text_widgets) <= 1:
            error_dialog = ctk.CTkInputDialog(
                text="Cannot delete the last page!",
                title="Error"
            )
            return

        # Confirm deletion
        confirm_dialog = ctk.CTkInputDialog(
            text=f"Delete page '{current_tab}'? This cannot be undone.",
            title="Confirm Delete"
        )

        # Remove page
        if current_tab in self.notes_data:
            del self.notes_data[current_tab]
        if current_tab in self.text_widgets:
            del self.text_widgets[current_tab]

        self.tab_view.delete(current_tab)
        self.save_notes()

    def auto_save(self, page_name):
        """Auto-save notes for a specific page."""
        if page_name in self.text_widgets:
            text_widget = self.text_widgets[page_name]
            content = text_widget.get("1.0", "end-1c")
            self.notes_data[page_name] = content
            self.save_notes()

    def load_notes(self):
        """Load notes from file."""
        if self.notes_file.exists():
            try:
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading notes: {e}")
                return {"Notes": ""}

        # Default: single "Notes" page
        return {"Notes": ""}

    def save_notes(self):
        """Save notes to file."""
        try:
            # Create data directory if needed
            self.notes_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(self.notes_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving notes: {e}")
