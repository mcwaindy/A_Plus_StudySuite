# Study Goals & Milestones Feature - Implementation Plan

## Overview
A motivational tracking system that helps users set study targets, track progress, and celebrate achievements.

---

## User Stories

### Story 1: Setting an Exam Target Date
**As a** student preparing for CompTIA A+  
**I want to** set a target exam date and get daily study recommendations  
**So that** I can stay on track and know how much to study each day

**Acceptance Criteria**:
- User can set/edit target exam date via UI dialog
- System calculates days until exam
- Based on current progress, daily recommendations are shown
- Data persists across sessions

---

### Story 2: Tracking Progress to Exam Readiness
**As a** student studying  
**I want to** see a visual progress bar showing my exam readiness  
**So that** I can stay motivated and see how close I am to being ready

**Acceptance Criteria**:
- Progress bar visible on dashboard/home screen
- Shows percentage toward readiness goal (e.g., "75% Ready")
- Updates after each study session
- Based on: cards studied, objectives covered, review performance

---

### Story 3: Celebrating Milestones
**As a** student  
**I want to** see celebrations when I hit study milestones  
**So that** I feel motivated to keep studying

**Acceptance Criteria**:
- Milestone events trigger: "🎉 You've studied 100 cards!", etc.
- Milestones tracked:
  - Cards studied (10, 25, 50, 100, 250, 500, 1000)
  - Objectives mastered (1, 2, 3 all objectives)
  - Study streak (3, 7, 14, 30 days in a row)
  - Perfect exam simulations (100% on practice exam)
- Visual notification appears in app
- Milestone achievement recorded in progress file

---

## Data Structure

### New File: `data/goals.json`
```json
{
  "exam_target_date": "2026-09-15",
  "target_readiness_percentage": 90,
  "milestones_achieved": [
	{
	  "name": "First 10 Cards",
	  "type": "cards_studied",
	  "threshold": 10,
	  "achieved_date": "2026-08-06",
	  "celebrated": true
	},
	{
	  "name": "Objective 1 Mastered",
	  "type": "objective_mastered",
	  "objective": "1",
	  "achieved_date": "2026-08-10",
	  "celebrated": true
	}
  ],
  "daily_goals": {
	"target_cards_per_day": 15,
	"target_exams_per_week": 2,
	"target_minutes_per_day": 45
  },
  "study_streak": {
	"current_days": 5,
	"longest_streak": 12,
	"last_study_date": "2026-08-11"
  }
}
```

### Modified File: `data/review_history.json`
Add fields to track the day's study time:
```json
{
  "timestamp": "2026-08-11T14:30:00",
  "exam": "All",
  "objectives": ["1"],
  "cards_studied": 20,
  "study_duration_minutes": 25,
  "cards_reviewed": [...],
  "exam_score_percentage": null
}
```

---

## Architecture

### New Files to Create

#### 1. `modules/goals_view.py` - Main Goals Dashboard
Purpose: Display goals, progress, and milestones
- Scrollable container with sections:
  - Exam target countdown
  - Readiness progress bar (0-100%)
  - Daily recommendation card
  - Recent milestones section
  - Study streak display
  - Action buttons (Set Goal, View All Milestones)

#### 2. `utils/goals_manager.py` - Goals Logic
Purpose: Core functionality for goals
- `GoalsManager` class:
  - Load/save goals data
  - Calculate exam readiness percentage
  - Calculate daily study recommendations
  - Track milestones and notify when achieved
  - Update study streak
  - Get next milestone info

Key Methods:
```python
class GoalsManager:
	def __init__(self):
		self.goals_data = self._load_goals()

	def set_exam_date(self, date: str) -> None
	def get_days_until_exam(self) -> int
	def calculate_readiness_percentage(self, review_history: list) -> float
	def get_daily_recommendation(self) -> dict
	def update_study_streak(self, review_data: dict) -> None
	def check_for_milestone_achievement(self, review_data: dict) -> list[dict]
	def mark_milestone_celebrated(self, milestone_id: str) -> None
	def get_progress_summary(self) -> dict
```

