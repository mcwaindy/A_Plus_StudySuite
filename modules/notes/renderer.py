import re
from html import escape

import markdown

from modules.notes.library import split_front_matter
from utils.paths import PROJECT_ROOT, as_file_url, project_path


STYLESHEET = project_path("assets", "styles", "notes.css")

EXTENSIONS = [
    "meta",          # safety net for stray metadata lines
    "toc",           # anchors + the on-this-page card
    "attr_list",     # ![alt](path){.bare}
    "admonition",    # !!! exam "Exam Tip"
    "def_list",      # term/definition blocks
    "sane_lists",
    "tables",
    "fenced_code",
    "nl2br",         # keeps Word-pasted line breaks intact; drop this line for soft wrapping
]
EXTENSION_CONFIGS = {"toc": {"toc_depth": "2-3"}}

# Show the on-this-page card only once a note is long enough to need it.
TOC_MIN_HEADINGS = 4

GROUP_BADGES = {"core1": "Core 1", "core2": "Core 2"}

LEADING_H1_RE = re.compile(r"\A\s*<h1[^>]*>(?P<text>.*?)</h1>", re.IGNORECASE | re.DOTALL)
STANDALONE_IMG_RE = re.compile(r"<p>\s*(?P<tag><img\b[^>]*?/?>)\s*</p>", re.IGNORECASE)
IMG_TAG_RE = re.compile(r"<img\b[^>]*?/?>", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
EXTERNAL_SRC_RE = re.compile(r"\A(?:https?:|file:|data:)", re.IGNORECASE)


def _attr(tag: str, name: str) -> str:
    """Pulls a double-quoted attribute value out of a tag string."""
    match = re.search(rf'\b{name}\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
    return match.group(1) if match else ""


def _with_src(tag: str, new_src: str) -> str:
    """Returns the tag with its src attribute swapped for new_src."""
    return re.sub(r'(\bsrc\s*=\s*")[^"]*(")', lambda m: m.group(1) + new_src + m.group(2),
                  tag, count=1, flags=re.IGNORECASE)


def _display_src(resolved):
    """Returns a source string that stays inside the project tree when possible."""
    try:
        relative = resolved.relative_to(PROJECT_ROOT)
    except ValueError:
        return as_file_url(resolved)
    return relative.as_posix()


def _resolve_image(src: str, note_dir):
    """Locates an image referenced from a note.

    Tries the note's own folder first so ../../images/... paths preview correctly in
    an external markdown editor, then falls back to project-root-relative so plain
    assets/images/... paths work too.

    :return: Absolute Path if found, None if the file does not exist.
    """
    if not src or EXTERNAL_SRC_RE.match(src):
        return None

    for candidate in (note_dir / src, PROJECT_ROOT / src):
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved

    return None


def _missing_image_block(src: str) -> str:
    """Dashed placeholder naming the path, so pending artwork is visible not silent."""
    return (
        '<div class="img-missing">'
        '<div class="img-missing-title">Image not found</div>'
        f'<div class="img-missing-path">{escape(src)}</div>'
        "</div>"
    )


def _process_images(html_body: str, note_dir) -> str:
    """Resolves image paths, wraps standalone images in captioned figures, and
    swaps unresolvable ones for a visible placeholder.
    """

    def standalone(match):
        tag = match.group("tag")
        src = _attr(tag, "src")

        if EXTERNAL_SRC_RE.match(src):
            return match.group(0)

        resolved = _resolve_image(src, note_dir)
        if resolved is None:
            return _missing_image_block(src)

        alt = _attr(tag, "alt")
        caption = f"<figcaption>{alt}</figcaption>" if alt else ""
        return f'<figure>{_with_src(tag, _display_src(resolved))}{caption}</figure>'

    html_body = STANDALONE_IMG_RE.sub(standalone, html_body)

    # Second pass catches images inside lists, tables, or inline runs, which the
    # figure pass deliberately leaves alone.
    def inline(match):
        tag = match.group(0)
        src = _attr(tag, "src")

        if EXTERNAL_SRC_RE.match(src):
            return tag

        resolved = _resolve_image(src, note_dir)
        if resolved is None:
            return f'<span class="img-missing-path">[missing: {escape(src)}]</span>'

        return _with_src(tag, _display_src(resolved))

    return IMG_TAG_RE.sub(inline, html_body)


def _count_headings(tokens) -> int:
    """Recursively counts entries in the toc extension's token tree."""
    return sum(1 + _count_headings(token.get("children", [])) for token in tokens)


def _badge_text(note) -> str:
    """Builds the header badge, e.g. 'Core 1 · 1.1'."""
    parts = [GROUP_BADGES.get(note.get("group_key", ""), "")]
    if note.get("objective"):
        parts.append(note["objective"])
    return " · ".join(p for p in parts if p)


def _load_stylesheet() -> str:
    """Reads the theme from disk on every render so Reload picks up CSS edits too."""
    try:
        return STYLESHEET.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Could not read {STYLESHEET}: {e}")
        return "body { background-color: #2b2b2b; color: #e0e0e0; }"


def _document(content: str) -> str:
    """Wraps rendered content in a full HTML document with the theme attached."""
    return (
        "<!DOCTYPE html><html><head><style>\n"
        f"{_load_stylesheet()}\n"
        "</style></head><body>"
        f'<div class="page">{content}</div>'
        "</body></html>"
    )


def render_note(note) -> str:
    """Converts a note record into a complete styled HTML document.

    :param note: Note dict from modules.notes.library.
    :return: HTML string ready for HtmlFrame.load_html().
    """
    try:
        raw = note["path"].read_text(encoding="utf-8")
    except OSError as e:
        return render_notice(
            "Could not open note",
            f"{escape(str(note['path']))}<br><br>{escape(str(e))}",
        )

    meta, body = split_front_matter(raw)

    md = markdown.Markdown(extensions=EXTENSIONS, extension_configs=EXTENSION_CONFIGS)
    html_body = md.convert(body)

    title = meta.get("title") or note.get("title", "")

    # The header card already shows the title; drop a duplicate leading H1, and
    # adopt its text when front matter did not supply one.
    leading = LEADING_H1_RE.match(html_body)
    if leading:
        if not meta.get("title"):
            title = TAG_RE.sub("", leading.group("text")).strip() or title
        html_body = html_body[leading.end():]

    html_body = _process_images(html_body, note["path"].parent)

    badge = _badge_text(note)
    header = (
        '<div class="note-header">'
        + (
            f'<div class="note-badge-row"><span class="note-badge">{escape(badge)}</span></div>'
            if badge
            else ""
        )
        + f'<div class="note-title">{escape(title)}</div>'
        "</div>"
    )

    toc = ""
    if _count_headings(getattr(md, "toc_tokens", [])) >= TOC_MIN_HEADINGS:
        toc = (
            '<div class="toc-card">'
            '<div class="toc-title">On this page</div>'
            f"{md.toc}"
            "</div>"
        )

    if not body.strip():
        html_body = _empty_note_body(note)

    return _document(header + toc + html_body)


def _empty_note_body(note) -> str:
    """Guidance shown for a stub note that has front matter but no content yet."""
    return (
        '<div class="notice">'
        '<div class="notice-title">This note is empty</div>'
        '<div class="notice-body">'
        f"Write it in <code>{escape(str(note['path']))}</code>, then press "
        "<strong>Reload</strong> — no need to restart the app.<br><br>"
        "See <code>assets/notes/_TEMPLATE.md</code> for the front matter, callout, "
        "and image conventions."
        "</div></div>"
    )


def render_notice(title: str, message: str) -> str:
    """Renders a standalone notice page for empty states and load failures.

    :param title: Short heading.
    :param message: Body text. May contain simple HTML.
    """
    return _document(
        '<div class="notice">'
        f'<div class="notice-title">{escape(title)}</div>'
        f'<div class="notice-body">{message}</div>'
        "</div>"
    )


def base_url() -> str:
    """file:// base for HtmlFrame, independent of the process working directory."""
    return as_file_url(PROJECT_ROOT)
