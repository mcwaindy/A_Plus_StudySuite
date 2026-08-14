# Quick Reference - Goals & Milestones Implementation

## 📍 Quick Navigation

| Need | File | Line |
|------|------|------|
| Full Plan | `docs/GOALS_AND_MILESTONES_PLAN.md` | See all details |
| Architecture | `docs/GOALS_ARCHITECTURE.md` | Data flow & diagrams |
| Phase 1 Summary | `docs/PHASE_1_SUMMARY.md` | What's done, what's next |
| Phase 1 Complete | `PHASE_1_COMPLETE.md` | Status report |
| Implementation | `utils/goals_manager.py` | Core logic (production-ready) |
| Data File | `data/goals.json` | Persistence storage |

---

## 🎯 GoalsManager - Essential API

### Basic Usage
```python
from utils.goals_manager import GoalsManager

gm = GoalsManager()
```

### Setting Up a Goal
```python
# User sets target exam date
gm.set_exam_date('2026-09-15')  # Returns True/False

# Get days remaining
days = gm.get_days_until_exam()  # Returns 35 (or None if no date)
```

### Getting Progress
```python
# Get everything for dashboard
summary = gm.get_progress_summary()
# Returns dict with all metrics

# Get just readiness
readiness = gm.calculate_readiness_percentage()  # Returns 0-100.0

# Get daily recommendation
recommendation = gm.get_daily_recommendation()  # Returns string
```

### Tracking Study
```python
# After flashcard session completes
review_entry = {
	'timestamp': '2026-08-11T14:30:00',
	'exam': 'All',
	'objectives': ['1'],
	'cards_studied': 20,
	'study_duration_minutes': 25,
	'cards_reviewed': [...]
}

# Update streak
gm.update_study_streak(review_entry)

# Check for new milestones
new_milestones = gm.check_for_milestone_achievement()
for m in new_milestones:
	print(f"{m['icon']} {m['name']}")  # Show celebration!
```

### Milestone Management
```python
# Get recent achievements
recent = gm.get_recent_milestones(5)  # Last 5

# Get all achievements
all_ms = gm.get_all_milestones()

# Mark as shown
gm.mark_milestone_celebrated(index)
```

---

## 📊 Progress Summary Output

```python
summary = gm.get_progress_summary()

# Using in UI:
f"Days to exam: {summary['days_until_exam']}"  # "35 days"
f"Readiness: {summary['readiness_percentage']}%"  # "20.5%"
f"Cards studied: {summary['total_cards_studied']}"  # "100"
f"Streak: {summary['study_streak_current']} 🔥"  # "5 🔥"
summary['daily_recommendation']  # "Study 20 cards/day (~45 mins)"
summary['recent_milestones']  # List of 5 achievements
```

---

## 🎉 Milestone Types

### Cards Studied (7 milestones)
- 10, 25, 50, 100, 250, 500, 1000 cards

### Objectives (4 milestones)  
- Obj 1, 2, 3, and All 3 Mastered

### Study Streak (4 milestones)
- 3, 7, 14, 30 consecutive days

### Perfect Exams (optional)
- 💯 Single perfect exam
- 💯 Perfect week

---

## 🔄 Integration Points

### In flashcards_view.py (When session ends)
```python
gm = GoalsManager()

# Track the session
review_entry = {...}
gm.update_study_streak(review_entry)

# Check for celebrations
milestones = gm.check_for_milestone_achievement()
if milestones:
	show_celebration_dialog(milestones[0])
```

### In main.py (Sidebar)
```python
# Add button to sidebar
btn_goals = ctk.CTkButton(
	sidebar,
	text="  📊 Goals & Progress",
	command=lambda: self.switch_frame(GoalsView)
)
```

### In main.py (Init)
```python
self.goals_manager = GoalsManager()  # Initialize once
```

---

## ✅ Data Structure

### goals.json Layout
```json
{
  "exam_target_date": "2026-09-15",
  "target_readiness_percentage": 90,
  "milestones_achieved": [
	{
	  "name": "First 10 Cards",
	  "type": "cards_studied",
	  "threshold": 10,
	  "achieved_date": "2026-08-06T14:30:00",
	  "celebrated": true
	}
  ],
  "study_streak": {
	"current_days": 5,
	"longest_streak": 12,
	"last_study_date": "2026-08-11"
  }
}
```

---

## 🧮 Readiness Formula

```
Readiness % = (A × 0.4 + B × 0.3 + C × 0.3) × 100

A = Cards Studied / Target Cards (500)
B = Objectives Covered / 3
C = Cards Mastered / Total Cards Studied
```

**Example**: 100 cards, 2 objectives, 70% mastery
- A = 100/500 = 0.2
- B = 2/3 = 0.67
- C = 0.7
- **Readiness = (0.2×0.4 + 0.67×0.3 + 0.7×0.3) × 100 = 45%**

---

## ⏱️ Timeline

| Phase | What | Hours | Status |
|-------|------|-------|--------|
| 1 | Data + Logic | 3 | ✅ DONE |
| 2 | UI Components | 2.25 | 🚀 NEXT |
| 3 | Integration | 1.25 | 🚀 AFTER |

---

## 🔗 Files to Create Next (Phase 2)

1. **`modules/goals_view.py`** (Main dashboard)
   - Display exam countdown, readiness bar, recommendations
   - Show recent milestones, study streak
   - "Set Goal" button

2. **`modules/dialogs/goals_dialog.py`** (Goal editor)
   - Date picker for exam
   - Readiness target selector
   - Save/Cancel buttons

3. **`modules/dialogs/milestone_dialog.py`** (Celebration popup)
   - Icon + milestone name
   - Progress reminder
   - Celebration animation

---

## 🧪 Quick Test

```python
# Test the implementation works
python
>>> from utils.goals_manager import GoalsManager
>>> gm = GoalsManager()
>>> gm.set_exam_date('2026-09-15')
True
>>> gm.get_days_until_exam()
35
>>> summary = gm.get_progress_summary()
>>> summary['readiness_percentage']
0.0  # No data yet
>>> summary['daily_recommendation']
'Study... (readiness 0%)'
```

---

## 💡 Key Insights

1. **GoalsManager is the brain** - UI just calls it and displays results
2. **All calculations use review_history** - No hardcoded values
3. **Milestones trigger automatically** - Just call check_for_milestone_achievement()
4. **Data persists** - Save/load happens automatically
5. **UI stays simple** - Just call get_progress_summary() once per refresh

---

## 🆘 Common Issues

**Q: How do I test milestones?**  
A: Call `gm.check_for_milestone_achievement()` after adding review entries

**Q: When should I update study streak?**  
A: After each flashcard session completes, call `update_study_streak(review_entry)`

**Q: What if goals.json is corrupted?**  
A: GoalsManager auto-creates with defaults, prints error to console

**Q: Can users change goals later?**  
A: Yes! Just call `set_exam_date()` again, overwrites previous date

---

## 📌 Remember

- ✅ GoalsManager is production-ready
- ✅ Just need to build the UI in Phase 2
- ✅ All calculations are smart and data-driven
- ✅ Full documentation available
- ✅ Ready for advanced features later (AI recommendations, sharing, etc.)

---

**Status**: Phase 1 Complete, Phase 2 Ready 🚀
