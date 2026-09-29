"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          standalone_app.py
Description:   Complete, all-in-one, self-contained single-file version of the
               academic mini-project. Contains BFS, DFS, Maze model, GUI,
               statistics tracking, and comparative analysis in a single script.
=============================================================================
"""

import sys
import time
import random
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------------------------------------------------------
# 1. CONSTANTS & CELL TYPES
# -----------------------------------------------------------------------------
EMPTY = 0
WALL = 1
START = 2
GOAL = 3

COLOR_EMPTY = "#FFFFFF"
COLOR_WALL = "#2C3E50"
COLOR_START = "#27AE60"
COLOR_GOAL = "#E74C3C"
COLOR_VISITED_BFS = "#5DADE2"
COLOR_VISITED_DFS = "#AF7AC5"
COLOR_PATH = "#F39C12"
COLOR_GRID_LINE = "#BDC3C7"
COLOR_BG = "#ECF0F1"

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def get_neighbors(r: int, c: int, rows: int, cols: int, grid: list) -> list:
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc, rows, cols) and grid[nr][nc] != WALL:
            neighbors.append((nr, nc))
    return neighbors


def reconstruct_path(parent_dict: dict, start: tuple, goal: tuple) -> list:
    if goal not in parent_dict and start != goal:
        return []
    if start == goal:
        return [start]
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = parent_dict.get(curr)
    if path[-1] != start:
        return []
    path.reverse()
    return path


class SearchResult:
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.path_found = False
        self.path = []
        self.path_length = 0
        self.nodes_visited = 0
        self.visited_order = []
        self.execution_time = 0.0
        self.max_frontier_size = 0
        self.status_message = "Not started"


# -----------------------------------------------------------------------------
# 2. ALGORITHMS: BFS & DFS
# -----------------------------------------------------------------------------
def solve_bfs(grid: list, start: tuple, goal: tuple) -> SearchResult:
    result = SearchResult("BFS")
    rows, cols = len(grid), len(grid[0])
    if not in_bounds(start[0], start[1], rows, cols) or not in_bounds(goal[0], goal[1], rows, cols):
        result.status_message = "Start or Goal out of bounds."
        return result
    if grid[start[0]][start[1]] == WALL or grid[goal[0]][goal[1]] == WALL:
        result.status_message = "Start or Goal on a wall."
        return result

    t0 = time.perf_counter()
    if start == goal:
        result.path_found = True
        result.path = [start]
        result.execution_time = time.perf_counter() - t0
        result.status_message = "Start equals Goal."
        return result

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    order = []
    max_front = 1
    found = False

    while queue:
        if len(queue) > max_front:
            max_front = len(queue)
        curr = queue.popleft()
        order.append(curr)

        if curr == goal:
            found = True
            break

        for nbr in get_neighbors(curr[0], curr[1], rows, cols, grid):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = curr
                queue.append(nbr)

    result.execution_time = time.perf_counter() - t0
    result.nodes_visited = len(order)
    result.visited_order = order
    result.max_frontier_size = max_front

    if found:
        path = reconstruct_path(parent, start, goal)
        result.path_found = True
        result.path = path
        result.path_length = len(path) - 1
        result.status_message = f"Goal reached! Optimal path found ({result.path_length} steps)."
    else:
        result.status_message = "No path exists to the Goal."
    return result


def bfs_step_generator(grid: list, start: tuple, goal: tuple):
    rows, cols = len(grid), len(grid[0])
    result = SearchResult("BFS")
    t0 = time.perf_counter()
    if start == goal:
        result.path_found = True
        result.path = [start]
        result.execution_time = time.perf_counter() - t0
        yield ('found', [start], result)
        return

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    order = []
    max_front = 1
    found = False

    while queue:
        if len(queue) > max_front:
            max_front = len(queue)
        curr = queue.popleft()
        order.append(curr)
        yield ('visit', curr, len(order), len(queue))

        if curr == goal:
            found = True
            break

        for nbr in get_neighbors(curr[0], curr[1], rows, cols, grid):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = curr
                queue.append(nbr)

    result.execution_time = time.perf_counter() - t0
    result.nodes_visited = len(order)
    result.max_frontier_size = max_front
    if found:
        path = reconstruct_path(parent, start, goal)
        result.path_found = True
        result.path = path
        result.path_length = len(path) - 1
        yield ('found', path, result)
    else:
        yield ('not_found', result)


def solve_dfs(grid: list, start: tuple, goal: tuple) -> SearchResult:
    result = SearchResult("DFS")
    rows, cols = len(grid), len(grid[0])
    if not in_bounds(start[0], start[1], rows, cols) or not in_bounds(goal[0], goal[1], rows, cols):
        result.status_message = "Start or Goal out of bounds."
        return result
    if grid[start[0]][start[1]] == WALL or grid[goal[0]][goal[1]] == WALL:
        result.status_message = "Start or Goal on a wall."
        return result

    t0 = time.perf_counter()
    if start == goal:
        result.path_found = True
        result.path = [start]
        result.execution_time = time.perf_counter() - t0
        result.status_message = "Start equals Goal."
        return result

    stack = [start]
    visited = {start}
    parent = {start: None}
    order = []
    max_front = 1
    found = False

    while stack:
        if len(stack) > max_front:
            max_front = len(stack)
        curr = stack.pop()
        order.append(curr)

        if curr == goal:
            found = True
            break

        neighbors = get_neighbors(curr[0], curr[1], rows, cols, grid)
        for nbr in reversed(neighbors):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = curr
                stack.append(nbr)

    result.execution_time = time.perf_counter() - t0
    result.nodes_visited = len(order)
    result.visited_order = order
    result.max_frontier_size = max_front

    if found:
        path = reconstruct_path(parent, start, goal)
        result.path_found = True
        result.path = path
        result.path_length = len(path) - 1
        result.status_message = f"Goal reached! Path found ({result.path_length} steps)."
    else:
        result.status_message = "No path exists to the Goal."
    return result


def dfs_step_generator(grid: list, start: tuple, goal: tuple):
    rows, cols = len(grid), len(grid[0])
    result = SearchResult("DFS")
    t0 = time.perf_counter()
    if start == goal:
        result.path_found = True
        result.path = [start]
        result.execution_time = time.perf_counter() - t0
        yield ('found', [start], result)
        return

    stack = [start]
    visited = {start}
    parent = {start: None}
    order = []
    max_front = 1
    found = False

    while stack:
        if len(stack) > max_front:
            max_front = len(stack)
        curr = stack.pop()
        order.append(curr)
        yield ('visit', curr, len(order), len(stack))

        if curr == goal:
            found = True
            break

        neighbors = get_neighbors(curr[0], curr[1], rows, cols, grid)
        for nbr in reversed(neighbors):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = curr
                stack.append(nbr)

    result.execution_time = time.perf_counter() - t0
    result.nodes_visited = len(order)
    result.max_frontier_size = max_front
    if found:
        path = reconstruct_path(parent, start, goal)
        result.path_found = True
        result.path = path
        result.path_length = len(path) - 1
        yield ('found', path, result)
    else:
        yield ('not_found', result)


# -----------------------------------------------------------------------------
# 3. MAZE DATA MODEL
# -----------------------------------------------------------------------------
class Maze:
    def __init__(self, rows: int = 21, cols: int = 21):
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.start = (1, 1)
        self.goal = (rows - 2, cols - 2)
        self.load_preset("Classic Academic")

    def resize(self, new_rows: int, new_cols: int):
        self.rows = new_rows
        self.cols = new_cols
        self.grid = [[EMPTY for _ in range(new_cols)] for _ in range(new_rows)]
        self.start = (1, 1)
        self.goal = (new_rows - 2, new_cols - 2)
        self.load_preset("Classic Academic")

    def clear(self):
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid[self.start[0]][self.start[1]] = EMPTY
        self.grid[self.goal[0]][self.goal[1]] = EMPTY

    def reset_search(self):
        pass

    def set_start(self, r: int, c: int) -> bool:
        if not in_bounds(r, c, self.rows, self.cols) or (r, c) == self.goal or self.grid[r][c] == WALL:
            return False
        self.start = (r, c)
        return True

    def set_goal(self, r: int, c: int) -> bool:
        if not in_bounds(r, c, self.rows, self.cols) or (r, c) == self.start or self.grid[r][c] == WALL:
            return False
        self.goal = (r, c)
        return True

    def set_wall(self, r: int, c: int) -> bool:
        if not in_bounds(r, c, self.rows, self.cols) or (r, c) == self.start or (r, c) == self.goal:
            return False
        self.grid[r][c] = WALL
        return True

    def remove_wall(self, r: int, c: int) -> bool:
        if in_bounds(r, c, self.rows, self.cols) and self.grid[r][c] == WALL:
            self.grid[r][c] = EMPTY
            return True
        return False

    def generate_labyrinth(self):
        self.grid = [[WALL for _ in range(self.cols)] for _ in range(self.rows)]
        start_r, start_c = 1, 1
        self.grid[start_r][start_c] = EMPTY
        stack = [(start_r, start_c)]
        visited = {(start_r, start_c)}

        while stack:
            cr, cc = stack[-1]
            candidates = []
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = cr + dr, cc + dc
                if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                    if (nr, nc) not in visited:
                        candidates.append((nr, nc, dr // 2, dc // 2))

            if candidates:
                nr, nc, w_dr, w_dc = random.choice(candidates)
                self.grid[cr + w_dr][cc + w_dc] = EMPTY
                self.grid[nr][nc] = EMPTY
                visited.add((nr, nc))
                stack.append((nr, nc))
            else:
                stack.pop()

        self.start = (1, 1)
        self.grid[1][1] = EMPTY
        self.goal = (self.rows - 2, self.cols - 2)
        if self.grid[self.goal[0]][self.goal[1]] == WALL:
            for r in range(self.rows - 2, 0, -1):
                for c in range(self.cols - 2, 0, -1):
                    if self.grid[r][c] == EMPTY:
                        self.goal = (r, c)
                        break
                if self.grid[self.goal[0]][self.goal[1]] == EMPTY:
                    break

        extra = (self.rows * self.cols) // 18
        for _ in range(extra):
            rr = random.randint(1, self.rows - 2)
            rc = random.randint(1, self.cols - 2)
            if self.grid[rr][rc] == WALL:
                self.grid[rr][rc] = EMPTY

    def generate_random_obstacles(self, density: float = 0.28):
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (1, 1)
        self.goal = (self.rows - 2, self.cols - 2)
        for r in range(self.rows):
            self.grid[r][0] = WALL
            self.grid[r][self.cols - 1] = WALL
        for c in range(self.cols):
            self.grid[0][c] = WALL
            self.grid[self.rows - 1][c] = WALL

        protected = {self.start, self.goal, (1, 2), (2, 1), (self.rows - 2, self.cols - 3), (self.rows - 3, self.cols - 2)}
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                if (r, c) not in protected and random.random() < density:
                    self.grid[r][c] = WALL

    def load_preset(self, name: str):
        self.clear()
        for r in range(self.rows):
            self.grid[r][0] = WALL
            self.grid[r][self.cols - 1] = WALL
        for c in range(self.cols):
            self.grid[0][c] = WALL
            self.grid[self.rows - 1][c] = WALL

        self.start = (1, 1)
        self.goal = (self.rows - 2, self.cols - 2)

        if name == "Classic Academic":
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c] = WALL
            self.start = (1, 1)
            self.goal = (self.rows - 2, self.cols - 2)
            self.grid[1][1] = EMPTY
            self.grid[self.goal[0]][self.goal[1]] = EMPTY

            for r in range(1, self.rows - 1):
                self.grid[r][1] = EMPTY
            for c in range(1, self.cols - 1):
                self.grid[self.rows - 2][c] = EMPTY

            for c in range(1, self.cols - 1):
                self.grid[1][c] = EMPTY

            right_col = self.cols - 2
            left_col = max(3, self.cols // 5)
            for r in range(3, self.rows - 3, 2):
                for c in range(left_col, right_col + 1):
                    self.grid[r][c] = EMPTY
                if ((r - 3) // 2) % 2 == 0:
                    self.grid[r - 1][right_col] = EMPTY
                else:
                    self.grid[r - 1][left_col] = EMPTY
            self.grid[2][right_col] = EMPTY

            last_r = (self.rows - 4) if (self.rows - 4) % 2 == 1 else (self.rows - 5)
            end_c = left_col if ((last_r - 3) // 2) % 2 == 0 else right_col
            for r in range(last_r, self.rows - 1):
                self.grid[r][end_c] = EMPTY
            for c in range(min(end_c, self.cols - 2), max(end_c, self.cols - 2) + 1):
                self.grid[self.rows - 3][c] = EMPTY
            self.grid[self.rows - 3][self.cols - 2] = EMPTY
            self.grid[self.rows - 2][self.cols - 2] = EMPTY

        elif name == "Trap Maze (No Path)":
            gr, gc = self.goal
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = gr + dr, gc + dc
                    if in_bounds(nr, nc, self.rows, self.cols) and (nr, nc) != self.goal:
                        self.grid[nr][nc] = WALL


# -----------------------------------------------------------------------------
# 4. GUI IMPLEMENTATION
# -----------------------------------------------------------------------------
class StandaloneMazeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Maze Solver - BFS & DFS Path Finding Visualization")
        self.geometry("1180x820")
        self.minsize(980, 720)
        self.configure(bg=COLOR_BG)

        self.grid_rows = 21
        self.grid_cols = 21
        self.maze = Maze(self.grid_rows, self.grid_cols)

        self.interaction_mode = tk.StringVar(value="wall")
        self.is_running = False
        self.cancel_search = False
        self.animation_job = None
        self.active_algorithm = None
        self.search_generator = None
        self.speed_ms = tk.IntVar(value=15)
        self.visited_overlay = {}
        self.current_path = []

        self._build_header()
        self._build_main_layout()
        self._build_statusbar()

        self.canvas.bind("<Configure>", lambda e: self.draw_maze())
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)

        self.after(100, self.draw_maze)

    def _build_header(self):
        hdr = tk.Frame(self, bg="#1E293B", pady=12, padx=20)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="AI-Based Maze Solver", font=("Segoe UI", 18, "bold"), fg="#F8FAFC", bg="#1E293B").pack(anchor="w")
        tk.Label(hdr, text="Foundations of AI • Breadth-First Search (BFS) vs. Depth-First Search (DFS)", font=("Segoe UI", 10), fg="#94A3B8", bg="#1E293B").pack(anchor="w")

        btn_box = tk.Frame(hdr, bg="#1E293B")
        btn_box.place(relx=1.0, rely=0.5, anchor="e")
        tk.Button(btn_box, text="📘 About Algorithms", font=("Segoe UI", 9, "bold"), bg="#3B82F6", fg="white", relief=tk.FLAT, padx=10, pady=4, cursor="hand2", command=self.show_about_algorithms).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="🎓 Project Info", font=("Segoe UI", 9, "bold"), bg="#64748B", fg="white", relief=tk.FLAT, padx=10, pady=4, cursor="hand2", command=self.show_project_info).pack(side=tk.LEFT, padx=5)

    def _build_main_layout(self):
        main = tk.Frame(self, bg=COLOR_BG, padx=12, pady=10)
        main.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(main, bg=COLOR_BG)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        c_border = tk.Frame(left, bg="#CBD5E1", bd=2, relief=tk.SOLID)
        c_border.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(c_border, bg=COLOR_EMPTY, highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._build_legend(left)

        right = tk.Frame(main, bg=COLOR_BG, width=380)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right.pack_propagate(False)

        self._build_controls(right)
        self._build_stats(right)

    def _build_legend(self, parent):
        leg = tk.Frame(parent, bg="#FFFFFF", bd=1, relief=tk.SOLID, pady=6, padx=8)
        leg.pack(fill=tk.X, pady=(8, 0))
        items = [
            ("Start (S)", COLOR_START), ("Goal (G)", COLOR_GOAL), ("Wall (#)", COLOR_WALL),
            ("BFS Visited", COLOR_VISITED_BFS), ("DFS Visited", COLOR_VISITED_DFS),
            ("Final Path", COLOR_PATH), ("Empty", "#F1F5F9")
        ]
        for name, col in items:
            box = tk.Frame(leg, bg="#FFFFFF")
            box.pack(side=tk.LEFT, expand=True, padx=4)
            tk.Label(box, bg=col, width=2, height=1, relief=tk.SOLID, bd=1).pack(side=tk.LEFT, padx=(0, 4))
            tk.Label(box, text=name, font=("Segoe UI", 8, "bold"), bg="#FFFFFF", fg="#334155").pack(side=tk.LEFT)

    def _build_controls(self, parent):
        grp = tk.LabelFrame(parent, text="Control Panel", font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#1E293B", padx=12, pady=10, bd=1, relief=tk.SOLID)
        grp.pack(fill=tk.X, pady=(0, 10))

        tk.Label(grp, text="1. Run Algorithms", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#475569").pack(anchor="w", pady=(0, 4))
        r_frame = tk.Frame(grp, bg="#FFFFFF")
        r_frame.pack(fill=tk.X, pady=(0, 6))

        self.btn_bfs = tk.Button(r_frame, text="▶ Run BFS", font=("Segoe UI", 9, "bold"), bg="#0284C7", fg="white", relief=tk.FLAT, pady=6, cursor="hand2", command=lambda: self.start_search("BFS"))
        self.btn_bfs.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_dfs = tk.Button(r_frame, text="▶ Run DFS", font=("Segoe UI", 9, "bold"), bg="#7C3AED", fg="white", relief=tk.FLAT, pady=6, cursor="hand2", command=lambda: self.start_search("DFS"))
        self.btn_dfs.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

        self.btn_compare = tk.Button(grp, text="⚖ Compare BFS vs DFS", font=("Segoe UI", 9, "bold"), bg="#059669", fg="white", relief=tk.FLAT, pady=6, cursor="hand2", command=self.run_comparison)
        self.btn_compare.pack(fill=tk.X, pady=(0, 6))

        self.btn_stop = tk.Button(grp, text="⏹ Stop Search", font=("Segoe UI", 9, "bold"), bg="#DC2626", fg="white", relief=tk.FLAT, pady=4, cursor="hand2", state=tk.DISABLED, command=self.stop_search)
        self.btn_stop.pack(fill=tk.X, pady=(0, 10))

        tk.Label(grp, text="2. Mouse Edit Mode", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#475569").pack(anchor="w", pady=(0, 4))
        m_frame = tk.Frame(grp, bg="#FFFFFF")
        m_frame.pack(fill=tk.X, pady=(0, 10))
        for idx, (label, mode_val) in enumerate([("Add Wall", "wall"), ("Erase Wall", "erase"), ("Set Start", "start"), ("Set Goal", "goal")]):
            tk.Radiobutton(m_frame, text=label, variable=self.interaction_mode, value=mode_val, font=("Segoe UI", 8), bg="#FFFFFF", selectcolor="#E2E8F0").grid(row=idx // 2, column=idx % 2, sticky="w", padx=4, pady=2)

        tk.Label(grp, text="3. Maze Management", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#475569").pack(anchor="w", pady=(0, 4))
        g_frame = tk.Frame(grp, bg="#FFFFFF")
        g_frame.pack(fill=tk.X, pady=(0, 6))
        self.btn_gen_dfs = tk.Button(g_frame, text="🌀 Labyrinth (DFS)", font=("Segoe UI", 8, "bold"), bg="#475569", fg="white", relief=tk.FLAT, pady=4, cursor="hand2", command=self.generate_labyrinth)
        self.btn_gen_dfs.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        self.btn_gen_random = tk.Button(g_frame, text="🎲 Random Walls", font=("Segoe UI", 8, "bold"), bg="#475569", fg="white", relief=tk.FLAT, pady=4, cursor="hand2", command=self.generate_random)
        self.btn_gen_random.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        p_frame = tk.Frame(grp, bg="#FFFFFF")
        p_frame.pack(fill=tk.X, pady=(0, 6))
        tk.Label(p_frame, text="Preset:", font=("Segoe UI", 8), bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 4))
        self.preset_combo = ttk.Combobox(p_frame, values=["Classic Academic", "Trap Maze (No Path)"], state="readonly", font=("Segoe UI", 8))
        self.preset_combo.current(0)
        self.preset_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_select)

        clr_frame = tk.Frame(grp, bg="#FFFFFF")
        clr_frame.pack(fill=tk.X, pady=(0, 10))
        self.btn_reset = tk.Button(clr_frame, text="🔄 Reset Search", font=("Segoe UI", 8, "bold"), bg="#E2E8F0", fg="#1E293B", relief=tk.FLAT, pady=4, cursor="hand2", command=self.reset_search_state)
        self.btn_reset.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        self.btn_clear = tk.Button(clr_frame, text="🗑 Clear Maze", font=("Segoe UI", 8, "bold"), bg="#E2E8F0", fg="#DC2626", relief=tk.FLAT, pady=4, cursor="hand2", command=self.clear_maze)
        self.btn_clear.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        tk.Label(grp, text="4. Animation Speed", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#475569").pack(anchor="w", pady=(0, 2))
        s_frame = tk.Frame(grp, bg="#FFFFFF")
        s_frame.pack(fill=tk.X)
        tk.Label(s_frame, text="Delay (ms):", font=("Segoe UI", 8), bg="#FFFFFF").pack(side=tk.LEFT)
        tk.Scale(s_frame, from_=1, to=80, orient=tk.HORIZONTAL, variable=self.speed_ms, bg="#FFFFFF", highlightthickness=0, length=160).pack(side=tk.RIGHT)

    def _build_stats(self, parent):
        grp = tk.LabelFrame(parent, text="Search Statistics", font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#1E293B", padx=12, pady=10, bd=1, relief=tk.SOLID)
        grp.pack(fill=tk.BOTH, expand=True)

        self.stat_labels = {}
        for text_lbl, def_val in [
            ("Algorithm Used:", "None"), ("Search Status:", "Ready"), ("Path Found:", "--"),
            ("Path Length (Edges):", "0"), ("Nodes Visited:", "0"), ("Frontier Peak:", "0"),
            ("Execution Time:", "0.000 ms")
        ]:
            r = tk.Frame(grp, bg="#FFFFFF", pady=3)
            r.pack(fill=tk.X)
            tk.Label(r, text=text_lbl, font=("Segoe UI", 9), bg="#FFFFFF", fg="#64748B").pack(side=tk.LEFT)
            val = tk.Label(r, text=def_val, font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#0284C7" if text_lbl == "Search Status:" else "#0F172A")
            val.pack(side=tk.RIGHT)
            self.stat_labels[text_lbl] = val

    def _build_statusbar(self):
        self.status_bar = tk.Label(self, text="Ready. Click Run BFS or DFS to begin search.", font=("Segoe UI", 9), bg="#E2E8F0", fg="#334155", anchor="w", padx=12, pady=4)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def draw_maze(self, overlay=None, path=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return
        margin = 15
        cell_size = min((w - 2 * margin) / self.maze.cols, (h - 2 * margin) / self.maze.rows)
        start_x = (w - cell_size * self.maze.cols) / 2
        start_y = (h - cell_size * self.maze.rows) / 2
        self.cell_size = cell_size
        self.start_x = start_x
        self.start_y = start_y

        overlay = overlay or {}
        path_set = set(path) if path else set()

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                x1, y1 = start_x + c * cell_size, start_y + r * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                if (r, c) == self.maze.start:
                    col = COLOR_START
                elif (r, c) == self.maze.goal:
                    col = COLOR_GOAL
                elif (r, c) in path_set:
                    col = COLOR_PATH
                elif (r, c) in overlay:
                    col = overlay[(r, c)]
                elif self.maze.grid[r][c] == WALL:
                    col = COLOR_WALL
                else:
                    col = COLOR_EMPTY

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=col, outline=COLOR_GRID_LINE, width=1)
                if (r, c) == self.maze.start:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="S", font=("Segoe UI", max(8, int(cell_size * 0.45)), "bold"), fill="#FFFFFF")
                elif (r, c) == self.maze.goal:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="G", font=("Segoe UI", max(8, int(cell_size * 0.45)), "bold"), fill="#FFFFFF")

    def _coords_to_grid(self, ex, ey):
        if not hasattr(self, 'cell_size') or self.cell_size <= 0:
            return None, None
        c = int((ex - self.start_x) // self.cell_size)
        r = int((ey - self.start_y) // self.cell_size)
        return (r, c) if in_bounds(r, c, self.maze.rows, self.maze.cols) else (None, None)

    def on_canvas_click(self, e):
        if self.is_running:
            return
        r, c = self._coords_to_grid(e.x, e.y)
        if r is not None:
            self._apply_action(r, c)

    def on_canvas_drag(self, e):
        if self.is_running:
            return
        r, c = self._coords_to_grid(e.x, e.y)
        if r is not None and self.interaction_mode.get() in ("wall", "erase"):
            self._apply_action(r, c)

    def on_canvas_right_click(self, e):
        if self.is_running:
            return
        r, c = self._coords_to_grid(e.x, e.y)
        if r is not None:
            self.maze.remove_wall(r, c)
            self.draw_maze()

    def _apply_action(self, r, c):
        m = self.interaction_mode.get()
        if m == "wall":
            self.maze.set_wall(r, c)
        elif m == "erase":
            self.maze.remove_wall(r, c)
        elif m == "start":
            self.maze.set_start(r, c)
        elif m == "goal":
            self.maze.set_goal(r, c)
        self.draw_maze()

    def start_search(self, algo: str):
        if self.is_running:
            return
        self.is_running = True
        self.cancel_search = False
        self.active_algorithm = algo
        self.visited_overlay = {}
        self.current_path = []
        self.draw_maze()
        self.btn_stop.config(state=tk.NORMAL)
        self.stat_labels["Algorithm Used:"].config(text=algo)
        self.stat_labels["Search Status:"].config(text=f"Running {algo}...", fg="#0284C7")

        if algo == "BFS":
            self.search_generator = bfs_step_generator(self.maze.grid, self.maze.start, self.maze.goal)
        else:
            self.search_generator = dfs_step_generator(self.maze.grid, self.maze.start, self.maze.goal)
        self._anim_step()

    def _anim_step(self):
        if not self.is_running or self.cancel_search:
            self._finish_search(None, cancelled=True)
            return

        delay = self.speed_ms.get()
        steps = 6 if delay <= 5 else (2 if delay <= 15 else 1)
        col = COLOR_VISITED_BFS if self.active_algorithm == "BFS" else COLOR_VISITED_DFS

        for _ in range(steps):
            try:
                ev = next(self.search_generator)
            except StopIteration:
                self._finish_search(None)
                return

            if ev[0] == "visit":
                node, cnt, fr = ev[1], ev[2], ev[3]
                if node != self.maze.start and node != self.maze.goal:
                    self.visited_overlay[node] = col
                self.stat_labels["Nodes Visited:"].config(text=str(cnt))
                self.stat_labels["Frontier Peak:"].config(text=str(fr))
            elif ev[0] == "found":
                path, res = ev[1], ev[2]
                self._trace_path(path, res)
                return
            elif ev[0] == "not_found":
                self._finish_search(ev[1])
                return

        self.draw_maze(self.visited_overlay)
        self.animation_job = self.after(delay, self._anim_step)

    def _trace_path(self, path, res):
        idx = 0
        p_prog = []
        def step():
            nonlocal idx
            if not self.is_running or self.cancel_search:
                self._finish_search(res)
                return
            if idx < len(path):
                n = path[idx]
                if n != self.maze.start and n != self.maze.goal:
                    p_prog.append(n)
                idx += 1
                self.draw_maze(self.visited_overlay, p_prog)
                self.after(20, step)
            else:
                self._finish_search(res)
        step()

    def _finish_search(self, res, cancelled=False):
        self.is_running = False
        self.btn_stop.config(state=tk.DISABLED)
        if cancelled:
            self.stat_labels["Search Status:"].config(text="Stopped", fg="#DC2626")
            return
        if res and res.path_found:
            self.stat_labels["Search Status:"].config(text="Goal Reached!", fg="#059669")
            self.stat_labels["Path Found:"].config(text="Yes", fg="#059669")
            self.stat_labels["Path Length (Edges):"].config(text=str(res.path_length))
            self.stat_labels["Execution Time:"].config(text=f"{res.execution_time*1000:.3f} ms")
            self.draw_maze(self.visited_overlay, res.path)
        else:
            self.stat_labels["Search Status:"].config(text="No Path!", fg="#DC2626")
            self.stat_labels["Path Found:"].config(text="No", fg="#DC2626")
            messagebox.showinfo("Result", "No path exists between Start and Goal!")

    def stop_search(self):
        self.cancel_search = True

    def run_comparison(self):
        b = solve_bfs(self.maze.grid, self.maze.start, self.maze.goal)
        d = solve_dfs(self.maze.grid, self.maze.start, self.maze.goal)
        msg = (
            f"=== BFS vs DFS Comparison ===\n\n"
            f"Path Found:   BFS={b.path_found}  |  DFS={d.path_found}\n"
            f"Path Length:  BFS={b.path_length} (Optimal) |  DFS={d.path_length}\n"
            f"Nodes Visited: BFS={b.nodes_visited} |  DFS={d.nodes_visited}\n"
            f"Execution Time: BFS={b.execution_time*1000:.3f} ms | DFS={d.execution_time*1000:.3f} ms\n\n"
            f"Key Principle: BFS guarantees shortest path in unweighted graphs."
        )
        messagebox.showinfo("BFS vs DFS Comparison", msg)

    def generate_labyrinth(self):
        self.maze.generate_labyrinth()
        self.reset_search_state()

    def generate_random(self):
        self.maze.generate_random_obstacles()
        self.reset_search_state()

    def on_preset_select(self, e=None):
        self.maze.load_preset(self.preset_combo.get())
        self.reset_search_state()

    def reset_search_state(self):
        self.visited_overlay = {}
        self.draw_maze()
        self.stat_labels["Search Status:"].config(text="Ready")
        self.stat_labels["Path Found:"].config(text="--")

    def clear_maze(self):
        self.maze.clear()
        self.reset_search_state()

    def show_about_algorithms(self):
        messagebox.showinfo(
            "About Search Algorithms",
            "Breadth-First Search (BFS):\n"
            "• Explores level-by-level using a FIFO Queue.\n"
            "• Optimal: Always finds the shortest path.\n\n"
            "Depth-First Search (DFS):\n"
            "• Explores deeply using a LIFO Stack.\n"
            "• Non-optimal: May find longer detours."
        )

    def show_project_info(self):
        messagebox.showinfo(
            "Project Info",
            "AI-Based Maze Solver Using BFS & DFS\n"
            "Domain: Foundations of Artificial Intelligence\n"
            "Technology: Python 3 + Pure Tkinter\n"
            "Academic Mini Project"
        )


if __name__ == "__main__":
    app = StandaloneMazeApp()
    app.mainloop()
