"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          utils.py
Description:   Common constants, cell types, color palette, and utility
               helper functions for grid operations, neighbor validation,
               and path reconstruction.
=============================================================================
"""

import time
from collections import deque

# -----------------------------------------------------------------------------
# Cell Types (State Constants)
# -----------------------------------------------------------------------------
EMPTY = 0       # Passable pathway / empty cell
WALL = 1        # Impassable obstacle / barrier
START = 2       # Start position (Initial state)
GOAL = 3        # Target position (Goal state)
VISITED_BFS = 4 # Cell visited during Breadth-First Search
VISITED_DFS = 5 # Cell visited during Depth-First Search
PATH = 6        # Final reconstructed solution path
FRONTIER = 7    # Cell currently in queue/stack (boundary of search)

# -----------------------------------------------------------------------------
# Color Palette (Modern, high-contrast, academic presentation)
# -----------------------------------------------------------------------------
COLOR_EMPTY = "#FFFFFF"        # Clean white for walkable cells
COLOR_WALL = "#2C3E50"         # Dark slate / charcoal for walls
COLOR_START = "#27AE60"        # Vibrant green for Start
COLOR_GOAL = "#E74C3C"         # Crimson red for Goal
COLOR_VISITED_BFS = "#5DADE2"  # Sky blue for BFS explored nodes
COLOR_VISITED_DFS = "#AF7AC5"  # Amethyst purple for DFS explored nodes
COLOR_PATH = "#F39C12"         # Radiant amber/orange for the solution path
COLOR_CURRENT = "#F1C40F"      # Bright yellow for actively expanding node
COLOR_GRID_LINE = "#BDC3C7"    # Soft gray for grid cell boundaries
COLOR_BG = "#ECF0F1"           # Light neutral gray for UI background

# -----------------------------------------------------------------------------
# Movement Vectors (4-Connected Grid: Orthogonal movements only)
# Disallowing diagonal movements prevents cutting through wall corners.
# Standard exploration order: Up, Right, Down, Left (North, East, South, West)
# -----------------------------------------------------------------------------
DIRECTIONS = [
    (-1, 0),  # Up
    (0, 1),   # Right
    (1, 0),   # Down
    (0, -1)   # Left
]

DIRECTION_NAMES = ["Up", "Right", "Down", "Left"]


def in_bounds(row: int, col: int, total_rows: int, total_cols: int) -> bool:
    """
    Check if a coordinate (row, col) is within the grid boundaries.

    Args:
        row: Row index
        col: Column index
        total_rows: Total number of rows in grid
        total_cols: Total number of columns in grid

    Returns:
        True if inside grid boundaries, False otherwise.
    """
    return 0 <= row < total_rows and 0 <= col < total_cols


def get_neighbors(row: int, col: int, total_rows: int, total_cols: int, grid: list) -> list:
    """
    Retrieve all valid adjacent neighbor cells that are walkable (not walls).
    Strictly orthogonal (Up, Right, Down, Left).

    Args:
        row: Current row index
        col: Current column index
        total_rows: Total rows in the maze
        total_cols: Total columns in the maze
        grid: 2D list representing the maze

    Returns:
        List of tuples [(nr, nc), ...] representing valid neighboring coordinates.
    """
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        # Boundary check
        if in_bounds(nr, nc, total_rows, total_cols):
            # Collision check: Cannot walk through walls
            if grid[nr][nc] != WALL:
                neighbors.append((nr, nc))
    return neighbors


def reconstruct_path(parent_dict: dict, start: tuple, goal: tuple) -> list:
    """
    Reconstruct the path from Start to Goal using the parent pointer dictionary.
    
    Backtracks: Goal -> Parent(Goal) -> ... -> Start
    Then reverses to produce: Start -> ... -> Goal.

    Args:
        parent_dict: Dictionary mapping child node (r, c) -> parent node (pr, pc)
        start: Tuple (start_row, start_col)
        goal: Tuple (goal_row, goal_col)

    Returns:
        List of coordinates [(r1, c1), (r2, c2), ...] from start to goal.
        Returns an empty list if goal is not reachable from start.
    """
    if goal not in parent_dict and start != goal:
        return []

    if start == goal:
        return [start]

    path = []
    current = goal
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent_dict.get(current)

    # If the backtrack did not reach start, no valid path exists
    if path[-1] != start:
        return []

    # Reverse to obtain Start -> Goal order
    path.reverse()
    return path


class SearchResult:
    """
    Container class to store the outcome and performance metrics of a search.
    """
    def __init__(self, algorithm: str):
        self.algorithm = algorithm           # Name of the algorithm ("BFS" or "DFS")
        self.path_found = False              # Boolean flag
        self.path = []                       # List of (r, c) in solution path
        self.path_length = 0                 # Number of steps in solution path (edges)
        self.nodes_visited = 0               # Total number of nodes expanded/visited
        self.visited_order = []              # Order of node visits (for animation)
        self.execution_time = 0.0            # Wall-clock execution time in seconds
        self.max_frontier_size = 0           # Maximum size of queue/stack (space metric)
        self.status_message = "Not started"  # Human-readable result summary

    def to_dict(self) -> dict:
        return {
            "algorithm": self.algorithm,
            "path_found": "Yes" if self.path_found else "No",
            "path_length": self.path_length,
            "nodes_visited": self.nodes_visited,
            "execution_time_sec": round(self.execution_time, 6),
            "execution_time_ms": round(self.execution_time * 1000, 3),
            "max_frontier_size": self.max_frontier_size,
            "status": self.status_message
        }

    def __str__(self):
        return (
            f"[{self.algorithm}] Path Found: {self.path_found} | "
            f"Path Length: {self.path_length} | "
            f"Nodes Visited: {self.nodes_visited} | "
            f"Time: {self.execution_time*1000:.3f} ms | "
            f"Max Frontier: {self.max_frontier_size}"
        )
