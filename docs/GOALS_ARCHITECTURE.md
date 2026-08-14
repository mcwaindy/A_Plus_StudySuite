# Study Goals & Milestones - Architecture & Integration Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN APPLICATION                         │
│                      (main.py)                              │
└──────────────────────┬──────────────────────────────────────┘
					   │
		┌──────────────┼──────────────┐
		│              │              │
		▼              ▼              ▼
	┌────────┐   ┌──────────┐  ┌──────────────┐
	│ Sidebar│───│  Goals   │  │ Flashcard   │
	│ Nav    │   │ View     │  │ View        │
	└────────┘   │ (📊)     │  │             │
				 └──────────┘  └──────────────┘
					   ^              │
					   │              │
					   │ reads/updates│
					   │              │ saves session
					   │              │
					┌──┴──────────────┴──┐
					│  GoalsManager      │
					│  (utils/)          │
					├────────────────────┤
					│ • Readiness calc   │
					│ • Streak tracking  │
					│ • Milestones       │
					│ • Recommendations  │
					└────────┬───────────┘
							 │
					┌────────┴───────────┐
					│                    │
					▼                    ▼
			┌───────────────┐  ┌──────────────────┐
			│ data/goals    │  │ data/review_     │
			│ .json         │  │ history.json     │
			└───────────────┘  └──────────────────┘
```

---

## Data Flow Diagram

### User Sets Exam Date
```
User clicks "Set Goal" button
		│
		▼
Goals Dialog opens (goals_dialog.py)
		│
		├─ User selects date (2026-09-15)
		├─ User confirms
		│
		▼
GoalsManager.set_exam_date('2026-09-15')
		│
		▼
goals.json updated with exam_target_date
		│
		▼
Goals View refreshes and displays:
  • "Days until exam: 35"
  • "Readiness: 0% → Get studying!"
  • Daily recommendation appears
```

### User Studies Flashcards
```
User completes flashcard session
		│
		├─ 20 cards studied
		├─ 5 marked "Needs Review"
		├─ Session duration: 25 minutes
		│
		▼
FlashcardView calls GoalsManager:
  gm.update_study_streak(review_entry)
  new_milestones = gm.check_for_milestone_achievement()
		│
		▼
GoalsManager processes:
  ✓ Updates study_streak (1st day = 1 day)
  ✓ Checks milestones (10 cards → achieved!)
  ✓ Saves updated data to goals.json
  ✓ Returns new milestone info
		│
		▼
FlashcardView shows milestone notification:
  ┌──────────────────────────────┐
  │ 🎉 First 10 Cards!           │
  │ You've started your journey! │
  │        [OK]                  │
  └──────────────────────────────┘
		│
		▼
User sees updated Goals dashboard:
  • Readiness: 4% (10 cards / 500 target)
  • Study Streak: 1 🔥
  • Cards Studied: 10
  • Daily Recommendation updated
```

### Goals Dashboard Updates
```
User views Goals View (📊)
		│
		▼
GoalsManager.get_progress_summary()
		│
		├─ Reads: goals.json + review_history.json
		├─ Calculates:
		│  • Readiness % = 4.5%
		│  • Days until exam = 35
		│  • Study streak = 1 day
		│  • Daily recommendation = "Study 20 cards"
		│  • Recent milestones = [First 10 Cards]
		│
		▼
Goals View displays:
  ┌─────────────────────────────────┐
  │     A+ STUDY SUITE              │
  │  📊 GOALS & PROGRESS             │
  ├─────────────────────────────────┤
  │  📅 Exam Target: Sept 15, 2026   │
  │     ⏱️  35 days remaining        │
  ├─────────────────────────────────┤
  │  📊 Readiness: ████░░░░░░░░ 4%   │
  │     Target: 90%                 │
  ├─────────────────────────────────┤
  │  💡 Daily Recommendation:        │
  │     Study 20 cards/day           │
  │     (~45 minutes)                │
  ├─────────────────────────────────┤
  │  🔥 Study Streak: 1 day          │
  │     Best: 5 days                 │
  │     Cards studied: 10            │
  ├─────────────────────────────────┤
  │  🎉 Recent Milestones:           │
  │     ✓ First 10 Cards!            │
  │                                  │
  │              [Set Goal]          │
  └─────────────────────────────────┘
```

---

## Component Interface Diagram

### GoalsManager Public API

```python
class GoalsManager:
	# Initialization
	__init__()                          # Load/create goals.json

	# Exam Date (What the user is training for)
	set_exam_date(date_str) → bool
	get_exam_date() → str | None
	get_days_until_exam() → int | None

	# Readiness (How ready are they?)
	calculate_readiness_percentage(
		review_history) → float         # 0-100
	get_daily_recommendation() → str    # "Study 20 cards/day"

	# Study Streak (Consistency tracking)
	update_study_streak(
		review_entry) → None            # Call after each session
	get_study_streak() → Dict[str, int] # {current, longest, last_date}

	# Milestones (Achievement tracking)
	check_for_milestone_achievement(
		review_history) → List[Dict]    # New achievements
	mark_milestone_celebrated(
		index) → None                   # Mark as shown
	get_recent_milestones(count) → List[Dict]
	get_all_milestones() → List[Dict]

	# Dashboard
	get_progress_summary() → Dict       # Everything for UI
