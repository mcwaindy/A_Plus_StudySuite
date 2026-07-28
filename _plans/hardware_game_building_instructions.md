Here is a detailed guide on how to add new images, categories, and JSON entries to extend the **Hardware Identification Mini-Game**!

---

# 📸 Hardware Identification Expansion Guide

This guide explains how to add new images (cables, network connectors, printer components, tools, RAM SODIMMs, etc.), map them in `data/hardware_images.json`, and categorize them so they dynamically integrate into **Module 2.c (Hardware Identification Game)** and **NotesView**.

---

## 📂 File & Directory Structure

When adding new hardware assets, place image files inside your `assets/` directory and map them inside `data/hardware_images.json`:

```text
A+_StudyProgram/
├── assets/
│   └── notes/
│       └── images/              <-- Place standalone hardware photos here (.png, .jpg, .webp)
│           ├── cat6a_cable.png
│           ├── laser_fuser.png
│           └── fiber_lc.png
├── data/
│   └── hardware_images.json     <-- Map quiz entries, options, & answers here
└── modules/
    └── game_view.py             <-- Automatically loads entries from hardware_images.json

```

---

## 📝 JSON Entry Schema (`data/hardware_images.json`)

Each entry inside `data/hardware_images.json` is represented as an object in the `"hardware_items"` array.

### Field Breakdown

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | `string` | A unique key identifier for the item (e.g., `"cable_lc_fiber"`). |
| `category` | `string` | The hardware grouping (e.g., `"Cables & Connectors"`, `"Printer Components"`). |
| `name` | `string` | The official name of the hardware component. |
| `image_path` | `string` | Relative path to the image file (e.g., `"assets/notes/images/fiber_lc.png"`). |
| `options` | `array` | Exactly **4 string choices** displayed during the game. |
| `correct_index` | `integer` | The zero-based index (`0`, `1`, `2`, or `3`) corresponding to the correct choice in `options`. |
| `explanation` | `string` | Brief exam note explaining the component's primary function and key CompTIA details. |

---

## 🛠️ Complete JSON Schema Template

Save this template into `data/hardware_images.json`. As you add new study images to `assets/notes/images/`, simply append new objects to the `"hardware_items"` array:

```json
{
  "hardware_items": [
    {
      "id": "cable_cat6a",
      "category": "Cables & Connectors",
      "name": "Cat 6a Twisted Pair Cable",
      "image_path": "assets/notes/images/cat6a_cable.png",
      "options": [
        "Cat 5e Cable",
        "Cat 6a Cable",
        "RG-6 Coaxial Cable",
        "Single-Mode Fiber"
      ],
      "correct_index": 1,
      "explanation": "Cat 6a features thicker shielding and tighter wire twists to support 10 Gbps speeds up to 100 meters (328 feet)."
    },
    {
      "id": "connector_lc_fiber",
      "category": "Cables & Connectors",
      "name": "LC Fiber Optic Connector",
      "image_path": "assets/notes/images/fiber_lc.png",
      "options": [
        "ST Fiber Connector",
        "SC Fiber Connector",
        "LC Fiber Connector",
        "BNC Connector"
      ],
      "correct_index": 2,
      "explanation": "Lucent Connector (LC) is a Small Form Factor (SFF) fiber optic connector utilizing a push-pull latching mechanism."
    },
    {
      "id": "printer_fuser",
      "category": "Printer Components",
      "name": "Laser Printer Fuser Assembly",
      "image_path": "assets/notes/images/laser_fuser.png",
      "options": [
        "Transfer Roller",
        "Primary Corona Wire",
        "Fuser Assembly",
        "Pickup Roller"
      ],
      "correct_index": 2,
      "explanation": "The fuser assembly uses pressure and high heat (approx. 350°F–400°F) to melt toner powder directly onto the paper."
    },
    {
      "id": "printer_transfer_belt",
      "category": "Printer Components",
      "name": "Color Laser Transfer Belt",
      "image_path": "assets/notes/images/transfer_belt.png",
      "options": [
        "Transfer Belt / Roller",
        "Duplexing Assembly",
        "Developer Roller",
        "Separation Pad"
      ],
      "correct_index": 0,
      "explanation": "In color laser printers, the transfer belt consolidates all four toner colors (Cyan, Magenta, Yellow, Black) before transferring the complete image to the paper."
    },
    {
      "id": "storage_sata_data",
      "category": "Storage & Expansion",
      "name": "7-Pin SATA Data Cable",
      "image_path": "assets/notes/images/sata_data_cable.png",
      "options": [
        "PATA / IDE Ribbon Cable",
        "SATA Data Cable",
        "eSATA Cable",
        "Molex Cable"
      ],
      "correct_index": 1,
      "explanation": "Standard 7-pin SATA data cables connect 2.5-inch SSDs, 3.5-inch HDDs, and optical drives to the motherboard at speeds up to 6 Gbps (SATA 3.0)."
    }
  ]
}

```

