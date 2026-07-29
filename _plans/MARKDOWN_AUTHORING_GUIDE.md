# Markdown Authoring Guide for A+ Study Suite Notes

## Overview

This guide explains how to create study notes for the A+ Study Suite in Markdown format. The notes system automatically discovers `.md` files from the `assets/notes/` directory, parses them, and renders them beautifully in the GUI.

**Key Point:** Your Markdown files are rendered with a professional dark theme, automatic table of contents generation, embedded images as base64 URIs, syntax highlighting, and support for exam callouts and definition lists.

---

## File Organization & Naming

### Directory Structure

```
assets/notes/
├── core1/          # CompTIA A+ 220-1101 notes
│   ├── 1.1_laptops.md
│   ├── 2.5_network_cables_connectors.md
│   └── ...
├── core2/          # CompTIA A+ 220-1102 notes
│   ├── 1.1_bios_uefi.md
│   └── ...
└── general/        # General IT topics (not exam-specific)
	├── command_line_basics.md
	└── ...
```

### Filename Format

Filenames are automatically parsed to extract the objective number and title:

```
[core#_]<objective>_<topic>.md
```

**Examples:**
- `core1_2.5_network_cables_connectors.md` → Objective 2.5, Core 1
- `2.1_storage_devices.md` → Objective 2.1 (auto-assigned to containing folder)
- `command_line_basics.md` → No objective (title only)

**Rules:**
- Use underscores (`_`) or hyphens (`-`) to separate words
- Include dots (`.`) for multi-level objectives (e.g., `2.5` for 2.5, `3.1.2` for 3.1.2)
- The filename becomes the fallback title if front matter is missing
- Title is capitalized and word-wrapped automatically

---

## Front Matter (Metadata)

Every note file should begin with YAML front matter between triple dashes. This explicitly sets the title and objective:

```markdown
---
title: Network Cables & Connectors
objective: 2.5
---

## First Section Heading
...
```

### Front Matter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Optional* | Display title shown in the note header and sidebar. If omitted, derived from filename. |
| `objective` | string | Optional* | Objective number (e.g., `2.5`, `3.1.2`). If omitted, derived from filename. |

*One or both should be present. If both are missing, the filename is used entirely.

### Example Front Matter

```markdown
---
title: BIOS & UEFI Configuration
objective: 1.1
---
```

---

## Document Structure

### Header Hierarchy

The note structure uses a clear heading hierarchy. Each level has distinct styling:

#### `# H1 — Main Topic (avoid using; reserved for internal use)`
Don't start with H1; it conflicts with the auto-generated note title.

#### `## H2 — Major Section`
Use for the primary sections of your note. Rendered with a blue left accent bar.

```markdown
## 🌐 Twisted Pair Ethernet Cabling
```

#### `### H3 — Subsection**
Use for detailed topic breakdowns. Rendered in green.

```markdown
### Cat 5
```

#### `#### H4 — Small Topic or Label**
Use sparingly for very granular labels. Rendered in uppercase.

```markdown
#### Maximum Speeds
```

### Horizontal Rules

Use `---` to visually separate major sections:

```markdown
---

## Next Major Section
```

---

## Text Formatting

### Bold & Italic

- **Bold:** `**text**` or `__text__`
- *Italic:* `*text*` or `_text_`
- ***Bold & Italic:*** `***text***` or `___text___`

**Rendered as:**
- Bold text is bright white; italic is slightly dimmed.

### Links

```markdown
[Link Text](https://example.com)
[Internal Anchor](#section-name)
```

### Code & Code Blocks

**Inline code:**
```markdown
The `ipconfig` command displays network settings.
```

Rendered with a green font on a dark background.

**Code blocks (fenced):**
```
	```bash
	C:\Users\Dylan> ipconfig

	Ethernet adapter Ethernet:
		IPv4 Address. . . . . . . . : 192.168.1.100
	```
```

Supports syntax highlighting for: `bash`, `powershell`, `python`, `cmd`, `html`, `javascript`, `json`, `xml`, etc.

---

## Lists

### Unordered Lists

