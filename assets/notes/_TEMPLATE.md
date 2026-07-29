---
title: Human-Readable Note Title
objective: 3.4
---

<!--
  HOW TO ADD A NOTE
  =================
  1. Copy this file into assets/notes/core1/ or assets/notes/core2/.
    2. Name it <objective>_<topic>.md   e.g.  2.5_network_cables_connectors.md
     The folder decides which sidebar section it lands in; the front matter
     above supplies the display title and objective badge.
  3. Write. Press the reload button in the notes header to see changes --
     no need to restart the app.

  Files starting with _ or . are skipped by the sidebar, which is why this
  template never shows up in the list.

  Do NOT put a top-level "# Title" heading in the body. The header card
  already renders the title, and a leading H1 is stripped automatically.
  Start your sections at "##".
-->

## Overview

Plain paragraphs, **bold**, *italic*, and `inline code` all work as normal.

Start sections at `##`. Once a note has four or more `##`/`###` headings, an
"On this page" card is generated automatically at the top.

---

## Callouts

Four spaces of indentation for the body. The quoted part is the title.

!!! exam "Exam Tip"
    Blue. Use for the fact most likely to appear on the test.

!!! tip "Remember"
    Green. Mnemonics, shortcuts, rules of thumb.

!!! note "Background"
    Purple. Context that is useful but not directly tested.

!!! warning "Watch Out"
    Amber. Easy-to-confuse distinctions.

!!! danger "Common Pitfall"
    Red. Safety issues and answers people reliably get wrong.

!!! example "Scenario"
    Cyan. Worked examples and troubleshooting walk-throughs.

---

## Images

Images live in the shared tree under `assets/images/<category>/`, which the
Hardware Identification game reads from as well. Reference them by path from
the project root:

    ![Descriptive caption](assets/images/cables/UTP_STP.png)

The alt text becomes the visible caption under the image. Paths relative to
this file (`../../images/cables/UTP_STP.png`) also work if you prefer live
preview in an external markdown editor.

If the file is not there yet you get a dashed "Image not found" placeholder
naming the path, rather than a silently broken image.

Add `{.bare}` to drop the border and rounded corners, for cutouts on
transparent backgrounds:

    ![Fuser assembly](assets/images/printers/laser_fuser.png){.bare}

To make an image available to the guessing game too, add it to
`data/image_catalog.json` with a `quiz` block. Reference diagrams that should
never become a quiz prompt get `"quiz": null`. Run
`python -m utils.image_library` to check every catalogued file resolves.

---

## Tables

| Standard | Max Speed | Max Distance | Frequency |
| -------- | --------- | ------------ | --------- |
| Cat 5e   | 1 Gbps    | 100 m        | 100 MHz   |
| Cat 6    | 10 Gbps   | 55 m         | 250 MHz   |
| Cat 6a   | 10 Gbps   | 100 m        | 500 MHz   |

---

## Definition Lists

Good for vocabulary drilling — the term sits above its indented definition.

UTP
:   Unshielded Twisted Pair. No foil shielding; cheap and flexible, but
    susceptible to EMI.

STP
:   Shielded Twisted Pair. Foil around the pairs or the bundle, for noisy
    environments like factory floors.

---

## Links

Links to `http://` or `https://` open in your real browser, not inside the
app pane.

To cross-reference another note, use its id — the path under `assets/notes/`
without the `.md`:

    [See the cables note](note:core1/2.5_network_cables_connectors)
