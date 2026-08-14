# Smart Study Testing Guide

## Quick Start

### 1. Launch the App
```bash
python main.py
```

### 2. Try Smart Study
1. Click **"🧠 Smart Study"** in the left sidebar (row 3, Study section)
2. Select objectives you want to study (or "All")
3. Set card limit (e.g., 10 cards per session)
4. Click **"Start Session"**

### 3. Review Cards
- **Front Side**: Shows the question/term
- **Status Badge**: Shows card urgency (OVERDUE/DUE SOON/CURRENT/NEW/MASTERED)
- **Click or Press Spacebar**: Flip to definition/back side
- **"Know It ✓"**: Mark as mastered → move to next card
- **"Needs Review ✗"**: Flag for future review → move to next card
- **Progress**: Shows "Card X of Y" and "Known: N | Review: M"

### 4. Session Complete
- View summary showing mastered vs. needs review
- See objective breakdown of cards to review
- Option: "New Session" (start again) or "Done" (exit)

### 5. Check Dashboard
1. Click **"📊 Goals & Progress"** in sidebar
2. Scroll down to **"🧠 SMART STUDY STATS"** section
3. See real-time statistics:
   - Cards Due Today
   - Overdue Cards
   - Learning Efficiency %
   - Estimated Mastery Date

---

## What to Verify

### ✅ Card Prioritization
**Expected Behavior**: 
- OVERDUE cards appear first (🔴 red badge)
- DUE SOON cards appear next (🟡 yellow badge)
- CURRENT cards appear after (🟢 green badge)
- NEW cards appear last (🔵 blue badge)

**How to Test**:
1. Run Smart Study multiple times
2. Mark most cards as "Know It ✓"
3. Mark 3-4 as "Needs Review ✗"
4. Start a new session
5. Verify reviewed cards appear at top of list

### ✅ Score Tracking
**Expected Behavior**:
- Counter updates: "Known: X | Review: Y"
- After session: review summary shows breakdown
- Score persists through session

**How to Test**:
1. Start session with 10 card limit
2. Click "Know It" 5 times, "Needs Review" 5 times
3. Check: Known: 5 | Review: 5 in summary
4. Review listed objective breakdown

### ✅ Review History
**Expected Behavior**:
- `data/review_history.json` gets new entry after session
- Entry includes timestamp, cards studied, cards reviewed
- Subsequent sessions show incremented totals

**How to Test**:
1. Complete a Smart Study session
2. Open `data/review_history.json` in text editor
3. Verify latest entry has today's timestamp
4. Check `"mode": "smart_study"` field

### ✅ Goals Integration
**Expected Behavior**:
- Study streak increments after Smart Study session
- Milestone celebrations trigger if criteria met
- Dashboard stats update after session

**How to Test**:
1. Note current streak in Goals dashboard
2. Complete a Smart Study session
3. Return to Goals dashboard
4. Verify streak incremented
5. Check if "Recent Milestones" section updated

### ✅ Status Badges
**Expected Behavior**:
- Badge color matches card urgency
- Description (OVERDUE, DUE SOON, etc.) is accurate
- Badge updates on next session

**How to Test**:
1. Note card status badges in first session
2. Mark some as "Know It", others as "Needs Review"
3. Immediately start new session
4. Verify statuses changed:
   - Reviewed cards marked "CURRENT" or "DUE SOON"
   - Older reviewed cards show higher intervals
   - Known cards show "MASTERED" after sufficient reviews

### ✅ Dashboard Stats
**Expected Behavior**:
- "Cards Due Today" matches current review schedule
- "Overdue" count shows cards past review date
- "Learning Efficiency" calculates from success rate
- "Mastery Date" estimates completion time

**How to Test**:
1. Complete Smart Study sessions daily
2. Watch stats change on Goals dashboard
3. Verify efficiency increases with correct answers
4. Check mastery date doesn't exceed exam date

---

## Common Issues & Fixes

### Issue: "No cards available" message in Smart Study
**Possible Causes**:
- Objectives filter doesn't match any cards
- Card limit set to 0

**Fix**:
- Select "All" objectives
- Use higher card limit (10+)

### Issue: Cards appear in wrong order
**Possible Causes**:
- card_metrics.json not initialized
- Priority score calculation bug

**Fix**:
- Delete `data/card_metrics.json`
- Restart app (will auto-reinitialize)

### Issue: Dashboard SR stats show "Start Smart Study sessions"
**Expected When**:
- No Smart Study sessions completed yet
- app running first time after Phase 4B

**Fix**:
- Complete at least one Smart Study session
- Refresh Goals dashboard

### Issue: Milestone popup doesn't appear
**Possible Causes**:
- Milestone criteria not met
- File permission issue on goals.json

**Fix**:
- Check `data/goals.json` is readable/writable
- Run more Smart Study sessions
- Check streak count in JSON file

---

## Data Files Reference

### `data/card_metrics.json`
- **Contains**: SM-2 metrics for each of 222 cards
- **Updated**: After every review (record_review)
- **Used by**: SpacedRepetitionManager for prioritization
- **Structure**: Array of objects with card_id, easiness_factor, interval, next_review_date, etc.

### `data/review_history.json`
- **Contains**: Summary of all study sessions (flashcards + smart study)
- **Updated**: After session completion
- **Used by**: GoalsManager for streak/milestone tracking
- **Structure**: Array of review objects with timestamp, mode, cards_studied, cards_reviewed

### `data/goals.json`
- **Contains**: User exam target, readiness target, milestones, streak data
- **Updated**: By GoalsManager after review session
- **Used by**: GoalsView dashboard
- **Structure**: Single object with exam_target_date, target_readiness_percentage, milestones_achieved array, study_streak object

---

## Performance Notes

- **Session Load Time**: ~1-2 seconds (loads 222 cards, prioritizes subset)
- **Card Switch Time**: <100ms (instant flip)
- **Summary Generation**: <500ms (aggregates reviewed cards)
- **Dashboard Refresh**: <1 second (updates all stats)

If slower than above, check:
1. CPU usage (background tasks?)
2. Disk I/O (file operations slow?)
3. JSON file sizes (review_history.json growing large?)

---

## Success Criteria Checklist

- [ ] App launches without errors
- [ ] Smart Study button visible in sidebar
- [ ] Can select objectives and card limit
- [ ] Cards display with status badges
- [ ] Flip interaction works (click or spacebar)
- [ ] Know It / Needs Review buttons functional
- [ ] Session completes and shows summary
- [ ] Review history saves to file
- [ ] Goals dashboard shows SR stats
- [ ] Streak updates after session
- [ ] New session uses updated card priorities
- [ ] No crashes or exceptions in logs

---

## Next Session Recommendations

If all tests pass ✅:
1. Complete 3-5 Smart Study sessions
2. Verify card difficulty scores update
3. Test milestone celebration
4. Check dashboard stats accuracy
5. Commit to branch: `git add . && git commit -m "Phase 4: Smart Study Implementation Complete"`

If issues found ⚠️:
1. Record issues in GitHub issues
2. Isolate problem area (backend vs. UI vs. persistence)
3. Run debugger with breakpoints
4. Check logs for stack traces
5. Revert last change if necessary

---

**Happy studying!** 🧠📚✨