#### 3. `modules/dialogs/goals_dialog.py` - Goal Setting Dialog
Purpose: UI for creating/editing goals
- Date picker for exam date
- Readiness percentage toggle (70%, 80%, 90%)
- Daily study goal inputs (cards/day, time/day)
- Save/Cancel buttons
- Input validation

---

## Implementation Steps

### Phase 1: Data & Core Logic (2 hours)

#### Step 1.1: Create Goals Data Structure
- [ ] Create `data/goals.json` with default values
- [ ] Create initialization script
- [ ] Handle missing/corrupt goals.json gracefully

#### Step 1.2: Implement GoalsManager
- [ ] Create `utils/goals_manager.py`
- [ ] Implement load/save methods
- [ ] Implement readiness calculation
  - Formula: `(cards_studied / target_cards) * (objectives_covered / 3) * (review_performance)`
  - cards_studied: from review_history
  - objectives_covered: count of objectives with cards studied
  - review_performance: (cards_known / cards_studied) percentage
- [ ] Implement milestone detection
- [ ] Implement study streak calculation

#### Step 1.3: Update Review History Schema
- [ ] Add `study_duration_minutes` field to each review entry
- [ ] Make update backward compatible (handle old entries)
- [ ] Test data loading with existing review_history.json

---

### Phase 2: UI Components (1.5 hours)

#### Step 2.1: Create Goals Dialog
- [ ] Build `modules/dialogs/goals_dialog.py`
- [ ] Date picker widget (CTkComboBox with date validation)
- [ ] Readiness percentage dropdown (70%, 80%, 90%)
- [ ] Daily goal inputs
- [ ] Save validation and feedback

#### Step 2.2: Create Goals View/Dashboard
- [ ] Build `modules/goals_view.py`
- [ ] Layout with sections:
  - Header: "Study Goals & Progress"
  - Exam countdown card
  - Readiness progress bar (visual + percentage)
  - Daily recommendation card
  - Study streak display
  - Recent milestones (last 5)
  - "Set Goal" and "View All Milestones" buttons

#### Step 2.3: Create Milestone List Dialog
- [ ] Show all achieved milestones with dates
- [ ] Show upcoming milestones with progress
- [ ] Filterable by type (cards studied, objectives, streak, exams)

---

### Phase 3: Integration (1 hour)

#### Step 3.1: Hook into App Lifecycle
- [ ] Initialize GoalsManager in main app
- [ ] Update review history when study session completes
- [ ] Check for new milestones after each review
- [ ] Update study streak on app startup

#### Step 3.2: Add to Sidebar Navigation
- [ ] Add "📊 Goals & Progress" button to main.py
- [ ] Create route to goals_view.py
- [ ] Add icon (📊 or 🎯)

#### Step 3.3: Add Milestone Notifications
- [ ] Create celebration dialog/notification
- [ ] Show when new milestone achieved
- [ ] Play optional sound (if implemented)
- [ ] Auto-dismiss or require acknowledgment

#### Step 3.4: Hook into Flashcard Session
- [ ] After session ends, update review history with:
  - cards_studied count
  - study_duration_minutes (from timer or elapsed time)
  - cards reviewed list
- [ ] Trigger milestone check
- [ ] Update goals dashboard

---

## Feature Details

### Readiness Calculation Formula

```
Readiness % = (A × 0.4 + B × 0.3 + C × 0.3) × 100

Where:
  A = Cards Studied Progress = min(cards_studied / target_cards, 1.0)
  B = Objectives Coverage = objectives_with_cards / 3
  C = Mastery Score = (cards_known / total_cards_studied)

Example:
  - Studied 250 cards (target: 500) = 0.5
  - Covered 2/3 objectives = 0.67
  - Mastery: 180 known / 250 studied = 0.72
  - Readiness = (0.5 × 0.4 + 0.67 × 0.3 + 0.72 × 0.3) × 100
			  = (0.2 + 0.201 + 0.216) × 100
			  = 61.7%
```

### Milestones List

#### Cards Studied Milestones
- 🎉 First 10 Cards!
- 🎉 Keep It Up - 25 Cards Studied!
- 🎉 50 Cards Down!
- 🎉 Century! 100 Cards Studied!
- 🎉 Super Grind - 250 Cards!
- 🎉 Halfway There - 500 Cards!
- 🎉 Legendary Grind - 1000 Cards Studied!