```markdown
* Point one
* Point two
  * Nested point
  * Another nested point
* Point three
```

### Ordered Lists

```markdown
1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step
```

### Definition Lists

Great for vocabulary and glossary content:

```markdown
Term One
:   The definition or explanation of Term One. Can be multiple lines.

Term Two
:   Short definition.
```

**Rendered as:**
- Term is bold white; definition is gray with a left border.

---

## Blockquotes

Use blockquotes to highlight important notes or background context:

```markdown
> This is a blockquote. It appears visually separated with a green left border
> and a subtle background.
>
> Multiple paragraphs are supported.
```

---

## Callouts (Admonitions)

Callouts highlight exam tips, warnings, and other critical information. Use the `!!!` syntax:

### Exam Tips

```markdown
!!! exam "Cat 6 vs. Cat 6a Distance"
	Cat 6 achieves 10 Gbps up to **55 meters**, while Cat 6a achieves 10 Gbps 
	all the way to **100 meters**. This distance split is the single most-tested 
	distinction between the two.
```

**Rendered as:** Blue left border, blue title.

### Tips & Hints

```markdown
!!! tip "Memory Trick"
	Remember: STP cables = **S**hielded for noisy environments.

!!! hint "Study Focus"
	Focus on fiber connector types for the exam.
```

**Rendered as:** Green left border.

### Notes & Info

```markdown
!!! note "Background"
	Fiber optics transmit light pulses through glass or plastic cores.

!!! info "Additional Context"
	EMI (electromagnetic interference) is completely absent in fiber networks.
```

**Rendered as:** Purple left border.

### Warnings & Cautions

```markdown
!!! warning "Common Mistake"
	Do not confuse Cat 5 (100 Mbps) with Cat 5e (1 Gbps).

!!! caution "Plenum Code Compliance"
	Plenum-rated cable is legally required in air ducts and raised floors.
```

**Rendered as:** Orange left border.

### Danger & Pitfalls

```markdown
!!! danger "Plenum vs. PVC Cable"
	**Plenum-rated cable** (CMP) has low-smoke jacket. Standard PVC (CM) 
	produces toxic fumes when burned and is **banned in plenum spaces**.

!!! pitfall "DVI Confusion"
	DVI-D is **Digital only**; DVI-A is **Analog only**; DVI-I is **Integrated**.
```

**Rendered as:** Red left border, red title.

### Examples

```markdown
!!! example "Real-World Scenario"
	In a factory with heavy electrical machinery, you would use STP cables
	to protect network signals from EMI.
```

**Rendered as:** Cyan left border.

---

## Images

### Inline Images (Auto-Wrapped in Figure)

Images in a paragraph by themselves are automatically wrapped in a `<figure>` with optional captions:

```markdown
![UTP vs STP Shielding Cross-Section](assets/images/cables/UTP_STP.png)
```

**Rendered as:**
- Bordered image centered on the page
- No caption if only alt text provided

### Images with Captions

Use the Markdown image syntax followed by a reference or separate line:

```markdown
![RJ-45 vs RJ-11 Connectors](assets/images/cables/rj_comparisons.png)

*Optional caption text below the image.*
```

### Image Path Resolution

The renderer tries to locate images in this order:

1. **Note-relative path:** If the image source is a relative path like `../../images/cables/UTP_STP.png`, the renderer looks relative to the note's folder first.
2. **Project-root-relative path:** Falls back to the project root, so `assets/images/cables/UTP_STP.png` works.

**Best Practice:** Use project-root-relative paths for consistency:
```markdown
![Alt Text](assets/images/cables/UTP_STP.png)
```

### Image Format Support

- **PNG** (`.png`) — Recommended
- **JPEG** (`.jpg`, `.jpeg`) — Supported
- **WebP** (`.webp`) — Supported
- **GIF** (`.gif`) — Supported

**Important:** The renderer detects actual file type from file content (magic bytes), not the extension. Misnamed files will still render correctly.

### Removing Image Borders

By default, images have a subtle border. To remove it (e.g., for cutout graphics):

