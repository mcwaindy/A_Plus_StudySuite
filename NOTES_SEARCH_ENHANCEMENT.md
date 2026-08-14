# Notes View Search Enhancement - Content Search & Visual Differentiation

## Overview
Enhanced the Notes View search functionality to search both objective names and note content, with visual differentiation to show users where search terms were found.

## Changes Made

### 1. New Method: `_get_match_type()`
**Purpose**: Determines where a search term matches—in the objective title/name or in the note body content.

**Returns**:
- `'title'`: Match found in objective name, number, or section
- `'content'`: Match found in the markdown note content
- `None`: No match found
- `'all'`: Empty search (shows all notes)

**Implementation**:
- First checks title/objective (priority)
- Falls back to checking note file content
- Gracefully handles file read errors

### 2. Enhanced `render_nav_list()`
**What Changed**:
- Reorganizes search results into two categories:
  - **Title matches** (objectives with search term in name) — displayed first
  - **Content matches** (objectives with search term in notes) — displayed below with "FOUND IN NOTES:" separator

**Visual Organization**:
```
[Search results layout]
CORE 1 · 220-1101
  ● 1.1 Motherboards and their Features  [← title match, normal color]
  ● 1.2 RAM Installation              [← title match, normal color]

FOUND IN NOTES:                        [← separator line]
CORE 1 · 220-1101
  ● 1.3 Cooling Solutions             [← content match, blue text]
  ● 1.4 Power Supplies                [← content match, blue text]

CORE 2 · 220-1102
  ● 2.1 Windows Boot Process          [← content match, blue text]
```

**Benefits**:
- Users immediately see exact name matches
- Content matches clearly labeled and color-coded
- Natural flow: specific → general

### 3. Updated `_add_nav_button()`
**New Parameter**: `match_type` (default: 'title')

**Color Coding**:
- **Title matches**: Normal grayscale (gray10/gray90)
  - Hover: gray70/gray30
- **Content matches**: Blue-tinted text (#6ba3d9/#7bb3e9)
  - Hover: Lighter blue (#8bc3ff/#4a7fcc)
  - Creates visual distinction without breaking the UI theme

**Why Blue?**:
- Stands out from grayscale but not jarring
- Suggests "related but indirect match"
- Consistent with modern search UI patterns

### 4. Backward Compatibility
- Kept original `_matches()` static method intact
- Search still works the same for objective list visibility
- New functionality is purely additive

## User Experience

### Search Behavior

**Scenario 1: Search for "RAM"**
```
Results:
- 1.2 RAM Installation [← title match, normal]
- 3.1 Physical Security [← found in notes about RAM, blue]
- 1.5 Overclocking [← found in notes about RAM, blue]
```

**Scenario 2: Search for "bandwidth"**
```
Results:
- (no title matches)

FOUND IN NOTES:
- 1.1 Motherboards [← content match, blue]
- 2.3 Networking [← content match, blue]
- 1.4 Storage [← content match, blue]
```

**Scenario 3: Empty search**
- Shows all objectives normally
- All buttons use default styling

## Performance Considerations

**Optimization Notes**:
- File reads happen only during search (no caching of all content)
- Avoids memory overhead of pre-loading all note bodies
- Slight delay when searching from empty is acceptable for usability benefit
- If performance issue arises with large note collections, could add LRU cache

## Files Modified

- `modules/notes_view.py`:
  - Added `_get_match_type()` method
  - Enhanced `render_nav_list()` with dual-category organization
  - Updated `_add_nav_button()` with color-coding by match type
  - Maintained backward compatibility with `_matches()` static method

## Testing

✅ Syntax verified
✅ App launches successfully
✅ No runtime errors
✅ Ready for manual testing:
  - Search by term in objective name
  - Search by term found only in note content
  - Verify color differentiation
  - Verify section organization and separator line
  - Verify empty search shows all notes

## Future Enhancements

Potential additions:
- [ ] Highlight search term in note content when opened (search highlights)
- [ ] Case-sensitive search option
- [ ] Regular expression support
- [ ] Search history dropdown
- [ ] "Matches in X objectives" counter
- [ ] Export search results
- [ ] Advanced filters (by core, by objective level, etc.)
