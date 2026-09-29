"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          gui.py
Description:   Interactive graphical user interface built with Tkinter.
               Provides real-time visualization of BFS and DFS search processes,
               interactive maze editing, algorithmic performance statistics,
               and dynamic comparison dialogs.
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time

from utils import (
    EMPTY, WALL, START, GOAL, VISITED_BFS, VISITED_DFS, PATH,
    COLOR_EMPTY, COLOR_WALL, COLOR_START, COLOR_GOAL,
    COLOR_VISITED_BFS, COLOR_VISITED_DFS, COLOR_PATH, COLOR_CURRENT,
    COLOR_GRID_LINE, COLOR_BG, SearchResult
)
from maze import Maze
from bfs import solve_bfs, bfs_step_generator
from dfs import solve_dfs, dfs_step_generator


class MazeApp(tk.Tk):
    """
    Main Tkinter application window for the AI Maze Solver.
    """

    def __init__(self):
        super().__init__()

        self.title("AI Maze Solver - BFS & DFS Path Finding Visualization")
        self.geometry("1180x820")
        self.minsize(980, 720)
        self.configure(bg=COLOR_BG)

        # Initialize Maze model (default 21x21)
        self.grid_rows = 21
        self.grid_cols = 21
        self.maze = Maze(self.grid_rows, self.grid_cols)

        # Mouse interaction modes: 'wall', 'erase', 'start', 'goal'
        self.interaction_mode = tk.StringVar(value="wall")

        # Animation state
        self.is_running = False
        self.cancel_search = False
        self.animation_job = None
        self.active_algorithm = None
        self.search_generator = None

        # Speed slider: delay in milliseconds per animation step
        self.speed_ms = tk.IntVar(value=15)

        # Last search results for comparison
        self.last_bfs_result = None
        self.last_dfs_result = None

        # Build GUI Components
        self._build_header()
        self._build_main_layout()
        self._build_statusbar()

        # Canvas rendering bindings
        self.canvas.bind("<Configure>", lambda e: self.draw_maze())
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)  # Right click to quick erase

        # Initial render
        self.after(100, self.draw_maze)

    # -------------------------------------------------------------------------
    # UI Building Blocks
    # -------------------------------------------------------------------------
    def _build_header(self):
        """Build the top banner and title area."""
        header_frame = tk.Frame(self, bg="#1E293B", pady=12, padx=20)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="AI-Based Maze Solver",
            font=("Segoe UI", 18, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Foundations of Artificial Intelligence • Breadth-First Search (BFS) vs. Depth-First Search (DFS) Visualization",
            font=("Segoe UI", 10),
            fg="#94A3B8",
            bg="#1E293B"
        )
        subtitle_label.pack(anchor="w")

        # Top-right quick actions
        btn_box = tk.Frame(header_frame, bg="#1E293B")
        btn_box.place(relx=1.0, rely=0.5, anchor="e")

        about_btn = tk.Button(
            btn_box,
            text="📘 About Algorithms",
            font=("Segoe UI", 9, "bold"),
            bg="#3B82F6",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.show_about_algorithms
        )
        about_btn.pack(side=tk.LEFT, padx=5)

        info_btn = tk.Button(
            btn_box,
            text="🎓 Project Info",
            font=("Segoe UI", 9, "bold"),
            bg="#64748B",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.show_project_info
        )
        info_btn.pack(side=tk.LEFT, padx=5)

    def _build_main_layout(self):
        """Construct the split-pane: Canvas on Left, Controls & Stats on Right."""
        main_frame = tk.Frame(self, bg=COLOR_BG, padx=12, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Container: Canvas and interactive legend
        left_container = tk.Frame(main_frame, bg=COLOR_BG)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Canvas Frame with a neat border
        canvas_border = tk.Frame(left_container, bg="#CBD5E1", bd=2, relief=tk.SOLID)
        canvas_border.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_border,
            bg=COLOR_EMPTY,
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Legend Bar below canvas
        self._build_legend(left_container)

        # Right Container: Control Panel & Statistics Panel
        right_container = tk.Frame(main_frame, bg=COLOR_BG, width=380)
        right_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_container.pack_propagate(False)

        self._build_control_panel(right_container)
        self._build_stats_panel(right_container)

    def _build_legend(self, parent):
        """Visual color legend explaining cell states."""
        legend_frame = tk.Frame(parent, bg="#FFFFFF", bd=1, relief=tk.SOLID, pady=6, padx=8)
        legend_frame.pack(fill=tk.X, pady=(8, 0))

        items = [
            ("Start (S)", COLOR_START),
            ("Goal (G)", COLOR_GOAL),
            ("Wall (#)", COLOR_WALL),
            ("BFS Visited", COLOR_VISITED_BFS),
            ("DFS Visited", COLOR_VISITED_DFS),
            ("Final Path", COLOR_PATH),
            ("Empty (.)", "#F1F5F9"),
        ]

        for label_text, color in items:
            box = tk.Frame(legend_frame, bg="#FFFFFF")
            box.pack(side=tk.LEFT, expand=True, padx=4)

            swatch = tk.Label(box, bg=color, width=2, height=1, relief=tk.SOLID, bd=1)
            swatch.pack(side=tk.LEFT, padx=(0, 4))

            lbl = tk.Label(box, text=label_text, font=("Segoe UI", 8, "bold"), bg="#FFFFFF", fg="#334155")
            lbl.pack(side=tk.LEFT)

    def _build_control_panel(self, parent):
        """Build controls: algorithm runners, maze generators, and edit tools."""
        controls_group = tk.LabelFrame(
            parent,
            text="Control Panel",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=12,
            pady=10,
            bd=1,
            relief=tk.SOLID
        )
        controls_group.pack(fill=tk.X, pady=(0, 10))

        # --- Section 1: Algorithm Execution ---
        algo_title = tk.Label(
            controls_group,
            text="1. Run Algorithms",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#475569"
        )
        algo_title.pack(anchor="w", pady=(0, 4))

        run_btn_frame = tk.Frame(controls_group, bg="#FFFFFF")
        run_btn_frame.pack(fill=tk.X, pady=(0, 6))

        self.btn_bfs = tk.Button(
            run_btn_frame,
            text="▶ Run BFS",
            font=("Segoe UI", 9, "bold"),
            bg="#0284C7",
            fg="white",
            relief=tk.FLAT,
            pady=6,
            cursor="hand2",
            command=lambda: self.start_search("BFS")
        )
        self.btn_bfs.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_dfs = tk.Button(
            run_btn_frame,
            text="▶ Run DFS",
            font=("Segoe UI", 9, "bold"),
            bg="#7C3AED",
            fg="white",
            relief=tk.FLAT,
            pady=6,
            cursor="hand2",
            command=lambda: self.start_search("DFS")
        )
        self.btn_dfs.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

        self.btn_compare = tk.Button(
            controls_group,
            text="⚖ Compare BFS vs DFS",
            font=("Segoe UI", 9, "bold"),
            bg="#059669",
            fg="white",
            relief=tk.FLAT,
            pady=6,
            cursor="hand2",
            command=self.run_comparison
        )
        self.btn_compare.pack(fill=tk.X, pady=(0, 6))

        # Stop / Pause button
        self.btn_stop = tk.Button(
            controls_group,
            text="⏹ Stop Search",
            font=("Segoe UI", 9, "bold"),
            bg="#DC2626",
            fg="white",
            relief=tk.FLAT,
            pady=4,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.stop_search
        )
        self.btn_stop.pack(fill=tk.X, pady=(0, 10))

        # --- Section 2: Drawing Tools ---
        draw_title = tk.Label(
            controls_group,
            text="2. Mouse Edit Mode",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#475569"
        )
        draw_title.pack(anchor="w", pady=(0, 4))

        mode_frame = tk.Frame(controls_group, bg="#FFFFFF")
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        modes = [
            ("Add Wall", "wall"),
            ("Erase Wall", "erase"),
            ("Set Start", "start"),
            ("Set Goal", "goal")
        ]
        for idx, (label, mode_val) in enumerate(modes):
            rb = tk.Radiobutton(
                mode_frame,
                text=label,
                variable=self.interaction_mode,
                value=mode_val,
                font=("Segoe UI", 8),
                bg="#FFFFFF",
                selectcolor="#E2E8F0",
                activebackground="#FFFFFF",
                cursor="hand2"
            )
            rb.grid(row=idx // 2, column=idx % 2, sticky="w", padx=4, pady=2)

        # --- Section 3: Maze Generation & Templates ---
        maze_title = tk.Label(
            controls_group,
            text="3. Maze Management & Presets",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#475569"
        )
        maze_title.pack(anchor="w", pady=(0, 4))

        gen_frame = tk.Frame(controls_group, bg="#FFFFFF")
        gen_frame.pack(fill=tk.X, pady=(0, 6))

        self.btn_gen_dfs = tk.Button(
            gen_frame,
            text="🌀 Labyrinth (DFS)",
            font=("Segoe UI", 8, "bold"),
            bg="#475569",
            fg="white",
            relief=tk.FLAT,
            pady=4,
            cursor="hand2",
            command=self.generate_labyrinth_maze
        )
        self.btn_gen_dfs.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_gen_random = tk.Button(
            gen_frame,
            text="🎲 Random Walls",
            font=("Segoe UI", 8, "bold"),
            bg="#475569",
            fg="white",
            relief=tk.FLAT,
            pady=4,
            cursor="hand2",
            command=self.generate_random_obstacles
        )
        self.btn_gen_random.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # Preset Dropdown
        preset_frame = tk.Frame(controls_group, bg="#FFFFFF")
        preset_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Label(preset_frame, text="Preset:", font=("Segoe UI", 8), bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 4))
        self.preset_combo = ttk.Combobox(
            preset_frame,
            values=["Classic Academic", "Spiral Labyrinth", "Trap Maze (No Path)", "Adjacent Start-Goal", "Open Field"],
            state="readonly",
            font=("Segoe UI", 8)
        )
        self.preset_combo.current(0)
        self.preset_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_select)

        # Clear and Reset buttons
        reset_frame = tk.Frame(controls_group, bg="#FFFFFF")
        reset_frame.pack(fill=tk.X, pady=(0, 10))

        self.btn_reset_search = tk.Button(
            reset_frame,
            text="🔄 Reset Search",
            font=("Segoe UI", 8, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            relief=tk.FLAT,
            pady=4,
            cursor="hand2",
            command=self.reset_search_state
        )
        self.btn_reset_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_clear_all = tk.Button(
            reset_frame,
            text="🗑 Clear Maze",
            font=("Segoe UI", 8, "bold"),
            bg="#E2E8F0",
            fg="#DC2626",
            relief=tk.FLAT,
            pady=4,
            cursor="hand2",
            command=self.clear_maze
        )
        self.btn_clear_all.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # --- Section 4: Configuration (Speed & Grid Size) ---
        cfg_title = tk.Label(
            controls_group,
            text="4. Configuration",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#475569"
        )
        cfg_title.pack(anchor="w", pady=(0, 2))

        speed_frame = tk.Frame(controls_group, bg="#FFFFFF")
        speed_frame.pack(fill=tk.X, pady=(0, 4))

        tk.Label(speed_frame, text="Speed Delay (ms):", font=("Segoe UI", 8), bg="#FFFFFF").pack(side=tk.LEFT)
        speed_scale = tk.Scale(
            speed_frame,
            from_=1,
            to=80,
            orient=tk.HORIZONTAL,
            variable=self.speed_ms,
            bg="#FFFFFF",
            highlightthickness=0,
            length=160
        )
        speed_scale.pack(side=tk.RIGHT)

        size_frame = tk.Frame(controls_group, bg="#FFFFFF")
        size_frame.pack(fill=tk.X)

        tk.Label(size_frame, text="Grid Size:", font=("Segoe UI", 8), bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 4))
        self.size_combo = ttk.Combobox(
            size_frame,
            values=["15 x 15 (Small)", "21 x 21 (Standard)", "27 x 27 (Large)", "33 x 33 (Dense)"],
            state="readonly",
            font=("Segoe UI", 8)
        )
        self.size_combo.current(1)
        self.size_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.size_combo.bind("<<ComboboxSelected>>", self.on_size_change)

    def _build_stats_panel(self, parent):
        """Construct the live search statistics and performance metrics panel."""
        stats_group = tk.LabelFrame(
            parent,
            text="Search Statistics",
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=12,
            pady=10,
            bd=1,
            relief=tk.SOLID
        )
        stats_group.pack(fill=tk.BOTH, expand=True)

        self.stat_labels = {}
        metrics = [
            ("Algorithm Used:", "None"),
            ("Search Status:", "Ready"),
            ("Path Found:", "--"),
            ("Path Length (Edges):", "0"),
            ("Nodes Visited:", "0"),
            ("Frontier Peak:", "0"),
            ("Execution Time:", "0.000 ms"),
        ]

        for idx, (label_text, default_val) in enumerate(metrics):
            row_frame = tk.Frame(stats_group, bg="#FFFFFF", pady=3)
            row_frame.pack(fill=tk.X)

            lbl = tk.Label(row_frame, text=label_text, font=("Segoe UI", 9), bg="#FFFFFF", fg="#64748B")
            lbl.pack(side=tk.LEFT)

            val_color = "#0F172A"
            if label_text == "Search Status:":
                val_color = "#0284C7"

            val = tk.Label(row_frame, text=default_val, font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg=val_color)
            val.pack(side=tk.RIGHT)

            self.stat_labels[label_text] = val

        # Theoretical summary note
        theory_box = tk.Frame(stats_group, bg="#F1F5F9", padx=8, pady=8, bd=1, relief=tk.SOLID)
        theory_box.pack(fill=tk.X, pady=(12, 0))

        tk.Label(
            theory_box,
            text="Theoretical Guarantee:\n• BFS: Always guarantees the SHORTEST path\n• DFS: Explores deep paths, may be non-optimal",
            font=("Segoe UI", 8),
            bg="#F1F5F9",
            fg="#334155",
            justify=tk.LEFT
        ).pack(anchor="w")

    def _build_statusbar(self):
        """Bottom status indicator bar."""
        self.status_bar = tk.Label(
            self,
            text="Ready. Select an algorithm or draw walls by clicking/dragging on the grid.",
            font=("Segoe UI", 9),
            bg="#E2E8F0",
            fg="#334155",
            anchor="w",
            padx=12,
            pady=4
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # -------------------------------------------------------------------------
    # Canvas Grid Rendering
    # -------------------------------------------------------------------------
    def draw_maze(self, overlay_cells=None, path_cells=None):
        """
        Renders the maze grid onto the Tkinter Canvas.
        
        Args:
            overlay_cells: Dictionary {(r, c): color} for visited / frontier nodes
            path_cells: List of (r, c) coordinates for the final path
        """
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 10 or height <= 10:
            return

        # Calculate cell dimensions to fit canvas with margin
        margin = 15
        available_w = max(10, width - 2 * margin)
        available_h = max(10, height - 2 * margin)

        cell_w = available_w / self.maze.cols
        cell_h = available_h / self.maze.rows
        cell_size = min(cell_w, cell_h)

        # Center the grid
        start_x = (width - cell_size * self.maze.cols) / 2
        start_y = (height - cell_size * self.maze.rows) / 2

        self.cell_size = cell_size
        self.start_x = start_x
        self.start_y = start_y

        overlay = overlay_cells or {}
        path_set = set(path_cells) if path_cells else set()

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                x1 = start_x + c * cell_size
                y1 = start_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Determine fill color
                if (r, c) == self.maze.start:
                    fill_color = COLOR_START
                elif (r, c) == self.maze.goal:
                    fill_color = COLOR_GOAL
                elif (r, c) in path_set:
                    fill_color = COLOR_PATH
                elif (r, c) in overlay:
                    fill_color = overlay[(r, c)]
                elif self.maze.grid[r][c] == WALL:
                    fill_color = COLOR_WALL
                else:
                    fill_color = COLOR_EMPTY

                # Draw grid cell rectangle
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline=COLOR_GRID_LINE,
                    width=1,
                    tags=f"cell_{r}_{c}"
                )

                # Draw text markers for Start ('S') and Goal ('G')
                if (r, c) == self.maze.start:
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="S",
                        font=("Segoe UI", max(8, int(cell_size * 0.45)), "bold"),
                        fill="#FFFFFF"
                    )
                elif (r, c) == self.maze.goal:
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="G",
                        font=("Segoe UI", max(8, int(cell_size * 0.45)), "bold"),
                        fill="#FFFFFF"
                    )

    # -------------------------------------------------------------------------
    # Mouse Interaction Handlers
    # -------------------------------------------------------------------------
    def _coords_to_grid(self, event_x, event_y):
        """Converts canvas (x, y) pixel coordinates to (row, col) grid indices."""
        if not hasattr(self, 'cell_size') or self.cell_size <= 0:
            return None, None
        col = int((event_x - self.start_x) // self.cell_size)
        row = int((event_y - self.start_y) // self.cell_size)
        if 0 <= row < self.maze.rows and 0 <= col < self.maze.cols:
            return row, col
        return None, None

    def on_canvas_click(self, event):
        """Handles single mouse click on grid."""
        if self.is_running:
            return
        r, c = self._coords_to_grid(event.x, event.y)
        if r is None or c is None:
            return
        self._apply_mouse_action(r, c)

    def on_canvas_drag(self, event):
        """Handles mouse drag (for painting walls or erasing)."""
        if self.is_running:
            return
        r, c = self._coords_to_grid(event.x, event.y)
        if r is None or c is None:
            return
        mode = self.interaction_mode.get()
        # Start and Goal should not be dragged continuously
        if mode in ("wall", "erase"):
            self._apply_mouse_action(r, c)

    def on_canvas_right_click(self, event):
        """Right-click allows immediate wall erasing regardless of selected mode."""
        if self.is_running:
            return
        r, c = self._coords_to_grid(event.x, event.y)
        if r is not None and c is not None:
            self.maze.remove_wall(r, c)
            self.draw_maze()

    def _apply_mouse_action(self, r, c):
        """Applies modification to cell (r, c) according to interaction mode."""
        mode = self.interaction_mode.get()

        if mode == "wall":
            self.maze.set_wall(r, c)
        elif mode == "erase":
            self.maze.remove_wall(r, c)
        elif mode == "start":
            if self.maze.grid[r][c] == WALL:
                self.set_status("Cannot place Start on a wall! Erase the wall first.")
                return
            if (r, c) == self.maze.goal:
                self.set_status("Start position cannot be the same as Goal position.")
                return
            self.maze.set_start(r, c)
            self.set_status(f"Start moved to cell ({r}, {c}).")
        elif mode == "goal":
            if self.maze.grid[r][c] == WALL:
                self.set_status("Cannot place Goal on a wall! Erase the wall first.")
                return
            if (r, c) == self.maze.start:
                self.set_status("Goal position cannot be the same as Start position.")
                return
            self.maze.set_goal(r, c)
            self.set_status(f"Goal moved to cell ({r}, {c}).")

        self.draw_maze()

    # -------------------------------------------------------------------------
    # Algorithm Execution & Animation Engine
    # -------------------------------------------------------------------------
    def start_search(self, algorithm_name: str):
        """
        Prepares and initiates the animated step-by-step search for BFS or DFS.
        """
        if self.is_running:
            return

        # Verification: Check if Start and Goal are valid and accessible
        if self.maze.start == self.maze.goal:
            messagebox.showwarning(
                "Invalid Setup",
                "Start and Goal are currently at the same position!"
            )
            return

        if self.maze.grid[self.maze.start[0]][self.maze.start[1]] == WALL:
            messagebox.showerror("Error", "Start position is located on a wall!")
            return

        if self.maze.grid[self.maze.goal[0]][self.maze.goal[1]] == WALL:
            messagebox.showerror("Error", "Goal position is located on a wall!")
            return

        # Lock controls during search animation
        self.is_running = True
        self.cancel_search = False
        self.active_algorithm = algorithm_name
        self._set_controls_state(tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        # Clear previous search overlays
        self.visited_overlay = {}
        self.current_path = []
        self.draw_maze()

        # Update stats
        self.stat_labels["Algorithm Used:"].config(text=algorithm_name)
        self.stat_labels["Search Status:"].config(text=f"Running {algorithm_name}...", fg="#0284C7")
        self.stat_labels["Path Found:"].config(text="Searching...")
        self.stat_labels["Path Length (Edges):"].config(text="--")
        self.stat_labels["Nodes Visited:"].config(text="0")
        self.stat_labels["Frontier Peak:"].config(text="0")
        self.stat_labels["Execution Time:"].config(text="Calculating...")
        self.set_status(f"Executing {algorithm_name}... Please wait.")

        # Create generator
        if algorithm_name == "BFS":
            self.search_generator = bfs_step_generator(self.maze.grid, self.maze.start, self.maze.goal)
        else:
            self.search_generator = dfs_step_generator(self.maze.grid, self.maze.start, self.maze.goal)

        # Start animation loop
        self._animation_step()

    def _animation_step(self):
        """Executes a single step or batch of steps of search exploration."""
        if not self.is_running or self.cancel_search:
            self._finalize_search(None, cancelled=True)
            return

        delay = self.speed_ms.get()

        # For very fast speeds, process multiple steps per frame for smooth high performance
        steps_per_tick = 1
        if delay <= 5:
            steps_per_tick = 6
        elif delay <= 15:
            steps_per_tick = 2

        color_visited = COLOR_VISITED_BFS if self.active_algorithm == "BFS" else COLOR_VISITED_DFS

        for _ in range(steps_per_tick):
            try:
                event = next(self.search_generator)
            except StopIteration:
                self._finalize_search(None)
                return

            event_type = event[0]

            if event_type == "visit":
                _, curr_node, visited_count, frontier_sz = event
                # Color visited cell (unless it's start or goal)
                if curr_node != self.maze.start and curr_node != self.maze.goal:
                    self.visited_overlay[curr_node] = color_visited

                self.stat_labels["Nodes Visited:"].config(text=str(visited_count))
                self.stat_labels["Frontier Peak:"].config(text=str(frontier_sz))

            elif event_type == "found":
                _, path, result_obj = event
                self.current_path = path
                self._animate_final_path(path, result_obj)
                return

            elif event_type == "not_found":
                _, result_obj = event
                self._finalize_search(result_obj)
                return

            elif event_type == "error":
                _, msg = event
                messagebox.showerror("Search Error", msg)
                self._finalize_search(None)
                return

        # Render current frame
        self.draw_maze(self.visited_overlay)

        # Schedule next tick
        self.animation_job = self.after(delay, self._animation_step)

    def _animate_final_path(self, path, result_obj):
        """Animates the final path trace in glowing gold from start to goal."""
        step_idx = 0
        path_progress = []

        def trace_step():
            nonlocal step_idx
            if not self.is_running or self.cancel_search:
                self._finalize_search(result_obj)
                return

            if step_idx < len(path):
                node = path[step_idx]
                if node != self.maze.start and node != self.maze.goal:
                    path_progress.append(node)
                step_idx += 1
                self.draw_maze(self.visited_overlay, path_progress)
                self.after(20, trace_step)
            else:
                self._finalize_search(result_obj)

        trace_step()

    def _finalize_search(self, result: SearchResult, cancelled: bool = False):
        """Cleanup and final metric display after search completes or is halted."""
        self.is_running = False
        self._set_controls_state(tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

        if cancelled:
            self.stat_labels["Search Status:"].config(text="Search Stopped by User", fg="#DC2626")
            self.set_status("Search was stopped.")
            return

        if result is None:
            return

        # Cache result
        if result.algorithm == "BFS":
            self.last_bfs_result = result
        else:
            self.last_dfs_result = result

        if result.path_found:
            self.stat_labels["Search Status:"].config(text="Goal Reached!", fg="#059669")
            self.stat_labels["Path Found:"].config(text="Yes", fg="#059669")
            self.stat_labels["Path Length (Edges):"].config(text=str(result.path_length))
            self.stat_labels["Nodes Visited:"].config(text=str(result.nodes_visited))
            self.stat_labels["Frontier Peak:"].config(text=str(result.max_frontier_size))
            self.stat_labels["Execution Time:"].config(
                text=f"{result.execution_time * 1000:.3f} ms ({result.execution_time:.5f} s)"
            )
            self.set_status(f"Success! {result.algorithm} found path of length {result.path_length}.")
            self.draw_maze(self.visited_overlay, result.path)
        else:
            self.stat_labels["Search Status:"].config(text="No Path Exists!", fg="#DC2626")
            self.stat_labels["Path Found:"].config(text="No", fg="#DC2626")
            self.stat_labels["Path Length (Edges):"].config(text="0")
            self.stat_labels["Nodes Visited:"].config(text=str(result.nodes_visited))
            self.stat_labels["Execution Time:"].config(
                text=f"{result.execution_time * 1000:.3f} ms"
            )
            self.set_status("No path exists from Start to Goal. Target is completely walled off.")
            self.draw_maze(self.visited_overlay)
            messagebox.showinfo(
                "Search Complete",
                "No path exists between Start and Goal!\nAll reachable nodes were explored."
            )

    def stop_search(self):
        """Cancels any running search."""
        if self.is_running:
            self.cancel_search = True
            if self.animation_job:
                self.after_cancel(self.animation_job)
            self._finalize_search(None, cancelled=True)

    def _set_controls_state(self, state):
        """Enables or disables interactive buttons to avoid concurrent state changes."""
        self.btn_bfs.config(state=state)
        self.btn_dfs.config(state=state)
        self.btn_compare.config(state=state)
        self.btn_gen_dfs.config(state=state)
        self.btn_gen_random.config(state=state)
        self.btn_reset_search.config(state=state)
        self.btn_clear_all.config(state=state)
        self.preset_combo.config(state="readonly" if state == tk.NORMAL else tk.DISABLED)
        self.size_combo.config(state="readonly" if state == tk.NORMAL else tk.DISABLED)

    # -------------------------------------------------------------------------
    # Comparison Mode (BFS vs DFS)
    # -------------------------------------------------------------------------
    def run_comparison(self):
        """
        Executes both BFS and DFS on the exact same maze without artificial animation delay,
        records accurate metrics, and displays a comprehensive academic comparison window.
        """
        if self.is_running:
            return

        if self.maze.grid[self.maze.start[0]][self.maze.start[1]] == WALL or \
           self.maze.grid[self.maze.goal[0]][self.maze.goal[1]] == WALL:
            messagebox.showerror("Error", "Start or Goal is on a wall. Clear it before comparing.")
            return

        self.set_status("Computing comparative benchmark for BFS and DFS...")

        # Run BFS
        bfs_res = solve_bfs(self.maze.grid, self.maze.start, self.maze.goal)
        # Run DFS
        dfs_res = solve_dfs(self.maze.grid, self.maze.start, self.maze.goal)

        self.last_bfs_result = bfs_res
        self.last_dfs_result = dfs_res

        self._show_comparison_dialog(bfs_res, dfs_res)

    def _show_comparison_dialog(self, bfs: SearchResult, dfs: SearchResult):
        """Displays a polished comparative analysis modal."""
        dialog = tk.Toplevel(self)
        dialog.title("Algorithm Comparison: BFS vs. DFS")
        dialog.geometry("640x520")
        dialog.minsize(580, 480)
        dialog.configure(bg="#F8FAFC")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        hdr = tk.Frame(dialog, bg="#1E293B", padx=16, pady=12)
        hdr.pack(fill=tk.X)

        tk.Label(
            hdr,
            text="Comparative Performance Analysis",
            font=("Segoe UI", 14, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        ).pack(anchor="w")

        tk.Label(
            hdr,
            text="Breadth-First Search (Queue) vs. Depth-First Search (Stack)",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w")

        # Table Container
        tbl_frame = tk.Frame(dialog, bg="#FFFFFF", bd=1, relief=tk.SOLID, padx=12, pady=12)
        tbl_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # Columns
        columns = ("Metric", "Breadth-First Search (BFS)", "Depth-First Search (DFS)", "Comparison Note")
        tree = ttk.Treeview(tbl_frame, columns=columns, show="headings", height=8)

        tree.heading("Metric", text="Metric")
        tree.heading("Breadth-First Search (BFS)", text="Breadth-First Search (BFS)")
        tree.heading("Depth-First Search (DFS)", text="Depth-First Search (DFS)")
        tree.heading("Comparison Note", text="Comparison Note")

        tree.column("Metric", width=150, anchor="w")
        tree.column("Breadth-First Search (BFS)", width=130, anchor="center")
        tree.column("Depth-First Search (DFS)", width=130, anchor="center")
        tree.column("Comparison Note", width=160, anchor="w")

        tree.pack(fill=tk.BOTH, expand=True)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#E2E8F0")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)

        # Row Data
        path_len_note = "BFS Optimal" if (bfs.path_length <= dfs.path_length and bfs.path_found) else "DFS longer path"
        nodes_note = "Fewer nodes" if bfs.nodes_visited < dfs.nodes_visited else "DFS explored differently"

        table_rows = [
            ("Path Found?", "Yes" if bfs.path_found else "No", "Yes" if dfs.path_found else "No", "Both complete on finite grid"),
            ("Path Length (Steps)", str(bfs.path_length), str(dfs.path_length), path_len_note),
            ("Nodes Visited", str(bfs.nodes_visited), str(dfs.nodes_visited), nodes_note),
            ("Execution Time", f"{bfs.execution_time*1000:.3f} ms", f"{dfs.execution_time*1000:.3f} ms", "Machine/grid dependent"),
            ("Max Frontier Size", str(bfs.max_frontier_size), str(dfs.max_frontier_size), "Queue vs Stack memory"),
            ("Data Structure", "Queue (FIFO)", "Stack (LIFO)", "First-in vs Last-in"),
            ("Shortest Path?", "Guaranteed (Optimal)", "No Guarantee", "Core syllabus theorem"),
            ("Time Complexity", "O(V + E)", "O(V + E)", "V = rows*cols, E = 4V"),
            ("Space Complexity", "O(V)", "O(V)", "Stores visited nodes")
        ]

        for row in table_rows:
            tree.insert("", tk.END, values=row)

        # Bottom Explanation
        summary_text = (
            "Key Takeaway for AI Mini Project:\n"
            f"• BFS explored {bfs.nodes_visited} nodes and produced an optimal path of {bfs.path_length} steps.\n"
            f"• DFS explored {dfs.nodes_visited} nodes and produced a path of {dfs.path_length} steps.\n"
            "BFS is mathematically guaranteed to find the shortest path in unweighted mazes.\n"
            "DFS explores one branch deeply, meaning it frequently takes longer detours."
        )

        tk.Label(
            dialog,
            text=summary_text,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            fg="#1E293B",
            justify=tk.LEFT,
            padx=16
        ).pack(anchor="w", pady=(0, 10))

        # Action Buttons in Modal
        btn_bar = tk.Frame(dialog, bg="#F8FAFC", padx=16, pady=8)
        btn_bar.pack(fill=tk.X)

        def view_bfs_path():
            dialog.destroy()
            self.stat_labels["Algorithm Used:"].config(text="BFS (Comparison)")
            self._finalize_search(bfs)

        def view_dfs_path():
            dialog.destroy()
            self.stat_labels["Algorithm Used:"].config(text="DFS (Comparison)")
            self._finalize_search(dfs)

        tk.Button(
            btn_bar,
            text="Show BFS Path on Maze",
            font=("Segoe UI", 9, "bold"),
            bg="#0284C7",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=view_bfs_path
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(
            btn_bar,
            text="Show DFS Path on Maze",
            font=("Segoe UI", 9, "bold"),
            bg="#7C3AED",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=view_dfs_path
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_bar,
            text="Close",
            font=("Segoe UI", 9),
            bg="#94A3B8",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=dialog.destroy
        ).pack(side=tk.RIGHT)

    # -------------------------------------------------------------------------
    # Maze Modification Actions
    # -------------------------------------------------------------------------
    def generate_labyrinth_maze(self):
        """Generates a perfect labyrinth using recursive backtracker algorithm."""
        self.stop_search()
        self.maze.generate_labyrinth()
        self.reset_search_state()
        self.set_status("Generated new labyrinth using Randomized DFS.")

    def generate_random_obstacles(self):
        """Generates random obstacle maze."""
        self.stop_search()
        self.maze.generate_random_obstacles(density=0.28)
        self.reset_search_state()
        self.set_status("Generated random obstacle maze with density 28%.")

    def on_preset_select(self, event=None):
        """Handles user selecting a preset template."""
        preset = self.preset_combo.get()
        self.stop_search()
        self.maze.load_preset(preset)
        self.reset_search_state()
        self.set_status(f"Loaded preset: '{preset}'.")

    def on_size_change(self, event=None):
        """Handles resizing the grid dimensions."""
        choice = self.size_combo.get()
        size_map = {
            "15 x 15 (Small)": 15,
            "21 x 21 (Standard)": 21,
            "27 x 27 (Large)": 27,
            "33 x 33 (Dense)": 33
        }
        dim = size_map.get(choice, 21)
        self.stop_search()
        self.grid_rows = dim
        self.grid_cols = dim
        self.maze.resize(dim, dim)
        self.reset_search_state()
        self.set_status(f"Grid resized to {dim}x{dim}.")

    def reset_search_state(self):
        """Clears visited and path highlights, retaining all walls."""
        self.stop_search()
        self.maze.reset_search()
        self.visited_overlay = {}
        self.current_path = []
        self.draw_maze()
        self.stat_labels["Algorithm Used:"].config(text="None")
        self.stat_labels["Search Status:"].config(text="Ready", fg="#0284C7")
        self.stat_labels["Path Found:"].config(text="--", fg="#0F172A")
        self.stat_labels["Path Length (Edges):"].config(text="0")
        self.stat_labels["Nodes Visited:"].config(text="0")
        self.stat_labels["Frontier Peak:"].config(text="0")
        self.stat_labels["Execution Time:"].config(text="0.000 ms")
        self.set_status("Search state reset. Walls and Start/Goal preserved.")

    def clear_maze(self):
        """Removes all walls and resets grid to empty."""
        self.stop_search()
        self.maze.clear()
        self.reset_search_state()
        self.set_status("Maze cleared. All walls removed.")

    def set_status(self, text: str):
        """Updates bottom status bar text."""
        self.status_bar.config(text=text)

    # -------------------------------------------------------------------------
    # Academic & Informational Dialogs
    # -------------------------------------------------------------------------
    def show_about_algorithms(self):
        """Displays rich educational modal explaining BFS and DFS."""
        win = tk.Toplevel(self)
        win.title("About Search Algorithms - AI Foundations")
        win.geometry("680x600")
        win.minsize(600, 500)
        win.configure(bg="#F8FAFC")
        win.transient(self)

        text_area = tk.Text(
            win,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            padx=16,
            pady=16,
            bg="#FFFFFF",
            relief=tk.FLAT
        )
        scroll = ttk.Scrollbar(win, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        content = """===================================================================
AI FOUNDATIONS: UNINFORMED SEARCH STRATEGIES
===================================================================

1. What is an Uninformed Search?
Uninformed (also called 'Blind') search algorithms have no additional information about the state space beyond the problem definition. They can generate successors and distinguish a goal state from a non-goal state, but they do not know whether one non-goal state is 'better' or 'closer' than another (no heuristic evaluation).

-------------------------------------------------------------------
2. Breadth-First Search (BFS)
-------------------------------------------------------------------
• Mechanism:
  - Explores the state space systematically level by level.
  - Expands the root node first, then all successors of the root, then their successors, and so on.
• Underlying Data Structure:
  - FIFO (First-In, First-Out) Queue.
  - Newly discovered nodes are enqueued at the back; expansions occur from the front.
• Path Reconstruction:
  - Stores a 'parent' dictionary mapping each node to the predecessor that discovered it.
• Properties:
  - Completeness: YES (If a solution exists in a finite graph, BFS is guaranteed to find it).
  - Optimality: YES (For unweighted graphs or uniform step costs, BFS is guaranteed to find the shortest path with the minimum number of steps).
  - Time Complexity: O(V + E) or O(b^d), where b is branching factor and d is depth of shallowest solution.
  - Space Complexity: O(V) or O(b^d) because all nodes on the current level must be retained in the queue.

-------------------------------------------------------------------
3. Depth-First Search (DFS)
-------------------------------------------------------------------
• Mechanism:
  - Explores one branch deeply before backtracking.
  - Always expands the deepest unexpanded node in the current frontier.
• Underlying Data Structure:
  - LIFO (Last-In, First-Out) Stack (or recursive call stack).
• Path Reconstruction:
  - Uses parent pointers recorded when each node is first pushed/visited.
• Properties:
  - Completeness: YES in finite state spaces with graph search (visited set prevents infinite loops).
  - Optimality: NO. DFS does NOT guarantee the shortest path. It may stumble into a long, tortuous route to the goal simply because that branch was explored first.
  - Time Complexity: O(V + E) or O(b^m), where m is the maximum depth.
  - Space Complexity: O(V) with visited set, or O(b*m) in tree search (linear space).

-------------------------------------------------------------------
4. Key Differences Summary
-------------------------------------------------------------------
Characteristic          BFS                         DFS
-------------------------------------------------------------------
Frontier Type           Queue (FIFO)                Stack (LIFO)
Exploration Style       Concentric, level-by-level  Deep plunge, backtracking
Shortest Path           Guaranteed Optimal          Not Guaranteed
Memory Consumption      High (Frontier grows wide)  Low/Moderate along branch
Color in Visualization  Sky Blue                    Amethyst Purple
===================================================================
"""
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)

    def show_project_info(self):
        """Displays academic metadata and project credits."""
        win = tk.Toplevel(self)
        win.title("Academic Project Information")
        win.geometry("540x440")
        win.configure(bg="#F8FAFC")
        win.transient(self)

        hdr = tk.Frame(win, bg="#1E293B", padx=16, pady=12)
        hdr.pack(fill=tk.X)

        tk.Label(
            hdr,
            text="Academic Mini Project",
            font=("Segoe UI", 13, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        ).pack(anchor="w")

        info_frame = tk.Frame(win, bg="#FFFFFF", padx=16, pady=16, bd=1, relief=tk.SOLID)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        details = [
            ("Project Title:", "AI-Based Maze Solver Using BFS & DFS"),
            ("Domain:", "Foundations of Artificial Intelligence"),
            ("Core Topics:", "Problem-solving agents, Uninformed search, State spaces"),
            ("Algorithms:", "Breadth-First Search, Depth-First Search"),
            ("Frontier Types:", "FIFO Queue (BFS), LIFO Stack (DFS)"),
            ("Technology:", "Python 3.14 + Pure Tkinter (Standard Library)"),
            ("Key Metric:", "Path Length, Visited Nodes, Execution Time"),
            ("Author / Mini Project:", "B.Tech / B.E. Computer Science & Engineering")
        ]

        for title, val in details:
            r = tk.Frame(info_frame, bg="#FFFFFF", pady=3)
            r.pack(fill=tk.X)
            tk.Label(r, text=title, font=("Segoe UI", 9, "bold"), fg="#475569", bg="#FFFFFF", width=18, anchor="w").pack(side=tk.LEFT)
            tk.Label(r, text=val, font=("Segoe UI", 9), fg="#0F172A", bg="#FFFFFF", anchor="w").pack(side=tk.LEFT)

        tk.Button(
            win,
            text="Close",
            font=("Segoe UI", 9),
            bg="#64748B",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=win.destroy
        ).pack(pady=(0, 12))


if __name__ == "__main__":
    app = MazeApp()
    app.mainloop()
