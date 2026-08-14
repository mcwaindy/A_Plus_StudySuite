# Auto-Save & Session Recovery - Testing Checklist

## Pre-Test Verification
- [x] All Python files compile without syntax errors
- [x] SessionManager imports successfully
- [x] All imports resolve in main.py and flashcards_view.py
- [x] App launches without errors
- [x] No corrupted data files found

---

## Test Scenario 1: First Launch (No Saved Session)
**Objective**: Verify app works normally when no session exists

**Steps**:
1. Ensure `data/session_state.json` does NOT exist (delete if present)
2. Launch app: `.venv\Scripts\python main.py`
3. Observe startup behavior

**Expected Results**:
- [ ] App launches without error
- [ ] No recovery dialog appears
- [ ] Welcome screen displays: "Welcome to CompTIA A+ Study Suite!"
- [ ] Sidebar shows all sections (Study, Practice, Dev Tools, Settings)
- [ ] No errors in console output

**Notes**: 
- This establishes baseline behavior
- Tests `check_for_session_recovery()` with no saved session

---

## Test Scenario 2: Start Flashcard Session & Auto-Save
**Objective**: Verify auto-save creates and updates session file

**Steps**:
1. Click "📚 Study" → "Flashcards"
2. Select an exam (e.g., "All")
3. Select objectives (e.g., "Objective 1")
4. Set card limit (e.g., 10)
5. Start study (click button to begin)
6. Read the first card, flip it
7. Mark as "Know It"
8. Observe progress to second card
9. Check if `data/session_state.json` was created:
   ```powershell
   Get-Content data/session_state.json | ConvertFrom-Json | ConvertTo-Json
   ```

**Expected Results**:
- [ ] Session file created after first card interaction
- [ ] Session file contains correct data:
  - [ ] `session_type`: "flashcard"
  - [ ] `timestamp`: Valid ISO datetime
  - [ ] `data.selected_exam`: Matches selection
  - [ ] `data.selected_objectives`: List with chosen objective
  - [ ] `data.card_limit`: 10
  - [ ] `data.score_known`: 1
  - [ ] `data.current_index`: 1
  - [ ] `data.study_mode`: "standard"
- [ ] File is valid JSON (parseable)
- [ ] No errors in console

**Notes**:
- Tests `auto_save_session()` trigger
- Confirms session structure is correct
- Validates JSON serialization

---

## Test Scenario 3: Simulate Crash & Recovery Dialog
**Objective**: Verify recovery dialog appears and shows correct session info

**Steps**:
1. Continue from Scenario 2 (session file should exist)
2. Study 2-3 more cards (advance to card index 3-4)
3. Do NOT complete the review
4. Close the app (Ctrl+C in terminal or close window)
5. Verify `data/session_state.json` still exists and has been updated
6. Relaunch app: `.venv\Scripts\python main.py`
7. Observe startup behavior

**Expected Results**:
- [ ] Recovery dialog appears (CTkToplevel window)
- [ ] Dialog title: "Resume Session?"
- [ ] Dialog shows message: "📚 Flashcard Session Found"
- [ ] Dialog displays session info:
  - [ ] Time ago (e.g., "moments ago", "X minutes ago")
  - [ ] Study mode (e.g., "Standard")
  - [ ] Cards studied (should be 3-4)
  - [ ] Score (e.g., "3 known" or similar)
- [ ] Two buttons visible:
  - [ ] "Resume Session" (green button)
  - [ ] "Start Fresh" (gray button)
- [ ] Dialog is modal (app waits for response)

**Notes**:
- Tests `check_for_session_recovery()` with valid session
- Tests `show_session_recovery_dialog()` rendering
- Confirms session_info formatting

---

## Test Scenario 4: Resume Session
**Objective**: Verify session state is fully restored

**Steps**:
1. From Scenario 3, click "Resume Session"
2. Dialog closes
3. Flashcard view loads
4. Observe the card display and progress

**Expected Results**:
- [ ] Flashcard view appears (not setup screen)
- [ ] Card display shows expected content
- [ ] Score displays correct numbers:
  - [ ] Should match score from before crash (e.g., "Mastered: 3")
- [ ] Card index is at correct position (3-4)
- [ ] Study mode matches (standard/smart)
- [ ] Selected objectives match original selection
- [ ] Can continue studying normally
- [ ] Each card interaction updates score
- [ ] Auto-save continues to update session file

