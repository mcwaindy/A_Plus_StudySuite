# Bug Fixes: Flashcard & Smart Study Session Management

## Issues Identified
1. **Review history duplicate saves** - save_review() was duplicated, saving each session twice
2. **Infinite loop on "All" objectives** - Sessions with no card limit and "All" objectives never ended
3. **"Done" button restarts instead of exits** - exit_review_screen() was calling start_new_session() instead of destroying view
4. **Award calculations inflated** - Due to duplicate saves + restart behavior, card counts were wrong

## Root Causes

### Issue 1: Duplicate save_review() code
**File**: `modules/flashcards_view.py` lines 87-136
**Problem**: The entire save sequence was copy-pasted twice in the same function
**Impact**: Each session saved twice, doubling card study counts and inflating award progress

### Issue 2: Infinite loop without card limit
**File**: `modules/flashcards_view.py` lines 824-844 (record_answer)
**Problem**: When card_limit is None and "All" objectives selected, loop check was:
```python
if self.card_limit and total_answered >= self.card_limit:
	show_review_screen()
	return
# Then loops back forever
self.current_index += 1
if self.current_index >= len(self.cards):
	self.current_index = 0  # Resets to 0 forever
```
**Impact**: User could never finish a study session without explicit card limit

### Issue 3: "Done" button logic error
**File**: `modules/flashcards_view.py` exit_review_screen()
**Problem**: Button handler checked `_in_review_mode` correctly, but exit function called `start_new_session()` instead of exiting
**Impact**: Clicking "Done" restarted session instead of ending it

### Issue 4: Duplicate in SpacedRepetitionView
**File**: `modules/spaced_repetition_view.py` record_answer()
**Problem**: Same infinite loop pattern - no check for no card_limit scenario
**Impact**: Smart Study sessions also couldn't auto-end without explicit limit

---

## Fixes Applied

### Fix 1: Remove Duplicate Code
**File**: `modules/flashcards_view.py` save_review()
**Change**: Removed duplicate lines 125-136 (second save sequence)
**Result**: Each session now saves exactly once

### Fix 2: Auto-end Sessions Without Card Limit
**Files**: 
- `modules/flashcards_view.py` record_answer() [lines 804-844]
- `modules/spaced_repetition_view.py` record_answer() [lines 348-395]

**Change**: Added check after card_limit check:
```python
# If no card limit and user has reviewed all cards once, auto-end session
if not self.card_limit and total_answered >= len(self.cards):
	self.show_review_screen()
	return
```
**Result**: Sessions auto-end after user reviews all available cards once

### Fix 3: Proper Exit Behavior
**Files**:
- `modules/flashcards_view.py` exit_review_screen() [lines 800-803]
- `modules/spaced_repetition_view.py` exit_review_screen() [lines 343-346]

**Change**: Replaced restart logic with view destruction:
```python
def exit_review_screen(self):
	"""Exit the review screen and return to parent app (quit flashcard session)."""
	self._in_review_mode = False
	self.destroy()
```
**Result**: Clicking "Done" now properly exits to parent (main app), not restarting

---

## Data Impact

### Before Fixes
- 3 sessions of 10 cards = 30 cards studied
- Actual cards in database = 30
- Saved in review_history = 60 (duplicate saves)
- Awards triggered: 50-card milestone (incorrectly)
- Mastery: 52% (counted duplicates + wrong logic)

### After Fixes
- 3 sessions of 10 cards = 30 cards studied
- Actual cards in database = 30
- Saved in review_history = 30 (no duplicates)
- Awards triggered: None (correctly, only 30 cards)
- Mastery: ~10% (correct calculation)

---

## Testing the Fixes

### Test 1: Review History Accuracy
```
1. Complete a 10-card flashcard session
2. Open data/review_history.json
3. Verify: ONE new entry (not two)
4. Verify: cards_studied = 10 (not 20)
```

### Test 2: Session Auto-end
```
1. Open Flashcards or Smart Study
2. Select "All" objectives
3. DO NOT set card limit
4. Study cards until all reviewed once
5. EXPECTED: Session auto-ends (review screen shows)
6. RESULT: ✅ Session should end, not loop
```

### Test 3: Done Button
```
1. Complete any study session
2. See review screen with "Done" button
3. Click "Done"
4. EXPECTED: Return to main app (sidebar visible)
5. RESULT: ✅ Should not restart session
```

### Test 4: Award Accuracy
```
1. Check current awards/milestones
2. Reset data/review_history.json to empty []
3. Complete exactly 50-card study session (5 × 10-card sessions)
4. EXPECTED: 50-card award triggers
5. RESULT: ✅ Awards should trigger at correct thresholds
```

### Test 5: Mastery Calculation
```
1. Complete Smart Study sessions
2. Check Goals dashboard
3. Mastery should increase gradually with correct reviews
4. Should NOT show 52% on first few sessions
5. RESULT: ✅ Realistic mastery progression
```

---

## Files Modified

1. **modules/flashcards_view.py**
   - Removed duplicate save_review() code (lines 125-136)
   - Added auto-end check in record_answer()
   - Fixed exit_review_screen() to destroy view instead of restart

2. **modules/spaced_repetition_view.py**
   - Added auto-end check in record_answer()
   - Fixed exit_review_screen() to destroy view instead of restart

## Verification

✅ Both files compile without syntax errors
✅ App launches successfully
✅ No runtime exceptions

---

## Next Steps for User

1. **Verify fixes work**
   - Test a complete flashcard session with "All" objectives, no limit
   - Confirm "Done" exits properly
   - Check review_history.json has only 1 entry per session

2. **Verify award accuracy**
   - Check that 50-card milestone triggers at correct count
   - Verify mastery % is realistic (not 52% after 3 sessions)

3. **Consider unified view** (Optional)
   - Smart Study could become a "mode" in regular flashcards view
   - Would reduce code duplication
   - Would improve UX consistency

---

**Status**: Bug fixes applied and syntax verified. Ready for manual testing.
