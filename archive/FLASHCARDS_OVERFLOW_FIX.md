# Flashcard Text Overflow Fix - Root Cause Identified & Fixed

## The Real Problem

The text was expanding beyond the card container because of **three compounding issues**:

### Issue 1: Unconstrained Label Expansion
```python
# BROKEN:
self.text_card.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
#                                      ↑
#                        "nsew" = stretch in ALL directions
#                        This allows text to expand beyond container!
```

The `sticky="nsew"` tells the label to fill all available space, including expanding **beyond** the parent container if the text doesn't fit.

### Issue 2: Row Weight = Unlimited Growth
```python
# BROKEN:
self.card_container.grid_rowconfigure(1, weight=1)
#                                            ↑
#                     weight=1 = grow to fill parent
#                     Makes the container expand infinitely
```

With `weight=1`, the entire card container wants to expand to fill the viewport, pulling the text with it.

### Issue 3: No Initial Wraplength
```python
# BROKEN:
wraplength=1  # Start with minimal
#  ↑
# This means on first render, text has NO wrapping
# It tries to fit on one line, overflowing off-screen
# Only AFTER the Configure event does _update_wrap_length() get called
```

The text would render at full width before the wrap calculation happened.

---

## The Fix

### Fix 1: Constrain Horizontal Expansion
```python
# FIXED:
self.text_card.grid(row=1, column=0, sticky="ew", padx=15, pady=10)
#                                      ↑
#         "ew" = stretch East-West only
#         Prevents vertical expansion
#         Keeps text INSIDE container horizontally
```

### Fix 2: No Row Expansion
```python
# FIXED:
self.card_container.grid_rowconfigure(0, weight=0)
self.card_container.grid_rowconfigure(1, weight=0)
self.card_container.grid_rowconfigure(2, weight=0)
#                                        ↑
#       weight=0 = size to content, don't expand
#       Card container now FITS its content, doesn't grow infinitely
```

### Fix 3: Reasonable Initial Wraplength
```python
# FIXED:
wraplength=400  # Use sensible default
#  ↑
# Prevents initial overflow on first render
# Gets refined by _update_wrap_length() later
# Text wraps immediately, doesn't overflow
```

### Fix 4: Accurate Wraplength Calculation
```python
# FIXED:
available_width = container_width - 70  # 20+20 (outer) + 15+15 (inner)
wrap_length = int(available_width * 0.95)  # Use 95% for safety margin
wrap_length = max(wrap_length, 200)  # Minimum 200px for readability

# Example:
# Window: 1000px
# Container after outer padding (20): 960px
# Available after inner padding (15): 930px
# Wrap at: 930 * 0.95 = 883px ✓
```

---

## Visual Comparison

### BEFORE (Text Overflows)
```
Window: 1000px wide
┌─────────────────────────────────────────┐
│ FlashcardView                           │
│ padx=20                                 │
│ ┌───────────────────────────────────┐   │
│ │ card_container (weight=1, grows)  │   │
│ │ sticky="nsew" (text expands)      │   │
│ │                                   │   │
│ │ [ Term Side ]                     │   │
│ │                                   │   │
│ │ ┌─────────────────────────────┐   │   │
│ │ │ Text (sticky="nsew")        │   │   │
│ │ │ doesn't wrap, goes off ---> │   │───┼─── OFF SCREEN! ❌
│ │ │ screen as one long line     │   │   │
│ │ └─────────────────────────────┘   │   │
│ │                    (Click flip)    │   │
│ │                                   │   │
│ └───────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### AFTER (Text Wraps Correctly)
```
Window: 1000px wide
┌─────────────────────────────────────────┐
│ FlashcardView                           │
│ padx=20                                 │
│ ┌───────────────────────────────────┐   │
│ │ card_container (weight=0, fits)   │   │
│ │ sticky="ew" (constrained)         │   │
│ │                                   │   │
│ │ [ Term Side ]                     │   │
│ │                                   │   │
│ │ Large Outline Dual In-line Memory │   │
│ │ Module (SODIMM). A compact memory │   │
│ │ form factor used in laptops.      │   │
│ │                                   │   │
│ │                    (Click flip)   │   │
│ │                                   │   │
│ └───────────────────────────────────┘   │  Fully visible! ✓
└─────────────────────────────────────────┘
```

---

## Changes Summary

| Aspect | Before | After |
|--------|--------|-------|
| **sticky parameter** | `"nsew"` (expand all) | `"ew"` (constrain vertical) |
| **Initial wraplength** | `1` (no wrapping) | `400` (wraps from start) |
| **Row weight** | `weight=1` (grow) | `weight=0` (fit content) |
| **Wrap calculation** | `container - 140px` | `(container - 70px) * 0.95` |
| **Padding basis** | Incorrect (missing layers) | Correct (known layers) |
| **Text overflow** | ❌ Overflows window | ✅ Stays inside card |

---

## How It Works Now

### Initial Render (without waiting for Configure event)
```
1. Card widget created with wraplength=400
2. Text displays immediately with wrapping
3. No initial overflow ✓

4. But wraplength might not be perfect yet
   (window might be wider or narrower than 400px)
```

### After Window Renders (Configure event)
```
1. self.card_container.bind("<Configure>", self._on_card_configure)
   fires when card is first rendered and on every resize

2. _update_wrap_length() calculates actual container width
3. Adjusts wraplength to match:
   - Container width minus padding (70px)
   - Times 0.95 for 5% safety margin

4. Result: Perfect wrapping at any window size ✓
```

### Window Resize
```
1. User resizes window
2. FlashcardView expands/contracts
3. card_container receives Configure event
4. _update_wrap_length() recalculates
5. Text reflows smoothly ✓
```

---

## Testing

After this fix:

1. ✅ Launch app and go to Flashcards view
2. ✅ Card should be fully visible (no text overflowing off-screen)
3. ✅ Text should wrap by word, not character
4. ✅ Resize window small → text wraps more
5. ✅ Resize window large → text spreads out
6. ✅ At full screen → text might fit on one line
7. ✅ At narrow window → text wraps to multiple lines
8. ✅ Card stays inside visible area at all times

---

## Key Insight

The problem wasn't just the wraplength calculation—it was that **the label was allowed to expand beyond its container**. The combination of:
- Unconstrained sticky direction
- Row weight = 1 (grow)
- Initial wraplength = 1 (no wrapping)

...meant the text would overflow before any wrapping could happen. Now with `sticky="ew"`, `weight=0`, and `wraplength=400`, the text is constrained from the start and refined as needed.