**Notes**:
- Tests `FlashcardView.__init__(recovered_session=...)`
- Confirms state reconstruction from JSON
- Validates that study flow continues seamlessly

---

## Test Scenario 5: Complete Session & Verify Cleanup
**Objective**: Verify session file is cleared after completing a review

**Steps**:
1. From Scenario 4 (resumed session), continue studying
2. Work through remaining cards until review screen appears
3. Observe review screen
4. Check if `data/session_state.json` still exists:
   ```powershell
   Test-Path data/session_state.json
   ```

**Expected Results**:
- [ ] Review screen displays normally with summary
- [ ] Session file is DELETED (Test-Path returns False)
- [ ] No errors in console
- [ ] Can click "New Review" or "Done" without issues

**Notes**:
- Tests `show_review_screen()` calling `clear_session()`
- Confirms cleanup happens
- Verifies no stale sessions accumulate

---

## Test Scenario 6: Start Fresh from Recovery Dialog
**Objective**: Verify "Start Fresh" clears session without resuming

**Steps**:
1. Create a session again (repeat Scenario 2-3)
2. Close app (don't complete)
3. Relaunch app
4. Recovery dialog appears
5. Click "Start Fresh" button
6. Observe behavior

**Expected Results**:
- [ ] Dialog closes
- [ ] Welcome screen appears (not flashcard view)
- [ ] Session file is DELETED
- [ ] No active session
- [ ] Can click "Flashcards" and start a fresh session normally

**Notes**:
- Tests "Start Fresh" button logic
- Confirms `clear_session()` works via button

---

## Test Scenario 7: Session Expiration (7 Days)
**Objective**: Verify old sessions are auto-cleared

**Steps**:
1. Manually create a test session file with old timestamp:
   ```powershell
   $oldSession = @{
	   session_type = "flashcard"
	   timestamp = (Get-Date).AddDays(-8).ToUniversalTime().ToString('o')
	   data = @{selected_exam="All"; cards_studied=@(); score_known=0}
   }
   $oldSession | ConvertTo-Json | Set-Content data/session_state.json
   ```
2. Relaunch app
3. Check behavior

**Expected Results**:
- [ ] No recovery dialog appears
- [ ] Welcome screen shows
- [ ] Session file is DELETED (expired session auto-cleared)
- [ ] `load_session()` returns None for old sessions

**Notes**:
- Tests `_is_session_expired()` logic
- Confirms expiration cleanup

---

## Test Scenario 8: Corrupted Session File
**Objective**: Verify graceful handling of invalid JSON

**Steps**:
1. Create a corrupted session file:
   ```powershell
   Set-Content data/session_state.json "{ broken json"
   ```
2. Relaunch app
3. Observe behavior

**Expected Results**:
- [ ] App launches without crashing
- [ ] No recovery dialog (corrupted file treated as invalid)
- [ ] Welcome screen appears
- [ ] Console shows error message or silent handling
- [ ] Session file may be deleted or left (should handle gracefully)

**Notes**:
- Tests error handling in `load_session()`
- Confirms app doesn't crash on bad data

---

## Test Scenario 9: Missing data/ Directory
**Objective**: Verify SessionManager creates data/ directory if missing

**Steps**:
1. Delete `data/` directory entirely:
   ```powershell
   Remove-Item -Recurse -Force data
   ```
2. Relaunch app
3. Start a flashcard session
4. Mark first card as Known

**Expected Results**:
- [ ] App launches normally (or creates data/ on demand)
- [ ] `data/` directory is created
- [ ] `data/session_state.json` is created
- [ ] Auto-save works normally
- [ ] No errors

**Notes**:
- Tests `_ensure_data_dir()` in SessionManager

---

## Test Scenario 10: Smart Study Mode Recovery
**Objective**: Verify recovery works with Smart Study (spaced repetition)

**Steps**:
1. Go to Study → Flashcards
2. Select objectives
3. Set card limit
4. **IMPORTANT**: Select "Smart Study" mode (if available in setup)
5. Start session
6. Review a few cards
7. Close app
8. Relaunch
9. Click "Resume Session"

**Expected Results**:
- [ ] Session file includes `study_mode: "smart"`
- [ ] Resumed session operates in smart mode
- [ ] Cards are prioritized by spaced repetition (if visible)
- [ ] Score and progress restored correctly

**Notes**:
- Tests mode persistence
- Confirms smart mode works with recovery

---

## Test Scenario 11: Multiple Sessions (Cleanup)
**Objective**: Verify only one session is stored (latest overwrites)

**Steps**:
1. Start Session A (Study Objective 1, 10 cards)
2. Review 3 cards
3. Close app
4. Relaunch
5. Click "Start Fresh" to clear
6. Start Session B (Study Objective 2, 20 cards)
7. Review 2 cards
8. Close app
9. Relaunch
10. Check recovery dialog

**Expected Results**:
- [ ] Recovery dialog shows Session B info (not A)
- [ ] Card count shows ~2 studied (B's count, not A's)
- [ ] Objectives match B (not A)
- [ ] Session file contains only latest session data

**Notes**:
- Confirms single-session design
- Shows latest session always overwrites

---

## Test Scenario 12: Exam Session Future-Proofing
**Objective**: Verify SessionManager supports exam sessions (for future use)

**Steps**:
1. Manually call SessionManager methods in Python REPL:
   ```python
   from utils.session_manager import SessionManager
   sm = SessionManager()

   exam_data = {
	   "current_question": 5,
	   "score": 45,
	   "exam_type": "practice"
   }

   sm.save_exam_session(exam_data)
   session = sm.load_session()
   print(session)  # Should show exam data
   ```

**Expected Results**:
- [ ] `save_exam_session()` works without errors
- [ ] Session file contains `session_type: "exam"`
- [ ] Exam data is persisted
- [ ] `load_session()` retrieves exam session correctly

**Notes**:
- Tests foundation for future exam recovery
- Confirms SessionManager is extensible

---

## Test Scenario 13: Concurrent App Instances
**Objective**: Verify behavior when multiple app windows open

**Steps**:
1. Start Session A
2. Review 3 cards
3. Close app
4. Open two instances of the app simultaneously (in separate terminals)
5. Each should see the same session file

**Expected Results**:
- [ ] Both instances show recovery dialog
- [ ] Both can attempt to resume (last one to touch file "wins")
- [ ] No crashes or file corruption
- [ ] Session persists in valid state

**Notes**:
- Tests file I/O safety
- Confirms JSON writes are atomic-enough for this use case

---

## Test Scenario 14: UI Responsiveness
**Objective**: Verify no lag or freezing during auto-save

**Steps**:
1. Start a flashcard session
2. Quickly mark multiple cards as Known/Needs Review (rapid clicks)
3. Observe UI responsiveness
4. Monitor console for any errors or warnings

**Expected Results**:
- [ ] UI remains responsive
- [ ] No visible lag when marking cards
- [ ] No dropped inputs
- [ ] No errors in console

**Notes**:
- Tests performance of frequent auto-saves
- Confirms ~2-5ms save time is acceptable

---

## Post-Test Cleanup
- [ ] Delete any test session files created
- [ ] Restore `data/` directory if deleted
- [ ] Verify app runs normally
- [ ] Commit tested code to git

---

## Summary Checklist

| Test Scenario | Status | Notes |
|---|---|---|
| 1. First Launch | ⬜ | No session → Welcome screen |
| 2. Auto-Save | ⬜ | Session file created and updated |
| 3. Recovery Dialog | ⬜ | Modal appears with correct info |
| 4. Resume Session | ⬜ | State fully restored |
| 5. Session Cleanup | ⬜ | File deleted after completion |
| 6. Start Fresh | ⬜ | Session cleared on demand |
| 7. Expiration | ⬜ | Old sessions auto-cleaned |
| 8. Corrupted File | ⬜ | Graceful error handling |
| 9. Missing data/ | ⬜ | Directory created on demand |
| 10. Smart Mode | ⬜ | Recovery works with spaced rep |
| 11. Multiple Sessions | ⬜ | Latest overwrites previous |
| 12. Exam Sessions | ⬜ | Future-proofing verified |
| 13. Concurrent Apps | ⬜ | File I/O safety confirmed |
| 14. UI Responsiveness | ⬜ | No lag during rapid saves |

---

## Notes for Tester
- Each scenario builds on previous ones where indicated
- Some scenarios can run independently
- Use `Get-Content data/session_state.json | ConvertFrom-Json` to inspect session files
- Check console output for any warnings or errors
- Report any crashes, hangs, or unexpected behavior
- Performance is acceptable if auto-save takes < 10ms per card

## Bugs/Issues Found
(To be filled during testing)

---

## Sign-Off
- [ ] All 14 scenarios passed
- [ ] No critical bugs found
- [ ] Feature ready for production
- [ ] Code committed to `bells_and_whistles` branch

Date: ___________
Tester: ___________
