# Notes Refinement Plan

## What We Have Now
- The notes browser scans `assets/notes/` dynamically instead of relying on a hardcoded list.
- Markdown notes are rendered through `modules/notes/renderer.py`, including callouts, tables, links, and image placeholders.
- Shared study assets live in `assets/images/` and are catalogued in `data/image_catalog.json` for both Notes and the Hardware Game.
- The note content and shared objective labels were still using early draft objective names.

## What Was Just Updated
- Renumbered the notes content to reflect the real CompTIA A+ 220-1101 objective map.
- Added a stub note for the missing Core 1 1.1 laptop objective.
- Retitled the existing notes so the sidebar now reflects the proper objective language.
- Repointed the shared image/objective metadata and sample questions to the corrected objective labels.
- Adjusted note image rendering to prefer project-relative image sources when possible.

## Near-Future Work
- Fill in the new 1.1 laptop note with actual study content.
- Expand the 3.1 motherboard/add-on card note with real material instead of the current stub.
- Add more Core 1 notes for the remaining objective groups so the sidebar mirrors the full exam outline.
- Verify image rendering in the running app once the local GUI dependencies are present.
- Clean up any remaining draft objective names in flashcards or practice question data as new content is added.