# Review Objective Visualization - Technical Options

## Current Implementation: Title Page

The notes view now displays a **professional title page** when you first open the Notes section. This page includes:

### Features
- **Study Statistics** — Shows progress (X of Y sections written)
- **Table of Contents** — Lists all objectives organized by Core 1 and Core 2
- **Clickable Navigation** — Click any objective to jump to its notes
- **Review Highlighting** — Objectives flagged for review show:
  - 🔴 Red circle icon before the title
  - Subtle red/pink background highlight
  - Left border accent in review color

### Current Visual Treatment
```
📚 CompTIA A+ Study Guide
Organized Study Notes

Progress: 8 of 10 sections written

Table of Contents

Core 1
✓ 1.1 - Laptop Hardware  [has review flag - highlighted]
✓ 1.2 - Mobile Devices   [written ✓]
  1.3 - Printers         [not written]

Core 2
✓ 🔴 2.1 - Protocols     [has review flag - highlighted]
✓ 2.5 - Cables          [written ✓]
```

---

## Potential Additional Visual Options for Review Objectives

Here are **GUI approaches** we could implement to enhance review visualization:

### Option 1: **Sidebar Highlighting** (Simple)
**Pros:**
- Always visible in navigation sidebar
- Low complexity to implement
- Quick glance at what needs review

**Cons:**
- Sidebar buttons are small
- Limited visual real estate
- Only shows when in notes view

**Implementation:** Add background color/border to objective buttons that are in review history.

---

### Option 2: **Notification Badge** (Medium)
**Pros:**
- Eye-catching
- Shows count of flagged cards per objective
- Doesn't clutter the UI much

**Cons:**
- Adds visual elements
- Badge updates only on refresh

**Implementation:** Add small badge (e.g., "3" in a colored circle) to objectives with 3+ flagged cards.

Example:
```
[1.1 Laptop Hardware] 🔴 3
[2.1 Protocols] 🔴 7
```

---

### Option 3: **Dynamic Color Gradient** (Medium)
**Pros:**
- Intuitive — more cards flagged = more red
- Useful for prioritization
- Single visual system

**Cons:**
- Requires color calculation
- Harder to distinguish between "1 card" vs "lots of cards"

**Implementation:** Color intensity based on number of flagged cards:
- Light red (1-2 cards)
- Medium red (3-5 cards)
- Intense red (6+ cards)

---

### Option 4: **Separate Review Panel** (Complex)
**Pros:**
- Complete info on what needs review
- Can show card details per objective
- Organized and detailed

**Cons:**
- Takes up significant UI space
- More complex to implement
- Might feel redundant with Review History

**Implementation:** Add a "Review Focus" collapsible panel on title page showing:
```
🎯 Objects Flagged for Review (12 total cards)

1.1 Laptop Hardware (2 cards)
  ☐ SO-DIMM
  ☐ ZIF Connector

2.1 Protocols (7 cards)
  ☐ DNS
  ☐ DHCP
  ...
```

---

### Option 5: **Heat Map / Progress Ring** (Medium+)
**Pros:**
- Visually rich and modern
- Shows review status at a glance

**Cons:**
- More complex rendering
- Might feel "gimmicky"

**Implementation:** Small circular progress indicator per objective:
```
Core 1
  ◯ 1.1 Laptop Hardware    [gray ring = not reviewed]
  ◐ 1.2 Mobile Devices     [partial red fill = some reviews]
  ● 1.3 Cables             [solid red = many reviews]
```

---

### Option 6: **Recent Review Highlight** (Simple)
**Pros:**
- Focuses on most recent work
- Clear temporal aspect
- Less overwhelming visually

**Cons:**
- Doesn't show all flagged items
- Requires tracking review timestamp

**Implementation:** Only highlight objectives from the most recent review session (default), with option to show "all time" or "last 3 sessions".

---

## Recommendation Summary

### Best for **Quick Visibility**: Option 1 (Sidebar Highlighting)
- Low friction to implement
- Always available in sidebar

### Best for **Detailed Planning**: Option 4 (Separate Review Panel)
- Complete information
- Integrated with title page

### Best **Balance of UX + Implementation**: Option 2 (Notification Badge)
- Visual clarity
- Relatively simple
- Useful count information

---

## Next Steps

Which approach would you like to implement?

1. **Sidebar Highlighting** — Add background/border color to nav buttons for reviewed objectives
2. **Review Panel on Title Page** — Show detailed list of flagged objectives below TOC
3. **Badge Notification** — Add card count badge to reviewed objectives
4. **Hybrid Approach** — Title page badge + sidebar color hint
5. **Something else** — Describe your preference

The title page is now fully functional and will automatically detect and highlight review objectives. We can layer on additional visualization approaches from here.
