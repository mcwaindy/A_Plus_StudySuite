# Game View Implementation Plan

## Objective
Enhance the game view to provide a comprehensive hardware identification game experience with:
1. Fixed canvas widget callback errors during round transitions
2. Comprehensive image-based quiz rounds
3. Motherboard component identification rounds
4. Score tracking and statistics
5. Category selection and difficulty levels

## Current Status
✓ Canvas widget error fixed - callback guards added
✓ Basic game structure in place
✓ 13 image categories with assets available
✓ Motherboard round renders correctly
✓ Standalone image round basic implementation done

## What Needs to be Built

### Phase 1: Quiz Data Population (Image Catalog Enhancement)
**Objective**: Populate `data/image_catalog.json` with quiz metadata for all available images

**Images to Process**:
- cables/ - 17 images (network, power, video, etc.)
- cpu/ - CPU packages and sockets
- memory/ - RAM types and configurations
- storage/ - Hard drives, SSDs, etc.
- expansion/ - Expansion cards
- power/ - Power supplies
- cooling/ - CPU coolers and fans
- printers/ - Printer components
- networking/ - Network devices
- tools/ - Diagnostic tools
- mobile/ - Laptop and mobile parts
- display/ - Monitors and display types

**Quiz Data Requirements per Image**:
```json
{
  "id": "unique_id",
  "category": "category_key",
  "file": "filename.png",
  "name": "Display Name",
  "quiz": {
	"options": ["Correct Answer", "Wrong 1", "Wrong 2", "Wrong 3"],
	"correct_index": 0,
	"explanation": "Why this is correct"
  }
}
```

**Strategy**: Start with high-priority A+ Core 1 categories:
1. Cables & Connectors (most tested)
2. RAM & Memory
3. CPUs & Sockets
4. Power supplies
5. Expand from there

### Phase 2: Game Round Rendering Improvements
**File**: `modules/game_view.py`

**Current Issues**:
- ✓ Fixed: Canvas callback errors on transition
- **TODO**: Ensure image round displays properly
- **TODO**: Better option button layout for different screen sizes
- **TODO**: Score display and progression feedback

**Improvements Needed**:
1. Visual feedback when answer selected (highlight correct/incorrect)
2. Brief explanation display after answer
3. Progress bar showing round number
4. Round countdown timer with visual indicator
5. Category display at top

### Phase 3: Enhanced Game Statistics & Results
**File**: `modules/game_view.py`

**Add to Game State**:
- Total questions answered
- Category breakdown of performance
- Time taken per round
- Streak tracking (consecutive correct)
- Speed bonus points

**End Game Screen**:
- Final score breakdown
- Category performance chart
- Suggested study areas (weak categories)
- Time statistics
- Play again / Change settings buttons

### Phase 4: Difficulty & Category Filtering
**File**: `modules/game_view.py`

**Game Mode Options**:
1. **All Hardware Mix** - Random mix of all categories
2. **Motherboard Layout** - Only motherboard components
3. **By Category** - Selected single category
4. **Core 1 Essential** - High-yield A+ Core 1 topics
5. **Core 2 Essential** - High-yield A+ Core 2 topics

**Difficulty Levels** (optional):
- Easy: Very different wrong answers
- Medium: Related but distinct components
- Hard: Very similar components in category

## Implementation Order

### Step 1: Fix Canvas Widget (DONE ✓)
- Added `is_destroyed` flag
- Added `destroy()` override with unbind cleanup
- Added guards to all event handlers
- Verified compilation

### Step 2: Populate Quiz Data (IN PROGRESS)
- Review available images by category
- Create quiz entries with options
- Test image loading in game rounds
- Validate quiz data structure

### Step 3: Improve Round Visuals
- Add category display header
- Add round preview image scaling
- Add visual feedback for answers
- Add brief explanation display

### Step 4: Enhance Scoring System
- Track per-category performance
- Track time per round
- Calculate streak bonuses
- Display real-time score updates

### Step 5: Add Result Screen
- Show final statistics
- Display category breakdown
- Suggest review areas
- Allow play again / settings reset

## Key Files to Modify

### 1. `data/image_catalog.json`
- **Action**: Add quiz entries for all images
- **Priority**: HIGH
- **Effort**: Medium (bulk data entry)

### 2. `modules/game_view.py`
- **Action**: Enhance rendering, add visual feedback
- **Priority**: HIGH
- **Effort**: Medium (UI improvements)

### 3. `utils/image_library.py`
- **Action**: May need helper function for category stats
- **Priority**: LOW
- **Effort**: Low

## Data Preparation Strategy

### For Each Category:
1. Screenshot each image briefly to understand it
2. Identify the component/device
3. Generate correct answer name
4. Create 3 plausible wrong answers (either from same category or related components)
5. Write brief explanation
6. Add to catalog JSON

### Wrong Answer Strategy:
- Option 1 (Correct)
- Option 2 (Similar component from same category)
- Option 3 (Common confusion/similar name)
- Option 4 (Unrelated but plausible)

Example - RJ45 Connector:
- ✓ Correct: RJ-45 Connector
- Wrong: RJ-11 Connector (similar but phone)
- Wrong: F-Type Connector (video, different connector)
- Wrong: LC Fiber Connector (network, different type)

## Testing Checklist

After implementation:
- [ ] Game launches without errors
- [ ] Motherboard round works
- [ ] Image round displays images correctly
- [ ] Options display with proper layout
- [ ] Answer submission works (both types)
- [ ] Round transitions smoothly
- [ ] Timer counts down correctly
- [ ] Score increments on correct answers
- [ ] End game screen displays
- [ ] Category filtering works
- [ ] Settings can be changed and applied

## Future Enhancements

1. **Image Description**: Show detailed component info
2. **Keyboard Support**: Arrow keys and Enter to select
3. **Custom Quizzes**: Player can create their own game sets
4. **Leaderboard**: Track best scores
5. **Spaced Repetition**: Focus on weak areas
6. **Image Annotation**: Show hotspots on components
7. **Video Explanations**: Link to reference videos

## Notes

- The fixed canvas widget should now handle transitions smoothly
- Quiz data can be populated incrementally - start with cables/connectors
- Visual improvements can be done after quiz data is ready
- Statistics/results screen can be added independently

