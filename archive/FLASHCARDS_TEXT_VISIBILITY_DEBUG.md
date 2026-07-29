# Flashcard Text Visibility - Debugging Guide

## Updated Wrap Calculation

I've simplified the calculation to be more accurate:

**OLD (Too conservative):**
```python
available_width = container_width - 70  # Subtract outer + inner padding
wrap_length = int(available_width * 0.95)  # Then reduce by 5%
# Result: Way too narrow!
```

**NEW (More accurate):**
```python
available_width = container_width - 30  # Only grid padx=15 on each side
wrap_length = max(available_width, 250)  # Use available space directly
# Result: Uses full available space
```

## Why the Change

When you use `grid(padx=15)`, tkinter only reserves 15px on each side within the parent container. It doesn't reduce the parent width.

### Layout Structure
```
FlashcardView (main)
  └─ card_container (padx=20 TO FlashcardView)
	  ├─ lbl_card_side (grid padx=15 WITHIN container)
	  ├─ text_card (grid padx=15 WITHIN container)  ← This is what matters
	  └─ lbl_click_prompt (grid padx=15 WITHIN container)
```

The container width from `winfo_width()` is **after** the outer 20px padding is applied. So we only need to subtract the inner 15px + 15px = 30px.

## What to Look For in Console Output

When you run the app, you should see output like:

```
Container width: 640, Wrap length: 610
Container width: 640, Wrap length: 610
Container width: 1024, Wrap length: 994
```

### If you see this:
- Container width is 640 or larger ✓
- Wrap length is close to container width (minus 30px) ✓
- Text should be visible ✓

### If you see this:
- Container width is 0 or -1 ❌
  → Container hasn't been rendered yet
  → Try resizing window to trigger Configure event

### If text is still invisible:
1. Check if wrap length values look reasonable
2. If wrap_length is too high, we need to subtract more padding
3. If wrap_length is too low, we've subtracted too much

## Testing Steps

1. Launch the app
2. Navigate to Flashcards view
3. Open a terminal to see console output
4. Watch for the container width and wrap length values
5. Try resizing the window and watch values update
6. Report the numbers you see

## Possible Issues

### Issue 1: Container not rendering
If you see "Container width: <= 1", the container hasn't been measured yet. This should resolve on first window resize.

### Issue 2: Text extends beyond visible area
If wrap_length is too high, we're not subtracting enough padding. 
- Try: `available_width = container_width - 50` (subtract more)
- Or: `available_width = container_width - 40` (subtract some)

### Issue 3: Text too narrow
If wrap_length seems too low (much smaller than container_width), we're subtracting too much.
- Try: `available_width = container_width - 20` (subtract less)
- Or: `available_width = container_width - 15`

## Quick Fix Options

If text is still too offset, try these padding values in order:

**Option A (least aggressive):**
```python
available_width = container_width - 20  # Minimal padding
wrap_length = max(available_width, 250)
```

**Option B (moderate):**
```python
available_width = container_width - 30  # Current setting
wrap_length = max(available_width, 250)
```

**Option C (more aggressive):**
```python
available_width = container_width - 50  # More conservative
wrap_length = max(available_width, 250)
```

**Option D (very aggressive - if margin issues):**
```python
available_width = container_width - 60  # Very conservative
wrap_length = max(available_width, 250)
```

## How to Test a Fix

1. Edit the `available_width = container_width - XX` line
2. Save the file
3. Close and reopen the app
4. Check console output to see new wrap_length values
5. See if text is now visible

## Final Debug Info to Provide

If text is still not visible, please provide:
1. Console output (first 5 lines after launching Flashcards view)
2. Window size you're testing with
3. Whether text is completely invisible or partially visible
4. Whether text is offset to the left, right, or both sides
