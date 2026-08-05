# A+ Study Suite - Documentation

## Project Overview

A+ Study Suite is a comprehensive study aid application for CompTIA A+ certification. It features motherboard diagram visualization, interactive hardware identification games, notes repository, flashcards, and exam simulations.

## Architecture

### Core Application Structure

- **`main.py`** - Application entry point
- **`modules/`** - Primary application screens and views
  - `diagram_view.py` - Motherboard diagram viewer with coordinate picker integration
  - `game_view.py` - Hardware identification game with motherboard and image rounds
  - `notes_view.py` - Study notes browser
  - `exam_view.py` - Exam simulation
  - `flashcards_view.py` - Flashcard study tool
  - `custom_exam_view.py` - Custom exam creator
  - `diagram/` - Shared rendering components
	- `canvas_widget.py` - Motherboard diagram canvas renderer
  - `notes/` - Notes rendering system
	- `library.py` - Notes catalog management
	- `renderer.py` - HTML/Markdown rendering
	- `html_compat.py` - HTML compatibility layer

- **`tools/`** - Standalone utilities
  - `coordinate_picker.py` - Launcher for the coordinate picker tool
  - `coordinate_picker_main.py` - Main coordinate picker UI for editing board hotspots

- **`utils/`** - Utility modules
  - `board_registry.py` - Motherboard data persistence and access
  - `image_library.py` - Image catalog loader for quiz data
  - `coordinate_translator.py` - Coordinate system conversions
  - `paths.py` - Path utilities

- **`data/`** - Application data
  - `motherboard/` - Motherboard JSON registry
	- `motherboard_nodes.json` - Motherboard definitions, hotspots, and display scaling
  - `flashcards.json` - Flashcard data
  - `questions.json` - Exam questions
  - `image_catalog.json` - Image quiz metadata and options

- **`assets/`** - Static resources
  - `images/` - Image library organized by category
	- `motherboard/` - Motherboard board diagrams
	- `cables/` - Cable and connector images
	- `display/` - Display technology images
	- `memory/` - RAM and memory images
	- `expansion/`, `cooling/`, `cpu/`, etc. - Other component categories
  - `notes/` - Study notes content
  - `styles/` - CSS stylesheets

## Key Features

### Motherboard Diagram Viewer
- Interactive motherboard diagram display with hotspot highlighting
- Per-board display scaling with visual feedback
- Coordinate picker integration for editing hotspot locations
- Support for multiple motherboard form factors (ATX, ITX, LPX, etc.)

### Hardware Identification Game
- Multiple game rounds with motherboard component identification
- Standalone image quiz rounds with multiple-choice options
- Score tracking and statistics

### Diagram Coordinate Picker
Standalone tool for managing motherboard component hotspots:
- Visual component editing with drag-and-drop coordinate selection
- Display scale adjustment for visual tuning
- Component description and metadata editing
- Real-time preview of board scaling

### Data Persistence
- JSON-based motherboard registry with per-board hotspot data
- Display scale stored per board for consistent rendering across views
- Image catalog with quiz metadata for standalone images

## Development Notes

### Display Scaling
- Display scale is a view-layer feature, not gameplay
- Diagram view and coordinate picker honor the board's `display_scale`
- Game view motherboard rounds render at native size (scale=1.0)

### Gameplay Architecture
- Motherboard identification rounds use the shared `DiagramCanvasWidget`
- Standalone image rounds use `data/image_catalog.json` for quiz metadata
- Multiple-choice options are supported for image quiz items

### Adding New Motherboards
1. Create a PNG diagram image and place in `assets/images/motherboard/`
2. Add board entry to `data/motherboard/motherboard_nodes.json` with:
   - Board title and image path
   - Image resolution (width, height)
   - Display scale (default 1.0)
   - Component hotspots array
3. Launch the coordinate picker to visually edit hotspot rectangles
4. Test in both diagram view and game view

## File Organization Best Practices

- **Source code**: Organized by feature (modules), not by type
- **Data**: Centralized in `data/`, organized by purpose (motherboards, flashcards, etc.)
- **Assets**: Organized by content type (images, styles, notes)
- **Tools**: Standalone utilities separate from core application
- **Utils**: Reusable utilities and helpers

## Running the Application

```bash
python main.py
```

To launch the coordinate picker directly:
```bash
python tools/coordinate_picker.py
```

## Version History & Cleanup

Previous development iterations have been cleaned up:
- Removed obsolete test scripts
- Removed duplicate launcher files
- Removed temporary implementation notes and markdown
- Consolidated application entry point to main.py
