# Documentation Index

Welcome to the A+ Study Suite! This is your guide to the project's documentation.

## 📖 Start Here

### [README.md](README.md)
**Project Overview & Architecture**  
Start here to understand what this project does and how it's structured.
- Project overview
- Core features
- Application architecture
- Running the application

### [STRUCTURE.md](STRUCTURE.md)
**Project Directory Organization**  
Visual guide to how files and directories are organized.
- Complete directory tree
- File categorization
- Quick reference map

## 🛠️ Development

### [DEVELOPMENT.md](DEVELOPMENT.md)
**Developer Setup & Guide**  
For developers who want to understand and extend the codebase.
- Project setup instructions
- Development workflow
- Adding new features
- Core systems explanation
- Code style guidelines
- Testing procedures
- Common issues & solutions

### [COORDINATE_PICKER_GUIDE.md](COORDINATE_PICKER_GUIDE.md)
**Motherboard Coordinate Picker Tool**  
Documentation for the standalone tool used to edit motherboard hotspots.
- Tool overview and launching
- User interface walkthrough
- Component editing workflow
- Display scale tuning
- Technical details
- Troubleshooting

## 📊 Data

### [DATA_SCHEMA.md](DATA_SCHEMA.md)
**Data Structure & Format Reference**  
Complete reference for all data file formats used in the application.
- Motherboard registry schema
- Image catalog format
- Flashcard structure
- Exam question format
- Validation rules
- Tips for adding data

## 📋 Project Reference

### [CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)
**Recent Cleanup & Reorganization**  
Summary of recent cleanup operations and project reorganization.
- Files removed and why
- Documentation created
- Improvements made
- Statistics

---

## Quick Navigation

**I want to...**
- 🎯 **Understand the overall project** → [README.md](README.md)
- 🏗️ **See the directory structure** → [STRUCTURE.md](STRUCTURE.md)
- 💻 **Set up development environment** → [DEVELOPMENT.md](DEVELOPMENT.md)
- 🔧 **Edit motherboard hotspots** → [COORDINATE_PICKER_GUIDE.md](COORDINATE_PICKER_GUIDE.md)
- 📝 **Add new quiz data** → [DATA_SCHEMA.md](DATA_SCHEMA.md)

---

## Project Statistics

| Metric | Value |
|--------|-------|
| **Production Python Files** | 12 |
| **Data Files** | 4 JSON files |
| **Image Categories** | 15+ |
| **Documentation Files** | 6 markdown files |
| **Total Asset Directories** | 18+ |

---

## File Locations at a Glance

```
main.py                          ← Start here to run the app
├── docs/
│   ├── INDEX.md                 ← You are here
│   ├── README.md                ← Project overview
│   ├── STRUCTURE.md             ← Directory layout
│   ├── DEVELOPMENT.md           ← Developer guide
│   ├── COORDINATE_PICKER_GUIDE.md
│   ├── DATA_SCHEMA.md
│   └── CLEANUP_SUMMARY.md
├── modules/                     ← Application screens
├── tools/                       ← Standalone utilities
├── utils/                       ← Shared code
├── data/                        ← Quiz and board data
├── assets/                      ← Images and styles
└── requirements.txt             ← Dependencies
```

---

## Key Features Overview

**Motherboard Diagram Viewer**  
Interactive display of computer motherboards with clickable hotspots for learning component locations.

**Hardware Identification Game**  
Quiz game where you identify computer components and learn their functions.

**Coordinate Picker Tool**  
Standalone utility for defining clickable regions on motherboard images.

**Study Suite**  
- Flashcards for memorization
- Exam simulations
- Study notes repository
- Custom exam builder

---

## Getting Started

### First Time Users
1. Read [README.md](README.md) for project overview
2. See [STRUCTURE.md](STRUCTURE.md) to understand organization
3. Run the application: `python main.py`

### For Developers
1. Start with [DEVELOPMENT.md](DEVELOPMENT.md)
2. Review [STRUCTURE.md](STRUCTURE.md) to understand file layout
3. Check [DATA_SCHEMA.md](DATA_SCHEMA.md) if you're working with data

### For Content Creators
1. Read [DATA_SCHEMA.md](DATA_SCHEMA.md) for data formats
2. Use [COORDINATE_PICKER_GUIDE.md](COORDINATE_PICKER_GUIDE.md) for board editing
3. Follow the guides for adding new quiz items

---

## Support & Help

Each documentation file is self-contained and includes:
- ✓ Clear examples
- ✓ Troubleshooting sections
- ✓ Related file references
- ✓ Quick start guides

**Having issues?**
- Check the relevant documentation's troubleshooting section
- Review [DEVELOPMENT.md](DEVELOPMENT.md) → "Common Issues & Solutions"
- Check file compilation: `python -m py_compile <filename>`

---

**Last Updated**: During cleanup and reorganization  
**Branch**: ui_refinement  
**Status**: ✅ Production Ready
