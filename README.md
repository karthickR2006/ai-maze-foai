# AI-Based Maze Solver Using Breadth-First Search and Depth-First Search

**Course / Subject:** Foundations of Artificial Intelligence  
**Domain:** Uninformed Search Strategies, Problem-Solving Agents  
**Target Level:** Undergraduate Computer Science & Engineering (B.Tech / B.E. / B.Sc)  
**Technology Stack:** Python 3 (Native Standard Library), Tkinter GUI  

---

## 📌 Project Overview
This project is an interactive educational simulation designed to demonstrate the mechanics and theoretical differences between two fundamental uninformed search algorithms:
1. **Breadth-First Search (BFS)** — Explores level by level using a **FIFO Queue** and guarantees the **shortest path** in unweighted grids.
2. **Depth-First Search (DFS)** — Explores deeply using a **LIFO Stack** and demonstrates **backtracking**, often finding long, non-optimal paths.

The application allows users to build custom mazes, place obstacles, generate authentic labyrinths via Randomized DFS, animate the search process step-by-step, and benchmark both algorithms dynamically on the exact same maze.

---

## 🌟 Key Features
- **Interactive Maze Canvas:** Click to place walls, click and drag to paint walls, right-click to quick-erase, or move Start (S) and Goal (G).
- **Procedural Maze Generators:**
  - *Randomized Labyrinth (DFS):* Generates a perfect labyrinth with guaranteed paths.
  - *Random Obstacles:* Scatters walls with customizable density.
  - *Curated Presets:* Classic Academic bifurcated maze, Spiral Labyrinth, Trap Maze (no path), and Adjacent Start-Goal.
- **Visual Search Animation:**
  - Start node: Green (`#27AE60`)
  - Goal node: Red (`#E74C3C`)
  - Walls: Dark Charcoal (`#2C3E50`)
  - BFS Visited: Sky Blue (`#5DADE2`)
  - DFS Visited: Amethyst Purple (`#AF7AC5`)
  - Solution Path: Glowing Amber (`#F39C12`)
- **Dynamic Performance Comparison:**
  - Side-by-side benchmark table comparing Path Found, Path Length, Nodes Visited, Peak Frontier Memory, and CPU Execution Time (in milliseconds).
- **Zero External Dependencies:** Built entirely with Python's built-in libraries (`tkinter`, `collections.deque`, `time`, `random`). No `pip install` required!
- **Dual Execution Formats:**
  - Modular clean structure for software engineering best practices.
  - Standalone single-file version (`standalone_app.py`) for simplified college lab submission.

---

## 📁 Project Structure

```text
ai_maze_solver/
│
├── main.py              # Primary application launcher (GUI, CLI, or Test Suite)
├── bfs.py               # Pure BFS algorithm & generator for GUI animation
├── dfs.py               # Pure DFS algorithm & generator for GUI animation
├── maze.py              # 2D Grid data model, wall manipulation & maze generators
├── gui.py               # Modern Tkinter user interface & Canvas renderer
├── utils.py             # Constants, color palette, neighbor logic, path reconstruction
├── test_solver.py       # Automated test suite (8 mandatory academic test cases)
├── standalone_app.py    # All-in-one single-file version for simple submission
├── PROJECT_REPORT.md    # Complete 28-section comprehensive academic project report
├── VIVA_QUESTIONS.md    # 20 viva voce questions with concise answers
└── README.md            # Setup, instructions, and user manual
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.8 or higher installed on your system.
- Standard Tkinter support (included by default in official Python Windows/macOS installers).

### 1. Launch the Graphical Interface (Recommended)
Open a terminal / command prompt in this directory and execute:

```bash
python main.py
```
*(On Windows systems where Python 3 is mapped to `python3.14` or `py`, use `python3.14 main.py` or `py main.py`)*

### 2. Run the Terminal-Based CLI Demonstration
If you are running in an environment without a desktop display or want a quick text output:

```bash
python main.py --cli
```

### 3. Run the Automated Academic Test Suite
Verifies all 8 academic test scenarios (Normal, Trapped, Large $35\times 35$, Dense Walls, DFS vs BFS length, etc.):

```bash
python main.py --test
```
*(or run `python test_solver.py` directly)*

### 4. Run the Standalone Single-File Version
If your professor requires a single `.py` file submission:

```bash
python standalone_app.py
```

---

## 🎮 How the GUI Works

1. **Step 1: Set Up the Maze**
   - Use the **Preset** dropdown to load `"Classic Academic"`.
   - Or click **"🌀 Labyrinth (DFS)"** to generate an intricate procedural maze.
   - Or select the **"Add Wall"** radio button and drag your mouse over the canvas to draw custom walls.
   - Select **"Set Start"** or **"Set Goal"** to reposition the start and target markers.

2. **Step 2: Adjust Settings**
   - Adjust the **Speed Delay (ms)** slider to speed up or slow down the search animation.
   - Change the **Grid Size** (e.g., $15 \times 15$, $21 \times 21$, $27 \times 27$, $33 \times 33$).

3. **Step 3: Run Search Algorithms**
   - Click **"▶ Run BFS"**: Watch the sky blue frontier expand outward level-by-level until it hits the goal and illuminates the shortest path in gold.
   - Click **"▶ Run DFS"**: Watch the purple frontier plunge down branches and backtrack from dead-ends.
   - Click **"⏹ Stop Search"** if you wish to cancel an ongoing animation.

4. **Step 4: Compare BFS vs. DFS**
   - Click **"⚖ Compare BFS vs DFS"**.
   - A modal window will display a comparative breakdown comparing:
     - Path Length (BFS shortest vs DFS detour)
     - Total Nodes Explored
     - Execution Time in milliseconds
     - Memory / Frontier usage

5. **Step 5: Theoretical Review**
   - Click **"📘 About Algorithms"** to review the time and space complexity theory.
   - Click **"🎓 Project Info"** for academic syllabus and course details.

---

## 📊 Summary of Theoretical Complexity

| Property | Breadth-First Search (BFS) | Depth-First Search (DFS) |
| :--- | :--- | :--- |
| **Frontier Structure** | Queue (FIFO) | Stack (LIFO) |
| **Time Complexity** | $\mathcal{O}(V + E)$ | $\mathcal{O}(V + E)$ |
| **Space Complexity** | $\mathcal{O}(V)$ | $\mathcal{O}(V)$ |
| **Completeness** | **Yes** (Finite graphs) | **Yes** (With visited set) |
| **Optimality (Shortest Path)**| **Guaranteed Optimal** | **Not Guaranteed** |

---

## 📝 Academic Submission Documentation
- **Full Project Report (28 Sections):** Refer to [PROJECT_REPORT.md](file:///C:/Users/ASUS/.gemini/antigravity/scratch/ai_maze_solver/PROJECT_REPORT.md)
- **Viva Voce Examination Questions (20 Q&A):** Refer to [VIVA_QUESTIONS.md](file:///C:/Users/ASUS/.gemini/antigravity/scratch/ai_maze_solver/VIVA_QUESTIONS.md)
