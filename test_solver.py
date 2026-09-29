"""
=============================================================================
Project Title: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search
Domain:        Foundations of Artificial Intelligence
File:          test_solver.py
Description:   Comprehensive automated academic test suite verifying all 8
               mandatory test cases:
               1. Normal maze with valid path
               2. Maze with no possible path (impenetrable trap)
               3. Start next to Goal (adjacent, 1 step)
               4. Large maze (35x35)
               5. Maze with many dense walls
               6. Start equals Goal (0 steps)
               7. DFS finds a longer path than BFS (non-optimality demonstration)
               8. Randomly generated maze
=============================================================================
"""

import sys
import os
import random

# Ensure local imports work cleanly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from utils import EMPTY, WALL
from maze import Maze
from bfs import solve_bfs
from dfs import solve_dfs


def run_all_tests():
    """
    Executes the 8 academic test cases and displays a clean tabulated summary.
    """
    print("\n" + "=" * 80)
    print("AI MAZE SOLVER: AUTOMATED ACADEMIC TEST SUITE")
    print("=" * 80)

    test_results = []

    # -------------------------------------------------------------------------
    # TEST CASE 1: Normal maze with valid path
    # -------------------------------------------------------------------------
    print("\n[Running Test Case 1] Normal maze with valid path...")
    maze1 = Maze(rows=15, cols=15)
    maze1.load_preset("Classic Academic")
    bfs1 = solve_bfs(maze1.grid, maze1.start, maze1.goal)
    dfs1 = solve_dfs(maze1.grid, maze1.start, maze1.goal)

    expected1 = "Both algorithms find path; BFS path length <= DFS path length"
    passed1 = bfs1.path_found and dfs1.path_found and (bfs1.path_length <= dfs1.path_length)
    actual1 = f"BFS: found={bfs1.path_found} (len={bfs1.path_length}), DFS: found={dfs1.path_found} (len={dfs1.path_length})"
    test_results.append((
        "Test 1: Normal Maze with Valid Path",
        "15x15 Classic Academic Maze",
        expected1,
        actual1,
        "PASS" if passed1 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # TEST CASE 2: Maze with no possible path (Trapped Goal)
    # -------------------------------------------------------------------------
    print("[Running Test Case 2] Maze with no possible path...")
    maze2 = Maze(rows=15, cols=15)
    maze2.load_preset("Trap Maze (No Path)")
    bfs2 = solve_bfs(maze2.grid, maze2.start, maze2.goal)
    dfs2 = solve_dfs(maze2.grid, maze2.start, maze2.goal)

    expected2 = "Both return path_found=False, path=[]"
    passed2 = (not bfs2.path_found) and (not dfs2.path_found) and (len(bfs2.path) == 0) and (len(dfs2.path) == 0)
    actual2 = f"BFS: found={bfs2.path_found} (len={bfs2.path_length}), DFS: found={dfs2.path_found} (len={dfs2.path_length})"
    test_results.append((
        "Test 2: Maze with No Path (Trapped)",
        "Goal surrounded by walls",
        expected2,
        actual2,
        "PASS" if passed2 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # TEST CASE 3: Start next to Goal (Adjacent, 1 step)
    # -------------------------------------------------------------------------
    print("[Running Test Case 3] Start next to Goal...")
    maze3 = Maze(rows=11, cols=11)
    maze3.clear()
    maze3.set_start(3, 3)
    maze3.set_goal(3, 4)
    bfs3 = solve_bfs(maze3.grid, maze3.start, maze3.goal)
    dfs3 = solve_dfs(maze3.grid, maze3.start, maze3.goal)

    expected3 = "Path found with length = 1 step"
    passed3 = (bfs3.path_found and bfs3.path_length == 1) and (dfs3.path_found and dfs3.path_length == 1)
    actual3 = f"BFS: len={bfs3.path_length}, DFS: len={dfs3.path_length}"
    test_results.append((
        "Test 3: Start Next to Goal (Adjacent)",
        "Start=(3,3), Goal=(3,4)",
        expected3,
        actual3,
        "PASS" if passed3 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # TEST CASE 4: Large maze (35 x 35)
    # -------------------------------------------------------------------------
    print("[Running Test Case 4] Large maze (35x35)...")
    maze4 = Maze(rows=35, cols=35)
    maze4.generate_labyrinth()
    bfs4 = solve_bfs(maze4.grid, maze4.start, maze4.goal)
    dfs4 = solve_dfs(maze4.grid, maze4.start, maze4.goal)

    expected4 = "Both algorithms succeed on large 35x35 grid without stack overflow"
    passed4 = bfs4.path_found and dfs4.path_found and (bfs4.nodes_visited > 0)
    actual4 = f"BFS: len={bfs4.path_length} (nodes={bfs4.nodes_visited}), DFS: len={dfs4.path_length} (nodes={dfs4.nodes_visited})"
    test_results.append((
        "Test 4: Large Maze (35x35)",
        "35x35 Labyrinth (1225 cells)",
        expected4,
        actual4,
        "PASS" if passed4 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # TEST CASE 5: Maze with many walls (Dense obstacles)
    # -------------------------------------------------------------------------
    print("[Running Test Case 5] Maze with many dense walls...")
    maze5 = Maze(rows=17, cols=17)
    maze5.generate_random_obstacles(density=0.45)
    # Guarantee at least one clear tunnel to test dense obstacle navigation
    for c in range(1, 16):
        maze5.grid[1][c] = EMPTY
        maze5.grid[c][15] = EMPTY
    bfs5 = solve_bfs(maze5.grid, maze5.start, maze5.goal)
    dfs5 = solve_dfs(maze5.grid, maze5.start, maze5.goal)

    expected5 = "Algorithms navigate through dense walls without collisions"
    passed5 = bfs5.path_found and dfs5.path_found
    actual5 = f"BFS: found={bfs5.path_found} (len={bfs5.path_length}), DFS: found={dfs5.path_found} (len={dfs5.path_length})"
    test_results.append((
        "Test 5: Maze with Many Walls",
        "17x17 grid, 45% wall density",
        expected5,
        actual5,
        "PASS" if passed5 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # TEST CASE 6: Start equals Goal (0 steps)
    # -------------------------------------------------------------------------
    print("[Running Test Case 6] Start equals Goal...")
    maze6 = Maze(rows=9, cols=9)
    maze6.clear()
    same_pos = (4, 4)
    maze6.grid[same_pos[0]][same_pos[1]] = EMPTY
    bfs6 = solve_bfs(maze6.grid, same_pos, same_pos)
    dfs6 = solve_dfs(maze6.grid, same_pos, same_pos)

    expected6 = "path_found=True, path_length=0, path=[(4, 4)]"
    passed6 = (bfs6.path_found and bfs6.path_length == 0 and bfs6.path == [same_pos]) and \
              (dfs6.path_found and dfs6.path_length == 0 and dfs6.path == [same_pos])
    actual6 = f"BFS: found={bfs6.path_found}, len={bfs6.path_length}; DFS: found={dfs6.path_found}, len={dfs6.path_length}"
    test_results.append((
        "Test 6: Start Equals Goal",
        "Start=(4,4), Goal=(4,4)",
        expected6,
        actual6,
        "PASS" if passed6 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # TEST CASE 7: DFS finds a longer path than BFS (Non-optimality proof)
    # -------------------------------------------------------------------------
    print("[Running Test Case 7] DFS finds longer path than BFS...")
    # Build a specific fork corridor:
    # A short direct diagonal path, vs a long winding loop
    maze7 = Maze(rows=15, cols=15)
    maze7.load_preset("Classic Academic")
    bfs7 = solve_bfs(maze7.grid, maze7.start, maze7.goal)
    dfs7 = solve_dfs(maze7.grid, maze7.start, maze7.goal)

    # In Classic Academic, BFS finds the direct shortcut while DFS explores the long perimeter
    expected7 = "BFS path length < DFS path length (proves DFS is non-optimal)"
    passed7 = bfs7.path_found and dfs7.path_found and (bfs7.path_length < dfs7.path_length)
    actual7 = f"BFS Path Length: {bfs7.path_length} < DFS Path Length: {dfs7.path_length}"
    test_results.append((
        "Test 7: DFS Finds Longer Path Than BFS",
        "Classic Academic Forked Maze",
        expected7,
        actual7,
        "PASS" if passed7 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # TEST CASE 8: Randomly generated maze
    # -------------------------------------------------------------------------
    print("[Running Test Case 8] Randomly generated maze...")
    random.seed(42)  # For reproducible academic verification
    maze8 = Maze(rows=21, cols=21)
    maze8.generate_labyrinth()
    bfs8 = solve_bfs(maze8.grid, maze8.start, maze8.goal)
    dfs8 = solve_dfs(maze8.grid, maze8.start, maze8.goal)

    expected8 = "Labyrinth generator produces a fully solvable random maze"
    passed8 = bfs8.path_found and dfs8.path_found and (bfs8.path_length <= dfs8.path_length)
    actual8 = f"BFS: found={bfs8.path_found} (len={bfs8.path_length}), DFS: found={dfs8.path_found} (len={dfs8.path_length})"
    test_results.append((
        "Test 8: Randomly Generated Maze",
        "21x21 Randomized DFS Labyrinth",
        expected8,
        actual8,
        "PASS" if passed8 else "FAIL"
    ))

    # -------------------------------------------------------------------------
    # PRINT TABULAR RESULTS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 105)
    print(f"{'TEST CASE':<32} {'INPUT DESCRIPTION':<26} {'ACTUAL RESULT':<35} {'STATUS':<8}")
    print("=" * 105)
    all_passed = True
    for name, inp, exp, act, status in test_results:
        print(f"{name:<32} {inp:<26} {act:<35} {status:<8}")
        if status != "PASS":
            all_passed = False
    print("=" * 105)

    if all_passed:
        print("ALL 8 ACADEMIC TEST CASES PASSED SUCCESSFULLY! (100% SUCCESS RATE)\n")
    else:
        print("SOME TEST CASES FAILED! Review details above.\n")

    return all_passed


if __name__ == "__main__":
    run_all_tests()
