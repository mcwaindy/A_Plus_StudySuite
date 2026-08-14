# Settings & Data Management Implementation

## Overview
Added a comprehensive Settings/Options menu to the app, providing users and developers with data reset capabilities for testing and fresh starts.

## New Files Created

### `modules/settings_view.py`
A new view providing data management and reset options:
- **SettingsView**: Main settings frame with scrollable layout
- **ConfirmDialog**: Custom confirmation dialog for destructive operations

#### Features:
1. **Reset All Statistics** (Red button)
   - Clears card metrics, review history, and goals
   - Complete data wipe for starting over

2. **Reset Card Metrics Only** (Orange button)
   - Resets spaced repetition data (intervals, ease factors, learning stages)
   - Preserves goals and review history

3. **Reset Review History**
   - Clears all study sessions and progress statistics
   - Keeps card metrics and goals intact

4. **Reset Goals**
   - Resets exam date, readiness target, milestones, and streaks
   - Sets to default values

5. **Data Files Info Section**
   - Shows all JSON files in `data/` directory
   - Displays file sizes for reference

#### Design:
- Color-coded buttons (red for full reset, orange for partial)
- Descriptive text explaining what each reset does
- Confirmation dialogs with clear warnings
- Auto-dismissing success/error messages
- Scrollable layout for future expansion

## Modified Files

### `main.py`
- Added import: `from modules.settings_view import SettingsView`
- Added new `4. SETTINGS` sidebar section
- Added `⚙️ Options` button linking to SettingsView
- Maintains consistent sidebar layout and styling

### `utils/goals_manager.py`
- Added `reset_goals()` method to GoalsManager
  - Resets all goals to default values
  - Saves changes to file

## Integration Points

### Sidebar Navigation
```
1. STUDY
   - 🎯 Goals
   - 📚 Flashcards

2. PRACTICE
   - 💠 Select Exam
   - 💠 Custom Objectives
   - 💠 Hardware Game
   - 📝 Notes
   - 💠 Diagram

3. DEV TOOLS
   - 📝 Notes

4. SETTINGS
   - ⚙️ Options
```

## Testing Support
This implementation directly addresses the need for reset capabilities:
- Developers can quickly reset card metrics to test spaced repetition independently
- Test scenarios can be run with clean data states
- Users can start fresh without manual file deletion

## Data Persistence
All reset operations are backed by:
- `GoalsManager` for goals reset
- `SpacedRepetitionManager` for card metrics reset
- Direct JSON manipulation for history reset

## Next Steps (Optional)
Potential future enhancements:
- Export/backup data before reset
- Reset individual objectives instead of all cards
- Data import/restore from backup
- Study preferences (card review limits, daily goals tuning)
- Debug mode toggle
- Data statistics/analytics dashboard

## Files Structure
```
modules/
  ├── settings_view.py          [NEW]
  ├── dev_tools_view.py         [Existing]
  └── ... (other views)

utils/
  ├── goals_manager.py          [MODIFIED - added reset_goals()]
  └── ... (other utilities)

main.py                          [MODIFIED - added Settings section/button]
```

## Verification
- ✅ `modules/settings_view.py` syntax verified
- ✅ `utils/goals_manager.py` syntax verified
- ✅ `main.py` syntax verified
- ✅ App launches successfully with Settings integrated
- ✅ All imports resolved correctly
