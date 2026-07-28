import json

from utils.paths import project_path


CATALOG_FILE = project_path("data", "image_catalog.json")
IMAGES_ROOT = project_path("assets", "images")

# Parsed catalog is cached because both NotesView and GameView read it, often
# several times per session. Call load_catalog(force=True) after editing the JSON.
_cache = None


def load_catalog(force: bool = False) -> dict:
    """Reads and validates data/image_catalog.json.

    Every image entry is resolved to an absolute path and given its category label.
    Malformed entries are skipped with a console warning rather than raising, so one
    bad record never takes down the app.

    :param force: Re-read from disk instead of returning the cached parse.
    :return: {"categories": [...], "images": [...], "warnings": [...]}
    """
    global _cache

    if _cache is not None and not force:
        return _cache

    catalog = {"categories": [], "images": [], "warnings": []}

    if not CATALOG_FILE.exists():
        catalog["warnings"].append(f"Catalog not found: {CATALOG_FILE}")
        _cache = catalog
        return catalog

    try:
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        catalog["warnings"].append(f"Catalog is not valid JSON: {e}")
        _cache = catalog
        return catalog

    catalog["categories"] = [
        c for c in raw.get("categories", []) if c.get("key") and c.get("label")
    ]
    labels = {c["key"]: c["label"] for c in catalog["categories"]}

    seen_ids = set()

    for entry in raw.get("images", []):
        item = _build_item(entry, labels, seen_ids, catalog["warnings"])
        if item:
            catalog["images"].append(item)
            seen_ids.add(item["id"])

    _cache = catalog
    return catalog


def _build_item(entry, labels, seen_ids, warnings):
    """Validates one raw catalog entry and expands it into a resolved item dict."""
    item_id = entry.get("id")
    category = entry.get("category")
    filename = entry.get("file")

    if not item_id or not category or not filename:
        warnings.append(f"Skipped entry missing id/category/file: {entry!r:.80}")
        return None

    if item_id in seen_ids:
        warnings.append(f"Duplicate image id '{item_id}' -- keeping the first one.")
        return None

    if category not in labels:
        warnings.append(
            f"'{item_id}' uses category '{category}', which is not declared in "
            f"the catalog's categories list."
        )
        return None

    image_path = IMAGES_ROOT / category / filename

    item = {
        "id": item_id,
        "name": entry.get("name", item_id),
        "category_key": category,
        "category": labels[category],
        "file": filename,
        "image_path": image_path,
        "exists": image_path.exists(),
        "objectives": entry.get("objectives", []),
        "quiz": None,
    }

    quiz = entry.get("quiz")
    if quiz:
        options = quiz.get("options", [])
        correct = quiz.get("correct_index", 0)

        if len(options) < 2:
            warnings.append(f"'{item_id}' quiz needs at least 2 options -- ignoring quiz.")
        elif not 0 <= correct < len(options):
            warnings.append(
                f"'{item_id}' correct_index {correct} is out of range for "
                f"{len(options)} options -- ignoring quiz."
            )
        else:
            item["quiz"] = {
                "options": options,
                "correct_index": correct,
                "explanation": quiz.get("explanation", ""),
            }

    return item


def categories(with_quiz_items: bool = False) -> list:
    """Returns declared categories as [{"key", "label"}].

    :param with_quiz_items: Only return categories that currently have at least one
        playable quiz item, so the game dropdown never offers an empty deck.
    """
    catalog = load_catalog()

    if not with_quiz_items:
        return list(catalog["categories"])

    playable = {
        img["category_key"]
        for img in catalog["images"]
        if img["quiz"] and img["exists"]
    }
    return [c for c in catalog["categories"] if c["key"] in playable]


def quiz_items(category_key=None, objectives=None) -> list:
    """Returns game-ready items, flattened into the shape GameView already consumes.

    Items without a quiz block, or whose image file is missing from disk, are excluded
    so the game never renders an empty picture frame.

    :param category_key: Restrict to one category key, or None for all.
    :param objectives: Iterable of objective strings to match, or None for all.
    :return: List of dicts with image_path, options, correct_index, explanation, category.
    """
    wanted = set(objectives) if objectives else None
    results = []

    for img in load_catalog()["images"]:
        if not img["quiz"] or not img["exists"]:
            continue
        if category_key and img["category_key"] != category_key:
            continue
        if wanted and not wanted.intersection(img["objectives"]):
            continue

        results.append(
            {
                "id": img["id"],
                "name": img["name"],
                "category": img["category"],
                "category_key": img["category_key"],
                "image_path": str(img["image_path"]),
                "options": img["quiz"]["options"],
                "correct_index": img["quiz"]["correct_index"],
                "explanation": img["quiz"]["explanation"],
            }
        )

    return results


def images_for_objective(objective: str) -> list:
    """Returns every catalog image tagged with the given objective, quiz or not."""
    return [
        img
        for img in load_catalog()["images"]
        if objective in img["objectives"] and img["exists"]
    ]


def missing_files() -> list:
    """Returns catalog entries whose image file is not on disk yet."""
    return [img for img in load_catalog()["images"] if not img["exists"]]


def _report():
    """Console validation summary. Run with: python -m utils.image_library"""
    catalog = load_catalog(force=True)
    images = catalog["images"]

    print(f"\nCatalog: {CATALOG_FILE}")
    print(f"Images root: {IMAGES_ROOT}\n")

    print(f"{len(catalog['categories'])} categories declared, "
          f"{len(categories(with_quiz_items=True))} currently playable:")
    for cat in catalog["categories"]:
        in_cat = [i for i in images if i["category_key"] == cat["key"]]
        playable = [i for i in in_cat if i["quiz"] and i["exists"]]
        print(f"  {cat['key']:<13} {cat['label']:<24} "
              f"{len(in_cat)} image(s), {len(playable)} playable")

    missing = missing_files()
    print(f"\n{len(images)} entries, {len(images) - len(missing)} resolved on disk.")

    if missing:
        print(f"\n{len(missing)} entry/entries awaiting artwork:")
        for img in missing:
            print(f"  {img['id']:<24} -> {img['image_path']}")

    if catalog["warnings"]:
        print(f"\n{len(catalog['warnings'])} warning(s):")
        for warning in catalog["warnings"]:
            print(f"  {warning}")
    else:
        print("\nNo schema warnings.")


if __name__ == "__main__":
    _report()
