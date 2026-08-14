# Next High-Priority Tasks - Quick Reference

## Task 2: Visual Consistency & Polish
**Current Status**: Partially complete (notes are polished, other views vary)  
**Estimated Effort**: 4-6 hours  
**Impact**: HIGH (professional appearance)  
**Priority**: HIGH

### Current State
- ✅ Notes view has refined typography (bold, letter-spacing, polished)
- ⚠️ Flashcard view uses default font sizing
- ⚠️ Exam view needs visual improvements
- ⚠️ Game view is functional but plain
- ⚠️ Button styling inconsistent across views

### Work Items
1. **Flashcard View Polish**
   - Apply consistent font sizing to card terms and definitions
   - Enhance progress label typography
   - Add shadow/depth to card display area
   - Improve button hover effects and animations

2. **Exam View Enhancement**
   - Standardize question display typography
   - Improve answer option styling
   - Add visual feedback on answer selection
   - Polish progress indicators

3. **Game View Refinement**
   - Enhance button styling and click feedback
   - Improve score display typography
   - Add animation to game state transitions
   - Polish component image display

4. **Standardize Across All Views**
   - Define consistent button styles (size, font, hover)
   - Consistent padding/margin standards
   - Unified color scheme for interactive elements
   - Consistent border radius and shadows

### Implementation Strategy
- Create a `theme_constants.py` or similar for centralized styling
- Define standard font sizes, weights, and colors
- Apply to each view incrementally
- Test visual consistency after each view update

### Files to Modify
- `modules/flashcards_view.py` (buttons, card display)
- `modules/exam_view.py` (question rendering)
- `modules/game_view.py` (UI elements)
- Possibly new: `utils/theme_constants.py` (centralized styles)

---

## Task 3: Error Handling & User Feedback
**Current Status**: Basic (print statements, no user dialogs)  
**Estimated Effort**: 2-3 hours  
**Impact**: MEDIUM-HIGH (better UX, error transparency)  
**Priority**: HIGH

### Current State
- ✅ Missing flashcard file handled
- ✅ Invalid JSON shows warning (sometimes)
- ❌ No user-friendly error dialogs
- ❌ Silent failures in some areas
- ❌ Exceptions printed to console, not shown to user

### Work Items
1. **Replace Console Print with Dialog**
   - Flashcard loading errors
   - JSON parse errors
   - File I/O failures
   - Session recovery errors

2. **Create Error Dialog Utility**
   - Standard CTkToplevel modal for errors
   - Consistent error message formatting
   - "OK" button to dismiss
   - Optional error details (expandable)

3. **Add Validation & Feedback**
   - Validate user inputs with friendly messages
   - Show warnings before destructive actions
   - Confirm successful operations where appropriate

4. **Logging & Debugging**
   - Suppress internal debug output by default
   - Add optional debug mode flag
   - Log important events to file (optional)

### Implementation Strategy
- Create `modules/dialogs/error_dialog.py` for error handling
- Create `modules/dialogs/info_dialog.py` for confirmations
- Audit all current try/except blocks
- Replace print() with dialog calls

### Files to Modify/Create
- New: `modules/dialogs/error_dialog.py`
- New: `modules/dialogs/info_dialog.py`
- Multiple view files (flashcards, exam, notes, etc.)
- `utils/session_manager.py` (error reporting)

---

## Task 4: Exam Question Editor/Creator
**Current Status**: Partial (selection UI exists, creation may need testing)  
**Estimated Effort**: 3-4 hours  
**Impact**: MEDIUM (valuable for custom content)  
**Priority**: MEDIUM-HIGH

### Current State
- ✅ Custom exam view allows selecting objectives
- ⚠️ Question storage may not be fully tested
- ❌ No question editing (modify/delete)
- ❌ No input validation
- ❌ No preview mode

### Work Items
1. **Test Current Question Creation**
   - Verify questions save to `data/questions.json`
   - Verify persistence across app restarts
   - Check for any data corruption

2. **Add Question Management UI**
   - View existing custom questions
   - Edit existing questions
   - Delete questions with confirmation
   - Search/filter questions

3. **Input Validation**
   - Required fields: question text, answer options, correct answer
   - Prevent duplicate questions
   - Sanitize inputs
   - Show validation errors clearly

4. **Question Preview**
   - Show how question will appear in exam
   - Preview with all answer options
   - Show correct answer (for editing)

### Implementation Strategy
- Extend `modules/custom_exam_view.py`
- Add dialog for editing individual questions
- Create question validator utility
- Test data persistence thoroughly

### Files to Modify
- `modules/custom_exam_view.py` (main work)
- Possibly new: `utils/question_validator.py`
- Possibly new: `modules/dialogs/question_editor_dialog.py`

---

## Task 5: Flashcard Merge Utility
**Current Status**: Tool exists but not integrated  
**Estimated Effort**: 2-3 hours  
**Impact**: MEDIUM (content management, not user-facing)  
**Priority**: MEDIUM

### Current State
- ✅ `utils/merge_flashcards.py` exists
- ⚠️ Not tested with real data
- ❌ No UI integration
- ❌ No documentation

### Work Items
1. **Test Merge Logic**
   - Test with actual Core 1 and Core 2 data
   - Verify merged data is valid JSON
   - Check for duplicate IDs
   - Validate objectives structure

2. **Create Merge UI**
   - Dialog to select files to merge
   - File picker for input files
   - Preview of merge results
   - Success/error feedback

3. **Error Handling**
   - Handle missing files gracefully
   - Check for ID conflicts
   - Validate all input files before merge
   - Provide rollback/undo option

### Implementation Strategy
- Keep merge utility in utils/ (backend)
- Add merge option to Settings or Dev Tools
- Create modal dialog for file selection
- Test thoroughly with real data

### Files to Modify
- `utils/merge_flashcards.py` (test and polish)
- `modules/dev_tools_view.py` or `modules/settings_view.py` (add merge option)
- Possibly new: `modules/dialogs/merge_dialog.py`

---

## Recommended Implementation Order

1. **NOW**: Auto-Save & Recovery ✅ (COMPLETE)
2. **NEXT**: Visual Consistency & Polish (4-6 hours, high impact)
3. **THEN**: Error Handling & User Feedback (2-3 hours, high impact)
4. **THEN**: Exam Question Editor (3-4 hours, medium impact)
5. **THEN**: Flashcard Merge Utility (2-3 hours, medium impact, internal)

**Total Remaining**: ~11-16 hours to reach highly polished state

---

## Quick Links to Related Files
- Project Guide: `PROJECT_COMPLETION_GUIDE.md`
- Session Recovery Docs: `SESSION_RECOVERY_IMPLEMENTATION.md`
- Testing Checklist: `AUTO_SAVE_TESTING_CHECKLIST.md`
- Current View Files:
  - `modules/flashcards_view.py` (1000+ lines)
  - `modules/exam_view.py`
  - `modules/game_view.py`
  - `modules/notes_view.py` (recently polished)
  - `modules/settings_view.py`
  - `modules/dev_tools_view.py`

---

## Notes
- All tasks maintain backward compatibility
- Focus on UX improvements and data integrity
- Keep code modular and reusable
- Document changes in PROJECT_COMPLETION_GUIDE.md as completed

Good luck with the next phase! 🚀
