import webbrowser
from urllib.parse import urlparse, unquote

import customtkinter as ctk
from tkinterweb import HtmlFrame

from modules.notes import html_compat, library, renderer


class NotesView(ctk.CTkFrame):
    """Study notes browser: a filterable objective sidebar beside a styled
    Markdown reading pane.

    Notes are discovered from assets/notes/ at load time rather than from a
    hardcoded map, so the list can never drift from what is on disk.
    """

    NAV_WIDTH = 260
    FONT_SCALE_MIN = 0.7
    FONT_SCALE_MAX = 1.6
    FONT_SCALE_STEP = 0.1
    MAX_LABEL_CHARS = 24

    SCROLLBAR_COLORS = {
        "trough": "#2b2b2b",
        "thumb": "#4a4a4a",
        "thumb_active": "#5e5e5e",
    }

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # Must run before the first page renders, or PNGs come out as alt text.
        html_compat.apply_image_fix()

        self.sections = []
        self.current_note = None
        self.nav_buttons = {}
        self.font_scale = 1.0

        # Grid: fixed-width nav column, content column takes the rest.
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_nav_panel()
        self.create_content_panel()

        self.refresh_library(select_default=True)

    # --- NAV PANEL --- #
    def create_nav_panel(self):
        """Left rail: filter box, grouped objective list, progress footer."""
        nav = ctk.CTkFrame(self, width=self.NAV_WIDTH, corner_radius=10)
        nav.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
        nav.grid_propagate(False)  # hold the width against the child list
        nav.grid_columnconfigure(0, weight=1)
        nav.grid_rowconfigure(2, weight=1)

        lbl_heading = ctk.CTkLabel(
            nav,
            text="STUDY NOTES",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray",
            anchor="w",
        )
        lbl_heading.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))

        self.filter_var = ctk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self.render_nav_list())

        self.entry_filter = ctk.CTkEntry(
            nav,
            placeholder_text="Filter objectives…",
            textvariable=self.filter_var,
            height=30,
        )
        self.entry_filter.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))

        self.nav_list = ctk.CTkScrollableFrame(nav, fg_color="transparent")
        self.nav_list.grid(row=2, column=0, sticky="nsew", padx=4, pady=0)
        self.nav_list.grid_columnconfigure(0, weight=1)

        self.lbl_progress = ctk.CTkLabel(
            nav,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray50",
            anchor="w",
        )
        self.lbl_progress.grid(row=3, column=0, sticky="ew", padx=16, pady=(6, 12))

    def create_content_panel(self):
        """Right side: breadcrumb + reader controls above the HTML pane."""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.lbl_breadcrumb = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray50",
        )
        self.lbl_breadcrumb.pack(side="left", padx=(4, 0))

        btn_reload = ctk.CTkButton(
            header,
            text="⟳  Reload",
            width=90,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self.reload_current,
        )
        btn_reload.pack(side="right", padx=(8, 4))

        # Text sizing, so long reading sessions are not stuck at one size.
        size_box = ctk.CTkFrame(header, fg_color="transparent")
        size_box.pack(side="right")

        ctk.CTkButton(
            size_box,
            text="-",
            width=34,
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.adjust_font_scale(-self.FONT_SCALE_STEP),
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            size_box,
            text="+",
            width=34,
            height=28,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self.adjust_font_scale(self.FONT_SCALE_STEP),
        ).pack(side="left", padx=2)

        self.html_view = HtmlFrame(
            content,
            messages_enabled=False,
            horizontal_scrollbar="auto",
            on_link_click=self.on_link_click,
        )
        self.html_view.grid(row=1, column=0, sticky="nsew")
        html_compat.style_scrollbars(self.html_view, self.SCROLLBAR_COLORS)

    # --- LIBRARY / NAV RENDERING --- #
    def refresh_library(self, select_default=False):
        """Rescans assets/notes/ and rebuilds the sidebar.

        :param select_default: Open the title page with table of contents.
        """
        self.sections = library.discover_notes()
        self.render_nav_list()

        written, total = library.count_written(self.sections)
        self.lbl_progress.configure(
            text=f"{written} of {total} written" if total else "No notes found"
        )

        if not select_default:
            return

        if self.sections:
            self.show_title_page()
        else:
            self.show_empty_library()

    def _first_note(self, prefer_written=False):
        """Returns the first note in sidebar order, preferring ones with content."""
        notes = [n for section in self.sections for n in section["notes"]]
        if not notes:
            return None
        if prefer_written:
            return next((n for n in notes if not n["is_empty"]), notes[0])
        return notes[0]

    def render_nav_list(self):
        """Draws the grouped, filtered objective list with visual differentiation by match type."""
        for child in self.nav_list.winfo_children():
            child.destroy()
        self.nav_buttons = {}

        needle = self.filter_var.get().strip().lower()
        row = 0
        matches_title = 0
        matches_content = 0

        # Categorize all notes by match type
        all_matches_by_type = {'title': [], 'content': [], 'all': []}

        for section in self.sections:
            for note in section["notes"]:
                match_type = self._get_match_type(note, needle)
                if match_type == 'title':
                    all_matches_by_type['title'].append((section, note))
                elif match_type == 'content':
                    all_matches_by_type['content'].append((section, note))
                elif match_type == 'all':
                    all_matches_by_type['all'].append((section, note))

        # If empty search, show ALL notes with default styling (no color coding)
        if not needle:
            section_map = {}
            for section, note in all_matches_by_type['all']:
                if section['label'] not in section_map:
                    section_map[section['label']] = (section, [])
                section_map[section['label']][1].append(note)

            for section_label, (section, notes) in section_map.items():
                lbl = ctk.CTkLabel(
                    self.nav_list,
                    text=section['label'].upper(),
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="gray",
                    anchor="w",
                )
                lbl.grid(row=row, column=0, sticky="ew", padx=12, pady=(12, 4))
                row += 1

                for note in notes:
                    self.nav_buttons[note["id"]] = self._add_nav_button(note, row, match_type='title')
                    row += 1

            self._highlight_active()
            return

        # Display title matches first (grouped by section)
        if all_matches_by_type['title']:
            section_map = {}
            for section, note in all_matches_by_type['title']:
                if section['label'] not in section_map:
                    section_map[section['label']] = (section, [])
                section_map[section['label']][1].append(note)

            for section_label, (section, notes) in section_map.items():
                lbl = ctk.CTkLabel(
                    self.nav_list,
                    text=section['label'].upper(),
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="gray",
                    anchor="w",
                )
                lbl.grid(row=row, column=0, sticky="ew", padx=12, pady=(12, 4))
                row += 1

                for note in notes:
                    self.nav_buttons[note["id"]] = self._add_nav_button(note, row, match_type='title')
                    row += 1
                    matches_title += 1

        # Display content matches with "Found in notes:" separator (grouped by section)
        if all_matches_by_type['content']:
            # Add separator (show even if no title matches)
            separator = ctk.CTkLabel(
                self.nav_list,
                text="FOUND IN NOTES:",
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color="#888",
                anchor="w",
            )
            separator.grid(row=row, column=0, sticky="ew", padx=12, pady=(16, 4))
            row += 1

            section_map = {}
            for section, note in all_matches_by_type['content']:
                if section['label'] not in section_map:
                    section_map[section['label']] = (section, [])
                section_map[section['label']][1].append(note)

            for section_label, (section, notes) in section_map.items():
                # Only show section header if it's NOT already shown in title matches
                if not any(s['label'] == section_label for s, _ in all_matches_by_type['title']):
                    lbl = ctk.CTkLabel(
                        self.nav_list,
                        text=section['label'].upper(),
                        font=ctk.CTkFont(size=11, weight="bold"),
                        text_color="gray",
                        anchor="w",
                    )
                    lbl.grid(row=row, column=0, sticky="ew", padx=12, pady=(12, 4))
                    row += 1

                for note in notes:
                    self.nav_buttons[note["id"]] = self._add_nav_button(note, row, match_type='content')
                    row += 1
                    matches_content += 1

        if not matches_title and not matches_content:
            message = "No matching objectives" if needle else "No notes in assets/notes/"
            ctk.CTkLabel(
                self.nav_list,
                text=message,
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color="gray50",
                wraplength=self.NAV_WIDTH - 50,
            ).grid(row=row, column=0, sticky="ew", padx=14, pady=14)

        self._highlight_active()

    def _add_nav_button(self, note, row, match_type='title'):
        """Creates one objective button, styled to match the app's main sidebar.

        match_type: 'title' for matches in objective name, 'content' for matches in note body
        """
        # Color coding based on match type
        if match_type == 'content':
            # Content matches get a subtle blue tint
            text_color_empty = ("gray40", "gray55")
            text_color_filled = ("#6ba3d9", "#7bb3e9")  # Blueish
            hover_color = ("#8bc3ff", "#4a7fcc")  # Lighter blue on hover
        else:
            # Title matches use normal colors
            text_color_empty = ("gray40", "gray55")
            text_color_filled = ("gray10", "gray90")
            hover_color = ("gray70", "gray30")

        btn = ctk.CTkButton(
            self.nav_list,
            text=self._nav_label(note),
            anchor="w",
            height=30,
            fg_color="transparent",
            text_color=text_color_empty if note["is_empty"] else text_color_filled,
            hover_color=hover_color,
            font=ctk.CTkFont(size=12),
            command=lambda target=note: self.select_note(target),
        )
        btn.grid(row=row, column=0, sticky="ew", padx=6, pady=1)
        return btn

    def _nav_label(self, note):
        """Builds the button caption: a written/empty marker, objective, and title."""
        marker = "○" if note["is_empty"] else "●"
        title = note["title"]

        if len(title) > self.MAX_LABEL_CHARS:
            title = title[: self.MAX_LABEL_CHARS - 1].rstrip() + "…"

        objective = f"{note['objective']}  " if note["objective"] else ""
        return f"  {marker}  {objective}{title}"

    def _get_match_type(self, note, needle):
        """
        Determine where a note matches the search term.
        Returns: 'title' if matches in title/objective, 'content' if in note body, None if no match.
        """
        if not needle:
            return 'all'

        needle_lower = needle.lower()

        # Check title/objective match (priority)
        title_haystack = f"{note['objective']} {note['title']} {note['group_label']}".lower()
        if needle_lower in title_haystack:
            return 'title'

        # Check content match
        try:
            if note['path'].exists():
                with open(note['path'], 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if needle_lower in content:
                        return 'content'
        except (OSError, KeyError):
            pass

        return None

    @staticmethod
    def _matches(note, needle):
        """Case-insensitive filter across objective number, title, and section."""
        if not needle:
            return True
        haystack = f"{note['objective']} {note['title']} {note['group_label']}".lower()
        return needle in haystack

    def _highlight_active(self):
        """Applies the selected background to whichever note is open."""
        for note_id, btn in self.nav_buttons.items():
            is_active = self.current_note and note_id == self.current_note["id"]
            btn.configure(fg_color=("gray75", "gray25") if is_active else "transparent")

    # --- NOTE DISPLAY --- #
    def select_note(self, note):
        """Renders a note into the reading pane and marks it active in the sidebar."""
        self.current_note = note
        self.lbl_breadcrumb.configure(text=note["group_label"])
        self._highlight_active()
        # Note: base_url is omitted because images are now embedded as data URIs,
        # which don't need a base URL to resolve. Including base_url can interfere
        # with data URI rendering in tkinterweb.
        self.html_view.load_html(renderer.render_note(note))

    def reload_current(self):
        """Rescans the notes folder and re-renders the open view from disk.

        Lets you edit Markdown (or the stylesheet) in another editor and see the
        result without restarting the app. If on the title page, reloads it.
        """
        open_id = self.current_note["id"] if self.current_note else None

        self.sections = library.discover_notes()
        written, total = library.count_written(self.sections)
        self.lbl_progress.configure(
            text=f"{written} of {total} written" if total else "No notes found"
        )

        # If we were viewing title page (current_note is None), reload title page
        if open_id is None:
            self.render_nav_list()
            if self.sections:
                self.show_title_page()
            else:
                self.show_empty_library()
            return

        note = library.find_note(self.sections, open_id) if open_id else None
        if note is None:
            note = self._first_note(prefer_written=True)

        self.current_note = note
        self.render_nav_list()

        if note:
            self.select_note(note)
        else:
            self.show_empty_library()

    def show_empty_library(self):
        """Shown when assets/notes/ contains no usable markdown files."""
        self.current_note = None
        self.lbl_breadcrumb.configure(text="")
        self.html_view.load_html(
            renderer.render_notice(
                "No notes found",
                "Add Markdown files under <code>assets/notes/core1/</code> or "
                "<code>assets/notes/core2/</code>, then press "
                "<strong>Reload</strong>.<br><br>"
                "Copy <code>assets/notes/_TEMPLATE.md</code> to get the front "
                "matter and callout syntax.",
            )
        )

    def show_title_page(self):
        """Display a title page with table of contents and study statistics."""
        self.current_note = None
        self.lbl_breadcrumb.configure(text="📖 Study Guide")

        # Generate the HTML for the title page
        html = self._generate_title_page_html()
        self.html_view.load_html(html)

    def _load_review_objectives(self):
        """Load all objectives that have been flagged for review."""
        from pathlib import Path
        import json

        review_objectives = set()
        review_path = Path("data/review_history.json")

        if review_path.exists():
            try:
                with open(review_path, "r", encoding="utf-8") as f:
                    reviews = json.load(f)
                    for review in reviews:
                        for card in review.get("cards_reviewed", []):
                            obj = card.get("objective", "")
                            if obj:
                                review_objectives.add(obj)
            except Exception as e:
                pass

        return review_objectives

    def _load_review_details(self):
        """Load detailed review info: {objective: [list of terms]}"""
        from pathlib import Path
        import json

        review_details = {}
        review_path = Path("data/review_history.json")

        if review_path.exists():
            try:
                with open(review_path, "r", encoding="utf-8") as f:
                    reviews = json.load(f)
                    for review in reviews:
                        for card in review.get("cards_reviewed", []):
                            obj = card.get("objective", "")
                            term = card.get("term", "")
                            if obj and term:
                                if obj not in review_details:
                                    review_details[obj] = []
                                review_details[obj].append(term)
            except:
                pass

        return review_details

    def _generate_title_page_html(self):
        """Generate HTML for the title page with table of contents."""
        from pathlib import Path
        import json

        review_objectives = self._load_review_objectives()
        review_details = self._load_review_details()  # Get detailed review info

        # Build the title page content
        content_parts = [
            '<div class="title-page">',
            '<div class="hero">',
            '<h1>Study Guide</h1>',
            '<p class="hero-subtitle">CompTIA A+ Reference</p>',
            '</div>',
        ]

        # Review Material section - build list of objectives that need review
        review_list_html = ""
        if review_objectives:
            # Build list with newlines and diamond bullets, each on its own non-wrapping line
            review_items = []
            for obj in sorted(review_details.keys()):
                terms = review_details[obj]
                # Extract just the objective number (e.g., "1.1" from "1.1 - Laptop Hardware...")
                obj_num = obj.split(' - ')[0] if ' - ' in obj else obj
                # Join first 3 terms with commas
                terms_str = ", ".join(terms[:3])
                if len(terms) > 3:
                    terms_str += f" (+{len(terms) - 3} more)"
                review_items.append(f'<nobr>◆ {obj_num}: {terms_str}</nobr>')

            # Join with actual line breaks
            review_list_html = "<br>".join(review_items)

        if review_list_html:
            content_parts.append('<div class="review-material-section">')
            content_parts.append('<details class="review-material-details">')
            content_parts.append('<summary class="review-material-summary">Review Material</summary>')
            content_parts.append(f'<div class="review-material-content">{review_list_html}</div>')
            content_parts.append('</details>')
            content_parts.append('</div>')

        # Original progress section (kept but hidden if reviews exist)
        if not review_objectives:
            written, total = library.count_written(self.sections)
            progress_pct = int((written / total * 100)) if total > 0 else 0

            content_parts.append('<div class="progress-section">')
            content_parts.append(f'<p class="progress-text">{written} of {total} sections · {progress_pct}% complete</p>')
            content_parts.append(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress_pct}%"></div></div>')
            content_parts.append('</div>')

        # Flatten all objectives with their section info, separated by exam
        core1_objectives = []
        core2_objectives = []
        core1_num = 1
        core2_num = 1

        for section in self.sections:
            section_name = section.get("name", "Unknown")
            section_label = section.get("label", section_name)

            for idx, note in enumerate(section.get("notes", [])):
                note_id = note.get("id", "")
                note_label = note.get("label", "Untitled")
                note_objective_short = note.get("objective", "")  # e.g., "1.1"
                note_title = note.get("title", "")  # e.g., "Laptop Hardware, Components & Physical Security"
                is_empty = note.get("is_empty", False)
                group_key = note.get("group_key", "")  # "core1", "core2", or ""

                # Build full objective label matching review history format
                # Review history uses: "1.1 - Laptop Hardware, Components & Physical Security"
                if note_objective_short and note_title:
                    full_objective = f"{note_objective_short} - {note_title}"
                else:
                    full_objective = note_objective_short or note_label

                is_reviewed = full_objective in review_objectives

                # If full objective doesn't match, try matching just the objective number with title validation
                # This handles cases where the title text differs between notes and review history
                if not is_reviewed and note_objective_short:
                    # Check if any reviewed objective starts with this objective number
                    for reviewed_obj in review_objectives:
                        if reviewed_obj.startswith(note_objective_short):
                            # Also check if there's significant title word overlap
                            # Extract title part from reviewed objective (after the dash)
                            reviewed_title = reviewed_obj.split(' - ')[1].lower() if ' - ' in reviewed_obj else ""
                            note_title_lower = note_title.lower()

                            # Check for keyword overlap (at least one common significant word)
                            reviewed_words = set(word for word in reviewed_title.split() if len(word) > 3)
                            note_words = set(word for word in note_title_lower.split() if len(word) > 3)

                            if reviewed_words & note_words:  # If there's intersection
                                is_reviewed = True
                                full_objective = reviewed_obj
                                break

                obj_data = {
                    'id': note_id,
                    'label': note_label,
                    'objective': full_objective,
                    'is_empty': is_empty,
                    'is_reviewed': is_reviewed,
                    'section': section_label,
                    'group_key': group_key,
                    'number': 0  # Will be set below based on group
                }

                if group_key == "core2":
                    obj_data['number'] = core2_num
                    core2_objectives.append(obj_data)
                    core2_num += 1
                else:
                    # core1 or anything else (general) goes to core1
                    obj_data['number'] = core1_num
                    core1_objectives.append(obj_data)
                    core1_num += 1

        # Display objectives in a 2-column layout (reading left-to-right)
        content_parts.append('<div class="objectives-container">')

        # Helper function to render objectives
        def render_objectives_section(objectives, section_title):
            if not objectives:
                return

            content_parts.append('<div class="objectives-section">')
            content_parts.append(f'<div class="objectives-section-title">{section_title}</div>')
            content_parts.append('<div class="objectives-columns">')

            # Create pairs of objectives that read left-to-right
            for i in range(0, len(objectives), 2):
                # Left item in the pair
                obj = objectives[i]
                review_class = " flagged" if obj['is_reviewed'] else ""

                # Build tooltip content with review details
                tooltip_text = ""
                if obj['is_reviewed'] and obj['objective'] in review_details:
                    terms = review_details[obj['objective']]
                    tooltip_text = "\n".join(terms[:10])  # Limit to 10 terms
                    if len(terms) > 10:
                        tooltip_text += f"\n... and {len(terms) - 10} more"

                content_parts.append('<div class="objective-row">')
                content_parts.append('<div class="objective-column">')
                content_parts.append(f'<a href="note:{obj["id"]}" class="objective-entry{review_class}">')
                content_parts.append(f'<div class="obj-number">{obj["number"]:02d}</div>')
                content_parts.append('<div class="obj-text">')
                content_parts.append(f'<div class="obj-title">{obj["label"]}</div>')

                # Show "Needs Review" for flagged items, dot for others
                if obj['is_reviewed']:
                    content_parts.append(f'<div class="obj-indicator flagged">Needs Review</div>')
                elif not obj['is_empty']:
                    content_parts.append('<div class="obj-indicator">·</div>')

                content_parts.append('</div>')
                content_parts.append('</a>')
                content_parts.append('</div>')

                # Right item in the pair (if it exists)
                if i + 1 < len(objectives):
                    obj = objectives[i + 1]
                    review_class = " flagged" if obj['is_reviewed'] else ""

                    tooltip_text = ""
                    if obj['is_reviewed'] and obj['objective'] in review_details:
                        terms = review_details[obj['objective']]
                        tooltip_text = "\n".join(terms[:10])
                        if len(terms) > 10:
                            tooltip_text += f"\n... and {len(terms) - 10} more"

                    content_parts.append('<div class="objective-column">')
                    content_parts.append(f'<a href="note:{obj["id"]}" class="objective-entry{review_class}">')
                    content_parts.append(f'<div class="obj-number">{obj["number"]:02d}</div>')
                    content_parts.append('<div class="obj-text">')
                    content_parts.append(f'<div class="obj-title">{obj["label"]}</div>')

                    # Show "Needs Review" for flagged items, dot for others
                    if obj['is_reviewed']:
                        content_parts.append(f'<div class="obj-indicator flagged">Needs Review</div>')
                    elif not obj['is_empty']:
                        content_parts.append('<div class="obj-indicator">·</div>')

                    content_parts.append('</div>')
                    content_parts.append('</a>')
                    content_parts.append('</div>')

                content_parts.append('</div>')

            content_parts.append('</div>')
            content_parts.append('</div>')

        # Render Core 1
        render_objectives_section(core1_objectives, "Core 1")

        # Render Core 2
        render_objectives_section(core2_objectives, "Core 2")

        content_parts.append('</div>')

        # Enhanced CSS with better typography, borders, and visual hierarchy
        css = """
        .title-page {
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 40px;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 2px solid #3a3a3a;
        }

        .title-page h1 {
            font-size: 3em;
            font-weight: 700;
            letter-spacing: -2px;
            margin: 0 0 12px 0;
            color: #f0f0f0;
        }

        .hero-subtitle {
            font-size: 1.1em;
            color: #888;
            margin: 0;
            font-weight: 400;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        /* Progress Section */
        .progress-section {
            text-align: center;
            margin-bottom: 50px;
        }

        .progress-text {
            font-size: 0.95em;
            color: #999;
            margin: 0 0 16px 0;
            letter-spacing: 0.3px;
        }

        .progress-bar {
            width: 100px;
            height: 2px;
            background: #2a2a2a;
            margin: 0 auto;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4da6ff 0%, #42a5f5 100%);
        }

        /* Review Material Section */
        .review-material-section {
            text-align: center;
            margin-bottom: 50px;
        }

        .review-material-details {
            display: inline-block;
            cursor: pointer;
            user-select: none;
        }

        .review-material-summary {
            font-size: 1.05em;
            color: #888;
            font-weight: 600;
            letter-spacing: 0.3px;
            list-style: none;
            padding: 0;
            margin: 0;
            display: block;
            cursor: pointer;
        }

        /* Remove default marker */
        .review-material-details::marker {
            display: none;
        }

        .review-material-details > summary::-webkit-details-marker {
            display: none;
        }

        /* Content inside the expandable review section */
        .review-material-content {
            margin-top: 12px;
            font-size: 0.9em;
            color: #888;
            line-height: 1.6;
            white-space: normal;
        }

        /* Objectives List Container */
        .objectives-container {
            margin-top: 20px;
        }

        /* Core section with header */
        .objectives-section {
            margin-bottom: 50px;
        }

        .objectives-section-title {
            font-size: 1.3em;
            font-weight: 700;
            color: #aaa;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid #2a2a2a;
        }

        /* Two-column table layout */
        .objectives-columns {
            display: block;
            width: 100%;
        }

        /* Row containing left and right columns */
        .objective-row {
            display: table;
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 0;
        }

        /* Column within a row */
        .objective-column {
            display: table-cell;
            vertical-align: top;
            width: 50%;
            padding-right: 32px;
            padding-left: 20px;
            border-left: 2px solid #4a4a4a;
        }

        .objective-column:first-child {
            padding-left: 20px;
        }

        .objective-column:last-child {
            padding-right: 0;
        }

        /* Individual Objective Entries */
        .objective-entry {
            display: block;
            margin-bottom: 20px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s ease;
            overflow: hidden;
        }

        .objective-entry:hover .obj-title {
            color: #4da6ff;
        }

        /* Flagged items */
        .objective-entry.flagged:hover .obj-title {
            color: #ff6b6b;
        }

        .objective-entry.flagged .obj-number {
            border-bottom-color: #ff6b6b;
        }

        /* Number with underline accent - floats left */
        .obj-number {
            float: left;
            font-size: 2.4em;
            font-weight: 700;
            color: #5a5a5a;
            letter-spacing: -2px;
            line-height: 1;
            padding-bottom: 6px;
            border-bottom: 2px solid #5a5a5a;
            width: 70px;
            text-align: center;
            margin-right: 16px;
            margin-bottom: 4px;
            transition: all 0.2s ease;
        }

        .objective-entry.flagged .obj-number {
            color: #ff6b6b;
            border-bottom-color: #ff6b6b;
        }

        /* Text container - flows around floated number */
        .obj-text {
            overflow: hidden;
        }

        /* Objective Title */
        .obj-title {
            font-size: 1.1em;
            font-weight: 700;
            color: #ddd;
            letter-spacing: 0.2px;
            line-height: 1.5;
            transition: color 0.2s ease;
            word-wrap: break-word;
        }

        /* Status Indicator - small dot or "Needs Review" text */
        .obj-indicator {
            font-size: 0.85em;
            margin-left: 8px;
            font-weight: bold;
            color: #4da6ff;
            display: inline;
            letter-spacing: 0.5px;
        }

        .obj-indicator.flagged {
            color: #ff6b6b;
            font-style: italic;
            font-weight: 700;
        }

        /* Responsive adjustments */
        @media (max-width: 620px) {
            .title-page {
                padding: 40px 20px;
            }

            .title-page h1 {
                font-size: 2.2em;
            }

            .objectives-columns {
                display: block;
            }

            .objective-column {
                display: block;
                width: 100%;
                padding-right: 0;
                padding-left: 0;
                margin-bottom: 0;
            }

            .objective-entry {
                margin-bottom: 16px;
            }

            .obj-number {
                font-size: 2em;
                min-width: 60px;
                margin-right: 12px;
                padding-bottom: 4px;
            }

            .obj-title {
                font-size: 0.9em;
            }
        }
        """

        # Build full HTML document
        content = "".join(content_parts)
        html = (
            "<!DOCTYPE html><html><head><style>\n"
            f"{renderer._load_stylesheet()}\n"
            f"{css}\n"
            "</style></head><body>"
            f'<div class="page">{content}</div>'
            "</body></html>"
        )

        return html

    def adjust_font_scale(self, delta):
        """Steps the reading text size within a sane range."""
        new_scale = round(self.font_scale + delta, 2)

        if not self.FONT_SCALE_MIN <= new_scale <= self.FONT_SCALE_MAX:
            return

        self.font_scale = new_scale
        self.html_view.configure(fontscale=new_scale)

    # --- LINK HANDLING --- #
    def on_link_click(self, url):
        """Routes clicks instead of letting the pane try to navigate.

        Three cases: in-page anchors scroll, note: links switch notes, and real
        URLs open in the system browser rather than inside the reading pane.
        """
        if not url:
            return

        if "note:" in url:
            note_id = unquote(url.split("note:", 1)[1]).strip("/")
            target = library.find_note(self.sections, note_id)
            if target:
                self.select_note(target)
            else:
                print(f"Note link points at an unknown note: {note_id}")
            return

        parsed = urlparse(url)

        if parsed.scheme in ("http", "https"):
            webbrowser.open(url)
            return

        if parsed.fragment:
            self.scroll_to_anchor(parsed.fragment)

    def scroll_to_anchor(self, anchor):
        """Scrolls the pane to a heading anchor generated by the toc extension."""
        try:
            element = self.html_view.document.getElementById(anchor)
            if element is not None:
                self.html_view.yview(element.node)
                return
        except Exception:
            pass  # fall through to the reload-with-fragment path

        if self.current_note:
            self.html_view.load_html(
                renderer.render_note(self.current_note),
                fragment=anchor,
            )
