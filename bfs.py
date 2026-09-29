"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          bfs.py
Description:   Breadth-First Search (BFS) algorithm implementation from scratch.
               Includes both instantaneous batch execution and a generator for
               interactive step-by-step GUI animation.
=============================================================================
"""

import time
from collections import deque
from utils import in_bounds, get_neighbors, reconstruct_path, SearchResult, WALL


def solve_bfs(grid: list, start: tuple, goal: tuple) -> SearchResult:
    """
    Solves the maze using Breadth-First Search (BFS).
    
    Theoretical Properties:
    - Strategy: Uninformed search, explores shallowest unexpanded nodes first.
    - Data Structure: FIFO Queue (collections.deque).
    - Completeness: Complete (always finds a solution if one exists in a finite state space).
    - Optimality: Optimal for unweighted graphs (guaranteed to find the shortest path).
    - Time Complexity: O(V + E) where V = nodes (rows * cols), E = orthogonal edges.
    - Space Complexity: O(V) to store visited set and queue frontier.

    Args:
        grid: 2D list representing the maze (0 = empty, 1 = wall).
        start: Tuple (start_row, start_col).
        goal: Tuple (goal_row, goal_col).

    Returns:
        SearchResult object containing path, visited nodes, execution time, etc.
    """
    result = SearchResult("BFS")
    total_rows = len(grid)
    total_cols = len(grid[0]) if total_rows > 0 else 0

    # Validation of start and goal
    if not in_bounds(start[0], start[1], total_rows, total_cols) or \
       not in_bounds(goal[0], goal[1], total_rows, total_cols):
        result.status_message = "Start or Goal position is out of grid bounds."
        return result

    if grid[start[0]][start[1]] == WALL or grid[goal[0]][goal[1]] == WALL:
        result.status_message = "Start or Goal position is located on a wall."
        return result

    start_time = time.perf_counter()

    # Trivial case: Start is already Goal
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

    # 1. Initialize FIFO Queue with the Start node
    queue = deque([start])

    # 2. Maintain a Visited Set to prevent redundant cycles
    visited = {start}

    # 3. Parent mapping for path reconstruction: child -> parent
    parent = {start: None}

    # 4. Tracking exploration history
    order_of_visit = []
    max_frontier = 1

    found = False

    # 5. Core BFS Loop (FIFO)
    while queue:
        # Track maximum frontier size for space complexity analysis
        if len(queue) > max_frontier:
            max_frontier = len(queue)

        # Dequeue the oldest node in the queue (FIFO)
        current = queue.popleft()
        order_of_visit.append(current)

        # Check if Goal is reached
        if current == goal:
            found = True
            break

        # Explore all valid orthogonal neighbors (Up, Right, Down, Left)
        for neighbor in get_neighbors(current[0], current[1], total_rows, total_cols, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    end_time = time.perf_counter()

    result.execution_time = end_time - start_time
    result.nodes_visited = len(order_of_visit)
    result.visited_order = order_of_visit
    result.max_frontier_size = max_frontier

    if found:
        # 6. Reconstruct shortest path by backtracking parent pointers
        path = reconstruct_path(parent, start, goal)
        result.path_found = True
        result.path = path
        result.path_length = len(path) - 1  # Number of movement steps
        result.status_message = f"Goal reached! Optimal path found ({result.path_length} steps)."
    else:
        result.path_found = False
        result.path = []
        result.path_length = 0
        result.status_message = "No path exists to the Goal (frontier exhausted)."

    return result


def bfs_step_generator(grid: list, start: tuple, goal: tuple):
    """
    Python Generator yielding BFS search progress step-by-step for UI animation.
    
    Yields:
        ('visit', current_node, current_visited_count, frontier_size)
        ('found', final_path, result_obj)
        ('not_found', result_obj)
        ('error', error_message)
    """
    total_rows = len(grid)
    total_cols = len(grid[0]) if total_rows > 0 else 0
    result = SearchResult("BFS")

    # Guard checks
    if not in_bounds(start[0], start[1], total_rows, total_cols) or \
       not in_bounds(goal[0], goal[1], total_rows, total_cols):
        yield ('error', "Start or Goal is out of bounds.")
        return

    if grid[start[0]][start[1]] == WALL or grid[goal[0]][goal[1]] == WALL:
        yield ('error', "Start or Goal is inside a wall.")
        return

    start_time = time.perf_counter()

    # Immediate start == goal check
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

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    order_of_visit = []
    max_frontier = 1
    found = False

    while queue:
        if len(queue) > max_frontier:
            max_frontier = len(queue)

        current = queue.popleft()
        order_of_visit.append(current)

        # Yield node expansion event to Tkinter GUI
        yield ('visit', current, len(order_of_visit), len(queue))

        if current == goal:
            found = True
            break

        for neighbor in get_neighbors(current[0], current[1], total_rows, total_cols, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

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
        result.status_message = f"Goal reached! Optimal path found ({result.path_length} steps)."
        yield ('found', path, result)
    else:
        result.path_found = False
        result.path = []
        result.path_length = 0
        result.status_message = "No path exists from Start to Goal."
        yield ('not_found', result)
