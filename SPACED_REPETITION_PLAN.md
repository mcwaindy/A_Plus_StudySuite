# 🧠 SPACED REPETITION IMPLEMENTATION PLAN

## 🎯 Mission
Implement a science-backed algorithm that intelligently prioritizes which cards users should study based on:
- Review history (when last studied)
- Performance (known vs needs review)
- Difficulty (how often marked as "needs review")
- Time since first seen

---

## 📊 The Algorithm

### Core Concept: SM-2 (SuperMemo 2) Adapted

The most proven spaced repetition algorithm in existence. Adapted for our use case.

### Key Metrics Per Card

**Easiness Factor (EF)**: 1.3 - 2.5 (default: 2.0)
- Higher = easier card (reviewed more often, less mistakes)
- Lower = harder card (reviewed less often, more mistakes)

**Interval (days)**: How many days until next review
- Day 1: 1 day
- Day 2: 3 days
- Day 3: 7 days
- Day 4: 14 days
- etc.

**Repetitions**: How many times successfully reviewed

**NextReviewDate**: Exact date card should next appear

**Difficulty Score**: 0-100% (% of times marked "needs review")

### Formula

```
New Interval = Old Interval × EF

New EF = EF + (0.1 - (5 - Grade) × (0.08 + (5 - Grade) × 0.02))

Where Grade = 5 (correct) or 0 (incorrect)
```

### In Practice

User studies card:
- ✅ Marks "Know It" → Grade 5 → Interval increases
- ❌ Marks "Needs Review" → Grade 0 → Interval stays short

Result: Hard cards appear more often, easy cards appear less often

---

## 📁 NEW FILES NEEDED

### 1. `utils/spaced_repetition_manager.py` (250-300 lines)
Core algorithm implementation
- Load card metrics from JSON
- Calculate next review date
- Score cards by priority
- Update metrics after review

### 2. `data/card_metrics.json` (NEW)
Persistent storage for card learning data
```json
{
  "fc_001": {
	"easiness_factor": 2.0,
	"interval": 1,
	"repetitions": 0,
	"next_review_date": "2026-08-15",
	"difficulty_score": 0.5,
	"last_review_date": "2026-08-14",
	"first_seen_date": "2026-08-14"
  }
}
```

### 3. `modules/spaced_repetition_view.py` (300-350 lines)
Smart study mode UI
- Shows cards prioritized by SR algorithm
- Emphasizes overdue cards
- Shows progress/streak
- Integrates with existing flashcard flow

### 4. `modules/dialogs/spaced_rep_info_dialog.py` (100-150 lines)
Info popup explaining SR and showing card stats

---

## 🔄 INTEGRATION POINTS

### With `modules/flashcards_view.py`
- NEW: "🧠 Smart Study" button alongside normal flashcards
- Or: Radio button to toggle "Smart Study" mode
- Reuse existing session flow
- Just change card order + add metrics

### With `utils/goals_manager.py`
- SR metrics contribute to readiness calculation
- Track efficiency improvements over time
- Show "Learning Curve" chart

### With `data/card_metrics.json`
- Create on first run (initialize all cards with defaults)
- Update after each session
- Persist across restarts

---

## 🎯 IMPLEMENTATION PHASES

### Phase 4A: Backend (SR Algorithm) - 2 hours
1. Create `SpacedRepetitionManager` class
2. Implement SM-2 algorithm
3. Card scoring logic
4. Metrics persistence
5. Tests/verification

### Phase 4B: UI (Study Interface) - 2 hours
1. Create `SpacedRepetitionView` 
2. Show prioritized cards
3. Display "overdue" indicator
4. Show learning statistics
5. Integrate with session flow

### Phase 4C: Integration - 1 hour
1. Add "🧠 Smart Study" button to sidebar
2. Connect to existing session flow
3. Update metrics after sessions
4. Display stats in goals dashboard

### Phase 4D: Polish & Testing - 1 hour
1. Visual polish (highlight overdue cards)
2. Performance optimization
3. Testing & validation
4. Documentation

**Total: 6 hours**

---

## 📊 EXPECTED IMPACT

### Before Spaced Repetition
- User studies: 20 random cards per day
- Retention: ~60% after 1 month
- Study time needed: High

### After Spaced Repetition
- User studies: 5-10 high-value cards per day + 10-15 new cards
- Retention: ~85% after 1 month (25% improvement!)
- Study time needed: Lower (more efficient)
- User feels: Smarter (they see improvement!)

