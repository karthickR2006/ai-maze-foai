"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          maze.py
Description:   Maze data model, grid representation, wall manipulation,
               random maze generators (Recursive Backtracker & Random Density),
               and predefined academic demonstration templates.
=============================================================================
"""

import random
from utils import EMPTY, WALL, START, GOAL, in_bounds, get_neighbors


class Maze:
    """
    Represents the 2D grid maze environment.
    Handles cell state transitions, user interactions (drawing walls, moving Start/Goal),
    and algorithmic maze generation.
    """

    def __init__(self, rows: int = 21, cols: int = 21):
        """
        Initialize the maze with specified dimensions.
        Odd numbers (e.g., 21x21, 15x15) are ideal for recursive backtracker mazes.
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.start = (1, 1)
        self.goal = (rows - 2, cols - 2)

        # Set up default academic maze
        self.load_preset("Classic Academic")

    def resize(self, new_rows: int, new_cols: int):
        """Resize the grid and reset start/goal to valid positions."""
        self.rows = new_rows
        self.cols = new_cols
        self.grid = [[EMPTY for _ in range(new_cols)] for _ in range(new_rows)]
        self.start = (1, 1)
        self.goal = (new_rows - 2, new_cols - 2)
        self.load_preset("Classic Academic")

    def clear(self):
        """Clears all walls and paths, retaining only Start and Goal."""
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        # Ensure start and goal are empty cells
        self.grid[self.start[0]][self.start[1]] = EMPTY
        self.grid[self.goal[0]][self.goal[1]] = EMPTY

    def reset_search(self):
        """
        Clears temporary search markers (visited and path cells)
        while preserving all walls and Start/Goal coordinates.
        """
        # Search state is rendered dynamically, but grid keeps static structure (EMPTY or WALL)
        # start and goal positions are guaranteed preserved.
        pass

    def set_start(self, r: int, c: int) -> bool:
        """
        Sets the Start position if coordinates are valid and not a wall or goal.
        """
        if not in_bounds(r, c, self.rows, self.cols):
            return False
        if (r, c) == self.goal:
            return False
        if self.grid[r][c] == WALL:
            return False

        self.start = (r, c)
        return True

    def set_goal(self, r: int, c: int) -> bool:
        """
        Sets the Goal position if coordinates are valid and not a wall or start.
        """
        if not in_bounds(r, c, self.rows, self.cols):
            return False
        if (r, c) == self.start:
            return False
        if self.grid[r][c] == WALL:
            return False

        self.goal = (r, c)
        return True

    def set_wall(self, r: int, c: int) -> bool:
        """Add a wall at (r, c) unless it is Start or Goal."""
        if not in_bounds(r, c, self.rows, self.cols):
            return False
        if (r, c) == self.start or (r, c) == self.goal:
            return False
        self.grid[r][c] = WALL
        return True

    def remove_wall(self, r: int, c: int) -> bool:
        """Remove a wall at (r, c)."""
        if not in_bounds(r, c, self.rows, self.cols):
            return False
        if self.grid[r][c] == WALL:
            self.grid[r][c] = EMPTY
            return True
        return False

    def toggle_wall(self, r: int, c: int) -> bool:
        """Toggle wall at (r, c) between WALL and EMPTY."""
        if not in_bounds(r, c, self.rows, self.cols):
            return False
        if (r, c) == self.start or (r, c) == self.goal:
            return False

        if self.grid[r][c] == WALL:
            self.grid[r][c] = EMPTY
        else:
            self.grid[r][c] = WALL
        return True

    def generate_labyrinth(self):
        """
        Generates a perfect labyrinth using Randomized Depth-First Search (Recursive Backtracker).
        Guarantees that a path exists between all open cells, including Start and Goal.
        Carves winding corridors separated by single-cell walls.
        """
        # Fill grid with walls
        self.grid = [[WALL for _ in range(self.cols)] for _ in range(self.rows)]

        # Start carving from cell (1, 1)
        start_r, start_c = 1, 1
        self.grid[start_r][start_c] = EMPTY

        stack = [(start_r, start_c)]
        visited_carve = {(start_r, start_c)}

        while stack:
            cr, cc = stack[-1]

            # Look 2 steps away in 4 cardinal directions
            candidates = []
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = cr + dr, cc + dc
                if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                    if (nr, nc) not in visited_carve:
                        candidates.append((nr, nc, dr // 2, dc // 2))

            if candidates:
                nr, nc, wall_dr, wall_dc = random.choice(candidates)
                # Knock down the wall in between
                self.grid[cr + wall_dr][cc + wall_dc] = EMPTY
                self.grid[nr][nc] = EMPTY
                visited_carve.add((nr, nc))
                stack.append((nr, nc))
            else:
                stack.pop()

        # Set Start and Goal to accessible carved pathways
        self.start = (1, 1)
        self.grid[1][1] = EMPTY

        # Ensure goal is near the bottom-right and walkable
        gr, gc = self.rows - 2, self.cols - 2
        # Adjust if even dimension
        if self.grid[gr][gc] == WALL:
            # find closest empty cell
            for r in range(self.rows - 2, 0, -1):
                for c in range(self.cols - 2, 0, -1):
                    if self.grid[r][c] == EMPTY:
                        gr, gc = r, c
                        break
                if self.grid[gr][gc] == EMPTY:
                    break
        self.goal = (gr, gc)

        # Knock down a few random internal walls to introduce multiple alternative paths
        # This creates distinct differences between BFS (finds shortcuts) and DFS (takes long branches)
        extra_openings = (self.rows * self.cols) // 18
        for _ in range(extra_openings):
            rr = random.randint(1, self.rows - 2)
            rc = random.randint(1, self.cols - 2)
            if self.grid[rr][rc] == WALL:
                self.grid[rr][rc] = EMPTY

    def generate_random_obstacles(self, density: float = 0.28):
        """
        Fills the grid with randomly scattered obstacle walls based on a given density.
        Ensures Start and Goal and their immediate neighbors remain unobstructed.
        """
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (1, 1)
        self.goal = (self.rows - 2, self.cols - 2)

        protected_cells = {
            self.start,
            self.goal,
            (self.start[0] + 1, self.start[1]),
            (self.start[0], self.start[1] + 1),
            (self.goal[0] - 1, self.goal[1]),
            (self.goal[0], self.goal[1] - 1),
        }

        # Add border walls
        for r in range(self.rows):
            self.grid[r][0] = WALL
            self.grid[r][self.cols - 1] = WALL
        for c in range(self.cols):
            self.grid[0][c] = WALL
            self.grid[self.rows - 1][c] = WALL

        # Scatter random walls
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                if (r, c) not in protected_cells:
                    if random.random() < density:
                        self.grid[r][c] = WALL

    def load_preset(self, preset_name: str):
        """
        Loads curated academic demonstration presets designed to illustrate
        specific search behavior, edge cases, and algorithmic differences.
        """
        self.clear()

        # Border walls for clean containment
        for r in range(self.rows):
            self.grid[r][0] = WALL
            self.grid[r][self.cols - 1] = WALL
        for c in range(self.cols):
            self.grid[0][c] = WALL
            self.grid[self.rows - 1][c] = WALL

        self.start = (1, 1)
        self.goal = (self.rows - 2, self.cols - 2)

        if preset_name == "Classic Academic":
            # Preset crafted to showcase the core AI search theorem:
            # - BFS finds the direct shortest path (36 steps on 21x21)
            # - DFS prioritizes the winding serpentine corridor (156 steps)
            
            # 1. Fill interior with walls
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c] = WALL

            self.start = (1, 1)
            self.goal = (self.rows - 2, self.cols - 2)
            self.grid[1][1] = EMPTY
            self.grid[self.goal[0]][self.goal[1]] = EMPTY

            # 2. Short Path (Direct corridor down and right)
            for r in range(1, self.rows - 1):
                self.grid[r][1] = EMPTY
            for c in range(1, self.cols - 1):
                self.grid[self.rows - 2][c] = EMPTY

            # 3. Long Detour Path (Serpentine winding labyrinth on the right half)
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

        elif preset_name == "Spiral Labyrinth":
            # Inward winding spiral corridor
            top = 2
            bottom = self.rows - 3
            left = 2
            right = self.cols - 3

            while top <= bottom and left <= right:
                # Top wall
                for c in range(left, right + 1):
                    self.grid[top][c] = WALL
                # Right wall
                for r in range(top, bottom + 1):
                    self.grid[r][right] = WALL
                # Bottom wall
                for c in range(right, left - 1, -1):
                    self.grid[bottom][c] = WALL
                # Left wall
                for r in range(bottom, top + 1, -1):
                    self.grid[r][left] = WALL

                # Create doorway to enter next inner layer
                self.grid[top + 1][left] = EMPTY

                top += 2
                bottom -= 2
                left += 2
                right -= 2

            self.start = (1, 1)
            # Center of spiral
            self.goal = (self.rows // 2, self.cols // 2)
            self.grid[self.goal[0]][self.goal[1]] = EMPTY

        elif preset_name == "Trap Maze (No Path)":
            # Completely walls off the Goal to test the 'No Path Exists' condition
            gr, gc = self.goal
            # Build an impenetrable box around Goal
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = gr + dr, gc + dc
                    if in_bounds(nr, nc, self.rows, self.cols) and (nr, nc) != self.goal:
                        self.grid[nr][nc] = WALL

        elif preset_name == "Adjacent Start-Goal":
            # Start and Goal are 1 step apart to test minimal base case
            self.start = (5, 5)
            self.goal = (5, 6)
            self.grid[5][5] = EMPTY
            self.grid[5][6] = EMPTY

        elif preset_name == "Open Field":
            # Pure open grid without internal walls
            pass

    def get_ascii_display(self) -> str:
        """Returns clean text-based ASCII representation of the maze."""
        lines = []
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                if (r, c) == self.start:
                    row_str.append("S")
                elif (r, c) == self.goal:
                    row_str.append("G")
                elif self.grid[r][c] == WALL:
                    row_str.append("#")
                else:
                    row_str.append(".")
            lines.append(" ".join(row_str))
        return "\n".join(lines)