```markdown
![Logo](assets/images/logo.png){.bare}
```

---

## Tables

Use Markdown pipe syntax:

```markdown
| Speed | Max Distance | Frequency | Primary Use |
|-------|--------------|-----------|-------------|
| 100 Mbps | 100 m | 100 MHz | Legacy networks |
| 1 Gbps | 100 m | 100 MHz | Home/office |
| 10 Gbps | 55 m | 250 MHz | Enterprise |
```

**Rendered as:**
- Header row has a dark background and blue text
- Rows alternate slightly different backgrounds for readability
- Borders are subtle

---

## Table of Contents (Auto-Generated)

The renderer automatically generates a table of contents from your H2 and H3 headings. It appears as a card just below the note header if the note has at least 4 headings.

**Example TOC card:**
```
📑 ON THIS PAGE

• Twisted Pair Ethernet Cabling
  ◦ Cat 5
  ◦ Cat 5e (Enhanced)
• Copper Connectors & Coaxial
• Fiber Optic Cabling
  ◦ Single-Mode vs. Multi-Mode
```

Users can click these links to jump to sections.

### Controlling TOC Depth

The TOC includes H2–H3 headings by default. To adjust this (advanced):
- H2 = major sections
- H3 = subsection detail

Keep your headings to this depth for a clean TOC.

---

## Special Note Features

### Note Header Card

Every note displays a header card with:
- **Badge:** The objective number (e.g., "2.5")
- **Title:** From front matter or filename
- **Group Label:** "Core 1 · 220-1101" or "Core 2 · 220-1102"

This is auto-generated; no manual formatting needed.

### Missing Images

If an image cannot be found, a placeholder is shown instead:
```
⚠️ IMAGE MISSING
assets/images/example.png
```

Check the file path and ensure the file exists in the correct location.

---

## Styling Applied by the Renderer

### Colors & Theme