---

## 🎮 USER EXPERIENCE

### Normal Flashcards (Existing)
```
Click "Flash Cards" → Random cards → Study → Done
```

### Smart Study (New)
```
Click "🧠 Smart Study" → Prioritized cards with:
  ⚠️ OVERDUE (red) - Should have studied yesterday
  📅 DUE SOON (yellow) - Study in next 2-3 days
  ✅ CURRENT (green) - On schedule
  ➕ NEW (blue) - First time seeing

Smart features:
  • Hard cards appear more often
  • Easy cards studied less often
  • Shows which cards you struggle with
  • Tracks improvement over time
  • Automatically schedules future reviews
```

---

## 🔍 KEY ALGORITHMS

### 1. Card Scoring (Priority Queue)
```
Score = Overdue_Days × 5 + Difficulty_Score × 2 + (1 / Interval)

Cards sorted by score (highest = most urgent)
```

### 2. Difficulty Detection
```
Difficulty = (Times_Marked_Review / Times_Seen) × 100

High difficulty (75%+) → Card appears every 1-3 days
Low difficulty (25%-) → Card appears every 7-14 days
```

### 3. Interval Calculation
```
If correct (Know It):
  New_Interval = Old_Interval × EF
  Max 30 days

If incorrect (Needs Review):
  New_Interval = 1 day
  EF reduced slightly
```

---

## 📈 METRICS DASHBOARD ADDITIONS

New section in Goals View:

```
🧠 SMART STUDY STATS
├─ Cards Due Today: 15
├─ Overdue Cards: 3
├─ Learning Efficiency: 78% ↑ (improvement from 72%)
├─ Average Interval: 8.3 days
└─ Cards Fully Mastered: 42 (15% of total)
```

---

## 🧪 TESTING STRATEGY

### Unit Tests (Implicit)
- Algorithm calculations correct
- Interval progression correct
- Score ranking correct
- Persistence working

### Integration Tests
- Card metrics created on first run
- Updates persist across sessions
- Flashcard session updates metrics
- Goals dashboard reflects changes

### User Tests
- Smart study shows harder cards more
- Easier cards show less often
- Overdue cards highlighted
- Progress visible over time

---

## 🚀 DELIVERABLES

By end of Phase 4:
- ✅ SM-2 algorithm implemented
- ✅ Card metrics persistent
- ✅ Smart study UI created
- ✅ Integrated with existing flow
- ✅ Dashboard shows smart study stats
- ✅ Full documentation
- ✅ Test guide

---

## 💡 BONUS FEATURES (If Time)

### 1. Learning Curve Chart
Show user's improvement over time
- X-axis: Days
- Y-axis: % Cards Mastered
- Visual proof of progress

### 2. Weak Spots Analyzer
Which objectives are hardest?
- List objectives by difficulty
- Show weakest topics
- Recommend focus areas

### 3. Prediction Engine
"At current pace, you'll master 80% by Sept 15"
- Estimate exam readiness
- Time-to-mastery calculation
- Confidence % based on data

### 4. Study Recommendations
"Study these 5 cards today for 80% efficiency"
- Personalized study plan
- Optimal card selection
- Time estimates

---

## 🎯 SUCCESS CRITERIA

✅ Smart study prioritizes correctly  
✅ Hard cards appear more frequently  
✅ Metrics persist across sessions  
✅ Goals dashboard reflects changes  
✅ Users see measurable improvement  
✅ Performance is fast (<100ms per card)  
✅ UI is intuitive and clear  

---

## 📋 IMPLEMENTATION CHECKLIST

- [ ] Phase 4A: Backend algorithm
  - [ ] SpacedRepetitionManager class
  - [ ] SM-2 algorithm implementation
  - [ ] Card scoring logic
  - [ ] Metrics persistence

- [ ] Phase 4B: UI implementation
  - [ ] SpacedRepetitionView class
  - [ ] Card display with priorities
  - [ ] Overdue indicators
  - [ ] Statistics display

- [ ] Phase 4C: Integration
  - [ ] Sidebar button
  - [ ] Session flow connection
  - [ ] Metrics updating
  - [ ] Dashboard display

- [ ] Phase 4D: Testing & Polish
  - [ ] Testing guide
  - [ ] Documentation
  - [ ] Performance check
  - [ ] UI polish

---

**Ready to start Phase 4A (Backend)? Let's build the algorithm!** 🚀
