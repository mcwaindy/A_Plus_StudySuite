# Coordinate Picker Tool Guide

## Overview

The Coordinate Picker is a standalone tool for defining and editing motherboard component hotspots (clickable regions) and their associated metadata.

## Launching the Tool

### From Main Application
- Open the Diagram view and click "Open Coordinate Picker" button

### Standalone Mode
```bash
python tools/coordinate_picker.py
```

## User Interface

### Top Section: Board Selection
- **Board Selector**: Dropdown to choose which motherboard to edit
- **Resolution Display**: Shows the loaded image dimensions

### Middle Section: Component List
- **Component List**: Shows all hotspots defined for the selected board
- **View/Edit Options**:
  - Double-click a component to edit it
  - Right-click for context menu options

### Canvas/Preview Area
- **Board Preview**: Visual representation of the selected board
- **Hotspot Display**: Shows all component rectangles overlaid on the board image
- **Click Hotspots**: Click the preview to select hotspots precisely

### Bottom Section: Component Editor
- **Component Name**: Name of the hardware component (e.g., "CPU", "RAM Slot 1")
- **Description**: Detailed description or part number
- **Coordinates**: X, Y, Width, Height values for the hotspot
- **Display Scale Slider**: Adjust how the board is displayed visually (1-200%)

## Editing Workflow

### Adding a New Component
1. Select a board from the dropdown
2. Click "Add Component" button
3. Fill in the component name and description
4. Click on the preview area to set the bounding box coordinates
5. Click "Save" to persist changes

### Editing an Existing Component
1. Double-click a component in the list
2. Modify the name, description, or coordinates
3. Click "Save" to update

### Removing a Component
1. Select the component from the list
2. Click "Delete" button
3. Confirm the deletion

### Adjusting Display Scale
1. Use the "Display Scale" slider (1-200%)
2. The preview updates in real-time to show how the board will appear
3. The scale is stored per-board in `motherboard_nodes.json`

## Technical Details

### Data Storage
- All changes are persisted to `data/motherboard/motherboard_nodes.json`
- Display scale is stored per-board with the board configuration
- Hotspot coordinates are stored as arrays: `[x, y, width, height]`

### Coordinate System
- Origin (0, 0) is at the top-left corner of the image
- X increases rightward, Y increases downward
- Coordinates are in pixels relative to the original image dimensions

### Display Scale
- Affects only visual presentation in diagram view and coordinate picker
- Does NOT affect game view (motherboard rounds use native scale)
- Range: 1.0 (100%, full size) to 2.0 (200%, enlarged)
- Useful for improving visibility on very large or detailed boards

## Tips & Tricks

1. **Precise Selection**: Use the numeric input fields for exact pixel values
2. **Visual Tuning**: Adjust display scale to find the optimal viewing size
3. **Component Naming**: Use clear, consistent names for easy identification
4. **Testing**: Switch to the Diagram view to verify hotspots appear correct

## Troubleshooting

### Picker Won't Launch
- Ensure `tools/coordinate_picker_main.py` exists and is executable
- Check for Python errors in the terminal
- Verify all dependencies are installed (customtkinter, PIL)

### Hotspots Not Appearing
- Ensure the board is selected correctly
- Verify the image file exists at the path specified in `motherboard_nodes.json`
- Check that hotspot coordinates are within the image bounds

### Changes Not Saved
- Ensure you click "Save" button (not just closing the form)
- Check file permissions on `data/motherboard/motherboard_nodes.json`
- Look for error messages in the picker window

## Related Files

- `tools/coordinate_picker_main.py` - Main application logic
- `tools/coordinate_picker.py` - Standalone launcher
- `utils/board_registry.py` - Data persistence layer
- `data/motherboard/motherboard_nodes.json` - Board registry storage
- `modules/diagram/canvas_widget.py` - Coordinate system and rendering
