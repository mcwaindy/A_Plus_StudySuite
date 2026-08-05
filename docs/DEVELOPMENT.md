# Development Guide

## Setup

### Prerequisites
- Python 3.14+
- customtkinter
- Pillow (PIL)
- tkinterweb (for HTML rendering in notes)

### Installation
```bash
cd A_Plus_StudySuite
python -m venv env
env\Scripts\activate
pip install customtkinter Pillow tkinterweb
```

### Running the Application
```bash
python main.py
```

## Project Structure

### Clear Separation of Concerns

```
A_Plus_StudySuite/
├── main.py                 # Application entry point
├── modules/                # UI screens and views
│   ├── diagram_view.py    # Motherboard diagram viewer
│   ├── game_view.py       # Game implementation
│   ├── notes_view.py      # Notes browser
│   ├── exam_view.py       # Exam simulator
│   ├── flashcards_view.py # Flashcard study
│   ├── custom_exam_view.py # Custom exam builder
│   ├── diagram/           # Shared diagram components
│   │   └── canvas_widget.py # Motherboard rendering widget
│   └── notes/             # Notes rendering
│       ├── library.py     # Notes catalog
│       ├── renderer.py    # HTML/Markdown rendering
│       └── html_compat.py # HTML compatibility
├── tools/                  # Standalone tools
│   ├── coordinate_picker.py      # Picker launcher
│   └── coordinate_picker_main.py # Picker UI
├── utils/                  # Utilities
│   ├── board_registry.py         # Board data persistence
│   ├── image_library.py          # Image catalog loader
│   ├── coordinate_translator.py  # Coordinate conversions
│   └── paths.py                  # Path utilities
├── data/                   # Application data
│   ├── motherboard/
│   │   └── motherboard_nodes.json # Board registry
│   ├── image_catalog.json         # Image quiz data
│   ├── flashcards.json            # Flashcard definitions
│   └── questions.json             # Exam questions
├── assets/                 # Static resources
│   ├── images/             # Image library by category
│   ├── notes/              # Study notes markdown
│   └── styles/             # CSS stylesheets
└── docs/                   # Documentation
	├── README.md           # Project overview
	├── COORDINATE_PICKER_GUIDE.md # Picker tool docs
	└── DEVELOPMENT.md      # This file
```

## Adding New Features

### Adding a New Study Module

1. Create a new view file in `modules/`:
   ```python
   # modules/my_view.py
   import customtkinter as ctk

   class MyView(ctk.CTkFrame):
	   def __init__(self, parent, **kwargs):
		   super().__init__(parent, **kwargs)
		   # Implementation here
   ```

2. Register the view in `main.py` navigation

3. Add any data requirements to `data/` directory

### Adding Motherboard Data

1. Create PNG diagram in `assets/images/motherboard/`

2. Add entry to `data/motherboard/motherboard_nodes.json`:
   ```json
   {
	 "board_id": "my_board",
	 "title": "My Motherboard",
	 "image_path": "assets/images/motherboard/my_board.png",
	 "resolution": [1920, 1080],
	 "display_scale": 1.0,
	 "components": []
   }
   ```

3. Use the Coordinate Picker tool to add component hotspots

### Adding Quiz Data

1. Add image to appropriate category in `assets/images/`

2. Add entry to `data/image_catalog.json`:
   ```json
   {
	 "id": "my_item",
	 "image_path": "assets/images/category/my_image.png",
	 "quiz": {
	   "options": ["Option A", "Option B", "Option C"],
	   "correct_index": 0,
	   "explanation": "Explanation text"
	 }
   }
   ```

## Core Systems

### Board Registry (`utils/board_registry.py`)
- Single source of truth for motherboard data
- Loads from and saves to `data/motherboard/motherboard_nodes.json`
- Provides access methods: `get_board()`, `get_all_boards()`, `update_board()`

### Diagram Canvas Widget (`modules/diagram/canvas_widget.py`)
- Shared rendering engine for all board visualizations
- Handles display scaling and hotspot rendering
- Used by both diagram view and game view
- Method signature: `load_board(board_info, zoom_level=1.0, selected_comp=None, apply_display_scale=True)`

### Image Library (`utils/image_library.py`)
- Loads and caches `data/image_catalog.json`
- Resolves relative paths for images
- Provides quiz metadata access

## Display Scale System

### Key Principles
- **View-layer only**: Scale is for visual presentation, not gameplay
- **Per-board**: Each board can have independent scale
- **Context-aware**: Diagram/picker use it, game doesn't

### Implementation
1. Scale value stored in board JSON: `"display_scale": 1.5`
2. Canvas widget uses `apply_display_scale` parameter
3. Diagram view: `load_board(..., apply_display_scale=True)`
4. Game view: `load_board(..., apply_display_scale=False)`

### Hotspot Scaling
- Hotspot coordinates are scaled along with the image
- Click detection uses effective zoom (original * scale factor)
- Selection rectangle moves with scaled content

## Common Tasks

### Debugging Board Loading
```python
from utils.board_registry import BoardRegistry

registry = BoardRegistry()
board = registry.get_board("modern_atx")
print(board.get("resolution"))  # Check image dimensions
print(board.get("display_scale"))  # Check scaling
```

### Testing Hotspot Click Detection
```python
# In coordinate_picker_main.py or diagram_view.py
# Check the _check_hotspot_click() method for coordinate translation
```

### Adding New Game Round Types
1. Add data structure to quiz metadata
2. Implement round rendering in `game_view.py`
3. Update answer checking logic

## Testing

### Manual Testing Checklist
- [ ] Main window launches and shows all view options
- [ ] Diagram view loads and displays boards correctly
- [ ] Coordinate picker opens from diagram view
- [ ] Hotspots are clickable in diagram view
- [ ] Game view loads and rounds are playable
- [ ] Display scale changes in picker affect preview
- [ ] Changes persist after restart
- [ ] Notes view loads and displays content
- [ ] All assets load without errors

### Python Compilation Check
```bash
python -m py_compile main.py modules/diagram_view.py modules/game_view.py tools/coordinate_picker_main.py
```

## Performance Considerations

- Board images are loaded and cached via PIL
- Canvas redraw uses `after_idle()` for deferred rendering
- Large image catalogs should be lazy-loaded if needed
- Display scale affects visual performance but not gameplay

## Code Style

- Use type hints for clarity
- Follow PEP 8 conventions
- Keep UI logic separate from data logic
- Use descriptive variable and function names
- Add comments for complex algorithms

## Common Issues & Solutions

### Canvas Not Redrawing
- Ensure `_refresh_canvas()` is called after data changes
- Check that `update_idletasks()` is called before checking size
- Deferred refresh with `after_idle()` handles initialization

### Hotspots Not Responding to Clicks
- Verify coordinates are in image space, not canvas space
- Check that click translation accounts for display scale
- Ensure hotspot rectangles are within image bounds

### Performance Issues with Large Boards
- Consider reducing image resolution
- Profile with Python cProfile if slowness persists
- Check for unnecessary redraws in event handlers

## Future Improvements

- [ ] Batch import of quiz items
- [ ] Advanced filtering/search in notes
- [ ] Custom color schemes for hotspots
- [ ] Undo/redo in coordinate picker
- [ ] Keyboard shortcuts for common tasks
- [ ] Dark mode support

## Resources

- [customtkinter Documentation](https://customtkinter.tomSchiffer.de/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Python tkinter Guide](https://docs.python.org/3/library/tkinter.html)