---

## 🏷️ Adding & Registering New Hardware Categories

To add a brand-new category (e.g., `"Network Tools"` or `"RAM & Memory Types"`) so users can filter by it in the setup screen:

### Step 1: Add JSON Items with the New Category Name

In `data/hardware_images.json`, set `"category"` to your new category name:

```json
{
  "id": "tool_crimper",
  "category": "Network Tools",
  "name": "RJ-45 Modular Crimper",
  "image_path": "assets/notes/images/rj45_crimper.png",
  "options": [
    "Punch Down Tool",
    "Cable Stripper",
    "RJ-45 Modular Crimper",
    "Tone Generator & Probe"
  ],
  "correct_index": 2,
  "explanation": "A modular crimper pinches the metallic contacts inside an RJ-45 or RJ-11 connector onto individual twisted-pair wire leads."
}

```

### Step 2: Update Category Dropdown in `modules/game_view.py`

In `modules/game_view.py`, find the `show_setup_screen()` method and add your new category option string to `self.category_menu`:

```python
self.category_menu = ctk.CTkOptionMenu(
    card,
    values=[
        "All Hardware Mix",
        "Motherboard Layout",
        "Cables & Connectors",
        "Printer Components",
        "Network Tools",          # <-- ADD YOUR NEW CATEGORY HERE
        "RAM & Memory Types"      # <-- ADD YOUR NEW CATEGORY HERE
    ],
    width=250
)

```

### Step 3: Update Filter Logic in `build_round_deck()`

In `modules/game_view.py`, add a matching `elif` check inside `build_round_deck()` so the game knows which items to pull into the deck when that category is selected:

```python
def build_round_deck(self):
    self.round_deck = []

    # 1. Motherboard Items
    if self.selected_category in ["All Hardware Mix", "Motherboard Layout"]:
        mb_info = self.all_boards_data.get("modern_atx", {})
        for comp in mb_info.get("components", []):
            self.round_deck.append({"type": "motherboard", "data": comp})

    # 2. Standalone Image Items
    if self.selected_category != "Motherboard Layout":
        for item in self.hardware_items:
            cat = item.get("category", "")
            
            # Match item category against selected dropdown filter
            if (
                self.selected_category == "All Hardware Mix"
                or (self.selected_category == "Cables & Connectors" and "Cable" in cat)
                or (self.selected_category == "Printer Components" and "Printer" in cat)
                or (self.selected_category == "Network Tools" and "Tools" in cat)       # <-- ADD THIS
                or (self.selected_category == "RAM & Memory Types" and "Memory" in cat) # <-- ADD THIS
            ):
                self.round_deck.append({"type": "image_item", "data": item})

    random.shuffle(self.round_deck)

```

---

## 💡 Best Practices for Adding Images

1. **Resolution & Aspect Ratio:**
* Standardize standalone images to roughly **400×400** to **600×600** pixels.
* `Pillow` will automatically scale down larger images using `thumbnail()`, but smaller files keep app load times fast.


2. **Transparent / Clean Backgrounds:**
* Use `.png` images with neutral white, dark gray, or transparent backgrounds so hardware components remain clear in both Light and Dark UI modes.


3. **Plausible Distractors:**
* When writing the 4 string choices in `"options"`, include closely related A+ exam terms (e.g., put ST and SC fiber connectors as wrong options for an LC fiber question) to reinforce critical exam distinctions.