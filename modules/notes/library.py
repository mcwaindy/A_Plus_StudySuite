import re

from utils.paths import project_path


NOTES_ROOT = project_path("assets", "notes")

# Folders map to sidebar sections. Anything else falls back to a title-cased
# folder name, so dropping in assets/notes/networking/ just works.
GROUP_LABELS = {
    "core1": "Core 1 · 220-1101",
    "core2": "Core 2 · 220-1102",
    "": "General",
}
GROUP_ORDER = ["core1", "core2", ""]

# Matches an optional core prefix, an objective number, then the topic:
#   core1_1.1_cables.md  ->  core1 / 1.1 / cables
#   3.2_ram.md           ->  ----- / 3.2 / ram
FILENAME_RE = re.compile(
    r"^(?:core(?P<core>\d+)[_\-\s]+)?(?P<objective>\d+(?:\.\d+)*)[_\-\s]+(?P<topic>.+)$"
)

FRONT_MATTER_FENCE = re.compile(r"^-{3}\s*$")
FRONT_MATTER_KEY = re.compile(r"^(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)$")


def split_front_matter(text: str):
    """Separates a leading --- fenced metadata block from the note body.

    Mirrors the subset of Python-Markdown's meta extension we actually use, so the
    sidebar can index dozens of files without paying for a full markdown parse.

    :param text: Raw file contents.
    :return: (metadata dict with lowercased keys, body string).
    """
    lines = text.splitlines()

    if not lines or not FRONT_MATTER_FENCE.match(lines[0]):
        return {}, text

    meta = {}

    for i, line in enumerate(lines[1:], start=1):
        if FRONT_MATTER_FENCE.match(line) or line.strip() == "...":
            return meta, "\n".join(lines[i + 1:])

        match = FRONT_MATTER_KEY.match(line)
        if match:
            meta[match.group("key").lower()] = match.group("value").strip()

    # Unterminated fence -- treat the whole file as body rather than eating it.
    return {}, text


def _natural_key(objective: str):
    """Sort key so 1.2 comes before 1.10 instead of after it."""
    if not objective:
        return (1, [])
    return (0, [int(part) if part.isdigit() else 0 for part in objective.split(".")])


def _group_for(path, meta):
    """Determines which sidebar section a note belongs to."""
    relative = path.relative_to(NOTES_ROOT)
    folder = relative.parts[0].lower() if len(relative.parts) > 1 else ""

    # Flat files can still declare their core via front matter or a core1_ prefix.
    if not folder:
        core = meta.get("core", "")
        if not core:
            match = FILENAME_RE.match(path.stem)
            core = match.group("core") if match and match.group("core") else ""
        if core:
            folder = f"core{core}"

    label = GROUP_LABELS.get(folder) or folder.replace("_", " ").title()
    return folder, label


def _title_from_filename(stem: str):
    """Derives (objective, title) from a filename when front matter is absent."""
    match = FILENAME_RE.match(stem)

    if not match:
        return "", stem.replace("_", " ").replace("-", " ").strip().title()

    topic = match.group("topic").replace("_", " ").replace("-", " ").strip()
    return match.group("objective"), topic.title()


def load_note(path):
    """Reads one .md file and builds its index record.

    :param path: Path to a markdown file under NOTES_ROOT.
    :return: Note dict, or None if the file could not be read.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Could not read note {path}: {e}")
        return None

    meta, body = split_front_matter(text)
    group_key, group_label = _group_for(path, meta)
    fallback_objective, fallback_title = _title_from_filename(path.stem)

    objective = meta.get("objective", fallback_objective)
    title = meta.get("title", fallback_title)

    relative = path.relative_to(NOTES_ROOT)

    return {
        "id": relative.with_suffix("").as_posix(),
        "path": path,
        "group_key": group_key,
        "group_label": group_label,
        "objective": objective,
        "title": title,
        "label": f"{objective}  {title}".strip() if objective else title,
        "is_empty": not body.strip(),
        "sort_key": (_natural_key(objective), title.lower()),
    }


def discover_notes():
    """Scans assets/notes/ for markdown files and returns them grouped for the sidebar.

    Files beginning with '_' or '.' are skipped, which is how _TEMPLATE.md stays out
    of the list. Replaces the old hardcoded notes_map, so the index can never drift
    from what is actually on disk.

    :return: List of {"key", "label", "notes": [...]} in GROUP_ORDER, then alphabetical.
    """
    if not NOTES_ROOT.exists():
        return []

    notes = []

    for path in NOTES_ROOT.rglob("*.md"):
        if path.name.startswith(("_", ".")):
            continue
        note = load_note(path)
        if note:
            notes.append(note)

    grouped = {}
    for note in notes:
        grouped.setdefault(note["group_key"], []).append(note)

    def group_rank(key):
        return (GROUP_ORDER.index(key), "") if key in GROUP_ORDER else (len(GROUP_ORDER), key)

    sections = []
    for key in sorted(grouped, key=group_rank):
        entries = sorted(grouped[key], key=lambda n: n["sort_key"])
        sections.append(
            {
                "key": key,
                "label": entries[0]["group_label"],
                "notes": entries,
            }
        )

    return sections


def find_note(sections, note_id):
    """Looks up a note by id across all sections. Returns None if absent."""
    for section in sections:
        for note in section["notes"]:
            if note["id"] == note_id:
                return note
    return None


def count_written(sections):
    """Returns (notes with content, total notes) for the sidebar progress footer."""
    total = sum(len(s["notes"]) for s in sections)
    written = sum(1 for s in sections for n in s["notes"] if not n["is_empty"])
    return written, total