#### Objectives Milestones
- 🎉 Objective 1 Mastered!
- 🎉 Objective 2 Mastered!
- 🎉 Objective 3 Mastered!
- 🎉 All Objectives Mastered!

#### Study Streak Milestones
- 🔥 3-Day Streak!
- 🔥 Week-Long Streak! (7 days)
- 🔥 Two-Week Grind! (14 days)
- 🔥 Monthly Commitment! (30 days)

#### Perfect Score Milestones
- 💯 Perfect Practice Exam!
- 💯 Two Perfects in a Row!
- 💯 Perfect Week! (All exams 100%)

### Daily Recommendations Algorithm

```python
def get_daily_recommendation(days_until_exam, readiness_pct):
	"""
	Calculate recommended daily study load.
	"""
	if days_until_exam <= 0:
		return "Exam day! Good luck! 🎓"

	if readiness_pct >= 90:
		return "You're exam-ready! Light review recommended (15 mins/day)"

	if readiness_pct >= 75:
		daily_cards = 20
		return f"Review unfamiliar cards ({daily_cards} cards/day)"

	deficit = (90 - readiness_pct)
	intensity_factor = deficit / 15  # Scales effort based on deficit
	daily_cards = int(20 * intensity_factor)

	return f"Study {daily_cards} new cards + 10 reviews ({45 * intensity_factor} mins/day)"
```

---

## Testing Checklist

- [ ] Goals file loads and saves correctly
- [ ] Readiness calculation produces 0-100% values
- [ ] Milestones trigger at correct thresholds
- [ ] Study streak updates correctly across days
- [ ] Milestone notifications appear and don't crash app
- [ ] Goals persist across app restarts
- [ ] Progress bar renders correctly with various percentages
- [ ] Exam countdown shows correct days
- [ ] Daily recommendations change based on progress
- [ ] All time calculations handle leap years and DST
- [ ] Old review_history.json entries work without study_duration field

---

## Acceptance Criteria for Completion

- ✅ User can set exam target date
- ✅ Readiness progress bar displays and updates
- ✅ Daily study recommendations appear
- ✅ Milestones trigger and show notifications
- ✅ Study streak tracked and displayed
- ✅ Goals dashboard accessible from sidebar
- ✅ All data persists across sessions
- ✅ No crashes on edge cases (missing fields, future dates, etc.)
- ✅ UI consistent with rest of app (fonts, colors, spacing)
- ✅ Helpful error messages if goals.json corrupted

---

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/goals-and-milestones

# After each phase, commit:
git add -A
git commit -m "Phase 1: Goals data structure and core logic"
git commit -m "Phase 2: Goals UI components and dialogs"
git commit -m "Phase 3: Goals integration with app lifecycle"

# When complete:
git push origin feature/goals-and-milestones
# Create PR and request review
```

---

## Future Enhancements (Post-MVP)

- [ ] Recurring goal reminders (email/desktop notifications)
- [ ] Goal sharing with mentor/study group
- [ ] AI-powered personalized recommendations based on weak areas
- [ ] Custom milestones (user-defined celebrations)
- [ ] Goal templates (e.g., "Prepare for exam in 30 days")
- [ ] Export progress report as PDF
- [ ] Integration with calendar app
- [ ] Leaderboard (if multiplayer added)
- [ ] Goal-based study session recommendations
- [ ] Predicted exam readiness date based on current pace

---

## Time Estimate Summary

| Phase | Component | Hours | Notes |
|-------|-----------|-------|-------|
| 1 | Data + Core Logic | 2.0 | GoalsManager, formulas |
| 2 | UI Components | 1.5 | Dialogs and views |
| 3 | Integration | 1.0 | Hookups and flow |
| - | Testing & Polish | 0.5 | Edge cases |
| **Total** | | **5 hours** | Could vary based on customization |

---

**Status**: Ready to implement  
**Priority**: HIGH - Significantly improves user engagement  
**Complexity**: LOW-MEDIUM (straightforward logic, standard UI patterns)
