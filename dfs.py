"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          dfs.py
Description:   Depth-First Search (DFS) algorithm implementation from scratch.
               Uses an explicit LIFO Stack to simulate deep exploration and
               backtracking without risk of stack overflow on large grids.
=============================================================================
"""

import time
from utils import in_bounds, get_neighbors, reconstruct_path, SearchResult, WALL


def solve_dfs(grid: list, start: tuple, goal: tuple) -> SearchResult:
    """
    Solves the maze using Depth-First Search (DFS).

    Theoretical Properties:
    - Strategy: Uninformed search, explores the deepest unexpanded node first.
    - Data Structure: LIFO Stack (standard Python list with append/pop).
    - Completeness: Complete in finite state spaces (with a visited set to avoid cycles).
    - Optimality: Non-optimal (does NOT guarantee the shortest path; often finds long, winding paths).
    - Time Complexity: O(V + E) where V = cells, E = orthogonal edges.
    - Space Complexity: O(V) in worst case (e.g. long serpentine corridors).

    Args:
        grid: 2D list representing the maze (0 = empty, 1 = wall).
        start: Tuple (start_row, start_col).
        goal: Tuple (goal_row, goal_col).

    Returns:
        SearchResult object containing path, visited nodes, execution time, etc.
    """
    result = SearchResult("DFS")
    total_rows = len(grid)
    total_cols = len(grid[0]) if total_rows > 0 else 0

    # Validation
    if not in_bounds(start[0], start[1], total_rows, total_cols) or \
       not in_bounds(goal[0], goal[1], total_rows, total_cols):
        result.status_message = "Start or Goal position is out of grid bounds."
        return result

    if grid[start[0]][start[1]] == WALL or grid[goal[0]][goal[1]] == WALL:
        result.status_message = "Start or Goal position is located on a wall."
        return result

    start_time = time.perf_counter()

    # Trivial case: Start is Goal
    if start == goal:
        end_time = time.perf_counter()
        result.path_found = True
        result.path = [start]
        result.path_length = 0
        result.nodes_visited = 1
        result.visited_order = [start]
        result.execution_time = end_time - start_time
        result.max_frontier_size = 1
        result.status_message = "Start equals Goal (0 steps required)."
        return result

    # 1. Initialize LIFO Stack with Start node
    stack = [start]

    # 2. Visited set
    visited = {start}

    # 3. Parent mapping for backtracking: child -> parent
    parent = {start: None}

    # 4. Tracking exploration history
    order_of_visit = []
    max_frontier = 1

    found = False

    # 5. Core DFS Loop (LIFO Stack)
    while stack:
        if len(stack) > max_frontier:
            max_frontier = len(stack)

        # Pop the most recently pushed node (LIFO)
        current = stack.pop()
        order_of_visit.append(current)

        # Check if Goal is reached
        if current == goal:
            found = True
            break

        # Explore neighbors
        # To maintain natural intuitive exploration (Up, Right, Down, Left),
        # when pushing to a LIFO stack we can push in reverse order so the first
        # direction is popped first.
        neighbors = get_neighbors(current[0], current[1], total_rows, total_cols, grid)
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    end_time = time.perf_counter()

    result.execution_time = end_time - start_time
    result.nodes_visited = len(order_of_visit)
    result.visited_order = order_of_visit
    result.max_frontier_size = max_frontier

    if found:
        # Reconstruct path
        path = reconstruct_path(parent, start, goal)
        result.path_found = True
        result.path = path
        result.path_length = len(path) - 1
        result.status_message = f"Goal reached! Path found ({result.path_length} steps - note: not necessarily shortest)."
    else:
        result.path_found = False
        result.path = []
        result.path_length = 0
        result.status_message = "No path exists to the Goal (stack exhausted)."

    return result


def dfs_step_generator(grid: list, start: tuple, goal: tuple):
    """
    Python Generator yielding DFS search progress step-by-step for UI animation.
    
    Yields:
        ('visit', current_node, current_visited_count, frontier_size)
        ('found', final_path, result_obj)
        ('not_found', result_obj)
        ('error', error_message)
    """
    total_rows = len(grid)
    total_cols = len(grid[0]) if total_rows > 0 else 0
    result = SearchResult("DFS")

    if not in_bounds(start[0], start[1], total_rows, total_cols) or \
       not in_bounds(goal[0], goal[1], total_rows, total_cols):
        yield ('error', "Start or Goal is out of bounds.")
        return

    if grid[start[0]][start[1]] == WALL or grid[goal[0]][goal[1]] == WALL:
        yield ('error', "Start or Goal is inside a wall.")
        return

    start_time = time.perf_counter()

    if start == goal:
        result.path_found = True
        result.path = [start]
        result.path_length = 0
        result.nodes_visited = 1
        result.visited_order = [start]
        result.execution_time = time.perf_counter() - start_time
        result.max_frontier_size = 1
        result.status_message = "Start is already at the Goal position."
        yield ('found', [start], result)
        return

    stack = [start]
    visited = {start}
    parent = {start: None}
    order_of_visit = []
    max_frontier = 1
    found = False

    while stack:
        if len(stack) > max_frontier:
            max_frontier = len(stack)

        current = stack.pop()
        order_of_visit.append(current)

        # Yield node visit to Tkinter animation
        yield ('visit', current, len(order_of_visit), len(stack))

        if current == goal:
            found = True
            break

        neighbors = get_neighbors(current[0], current[1], total_rows, total_cols, grid)
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    end_time = time.perf_counter()
    result.execution_time = end_time - start_time
    result.nodes_visited = len(order_of_visit)
    result.visited_order = order_of_visit
    result.max_frontier_size = max_frontier

    if found:
        path = reconstruct_path(parent, start, goal)
        result.path_found = True
        result.path = path
        result.path_length = len(path) - 1
        result.status_message = f"Goal reached! Path found ({result.path_length} steps - non-optimal demonstration)."
        yield ('found', path, result)
    else:
        result.path_found = False
        result.path = []
        result.path_length = 0
        result.status_message = "No path exists from Start to Goal."
        yield ('not_found', result)
