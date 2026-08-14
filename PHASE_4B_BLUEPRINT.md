# 🎮 PHASE 4B BLUEPRINT - UI Implementation

## 🎯 Mission
Build the user interface for Smart Study mode that uses the SR algorithm from Phase 4A.

---

## 📊 What We'll Build

### 1. `modules/spaced_repetition_view.py` (300+ lines)
**Purpose**: Smart Study mode UI  
**Replaces**: Normal flashcard view when "Smart Study" mode enabled

**Features**:
- Shows prioritized cards (hard cards first)
- Color-coded status indicators:
  - 🔴 OVERDUE (red) - Study yesterday
  - 🟡 DUE SOON (yellow) - Study next 2-3 days
  - 🟢 CURRENT (green) - On schedule
  - 🔵 NEW (blue) - First time
- Progress stats:
  - "Card 5 of 20" (only high-priority cards)
  - "Efficiency: 78%"
  - "Mastered: 42/222"
- Study session integrated
- Metrics updated on review

### 2. Sidebar Button & Navigation
**Location**: main.py sidebar  
**Options**:
- Add "🧠 Smart Study" button (separate from "Flash Cards")
- Or add toggle within "Flash Cards" setup

**Recommendation**: Separate button (clearer UX)

### 3. Dashboard Integration (Update)
**Update**: modules/goals_view.py  
**Add Section**: "🧠 SMART STUDY STATS"
```
Learning Efficiency: 78% ↑ (from 72%)
Cards Due Today: 15
Overdue Cards: 3
Weak Objective: "Windows Command Tools" (75% difficulty)
Estimated Mastery: Sept 15, 2026
```

---

## 🔄 Architecture

### Data Flow

```
User clicks "🧠 Smart Study"
	↓
SpacedRepetitionView initializes
	↓
Loads SpacedRepetitionManager
	↓
Gets prioritized cards via get_study_cards()
	↓
Displays them in order of priority
	↓
User studies each card
	↓
Marks "Know It" or "Needs Review"
	↓
record_review() updates metrics
	↓
Next card in priority order
	↓
Session completes → Results shown
	↓
Metrics update dashboard next time viewed
```

### UI Layout

```
SMART STUDY MODE
════════════════════════════════════════════
Header: 🧠 Smart Study Mode | Card 5 of 12

Progress Bar: ████████░░░░░░░░ 42%
Efficiency: 78% | Mastered: 42/222

Status Indicator: 
🔴 OVERDUE (2 days behind)

FLASHCARD (Large Display):
┌─────────────────────────────────┐
│     [ Term Side ]               │
│                                 │
│         TCP/IP                  │
│                                 │
│  (Click or press SPACE to flip) │
└─────────────────────────────────┘

Definition (on flip):
┌─────────────────────────────────┐
│   [ Definition Side ]           │
│                                 │
│  Transmission Control Protocol  │
│  + Internet Protocol - The      │
│  foundational protocols of the  │
│  modern internet...             │
│                                 │
└─────────────────────────────────┘

Buttons:
[Know It ✓] [Needs Review ✗]

Session Stats:
Studied: 5 | Known: 4 | Review: 1
Next Session: Tomorrow (3 cards)
════════════════════════════════════════════
```

---

## 📝 Implementation Phases

### Phase 4B-1: Core View (1 hour)
```python
# Create SpacedRepetitionView class
class SpacedRepetitionView(ctk.CTkFrame):
	def __init__(self, parent, config=None):
		# Load SR manager + get prioritized cards
		# Build UI (same as flashcards but with status indicators)

	def get_study_cards(self):
		# Call sr_manager.get_study_cards()
		# Filter by objective/exam

	def update_card_display(self):
		# Show current card with status color
		# Display priority indicator (🔴🟡🟢🔵)

	def record_answer(self, known: bool):
		# Call sr_manager.record_review()
		# Update metrics
		# Move to next card
```

### Phase 4B-2: Status Indicators (30 min)
```python
# Color-coded status display
Status Colors:
- Overdue: RGB(255, 50, 50) - Red
- Due Soon: RGB(255, 200, 0) - Yellow
- Current: RGB(50, 200, 50) - Green
- New: RGB(0, 100, 255) - Blue

Status Label:
┌────────────────────┐
│ 🔴 OVERDUE (2d)    │  ← Shows why urgent
└────────────────────┘
```

### Phase 4B-3: Sidebar Integration (30 min)
```python
# In main.py, add to sidebar:
btn_smart_study = ctk.CTkButton(
	sidebar,
	text="  🧠 Smart Study",
	command=lambda: self.switch_frame(SpacedRepetitionView)
)
btn_smart_study.grid(row=?, column=0, padx=10, pady=2, sticky="ew")
```

### Phase 4B-4: Dashboard Update (30 min)
```python
# In modules/goals_view.py, add:
smart_study_stats = sr_manager.get_learning_statistics()
# Display:
# - Learning Efficiency
# - Cards Due Today
# - Overdue Cards
# - Weak Objectives
# - Mastery Projection
```

