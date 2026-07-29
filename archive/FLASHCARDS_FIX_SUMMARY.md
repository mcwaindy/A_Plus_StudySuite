# Flashcard Wrapping Issue - Root Cause & Solution

## What Was Actually Wrong

The card was going off-screen because of **nested frame padding compounding**:

```
Layout Hierarchy (BROKEN):
FlashcardView
  └─ card_container (padx=20)
	  └─ content_frame (padx=20)  ← EXTRA NESTING!
		  └─ text_card
```

This meant:
- `card_container` reduces available space by 40px (20px left + 20px right)
- `content_frame` reduces it AGAIN by another 40px
- Total padding: 80px, but we were only calculating for part of it
- Result: Text wrapped at wrong width, or card elements went off-screen

---

## The Solution

### 1. Remove Nested content_frame
Instead of:
```python
content_frame = ctk.CTkFrame(self.card_container, ...)
content_frame.grid(...)
self.lbl_card_side.grid(parent=content_frame, ...)
```

Now do:
```python
# No intermediate frame
self.lbl_card_side.grid(parent=card_container, ...)  # Direct child
self.text_card.grid(parent=card_container, ...)      # Direct child
```

### 2. Fix Wrap Length Calculation
Changed from:
```python
available_width = container_width - 80  # ❌ Incomplete
```

To:
```python
available_width = container_width - 140  # ✅ Conservative & safe
wrap_length = max(available_width, 250)
```

The 140px accounts for:
- card_container padding: 40px (20 + 20)
- Internal padding for text: 30px (15 + 15)
- Safety margin: 70px

This ensures text never pushes beyond container bounds.

### 3. Better Render Detection
Added check before calculation:
```python
if container_width <= 1:
	return  # Container not yet rendered, try again later
```

This prevents calculation errors when layout first initializes.

---

## Expected Results After Fix

| Issue | Before | After |
|-------|--------|-------|
| Card edges off-screen | ❌ Yes, clipped | ✅ Fully visible |
| Wraps with window size | ❌ No | ✅ Yes, automatically |
| Responds to resize | ❌ No | ✅ Real-time reflow |
| Clean layout | ❌ No | ✅ Proper spacing |

---

## Files Modified

- `modules/flashcards_view.py`
  - Removed `content_frame` nesting in `create_card_widget()`
  - Updated `_update_wrap_length()` calculation
  - Now directly attaches labels to `card_container`

---

## Next Steps

Test the flashcards view by:
1. Launching the app
2. Navigating to Flashcards view  
3. Resizing the window - text should reflow smoothly
4. Check that card is fully visible with no clipping

If edges are still clipped:
- Increase safety margin: `container_width - 160` (from 140)
- Or reduce internal padding: `padx=10` (from 15)
