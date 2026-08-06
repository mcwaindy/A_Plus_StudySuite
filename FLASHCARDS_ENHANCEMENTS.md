# Flashcards View Enhancements

## New Features Added

### 1. **Configurable Card Limit**
- **Location**: Header controls, next to "Objectives" button
- **Options**: All, 10, 20, 30, 50 cards per session
- **Behavior**: When a card limit is set, the study session ends after reviewing that many cards (regardless of exam or objective selection)
- **Reset**: Changing the card limit resets the current session score and reviewed cards list

### 2. **Multi-Select Objectives**
- **Location**: Header controls, "Objectives" button (replaces single-select dropdown)
- **Features**:
  - Click the button to open a dialog with checkboxes for each objective
  - Select one or more objectives to include in your study session
  - "All Objectives" option to study everything
  - Button displays your selection:
	- "All Objectives" if all selected
	- "Obj: 1, 2, 3" if specific objectives selected
  - When you change objectives, cards are re-filtered immediately
  - Useful for combining related objectives or focusing on specific studies

### 3. **Finish Review Screen**
- **Trigger**: Automatically shown when card limit is reached
- **Display**:
  - Session summary (Cards Studied, Mastered, Needs Review)
  - Organized list of cards marked as "Needs Review" grouped by objective
  - Each objective shows the specific terms that were missed
  - Visual formatting with bullet points for easy scanning

- **Controls at Review Screen**:
  - "New Review" button: Start a fresh study session with same filters and limits
  - "Done" button: Return to main flashcard interface

### 4. **Persistent Review History**
- **Storage**: Reviews are saved to `data/review_history.json` (non-volatile)
- **Automatic Save**: Each completed session is automatically saved with:
  - Exam and objectives selection (now supports multiple objectives)
  - Number of cards studied
  - List of cards marked as "Needs Review"

- **Review History Dialog**:
  - Located in bottom controls bar: "📋 Review History" button
  - Shows all past review sessions (newest first)
  - Each session displays:
	- Session number and metadata (exam, objectives, study count)
	- Preview of cards that needed review, grouped by objective
	- Truncated if many cards (shows first 3 + count of remaining)
  - Persistent across sessions - data survives app restarts

## Usage Workflow

### Typical Study Session:
1. **Set exam filter** (All, Core 1, Core 2)
2. **Select objectives** - Click "Objectives" button to choose:
   - Single objective
   - Multiple objectives (e.g., 1, 2, and 3)
   - All objectives
3. **Set card limit** (e.g., "20" to study 20 cards)
4. **Study cards** by marking them as "Know It ✓" or "Needs Review ✗"
5. **Reach limit** → Automatic review screen appears
6. **Review** your missed cards organized by objective
7. **Choose action**:
   - "New Review" to study again with same settings
   - "Done" to exit
8. **Later**: Click "📋 Review History" to see all past sessions anytime

## Data Persistence

### File Structure:
```
data/
├── flashcards.json          (existing - flashcard database)
└── review_history.json      (new - review session history)
```

### Review History Format (Updated):
```json
[
  {
	"timestamp": "...",
	"exam": "All",
	"objectives": ["1", "2"],
	"cards_studied": 20,
	"cards_reviewed": [
	  {
		"id": "c1_001",
		"term": "RAM",
		"objective": "2.1 - Memory"
	  },
	  ...
	]
  },
  ...
]
```

## Implementation Details

### Key Methods:
- `show_objective_selector()` - Opens dialog for multi-select objectives
- `on_objective_checkbox_change()` - Handles checkbox interactions
- `apply_objective_selection()` - Applies selection and re-filters cards
- `filter_cards_by_exam_and_objective()` - Enhanced to handle objective list
- `on_exam_change()` - Updated for multi-objective compatibility
- `on_card_limit_change()` - Handles card limit dropdown selection
- `record_answer()` - Tracks reviewed cards and checks for limit
- `show_review_screen()` - Displays finish screen with organized review data
- `save_review()` - Persists review session to JSON file (now includes objectives list)
- `load_reviews()` - Retrieves past reviews from storage
- `show_review_history_dialog()` - Displays review history in popup dialog
- `on_btn_review_click()` - Context-aware button (study mode vs review mode)
- `on_btn_know_click()` - Context-aware button (study mode vs review mode)
- `start_new_session()` - Resets and starts fresh session
- `exit_review_screen()` - Exits review mode and returns to study

### State Variables:
- `self.selected_objectives` - List of objective numbers (e.g., ["1", "2", "3"] or ["All"])
- `self.card_limit` - Maximum cards for current session (None = unlimited)
- `self.reviewed_cards` - List of cards marked as needing review
- `self.cards_studied` - List of all cards studied in current session
- `self._in_review_mode` - Flag indicating if review screen is displayed
- `self.obj_button` - Reference to objectives button for updating text

## Example Workflows

### Focus Study (Single Objective):
1. Click "Objectives" → Select only "Objective 2"
2. Button shows "Obj: 2"
3. Only cards from Objective 2 appear
4. Set card limit to 15 (just from Obj 2)
5. Study and get instant feedback on Objective 2 mastery

### Comprehensive Study (Multiple Objectives):
1. Click "Objectives" → Select "1", "2", and "3"
2. Button shows "Obj: 1, 2, 3"
3. Mixed cards from all three objectives
4. Set card limit to 50 for a longer session
5. Review which objectives need the most work

### Exam Prep:
1. Select "Core 1" from exam dropdown
2. Click "Objectives" → Select objectives you struggled with
3. Set card limit to 30
4. Study and review until you master them
5. Check "Review History" to see your improvement over multiple sessions

## Future Enhancement Ideas
- Add timestamps to review history for better tracking
- Allow filtering review history by exam/objective
- Export review history to CSV/PDF
- Statistics dashboard showing study patterns over time
- Ability to directly study only "reviewed" cards from a past session
- Remember last-used objective selection for faster studying
