# Data Schema Reference

## Motherboard Registry (`data/motherboard/motherboard_nodes.json`)

Full structure of a motherboard entry:

```json
{
  "board_id": "unique_identifier",
  "title": "Display Name",
  "image_path": "assets/images/motherboard/image.png",
  "resolution": [
	1920,
	1080
  ],
  "display_scale": 1.0,
  "components": [
	{
	  "name": "Component Name",
	  "description": "Component Description",
	  "coordinates": [
		100,
		200,
		150,
		100
	  ]
	}
  ]
}
```

### Field Descriptions

- **board_id** (string, required): Unique identifier for the board, used internally
- **title** (string, required): Human-readable display name for UI
- **image_path** (string, required): Relative path to the board PNG image
- **resolution** (array of 2 integers, required): [width, height] of the image in pixels
- **display_scale** (float, required): Visual scaling factor
  - Range: 1.0 to 2.0 (100% to 200%)
  - Only affects diagram view and coordinate picker
  - Game view always uses 1.0
- **components** (array of objects, required): Hotspot definitions
  - **name** (string): Component name (e.g., "CPU", "RAM Slot 1")
  - **description** (string): Detailed description or notes
  - **coordinates** (array of 4 integers): [x, y, width, height]
	- x, y: Top-left corner in pixels
	- width, height: Dimensions in pixels
	- All coordinates relative to original image (before scaling)

### Example - Complete Board

```json
{
  "board_id": "modern_atx",
  "title": "Modern ATX Motherboard",
  "image_path": "assets/images/motherboard/modern_atx.png",
  "resolution": [1920, 1440],
  "display_scale": 1.2,
  "components": [
	{
	  "name": "CPU Socket",
	  "description": "Intel LGA 1700 Socket",
	  "coordinates": [850, 480, 280, 280]
	},
	{
	  "name": "RAM Slot 1",
	  "description": "DDR5 DIMM Slot",
	  "coordinates": [1300, 480, 80, 280]
	},
	{
	  "name": "BIOS Chip",
	  "description": "UEFI BIOS Flash Memory",
	  "coordinates": [200, 600, 100, 80]
	}
  ]
}
```

## Image Catalog (`data/image_catalog.json`)

Structure for quiz images:

```json
{
  "categories": [
	{
	  "name": "Cables",
	  "id": "cables"
	}
  ],
  "images": [
	{
	  "id": "rj45_connector",
	  "category": "cables",
	  "name": "RJ45 Connector",
	  "image_path": "assets/images/cables/RJ45.jpg",
	  "notes": "Standard Ethernet connector",
	  "quiz": {
		"options": [
		  "RJ45",
		  "RJ11",
		  "RJ25"
		],
		"correct_index": 0,
		"explanation": "RJ45 is the standard for Ethernet connections with 8 pins"
	  }
	}
  ]
}
```

### Field Descriptions

- **categories** (array): Organizational categories for images
  - **name** (string): Display name
  - **id** (string): Unique identifier

- **images** (array): Individual quiz items
  - **id** (string, required): Unique identifier
  - **category** (string, required): Category ID this belongs to
  - **name** (string, required): Display name for the item
  - **image_path** (string, required): Path to the image file
  - **notes** (string, optional): General notes/information
  - **quiz** (object, optional): Quiz metadata for game mode
	- **options** (array of strings): Multiple choice options
	- **correct_index** (integer): Index of correct answer (0-based)
	- **explanation** (string): Explanation for when answered

## Flashcards (`data/flashcards.json`)

Structure for flashcard study sets:

```json
{
  "cards": [
	{
	  "id": "card_001",
	  "front": "What is the standard Ethernet connector called?",
	  "back": "RJ45",
	  "category": "networking",
	  "difficulty": 1
	}
  ]
}
```

### Field Descriptions

- **cards** (array): Individual flashcard definitions
  - **id** (string): Unique identifier
  - **front** (string): Question or prompt
  - **back** (string): Answer
  - **category** (string): Topic category
  - **difficulty** (integer 1-5): Difficulty rating

## Exam Questions (`data/questions.json`)

Structure for exam simulation:

```json
{
  "questions": [
	{
	  "id": "q_001",
	  "question": "Which component controls the flow of data?",
	  "options": [
		"CPU",
		"RAM",
		"GPU",
		"PSU"
	  ],
	  "correct_index": 0,
	  "explanation": "The CPU is the central processing unit that controls data flow",
	  "category": "CPU",
	  "difficulty": 1
	}
  ]
}
```

### Field Descriptions

- **questions** (array): Individual exam questions
  - **id** (string): Unique identifier
  - **question** (string): Question text
  - **options** (array of strings): Multiple choice answers
  - **correct_index** (integer): Index of correct answer (0-based)
  - **explanation** (string): Explanation for the correct answer
  - **category** (string): Question category/topic
  - **difficulty** (integer 1-5): Difficulty rating

## Notes Structure (`assets/notes/`)

Markdown files organized by course and topic:

```
assets/notes/
├── core1/
│   ├── 1.1_intro.md
│   ├── 2.1_boards.md
│   ├── 3.1_cpus.md
│   └── ...
└── core2/
	├── ...
```

Each markdown file contains:
- Heading with topic name
- Structured content sections
- Inline images where applicable
- Links to related topics

## Validation Rules

### Motherboards
- board_id must be unique within the file
- image_path must point to existing file
- resolution must be [width, height] format
- display_scale must be between 0.5 and 2.0
- component coordinates must be within image bounds: 0 ≤ x < width, 0 ≤ y < height

### Image Catalog
- image ids must be unique
- category id must exist in categories
- correct_index must be valid (0 ≤ index < options.length)
- image_path must point to existing file

### Exam Questions
- question ids must be unique
- correct_index must be valid
- options array must have at least 2 elements
- category must match quiz categories

## Persistence

All JSON data is persisted by:
- **BoardRegistry** (`utils/board_registry.py`) - Handles motherboard_nodes.json
- Direct file I/O for other JSON files

Changes to data are automatically written to disk when:
- Board data is updated via coordinate picker
- Display scale is changed
- Components are added/edited/deleted

## Tips for Adding Data

1. **Validate JSON**: Use a JSON validator before loading
2. **Use meaningful ids**: Make IDs descriptive and lowercase with underscores
3. **Maintain consistency**: Use same naming conventions across all entries
4. **Test loading**: Verify files load without errors on application restart
5. **Backup**: Always backup JSON files before bulk edits
