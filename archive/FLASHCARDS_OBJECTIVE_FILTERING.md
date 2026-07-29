# Flashcards View Enhancement - Objective Filtering

**Date:** 7/29/2026  
**Feature:** Add objective-based filtering to flashcards  
**Status:** ✅ Complete

---

## Overview

Modified `modules/flashcards_view.py` to allow flashcards to be filtered by **main objective** (1, 2, 3, 4, 5) instead of requiring users to see all objectives at once or configure them by sub-objective.

---

## Changes Made

### 1. **Added State Management** 
- `self.all_cards` — Stores all loaded flashcards (unchanged)
- `self.cards` — Stores filtered cards based on selected objective
- `self.selected_objective` — Tracks currently selected objective

### 2. **New Methods**

#### `get_available_objectives()`
- Extracts unique main objectives from all flashcards
- Parses objective strings (e.g., "2.5 - Network Cables") to get main number ("2")
- Returns sorted list: `["1", "2", "3", "4", "5"]`

#### `filter_cards_by_objective(objective)`
- Filters `self.all_cards` by main objective number
- Returns all cards if objective is "All"
- Example: `filter_cards_by_objective("2")` returns only cards from Objective 2

#### `on_objective_change(choice)`
- Callback for objective dropdown selection
- Re-filters cards when user selects a different objective
- Resets progress counters and card index to start fresh

### 3. **Updated UI Header**

**Before:**
```
[Objective: --] [Start with Definition toggle]
```

**After:**
```
[Select Objective: ▼] [Card info] [Start with Definition toggle]
```

Added dropdown menu showing:
- "All" — Shows all flashcards
- "Objective 1" — Only Objective 1 cards
- "Objective 2" — Only Objective 2 cards
- etc.

### 4. **Enhanced update_card_display()**
- Shows filtering info: "Objective 2" or "All Objectives"
- Displays current card count for filtered set
- Shows "No flashcards available" if selection has no cards

---

## How It Works

1. **Load:** All flashcards load from `data/flashcards.json`
2. **Extract:** Main objectives automatically detected from card metadata
3. **Display:** Dropdown shows available objectives
4. **Filter:** User selects objective → cards filtered in real-time
5. **Study:** Study the filtered set with progress tracking
6. **Switch:** Selecting new objective resets counters and starts fresh

---

## JSON Format (No Changes Required)

Existing flashcard format is unchanged:

```json
[
  {
	"id": "fc_001",
	"objective": "2.5 - Network Cables & Connectors",
	"term": "RJ-45",
	"definition": "8-position connector for Ethernet...",
	"image_path": null
  }
]
```

The **main objective** is automatically extracted from the first number (e.g., "2" from "2.5").

---

## Usage

1. Click **Flash Cards** in the sidebar
2. Use the **"Select Objective"** dropdown to choose:
   - **All** — All flashcards
   - **Objective 1** — Mobile Devices
   - **Objective 2** — Networking
   - **Objective 3** — Hardware
   - **Objective 4** — Cloud/Virtualization
   - **Objective 5** — Troubleshooting
3. Study the cards in the selected set
4. Toggle "Start with Definition" if desired
5. Record answers with "Know It" or "Needs Review"
6. Switch objectives anytime to study a different domain

---

## Benefits

✅ **Organized Study** — Focus on one domain at a time  
✅ **Automatic Detection** — Objectives found automatically from flashcard data  
✅ **No Config Changes** — Existing JSON works as-is  
✅ **Progress Tracking** — Score resets per objective for clarity  
✅ **Quick Switching** — Change objectives instantly  

---

## Testing Checklist

- [x] Syntax validation passed
- [ ] Launch app and verify dropdown appears
- [ ] Select "Objective 2" and verify only Obj 2 cards show
- [ ] Switch between objectives and verify filtering works
- [ ] Test "All" option shows all cards
- [ ] Verify progress counters reset when changing objectives
- [ ] Test with empty objective (no cards) shows message

---

## Files Modified

- ✏️ `modules/flashcards_view.py` — Added filtering logic and UI

## Files Unchanged

- `data/flashcards.json` — No JSON schema changes
- `main.py` — No integration changes needed
- Other modules — No impact

---

## Next Steps

1. Test the flashcards view in the app
2. Add more flashcards to `data/flashcards.json` as needed
3. Consider adding category labels (e.g., "Mobile Devices", "Networking") to dropdown if desired

---

**Implementation Complete!** 🎉
