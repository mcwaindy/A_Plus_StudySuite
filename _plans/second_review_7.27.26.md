Here is a comprehensive summary of everything accomplished so far, along with a detailed roadmap for the upcoming phases based on your **A+ Study Program Development Discussion** document.

---

# 📚 CompTIA A+ Study Suite — Project Summary & Roadmap

## 🚀 Accomplishments So Far

### **Phase 1: Project Architecture & Data Schema**

* **Directory Structure:** Established a modular layout including `assets/` (images, notes), `data/` (JSON stores), and `modules/` (Python views).


* **JSON Schemas:** Defined and created core databases:
* `data/flashcards.json` for term/definition review with objective tagging.


* `data/questions.json` for custom/full practice exams.


* `data/motherboard_nodes.json` for interactive diagram hotspot coordinates.




* **Data Verification:** Confirmed environment data loading using `Path` and `json.load`.



### **Phase 2: Core Application & Navigation Architecture**

* **Single-Window Frame Swapper:** Implemented `App(ctk.CTk)` in `main.py` using Object-Oriented Programming (OOP).


* **Responsive Layout:** Constructed a persistent left sidebar paired with a main content frame utilizing `grid_columnconfigure` and `sticky="nsew"` for responsive window resizing.


* **Dynamic Frame Switching:** Created `switch_frame()` to destroy old view instances and instantiate new ones smoothly without memory leaks.



### **Phase 3: Core Study Modules (In Progress)**

* **Flashcards Engine (`modules/flashcards_view.py`):**
* Built interactive card flipping, start-side toggling (*Term* vs. *Definition*), and mastery tracking (*Mastered* vs. *Needs Review*).


* Resolved initialization order bugs so all UI components instantiate before state updates occur.




* **Notes Viewer (`modules/notes_view.py`):**
* Created an objective dropdown (`CTkOptionMenu`) and a scrollable content area (`CTkScrollableFrame`).


* Upgraded from `.txt` to `.md` (Markdown) parsing to support rich text formatting (headings, bold text, bullet points) generated from Microsoft Word or raw Markdown.





---

## 🗺️ Next Steps & Development Roadmap

```
Phase 3 Completion (Motherboard Diagram) 
       │
       ▼
Phase 4: Practice Exam Suite (Full, Custom, Hardware Game) 
       │
       ▼
Phase 5: Performance Tracking & Refinements

```

### 1. **Complete Phase 3: Interactive Motherboard Diagram (`1.c`)**

* **Goal:** Load `motherboard_modern.jpg` and display clickable hotspot overlays based on coordinate data in `motherboard_nodes.json`.


* **Key Features:**
* Render motherboard images dynamically using `Pillow` (`PIL.ImageTk`).


* Overlay bounding boxes or clickable nodes (e.g., LGA 1700 CPU Socket, DDR5 RAM Slots).


* Display a detailed component summary panel when a hotspot is clicked.





---

### 2. **Phase 4: Practice & Exam Engines**

* **`2.a` Full Exam Mode (`modules/quiz_view.py`):**

* Load questions from `data/questions.json`.


* Implement multiple-choice selection, question navigation (Next/Previous), and instant answer validation with explanations.




* **`2.b` Custom Objective Exams:**

* Allow users to filter practice questions by specific CompTIA A+ objectives (e.g., only Core 1 Objective 1.2).




* **`2.c` Hardware Guessing Game:**

* A visual guessing game displaying hardware images (`assets/images/`) and prompting the user to identify components against a timer or score counter.





---

### 3. **Phase 5: Data Persistence & Polishing**

* **Progress Tracking:** Save user mastery metrics, exam scores, and weak objectives locally (e.g., `data/user_stats.json`).
* **UI Polish:** Add custom accent colors, icon support, and keyboard shortcuts for rapid flashcard flipping (e.g., Spacebar to flip, Arrow keys to navigate).

---

# 📌 Document Addendum: Inline Image Rendering in Notes Viewer

## 🛠️ Design Consideration: Multimedia Notes Engine
**Issue:** CompTIA A+ notes require visual aids (e.g., RJ-45 connector pinouts, motherboard socket types, cable heads) embedded directly alongside text notes. Standard CustomTkinter text widgets or simple text labels do not parse and display inline images automatically when reading `.md` files.

---

## 🎯 Proposed Solutions & Architectural Approaches

### **Option 1: Custom Markdown Image Parser (Pillow + CustomTkinter)**
Extend `render_markdown()` in `modules/notes_view.py` to detect standard Markdown image syntax (`![Alt Text](path/to/image.png)`) and dynamically render images as `CTkLabel` or `CTkImage` widgets.

* **Markdown Syntax Example:**
  ```markdown
  ### Connectors
  * **RJ-45:** 8-position connector used for Ethernet.
  
  ![RJ45 Pinout Diagram](assets/images/rj45_cable.png)