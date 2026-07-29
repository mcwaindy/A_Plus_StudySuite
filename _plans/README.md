# 📋 Planning & Reference Documents

This directory contains planning documents, guides, and archived project information.

## 📖 Essential Reading

### For Creating Study Notes
**→ Start here:** [`MARKDOWN_AUTHORING_GUIDE.md`](MARKDOWN_AUTHORING_GUIDE.md)

Complete guide for writing notes including:
- File organization and naming conventions
- YAML front matter (title, objective)
- Markdown formatting reference (headings, lists, tables, code)
- Callout/admonition types with color-coded styling
- Image embedding and path resolution
- CSS theming and styling
- Practical workflow and examples
- Troubleshooting FAQ

### For Understanding the Architecture
**→ Technical reference:** [`notes_refinement_7.29.26.md`](notes_refinement_7.29.26.md)

Details about the notes rendering backend:
- How Markdown is converted to HTML
- Image discovery and base64 embedding
- MIME-type detection from file content
- Markdown extensions enabled
- CSS file location and customization

---

## 📚 Reference Documents

### Project Archive
**File:** [`PROJECT_ARCHIVE.md`](PROJECT_ARCHIVE.md)

Comprehensive summary of all completed phases:
- **Phase 1:** Project architecture & data schema ✅
- **Phase 2:** Navigation shell & core app ✅
- **Phase 3:** Study modules (notes, flashcards, motherboard) ✅
- **Phase 3.1:** Image rendering fix ✅
- **Phase 4:** Practice suite (upcoming)

Also includes:
- Repository structure overview
- Key lessons learned
- Getting started instructions
- Historical timeline

### Cleanup Summary
**File:** [`CLEANUP_SUMMARY.md`](CLEANUP_SUMMARY.md)

Record of workspace cleanup (7/29/2026):
- Files removed (debug scripts, obsolete docs)
- Files created (new guides, archive)
- Before/after workspace comparison
- Going-forward recommendations

---

## 🎮 Feature Development

### Hardware Game
**File:** [`hardware_game_building_instructions.md`](hardware_game_building_instructions.md)

Instructions for implementing the hardware identification game feature.

### Motherboard Diagram
**File:** [`coordinates_motherboard_instructions.md`](coordinates_motherboard_instructions.md)

Instructions for configuring motherboard diagram hotspots and component coordinates.

---

## 🗂️ Organization

Documents are organized by purpose:

| Document | Purpose | Audience |
|----------|---------|----------|
| `MARKDOWN_AUTHORING_GUIDE.md` | Writing study notes | Content creators |
| `notes_refinement_7.29.26.md` | Architecture reference | Developers |
| `PROJECT_ARCHIVE.md` | Project history & status | Everyone |
| `CLEANUP_SUMMARY.md` | Repository maintenance | Maintainers |
| `hardware_game_building_instructions.md` | Feature development | Developers |
| `coordinates_motherboard_instructions.md` | Feature development | Developers |

---

## 🚀 Quick Start

**I want to...**

→ **Create a study note**  
1. Read `MARKDOWN_AUTHORING_GUIDE.md`
2. Create a `.md` file in `assets/notes/core1/`, `assets/notes/core2/`, or `assets/notes/general/`
3. Add front matter (title, objective)
4. Write content using Markdown
5. Test in the app

→ **Understand how notes render**  
1. Read `notes_refinement_7.29.26.md` for technical details
2. Check `assets/styles/notes.css` for styling

→ **See what's been done & what's next**  
1. Read `PROJECT_ARCHIVE.md` for phase completion status
2. Review `CLEANUP_SUMMARY.md` for recent changes

→ **Build a new feature (game, exams)**  
1. Check `PROJECT_ARCHIVE.md` for Phase 4 roadmap
2. Read relevant feature doc (`hardware_game_building_instructions.md`, etc.)

---

## 📝 Contributing

When adding new plans or documentation:

1. **Use clear filenames** — Indicate purpose and date if applicable
2. **Add a summary line** — First line should describe what the document contains
3. **Keep it up-to-date** — Archive docs when phase completes; move old docs to `PROJECT_ARCHIVE.md`
4. **Reference actively** — Link between related documents for easy navigation
5. **Maintain structure** — Keep planning docs in `_plans/`, never in root

---

## ✨ Last Updated

- **Cleanup:** 7/29/2026 (removed debug scripts, archived old plans)
- **Authoring Guide:** 7/29/2026 (new)
- **Project Archive:** 7/29/2026 (new)
- **Notes Architecture:** 7/29/2026 (current)

---

**Questions?** Check the relevant document above or review the codebase in `modules/` and `assets/`.
