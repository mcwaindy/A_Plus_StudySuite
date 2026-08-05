# Project Structure Overview

## Directory Tree

```
A_Plus_StudySuite/
│
├── main.py                          # Application entry point
├── requirements.txt                 # Dependency list
├── .gitignore                       # Git ignore patterns
│
├── docs/                            # Documentation (NEW)
│   ├── README.md                    # Project overview & architecture
│   ├── DEVELOPMENT.md               # Development guide & setup
│   ├── COORDINATE_PICKER_GUIDE.md   # Coordinate picker tool usage
│   └── DATA_SCHEMA.md               # Data structure reference
│
├── modules/                         # Application screens & views
│   ├── __init__.py
│   ├── diagram_view.py              # Motherboard diagram viewer
│   ├── game_view.py                 # Hardware identification game
│   ├── notes_view.py                # Study notes browser
│   ├── exam_view.py                 # Exam simulator
│   ├── flashcards_view.py           # Flashcard study tool
│   ├── custom_exam_view.py          # Custom exam builder
│   ├── diagram/                     # Shared diagram components
│   │   ├── __init__.py
│   │   └── canvas_widget.py         # Motherboard canvas renderer
│   └── notes/                       # Notes rendering system
│       ├── __init__.py
│       ├── library.py               # Notes catalog management
│       ├── renderer.py              # HTML/Markdown rendering
│       └── html_compat.py           # HTML compatibility layer
│
├── tools/                           # Standalone utilities
│   ├── __init__.py
│   ├── coordinate_picker.py         # Coordinate picker launcher
│   └── coordinate_picker_main.py    # Coordinate picker UI
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── board_registry.py            # Motherboard data persistence
│   ├── image_library.py             # Image catalog loader
│   ├── coordinate_translator.py     # Coordinate system conversions
│   └── paths.py                     # Path utility functions
│
├── data/                            # Application data
│   ├── motherboard/
│   │   └── motherboard_nodes.json   # Motherboard registry (hotspots, scaling)
│   ├── image_catalog.json           # Image quiz data & options
│   ├── flashcards.json              # Flashcard definitions
│   └── questions.json               # Exam questions
│
├── assets/                          # Static resources
│   ├── images/                      # Image library
│   │   ├── motherboard/             # Motherboard board PNG images
│   │   ├── cables/                  # Cable and connector images
│   │   ├── display/                 # Display technology images
│   │   ├── memory/                  # RAM and memory images
│   │   ├── expansion/               # Expansion card images
│   │   ├── cooling/                 # CPU cooler images
│   │   ├── cpu/                     # CPU component images
│   │   ├── storage/                 # Storage device images
│   │   ├── networking/              # Network component images
│   │   ├── power/                   # Power supply images
│   │   ├── printers/                # Printer images
│   │   ├── tools/                   # Tool and diagnostic images
│   │   └── mobile/                  # Mobile device images
│   ├── notes/                       # Study notes (Markdown)
│   │   └── core1/                   # CompTIA A+ Core 1 topics
│   └── styles/                      # CSS stylesheets
│
├── archive/                         # Archived/old files
├── env/                             # Python virtual environment
├── _plans/                          # Implementation plans (project management)
├── .vscode/                         # VS Code settings
├── .vs/                             # Visual Studio data
├── .idea/                           # IntelliJ IDEA settings
└── __pycache__/                     # Python cache (ignored)
```

## File Categories

### Source Code (Production)
- `main.py` - Single entry point
- `modules/` - UI layer (6 main views + helpers)
- `tools/` - External utilities
- `utils/` - Shared utilities
- All `.py` files: ~12 production modules

### Data Files
- `data/motherboard/motherboard_nodes.json` - Board registry
- `data/image_catalog.json` - Quiz images
- `data/flashcards.json` - Flashcard data
- `data/questions.json` - Exam questions

### Static Assets
- `assets/images/` - 15+ image categories
- `assets/notes/` - Study markdown content
- `assets/styles/` - CSS

### Documentation
- `docs/README.md` - Project overview
- `docs/DEVELOPMENT.md` - Developer guide
- `docs/COORDINATE_PICKER_GUIDE.md` - Tool documentation
- `docs/DATA_SCHEMA.md` - Data structure reference

### Root Configuration
- `requirements.txt` - Dependencies
- `.gitignore` - Git configuration

## Cleanup Complete ✓

### Removed Files (28 total)
- ❌ 2 test scripts (`test_display_scale.py`, `test_picker_launch.py`)
- ❌ 1 duplicate launcher (`run_coordinate_picker.py`)
- ❌ 2 old module versions (`diagram_view_old.py`, `game_view_old.py`)
- ❌ 19 temporary markdown documentation files
- ❌ 4 empty reference text files (.txt)
- ❌ 1 temporary output log
- ❌ 1 legacy SVG parser (`utils/svg_parser.py`)

### Result
✓ **Clean, organized structure**
✓ **Only production code in root directories**
✓ **Comprehensive documentation in `/docs`**
✓ **Zero duplicate/obsolete files**
✓ **Clear separation of concerns**

## Key Improvements

1. **Single Entry Point**: `main.py` is the only production file in root
2. **Organized Sources**: Source code logically grouped by function
3. **Complete Documentation**: All aspects documented in `/docs` directory
4. **Clean Data Layer**: JSON data centralized and validated
5. **Asset Management**: Static files organized by type and category
6. **Tool Isolation**: Standalone utilities separate and documented
7. **No Clutter**: No test files, logs, or temp documentation

## Quick Start

### Run Application
```bash
python main.py
```

### Launch Coordinate Picker
```bash
python tools/coordinate_picker.py
```

### See Documentation
- Start with `docs/README.md` for overview
- Check `docs/DEVELOPMENT.md` for setup and contribution
- Use `docs/DATA_SCHEMA.md` for data structure info
- See `docs/COORDINATE_PICKER_GUIDE.md` for tool usage

---

**Repository**: Branch `ui_refinement` - A clean, production-ready structure
