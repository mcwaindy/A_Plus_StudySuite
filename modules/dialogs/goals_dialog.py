"""
Goals Dialog - UI for setting exam target date and readiness goal.
"""

import customtkinter as ctk
from datetime import datetime, timedelta


class GoalsDialog(ctk.CTkToplevel):
    """Dialog for setting study goals."""

    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.title("📅 Set Study Goals")
        self.geometry("400x300")
        self.callback = callback

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Make it modal
        self.transient(parent)
        self.grab_set()

        # Create content
        self.create_content()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def create_content(self):
        """Create dialog content."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Set Your Study Goals",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))

        # Content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)

        # Exam date section
        date_label = ctk.CTkLabel(
            content_frame,
            text="Target Exam Date",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        date_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Date entry
        date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        date_frame.grid_columnconfigure(1, weight=1)

        self.month_var = ctk.StringVar(value="09")
        self.day_var = ctk.StringVar(value="15")
        self.year_var = ctk.StringVar(value="2026")

        # Month
        ctk.CTkLabel(date_frame, text="Month:", font=ctk.CTkFont(size=10)).grid(row=0, column=0, sticky="w")
        month_box = ctk.CTkComboBox(
            date_frame,
            values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
            variable=self.month_var,
            width=60,
            state="readonly"
        )
        month_box.grid(row=0, column=1, sticky="w", padx=(5, 10))

        # Day
        ctk.CTkLabel(date_frame, text="Day:", font=ctk.CTkFont(size=10)).grid(row=0, column=2, sticky="w")
        day_options = [str(i).zfill(2) for i in range(1, 32)]
        day_box = ctk.CTkComboBox(
            date_frame,
            values=day_options,
            variable=self.day_var,
            width=60,
            state="readonly"
        )
        day_box.grid(row=0, column=3, sticky="w", padx=(5, 10))

        # Year
        ctk.CTkLabel(date_frame, text="Year:", font=ctk.CTkFont(size=10)).grid(row=0, column=4, sticky="w")
        year_options = [str(i) for i in range(2026, 2031)]
        year_box = ctk.CTkComboBox(
            date_frame,
            values=year_options,
            variable=self.year_var,
            width=70,
            state="readonly"
        )
        year_box.grid(row=0, column=5, sticky="w", padx=(5, 0))

        # Readiness section
        readiness_label = ctk.CTkLabel(
            content_frame,
            text="Target Readiness Level",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        readiness_label.grid(row=2, column=0, sticky="w", pady=(15, 5))

        self.readiness_var = ctk.StringVar(value="90")
        readiness_box = ctk.CTkComboBox(
            content_frame,
            values=["70", "80", "90"],
            variable=self.readiness_var,
            state="readonly",
            width=100
        )
        readiness_box.grid(row=3, column=0, sticky="w")

        # Info label
        info_label = ctk.CTkLabel(
            content_frame,
            text="The percentage of mastery needed before your exam.",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50")
        )
        info_label.grid(row=4, column=0, sticky="w", pady=(5, 0))

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=("gray70", "gray30"),
            text_color=("gray10", "gray90")
        )
        cancel_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Goal",
            command=self.save_goal
        )
        save_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def save_goal(self):
        """Save the goal and close dialog."""
        try:
            date_str = f"{self.year_var.get()}-{self.month_var.get()}-{self.day_var.get()}"
            # Validate date
            datetime.strptime(date_str, "%Y-%m-%d")

            readiness = int(self.readiness_var.get())

            if self.callback:
                self.callback(date_str, readiness)

            self.destroy()
        except ValueError as e:
            # Show error
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("Invalid Date")
            error_dialog.geometry("300x100")

            error_label = ctk.CTkLabel(
                error_dialog,
                text="Please enter a valid date.",
                font=ctk.CTkFont(size=12)
            )
            error_label.pack(pady=20)

            ok_btn = ctk.CTkButton(
                error_dialog,
                text="OK",
                command=error_dialog.destroy,
                width=100
            )
            ok_btn.pack(pady=10)
