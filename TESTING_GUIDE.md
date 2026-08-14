# 🧪 QUICK TEST GUIDE - Phase 3 Integration

Run this to verify everything works!

---

## ⚡ Quick Start Test (5 minutes)

### Step 1: Launch the App
```bash
python main.py
```

### Step 2: Complete a Flashcard Session
```
1. Click "Flash Cards" button
2. Select:
   - Exam: "All" (or any exam)
   - Objectives: "All" (or select specific ones)
   - Card Limit: "10"
3. Click "Start Review"
4. Study cards: Click "Know It ✓" on each card (to progress faster)
5. After 10 cards → Review screen appears
6. 🎉 LOOK FOR: Celebration dialog "First 10 Cards"
7. Click "Celebrate!" to close
8. Click "Done" to exit
```

### Step 3: Check the Goals Dashboard
```
1. Click "📊 Goals & Progress" button (top of STUDY section)
2. Should see:
   ✅ Study Streak: "1 day" with 🔥 icon
   ✅ Milestones section showing "First 10 Cards" 🎉
   ✅ Readiness bar (likely ~32% or similar)
   ✅ Buttons: "Set Goal" and "All Milestones"
3. Click "All Milestones" → See "First 10 Cards" in history
```

---

## 📊 Full Test Suite (15 minutes)

### Test 1: First Milestone Trigger
**Goal**: Verify celebration dialog appears on first session
```
Step 1: Start fresh (or skip if already tested)
Step 2: Complete 10-card flashcard session (set card limit to 10)
Step 3: EXPECT: 🎉 "First 10 Cards" celebration dialog
Step 4: Close dialog, verify review screen shows results
✅ PASS if: Celebration appeared + review screen shown
```

### Test 2: Streak Tracking  
**Goal**: Verify study streak increments daily and resets on gap
```
Day 1:
  Step 1: Complete 10-card session
  Step 2: Check Goals → Streak should be "1 day" 🔥
  Step 3: Total cards should be "10"

Day 2:
  Step 1: Complete another 10-card session
  Step 2: Check Goals → Streak should be "2 days" 🔥
  Step 3: Total cards should be "20"

Day 3 (skip):
  Step 1: Do NOT study

Day 4:
  Step 1: Complete 10-card session
  Step 2: Check Goals → Streak should reset to "1 day" 🔥
  Step 3: Note: This shows reset works after 2+ day gap

✅ PASS if: Streak increments on consecutive days and resets on gap
```

### Test 3: Multiple Milestones
**Goal**: Verify additional milestones trigger as cards accumulate
```
Before test: Complete sessions until total > 20 cards

Test:
  Step 1: Complete session to reach 25 cards total
  Step 2: EXPECT: 🎉 "Keep It Up - 25 Cards" celebration
  Step 3: Check Goals → Milestones should show both:
		  ✅ First 10 Cards 🎉
		  ✅ Keep It Up - 25 Cards 🎉
  Step 4: Complete sessions to reach 50 cards total
  Step 5: EXPECT: 🎉 "50 Cards Down!" celebration
  Step 6: Check Goals → All Milestones shows all three

✅ PASS if: Multiple milestones trigger progressively
```

### Test 4: Goals Dashboard Features
**Goal**: Verify all dashboard elements display correctly
```
Step 1: Click "📊 Goals & Progress" button
Step 2: Verify these sections exist:
  ✅ Header with app title
  ✅ Countdown section (says "No exam date set" if not set)
  ✅ Readiness section with progress bar
  ✅ Recommendation section (suggests daily action)
  ✅ Streak section (shows current + best)
  ✅ Milestones section (shows recent achievements)
  ✅ Action buttons: "Set Goal" and "All Milestones"

Step 3: Click "Set Goal"
  Step 3a: Date picker dialog should appear
  Step 3b: Select a date (e.g., Sept 15, 2026)
  Step 3c: Select readiness target (e.g., 90%)
  Step 3d: Click "Save"
  Step 3e: Return to dashboard → countdown should update

Step 4: Click "All Milestones"
  Step 4a: Dialog shows list of all achievements
  Step 4b: Shows date achieved + icon
  Step 4c: Can scroll if many milestones

✅ PASS if: All sections display + dialogs work + data updates
```

### Test 5: Streak Milestone (Bonus)
**Goal**: Verify 3-day streak milestone triggers
```
Note: This requires 3 actual days of study. Shortcut for testing:

Option A (Real test - takes 3 days):
  Day 1: Complete session → Streak: 1 day
  Day 2: Complete session → Streak: 2 days
  Day 3: Complete session → Expect: 🔥 "3-Day Streak!" celebration

Option B (Manual test - for developers):
  Step 1: Edit data/goals.json
  Step 2: Change: "current_days": 2
  Step 3: Restart app, complete session
  Step 4: Expect: 🔥 "3-Day Streak!" celebration

✅ PASS if: Celebration appears when streak reaches 3 days
```

---

## 🔍 Data Verification Tests

### Check Timestamps are Saved Correctly
```
Step 1: Complete a flashcard session
Step 2: Open data/review_history.json in text editor
Step 3: Look for timestamp in this format:
		"timestamp": "2026-01-15T14:30:00.123456"
Step 4: Should NOT look like: "C:\Users\Dylan\..." (old broken format)

✅ PASS if: Timestamp is ISO format (YYYY-MM-DDTHH:MM:SS)
```

### Check Goals Data Saves
```
Step 1: Complete a session
Step 2: Open data/goals.json in text editor
Step 3: Should contain:
  {
	"exam_target_date": null or "2026-09-15",
	"target_readiness_percentage": 90,
	"milestones_achieved": [
	  {
		"name": "First 10 Cards",
		"type": "cards_studied",
		"achieved_date": "2026-01-15T14:30:00",
		...
	  }
	],
	"study_streak": {
	  "current_days": 1,
	  "longest_streak": 3,
	  "last_study_date": "2026-01-15"
	}
  }

✅ PASS if: Structure is correct + data is populated
```

