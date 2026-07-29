# Flashcard Text Offset Issue - Complete Troubleshooting

## Current Approach

We're now measuring **actual rendered widget widths** instead of calculating:

```python
wrapper_width = self.text_card.winfo_width()  # Actual rendered width
container_width = self.card_container.winfo_width()  # Actual container rendered width
```

This is more reliable than trying to predict padding effects.

## Expected Console Output

When you run the app and look at Flashcards, you should see:

```
Wrapper widget width: 580, Container width: 640
Setting wraplength to: 570

Wrapper widget width: 580, Container width: 640
Setting wraplength to: 570

Wrapper widget width: 1280, Container width: 1340
Setting wraplength to: 1270
```

## What Each Number Means

- **Wrapper widget width:** The actual measured width of the text_card.winfo_width()
- **Container width:** The actual measured width of the card_container
- **Wraplength:** The calculated wrap point for text

### If wrapper_width shows 1 or -1
- Widget hasn't been rendered yet
- Will be recalculated when Configure event fires
- Try resizing window to trigger recalculation

### If wrapper_width shows a real number
- Widget has been rendered
- Wraplength should be set correctly
- Text should wrap at that width

## If Text is Still Invisible

### Step 1: Check Console Output
Look for the print statements. If you don't see them:
- Configure event might not be firing
- Try resizing the window

### Step 2: Interpret the Numbers
If you see something like:
```
Wrapper widget width: 0, Container width: 0
```
→ Widgets aren't rendering. Check if they're being added to grid properly.

If you see something like:
```
Wrapper widget width: 50, Container width: 640
```
→ Wrapper is too narrow. Grid padding might be wrong.

If you see something like:
```
Wrapper widget width: 600, Container width: 640
```
→ This looks right. Wraplength should be ~590. Text should be visible.

### Step 3: Test with Extreme Wraplength
If text is still not visible, try setting a very large wraplength:

```python
# In _update_wrap_length, replace the wrap_length calculation with:
wrap_length = 10000  # Very large, no wrapping
```

If text appears with `wraplength=10000`, then the wrapping calculation is wrong.
If text doesn't appear even with huge wraplength, the problem is elsewhere.

## Possible Root Causes

### Cause 1: Grid Padding Conflicts
The padding might be collapsing or interfering. Try removing padding:

**Current:**
```python
text_wrapper.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
```

**Test:**
```python
text_wrapper.grid(row=1, column=0, sticky="ew", padx=0, pady=10)  # Remove padx
```

If text becomes visible, padding is the issue.

### Cause 2: Frame Width Not Updating
The wrapper frame's width might not be updating properly. Add:

```python
text_wrapper.update_idletasks()  # Force layout update
wrapper_width = self.text_card.winfo_width()
```

### Cause 3: Label Not Inheriting Width
The label inside might not be stretching to fill the wrapper. Check `sticky="ew"` is set correctly.

## Quick Fixes to Try (In Order)

### Fix 1: Increase Wraplength Directly
```python
wrap_length = max(wrapper_width, 250)  # Remove the -10
```

### Fix 2: Use Container Width Directly
```python
if wrapper_width > 1:
	wrap_length = wrapper_width
else:
	wrap_length = container_width - 20
```

### Fix 3: Use Very High Initial Wraplength
Change initial label creation:
```python
self.text_card = ctk.CTkLabel(
	text_wrapper,
	...
	wraplength=2000,  # Very high default
)
```

### Fix 4: Force Widget Update Before Wrapping
```python
def _update_wrap_length(self):
	self.text_card.update()  # Force update
	wrapper_width = self.text_card.winfo_width()
	...
```

## Information Needed to Proceed

When you test this, please provide:

1. **Console output** (first 10 lines after navigating to Flashcards)
2. **Window size** you're testing with
3. **What you see**: Text completely invisible? Partially visible? Offset to one side?
4. **Console errors** if any

Example:
```
"I see:
Wrapper widget width: 500, Container width: 560
Setting wraplength to: 490

The text is completely invisible. I'm using a window that's 800px wide."
```

This will help identify exactly what's going wrong.