```

---

## Integration Checklist for Phase 2-3

### Phase 2: Create UI Components

#### Goals Dialog (`modules/dialogs/goals_dialog.py`)
```
Inputs:
  - ExamDatePicker (CTkComboBox or custom date widget)
  - Readiness dropdown (70%, 80%, 90%)
  - Optional: Daily goal inputs

Outputs:
  - Calls: GoalsManager.set_exam_date()
  - Returns: Dialog confirmed or cancelled
```

#### Goals View (`modules/goals_view.py`)
```
Inputs:
  - Parent frame
  - GoalsManager instance

Displays:
  - Exam countdown (from get_days_until_exam)
  - Progress bar (from calculate_readiness_percentage)
  - Daily recommendation (from get_daily_recommendation)
  - Study streak (from get_study_streak)
  - Milestones list (from get_recent_milestones)

Interactions:
  - "Set Goal" button → Open goals_dialog
  - "View All Milestones" → Show milestones_list_dialog
```

#### Milestone Notification Dialog
```
Triggers when:
  - New milestone in check_for_milestone_achievement()

Displays:
  - Milestone icon (🎉, 🔥, 💯, 🎯, 🏆)
  - Milestone name
  - Progress toward next milestone

Actions:
  - User clicks OK
  - Dialog closes
  - GoalsManager.mark_milestone_celebrated()
```

### Phase 3: Integration

#### In `main.py` (Sidebar):
```python
btn_goals = ctk.CTkButton(
	sidebar,
	text="  📊 Goals & Progress",
	anchor="w",
	command=lambda: self.switch_frame(GoalsView)
)
btn_goals.grid(row=?, column=0, padx=10, pady=2, sticky="ew")
```

#### In `main.py` (App init):
```python
def __init__(self):
	# ... existing code ...
	from utils.goals_manager import GoalsManager
	self.goals_manager = GoalsManager()
```

#### In `modules/flashcards_view.py` (Session end):
```python
def finish_review_screen(self):
	# ... existing code ...

	# NEW: Update goals/milestones
	from utils.goals_manager import GoalsManager
	gm = GoalsManager()

	review_entry = {
		'timestamp': datetime.now().isoformat(),
		'exam': self.selected_exam,
		'objectives': self.selected_objectives,
		'cards_studied': len(self.cards_studied),
		'study_duration_minutes': self.session_duration,
		'cards_reviewed': self.reviewed_cards
	}

	gm.update_study_streak(review_entry)
	new_milestones = gm.check_for_milestone_achievement()

	# Show milestone celebrations
	for milestone in new_milestones:
		if not milestone['celebrated']:
			self._show_milestone_notification(milestone)
```

---

## Testing Strategy

### Unit Tests (for GoalsManager)
```python
def test_set_exam_date():
	gm = GoalsManager()
	assert gm.set_exam_date('2026-09-15') == True
	assert gm.get_exam_date() == '2026-09-15'

def test_days_until_exam():
	gm = GoalsManager()
	gm.set_exam_date('2026-09-20')
	days = gm.get_days_until_exam()
	assert days > 0
	assert days < 100

def test_readiness_calculation():
	gm = GoalsManager()
	test_history = [
		{'cards_studied': 50, 'objectives': ['1'], ...},
		{'cards_studied': 50, 'objectives': ['2'], ...},
	]
	readiness = gm.calculate_readiness_percentage(test_history)
	assert 0 <= readiness <= 100

def test_milestone_detection():
	gm = GoalsManager()
	test_history = [
		{'cards_studied': 10, 'objectives': ['1'], ...},
	]
	milestones = gm.check_for_milestone_achievement(test_history)
	assert len(milestones) > 0
	assert milestones[0]['name'] == 'First 10 Cards!'
```

### Integration Tests
```python
def test_flashcard_to_goals_flow():
	# 1. Create session
	# 2. Complete flashcard review
	# 3. Verify goals.json updated
	# 4. Verify streak increased
	# 5. Verify milestone achieved and celebrated
```

### Manual Testing Checklist
- [ ] Set exam date via dialog
- [ ] Goals view displays correctly
- [ ] Progress bar updates after study session
- [ ] Study streak increments for consecutive days
- [ ] Milestone notification appears on achievement
- [ ] All data persists after app restart
- [ ] Goals view updates after flashcard session
- [ ] Daily recommendation changes based on progress

---

## Future Enhancements (Post-MVP)

1. **Goal Presets**
   - "Prepare in 30 days" (intensive)
   - "Prepare in 60 days" (moderate)
   - "Prepare in 90 days" (relaxed)

2. **Achievement Sharing**
   - Share milestone to social media
   - Print progress report

3. **Smart Notifications**
   - Daily reminder at set time
   - "You're behind on your goal" alert
   - "Keep the streak alive!" reminder

4. **Historical Analytics**
   - Charts showing progress over time
   - Trend analysis and predictions
   - Best study time identification

5. **Group Goals**
   - Study with a friend
   - Shared milestone celebrations
   - Friendly competition leaderboard

---

**Document Version**: 1.0  
**Status**: Ready for Phase 2 implementation  
**Last Updated**: August 2026