### Check Review History Format
```
Step 1: Open data/review_history.json
Step 2: Should contain array of review objects:
  [
	{
	  "timestamp": "2026-01-15T14:30:00.123456",
	  "exam": "Core 1",
	  "objectives": ["1.1 Motherboards"],
	  "cards_studied": 10,
	  "cards_reviewed": [
		{"id": "001", "term": "CPU", "objective": "1.2 CPUs"}
	  ]
	}
  ]

✅ PASS if: Each session is logged with correct format
```

---

## 🐛 Troubleshooting Tests

### If Celebration Dialog Doesn't Appear
```
Test 1: Check Card Limit
  - Make sure you set card limit to 10, 20, 50, or specific number
  - NOT "All cards" (unlimited won't trigger end screen)

Test 2: Check Review Save
  - After session, open data/review_history.json
  - Should have new entry with timestamp
  - If missing → Session didn't save properly

Test 3: Check Goals Manager
  - Open data/goals.json
  - Check if milestones_achieved array exists
  - If empty → Milestones not detected

Test 4: Check Console
  - Look for error messages in console output
  - Common: "Error updating goals: ..." 
  - If error exists → Check import paths
```

### If Streak Doesn't Update
```
Test 1: Check Date Format
  - Open data/goals.json
  - Find "last_study_date": "YYYY-MM-DD" format
  - Should match today's date after session

Test 2: Check Review Timestamp
  - Open data/review_history.json
  - Check timestamp is ISO format
  - If wrong → update_study_streak() can't parse it

Test 3: Check Goals File Exists
  - Ensure data/goals.json exists and is valid JSON
  - If corrupted → Streak can't update

Test 4: Manual Reset
  - Delete data/goals.json
  - Restart app (will create fresh copy)
  - Complete new session
```

### If Dashboard Shows No Data
```
Test 1: Refresh Dashboard
  - Click "Goals & Progress" multiple times
  - Sometimes display needs refresh

Test 2: Check File Permissions
  - Ensure data/ folder is writable
  - Check data/*.json files aren't read-only

Test 3: Check App Restart
  - Close app completely
  - Delete __pycache__ folders
  - Restart app fresh

Test 4: Verify Files Exist
  - data/goals.json should exist
  - data/review_history.json should exist
  - If missing → Complete a session to create them
```

---

## ✅ Success Criteria

Your integration is working if:

- ✅ Flashcards work normally (no changes to study flow)
- ✅ Sessions complete successfully
- ✅ Celebration dialog appears for first session
- ✅ Goals dashboard loads and shows data
- ✅ Streak increments on consecutive days
- ✅ New milestones trigger progressively
- ✅ Data persists across app restarts
- ✅ No error messages in console
- ✅ JSON files have correct format

---

## 📋 Test Checklist

Print this or use as checklist:

```
BASIC FUNCTIONALITY
☐ Flash Cards button works
☐ Can complete 10-card session
☐ Celebration dialog appears
☐ Review screen shows results

DASHBOARD
☐ "Goals & Progress" button exists
☐ Dashboard loads without errors
☐ Shows study streak
☐ Shows recent milestones
☐ "Set Goal" button works
☐ "All Milestones" button works

DATA PERSISTENCE
☐ data/review_history.json created
☐ data/goals.json created
☐ Timestamps are ISO format
☐ Milestones saved in goals.json
☐ Data survives app restart

STREAK TRACKING
☐ Streak: 1 day after first session
☐ Streak: 2 days after second session (next day)
☐ Streak: 1 day after 2-day gap
☐ Longest streak tracked

MILESTONES
☐ 10-card milestone triggers
☐ 25-card milestone triggers
☐ 50-card milestone triggers
☐ Multiple milestones shown in dashboard
☐ All milestones displayed in dialog

INTEGRATION
☐ No errors in console
☐ No breaking changes to flashcards
☐ No breaking changes to other screens
☐ Sidebar navigation still works
☐ App remains responsive
```

---

## 🚀 Running Tests

### Automated Python Test
```bash
# Verify all files compile
.venv\Scripts\python -m py_compile main.py modules/flashcards_view.py modules/goals_view.py utils/goals_manager.py

# Expected output: (no errors)
```

### Quick Manual Flow
```bash
# Run the app
python main.py

# Then manually test scenarios above
```

---

## 📊 Expected Results

### After First 10-Card Session
```
File: data/review_history.json
[
  {
	"timestamp": "2026-01-15T14:30:00.123456",
	"exam": "All",
	"objectives": ["All"],
	"cards_studied": 10,
	"cards_reviewed": [...]
  }
]

File: data/goals.json
{
  "milestones_achieved": [
	{
	  "name": "First 10 Cards",
	  "icon": "🎉",
	  "achieved_date": "2026-01-15T14:30:00",
	  "celebrated": false
	}
  ],
  "study_streak": {
	"current_days": 1,
	"longest_streak": 1,
	"last_study_date": "2026-01-15"
  }
}

UI: Goals Dashboard
- Streak: 1 day 🔥
- Milestones: First 10 Cards 🎉
- Readiness: ~32%
```

---

## 📞 Support

If tests fail:

1. Check console for error messages
2. Verify JSON files are valid (use JSONLint online)
3. Ensure data/ folder exists and is writable
4. Delete data/*.json and start fresh
5. Check Python version (should be 3.14+)
6. Verify customtkinter is installed (check in .venv)

---

**Ready to Test?** Run `python main.py` and complete a flashcard session! 🚀