---

## 🎨 UI Components Needed

### Status Badge
```
def create_status_badge(self, status: str) -> str:
	"""Return emoji + label for card status."""
	if status == "overdue":
		return "🔴 OVERDUE"
	elif status == "due_soon":
		return "🟡 DUE SOON"
	elif status == "current":
		return "🟢 CURRENT"
	elif status == "new":
		return "🔵 NEW"
	elif status == "mastered":
		return "✅ MASTERED"
```

### Progress Display
```
Progress: ████████░░░░░░░░ 5 of 12 (42%)
Efficiency: 78% | Mastered: 42/222 cards

Next Review:
├─ 3 cards due today
├─ 5 cards due tomorrow
└─ 8 cards due this week
```

### Session Statistics
```
This Session:
  Cards Studied: 12
  Marked Known: 10
  Marked Review: 2
  Efficiency: 83%

Card Breakdown:
  Overdue Fixed: 3 (from 5)
  New Cards: 9
  Learning Cards: 0
```

---

## 🔗 Integration Points

### With `modules/flashcards_view.py`
- Reuse session logic (mark known/review)
- Reuse review screen
- Update goals_manager (same as flashcards)
- Share styling/colors

### With `utils/goals_manager.py`
- Still call after session ends:
  - `goals_manager.update_study_streak()`
  - `goals_manager.check_for_milestone_achievement()`
- Add bonus milestone: "Smart Study Addict" 🧠

### With `modules/goals_view.py`
- Add SR statistics section
- Show weak objectives
- Display learning efficiency
- Show mastery date estimate

### With `data/card_metrics.json`
- Read: Get prioritized cards
- Write: Update after each review
- Persist: Auto-save metrics

---

## 📊 Expected UI State

### Start of Smart Study
```
🧠 SMART STUDY MODE
Status: 🔴 OVERDUE (2 days behind)
Card: 5 of 12

[ TCP/IP Large Display ]

[Know It ✓] [Needs Review ✗]

Progress: █████░░ 42% | 4 Known, 1 Review
```

### After Studying 5 Cards
```
🧠 SMART STUDY MODE
Status: 🟡 DUE SOON (1 day behind)
Card: 6 of 12

[ Firewall Large Display ]

[Know It ✓] [Needs Review ✗]

Progress: ██████░░ 50% | 4 Known, 2 Review
```

### After Session
```
SMART STUDY COMPLETE!

This Session:
  Cards Studied: 12
  Known: 10 (83%)
  Needs Review: 2

Next Session:
  Due Tomorrow: 5 cards
  Due Next Week: 8 cards

[New Smart Study] [Done]
```

---

## 🎯 Success Criteria

✅ Cards displayed in priority order  
✅ Status indicators show urgency  
✅ Session tracking works  
✅ Metrics update correctly  
✅ Dashboard shows SR stats  
✅ Performance fast (<100ms)  
✅ UI matches existing design  

---

## 💡 Advanced Features (Optional)

### 1. Study Recommendation
```
"Based on your pattern, study these 5 cards today for 80% efficiency"
- Pre-selects optimal subset
- Saves time
```

### 2. Weak Area Alert
```
⚠️ "Windows Command Tools" is 75% difficulty
   Recommend: Extra focus tomorrow
```

### 3. Learning Curve Display
```
Mastery over time:
  Week 1: 0% → 15%
  Week 2: 15% → 35%
  Week 3: 35% → 50%

Projection: Mastery by Sept 15
```

### 4. Streak Bonus
```
🔥 3-Day Smart Study Streak!
+5 extra cards recommended today
```

---

## 📋 Phase 4B Checklist

- [ ] Create SpacedRepetitionView class
- [ ] Implement card display with status badges
- [ ] Build study session logic
- [ ] Add metrics updating (record_review)
- [ ] Create review/results screen
- [ ] Add sidebar button
- [ ] Integrate with goals_manager (streaks/milestones)
- [ ] Update goals dashboard
- [ ] Test prioritization
- [ ] Test metrics persistence
- [ ] Polish UI and styling
- [ ] Write documentation
- [ ] Testing guide

---

## ⏱️ Estimated Time

- 1.0 hour: Core SpacedRepetitionView
- 0.5 hour: Status indicators + colors
- 0.5 hour: Sidebar integration
- 0.5 hour: Dashboard update
- 0.5 hour: Testing + polish
- **Total: 3.0 hours**

---

## 🚀 Ready to Start Phase 4B?

All backend is complete. UI is straightforward - mostly reusing existing patterns from flashcards_view.py.

Key differences:
1. **Card order**: Prioritized instead of random
2. **Status display**: Show why each card is important
3. **Metrics**: Update card_metrics.json instead of just review_history.json
4. **Dashboard**: Show SR stats

Let's build it! 🧠