- **Background:** Dark gray (#2b2b2b)
- **Text:** Light gray (#e0e0e0)
- **Accents:** Blue (#3B82F6) for headings, green (#10B981) for tips, red (#EF4444) for dangers
- **Links:** Light blue (#7fb0ff), underlined on hover

### Typography

- **Font:** Segoe UI (Windows) or system sans-serif
- **Line Height:** 1.65 (spacious for screen reading)
- **Max Width:** 820px (centered, prevents line sprawl)

### Copy-Paste Friendly

- Code blocks are copyable; syntax highlighting is applied but does not interfere with selection
- Callouts preserve formatting when copied

---

## Practical Authoring Workflow

### Step 1: Create the File

```bash
cd assets/notes/core1
touch 2.5_network_cables_connectors.md
```

### Step 2: Add Front Matter

```markdown
---
title: Network Cables & Connectors
objective: 2.5
---
```

### Step 3: Outline Sections

```markdown
---
title: Network Cables & Connectors
objective: 2.5
---

## Major Topic 1

### Subtopic
Content goes here.

## Major Topic 2

More content.
```

### Step 4: Add Content

Use headings, lists, callouts, and images as shown above.

### Step 5: Add Images

Place images in `assets/images/<category>/`:
```bash
mkdir -p assets/images/cables
# Copy image files here
```

Reference in Markdown:
```markdown
![UTP vs STP](assets/images/cables/UTP_STP.png)
```

### Step 6: Test in App

Launch the app, go to **STUDY** → **Select Objective**, and select your note to preview live rendering.

---

## Common Patterns

### Exam Objective Overview

```markdown
---
title: BIOS & UEFI Configuration
objective: 1.1
---

## 📋 Overview
A sentence or two about why this objective matters on the exam.

---

## BIOS Basics

### What is BIOS?
...

!!! exam "Key Distinction"
	BIOS and UEFI are firmware boot environments. On modern systems, UEFI is the default.

---

## See Also
- [Other Related Note](link)
- [External Reference](link)
```

### Glossary Note

```markdown
---
title: Networking Terminology
---

## Common Abbreviations

| Abbr. | Full Form | Definition |
|-------|-----------|------------|
| EMI | Electromagnetic Interference | Signal noise from nearby electrical devices |
| STP | Shielded Twisted Pair | Twisted-pair cable with foil shielding |
| UTP | Unshielded Twisted Pair | Twisted-pair cable without shielding |
```

### Comparison Note

```markdown
---
title: Cat 5 vs Cat 5e vs Cat 6
objective: 2.5
---

## Key Differences

Cat 5
: **Speed:** 100 Mbps  
**Distance:** 100 m  
**Use:** Legacy (don't install new)

Cat 5e
: **Speed:** 1 Gbps  
**Distance:** 100 m  
**Use:** Standard for homes/offices

Cat 6
: **Speed:** 10 Gbps (55 m) / 1 Gbps (100 m)  
**Distance:** Varies  
**Use:** Enterprise backbones
```

---

## Tips for Exam-Ready Notes

1. **Use Callouts Liberally** — Highlight exam tips, common mistakes, and distinctions.
2. **Include Visuals** — Images break up text and reinforce concepts.
3. **Define Terms** — Use definition lists for glossary content.
4. **Cross-Reference** — Link to related notes or sections.
5. **Keep It Scannable** — Use short paragraphs, bullet points, and headers.
6. **Test Live** — Always preview in the app to check rendering.
7. **Emoji in Headers** — Headers can include emoji for visual interest (e.g., `## 🌐 Networking`).

---

## Limitations & Workarounds

### Unsupported Features

The note renderer uses Tkhtml3 (CSS 2.1), which does NOT support:
- ❌ Flexbox or Grid layouts
- ❌ CSS animations or transitions
- ❌ CSS `box-shadow`
- ❌ CSS variables (`var()`)
- ❌ `@media` queries
- ❌ SVG images
- ❌ Embedded video

### Workarounds

| Need | Solution |
|------|----------|
| Side-by-side layout | Use an HTML table with no visible borders |
| Shadows/visual depth | Use border colors or background contrasts |
| Responsive design | Test at common window widths; static layout is fine |
| Complex graphics | Export as PNG/JPEG and embed as image |

---

## File Checklist

Before considering a note complete:

- ✅ Front matter present with `title` and `objective`
- ✅ File named according to pattern: `[core#_]<objective>_<topic>.md`
- ✅ At least one H2 heading
- ✅ All images exist and paths are correct
- ✅ At least one callout or key concept highlighted
- ✅ Spelled and grammar-checked
- ✅ Previewed in the app and renders without missing images
- ✅ Committed to version control

---

## Questions & Troubleshooting

### Q: Why don't my images show?
**A:** Check the file path and ensure the image file exists. If the path is correct but still doesn't render, the image type may be misnamed; the renderer detects actual MIME type from file bytes, so renaming won't help—check the file itself is valid.

### Q: Can I use HTML directly in my Markdown?
**A:** Yes, the Markdown parser supports HTML blocks and inline HTML. However, only CSS 2.1 / Tkhtml3 features will render.

### Q: How do I make a note not appear in the sidebar?
**A:** Notes must have a directory (`core1`, `core2`, `general`) to be discovered. Place files outside `assets/notes/` to exclude them.

### Q: Can I modify the CSS theme?
**A:** Yes! Edit `assets/styles/notes.css` directly. Changes take effect immediately on next note render. No Python files need to be edited.

### Q: What if my objective has more than one decimal level (e.g., 3.1.2)?
**A:** The parser supports arbitrary depth. Use the full objective in front matter: `objective: "3.1.2"`.

### Q: Can I have sub-notes or nested notes?
**A:** All notes are at the same level. Use cross-references with internal links instead:
```markdown
[See Also: Network Cables](2.5_network_cables_connectors)
```

---

## Summary

The A+ Study Suite notes system is designed to be:
- **Easy to Author** — Simple Markdown with YAML front matter
- **Visually Polished** — Professional dark theme with exam-focused callouts
- **Maintainable** — CSS-driven styling, no Python changes needed
- **Print-Friendly** — Static, readable layout
- **Extensible** — Table of contents, images, code, and more

Start writing! 🚀
