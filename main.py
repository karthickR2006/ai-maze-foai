"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          main.py
Description:   Main entry point of the application. Supports interactive
               Tkinter GUI visualization, terminal CLI demonstration, and
               automated test suite execution.
=============================================================================
"""

import sys
import os

# Add local directory to module search path to allow running from any working dir
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from maze import Maze
from bfs import solve_bfs
from dfs import solve_dfs


def run_cli_demo():
    """
    Runs a terminal-based demonstration of the maze solver.
    Useful for quick command-line verification or environments without GUI displays.
    """
    print("=" * 70)
    print("AI-BASED MAZE SOLVER: BFS VS. DFS (TERMINAL DEMO)")
    print("=" * 70)

    # 1. Initialize Maze
    maze = Maze(rows=15, cols=15)
    maze.load_preset("Classic Academic")

    print("\nInitial Maze Grid (S = Start, G = Goal, # = Wall, . = Empty):")
    print("-" * 50)
    print(maze.get_ascii_display())
    print("-" * 50)

    # 2. Run BFS
    print("\nExecuting Breadth-First Search (BFS)...")
    bfs_result = solve_bfs(maze.grid, maze.start, maze.goal)
    print(f"  • Path Found:       {bfs_result.path_found}")
    print(f"  • Path Length:      {bfs_result.path_length} steps (Optimal shortest path)")
    print(f"  • Nodes Visited:    {bfs_result.nodes_visited}")
    print(f"  • Max Frontier:     {bfs_result.max_frontier_size}")
    print(f"  • Execution Time:   {bfs_result.execution_time * 1000:.4f} ms")

    # 3. Run DFS
    print("\nExecuting Depth-First Search (DFS)...")
    dfs_result = solve_dfs(maze.grid, maze.start, maze.goal)
    print(f"  • Path Found:       {dfs_result.path_found}")
    print(f"  • Path Length:      {dfs_result.path_length} steps (May be non-optimal)")
    print(f"  • Nodes Visited:    {dfs_result.nodes_visited}")
    print(f"  • Max Frontier:     {dfs_result.max_frontier_size}")
    print(f"  • Execution Time:   {dfs_result.execution_time * 1000:.4f} ms")

    # 4. Comparative Analysis Table
    print("\n" + "=" * 70)
    print(f"{'METRIC':<25} {'BFS (Queue)':<20} {'DFS (Stack)':<20}")
    print("=" * 70)
    print(f"{'Path Found':<25} {str(bfs_result.path_found):<20} {str(dfs_result.path_found):<20}")
    print(f"{'Path Length':<25} {str(bfs_result.path_length) + ' (Optimal)':<20} {str(dfs_result.path_length):<20}")
    print(f"{'Nodes Visited':<25} {str(bfs_result.nodes_visited):<20} {str(dfs_result.nodes_visited):<20}")
    print(f"{'Max Frontier Size':<25} {str(bfs_result.max_frontier_size):<20} {str(dfs_result.max_frontier_size):<20}")
    print(f"{'Execution Time':<25} {f'{bfs_result.execution_time*1000:.3f} ms':<20} {f'{dfs_result.execution_time*1000:.3f} ms':<20}")
    print(f"{'Optimality Guarantee':<25} {'YES (Shortest)':<20} {'NO':<20}")
    print(f"{'Frontier Structure':<25} {'FIFO Queue':<20} {'LIFO Stack':<20}")
    print("=" * 70)


def main():
    """
    Evaluates command-line flags or starts the full Tkinter GUI.
    """
    if len(sys.argv) > 1:
        flag = sys.argv[1].lower()
        if flag in ("--cli", "-c", "cli"):
            run_cli_demo()
            return
        elif flag in ("--test", "-t", "test"):
            from test_solver import run_all_tests
            run_all_tests()
            return
        elif flag in ("--help", "-h"):
            print("Usage: python main.py [OPTION]")
            print("Options:")
            print("  (no args)  Launch graphical Tkinter user interface")
            print("  --cli      Run terminal text demonstration of BFS and DFS")
            print("  --test     Execute comprehensive academic test suite")
            print("  --help     Show this help message")
            return

    # Default: Launch Tkinter GUI
    try:
        import tkinter
        from gui import MazeApp
        app = MazeApp()
        app.mainloop()
    except Exception as e:
        print(f"[Notice] Could not initialize graphical GUI: {e}")
        print("Falling back to terminal CLI demonstration mode...\n")
        run_cli_demo()


if __name__ == "__main__":
    main()
