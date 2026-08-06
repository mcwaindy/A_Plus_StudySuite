# Multi-Select Objectives Feature - Quick Guide

## Overview
The flashcards view now supports selecting **multiple objectives at once** instead of just one. This allows you to study different objective combinations efficiently.

## How to Use

### Opening the Objective Selector
1. Look at the header section of the flashcards view
2. Find the "Objectives" button (previously was a dropdown)
3. Click it to open a dialog

### Selecting Objectives
The dialog shows:
- **"All Objectives"** checkbox at the top
- Individual checkboxes for each available objective (1, 2, 3, etc.)

#### Selection Rules:
- **Check "All Objectives"**: Deselects all specific objectives → studies all cards
- **Uncheck "All Objectives"**: Allows selecting specific objectives
- **Check specific objectives**: You can select any combination (1 + 2, or 1 + 2 + 3, etc.)
- **No objectives selected**: Automatically defaults to "All"

### Button Display
The "Objectives" button shows your current selection:
- **"All Objectives"** - if "All" is selected
- **"Obj: 1, 2, 3"** - if specific objectives selected (sorted numerically)

### Applying Your Selection
1. Check/uncheck boxes as needed
2. Click **"Apply"** button to confirm
3. Cards immediately re-filter to match your selection
4. Click **"Cancel"** if you change your mind

## Examples

### Example 1: Study Single Objective
1. Click "Objectives" button
2. Uncheck "All Objectives"
3. Check only "Objective 2"
4. Click "Apply"
5. Button shows "Obj: 2"
6. Only Objective 2 cards appear

### Example 2: Study Multiple Related Objectives
1. Click "Objectives" button
2. Uncheck "All Objectives"
3. Check "Objective 1" and "Objective 2"
4. Click "Apply"
5. Button shows "Obj: 1, 2"
6. Cards from both objectives mix together

### Example 3: Back to All
1. Click "Objectives" button
2. Check "All Objectives"
3. Click "Apply"
4. Button shows "All Objectives"
5. All cards available

## State After Selection

When you select objectives and apply:
- ✓ Card filtering updates immediately
- ✓ Deck is reshuffled with new cards
- ✓ Current index resets to first card
- ✓ Session scores reset to 0
- ✓ Review tracking clears
- ✓ Display updates to show objective info

## Integration with Other Features

### Card Limit
- Works seamlessly with card limit feature
- Study 15 cards from Objectives 1, 2, 3
- Or 10 cards from just Objective 2
- Card limit applies to selected objectives

### Review History
- Stores your objective selections in history
- Shows "Objectives: 1, 2" in past session display
- Backwards compatible with old single-objective records

### Exam Filtering
- Exam dropdown works independently
- You can combine:
  - Exam: Core 1
  - Objectives: 1, 3
  - Card Limit: 20
- All filters combine logically

## Technical Details

### State Variable
- `self.selected_objectives` - Changed from single string to list
- Format: `["All"]` or `["1", "2", "3"]` (sorted numerically)

### Filter Method
- `filter_cards_by_exam_and_objective()` now accepts list of objectives
- Backwards compatible with old format
- Returns only cards matching all filters

### Dialog UX
- Clean checkbox interface with scrollable frame
- "All Objectives" checkbox auto-manages mutual exclusivity
- Button text updates to show current selections
- Responsive design that works at any window size

## Tips & Tricks

1. **Quick Focus Study**: Select just Obj 1 + Obj 2 for focused sessions
2. **Progressive Learning**: Study Obj 1, then add Obj 2, then Obj 3
3. **Review Weak Areas**: Select only objectives you struggle with
4. **Exam Prep**: Combine objectives that appear together in actual exams
5. **Session Variety**: Change objective selection between sessions to maintain variety

## Backward Compatibility

- Old review history with single objectives still work
- Automatically converted to list format when displaying
- New sessions always use list format
- No migration needed - seamless upgrade

## Limitations

- Maximum objectives available depends on flashcard data
- Dialog shows all available objectives as checkboxes
- Button text truncates at reasonable length if many objectives selected
- Objectives are sorted alphanumerically in display

## Future Enhancements

- Preset objective combinations (e.g., "Pre-exam", "Quick review", etc.)
- Save/load custom objective sets
- Drag-and-drop objective ordering
- Objective importance weighting
- Smart recommendations based on weak areas
