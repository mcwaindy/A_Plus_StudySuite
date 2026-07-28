ApExamPrep/
│
├── assets/                  # All media files
│   ├── images/              # Hardware photos, diagrams
│   │   ├── motherboard_modern.jpg
│   │   ├── motherboard_old.jpg
│   │   ├── pcie_x16.png
│   │   └── rj45_cable.png
│   └── notes/               # Objective notes (.txt or .md files)
│       ├── core1_1.2_slots.md
│       └── core1_2.1_ports.md
│
├── data/                    # JSON data stores
│   ├── flashcards.json
│   ├── questions.json
│   └── motherboard_nodes.json
│
├── modules/                 # Python logic files (we'll build these later)
│   ├── __init__.py
│   ├── flashcards_view.py
│   ├── quiz_view.py
│   └── diagram_view.py
│
├── main.py                  # Entry point for your application
└── requirements.txt         # Package dependencies (customtkinter, Pillow)