# VIVA VOCE EXAMINATION PREPARATION GUIDE

## Subject: Foundations of Artificial Intelligence
## Project: AI-Based Maze Solver Using Breadth-First Search and Depth-First Search

---

### Q1. What is Artificial Intelligence (AI)?
**Answer:**  
Artificial Intelligence is the branch of computer science dedicated to building systems and software that can perform tasks normally requiring human intelligence. Examples include reasoning, learning, decision-making, problem-solving, and path-finding.

---

### Q2. What is a search algorithm in AI?
**Answer:**  
In AI, a search algorithm is a step-by-step technique that an autonomous agent uses to explore a state space (set of all possible configurations) from an **Initial State** to reach a desired **Goal State** through a sequence of valid actions.

---

### Q3. What is an uninformed search (blind search)?
**Answer:**  
An uninformed search is a search strategy that has no prior knowledge or heuristic estimate about how far a state is from the goal. It can only distinguish between a goal state and a non-goal state and generate adjacent successors. Examples are **Breadth-First Search (BFS)** and **Depth-First Search (DFS)**.

---

### Q4. What is Breadth-First Search (BFS)?
**Answer:**  
Breadth-First Search is an uninformed search algorithm that starts at the initial node and systematically explores all neighboring nodes at the current depth level before moving to the next deeper level.

---

### Q5. What is Depth-First Search (DFS)?
**Answer:**  
Depth-First Search is an uninformed search algorithm that starts at the initial node and plunges deeply along a single path as far as possible until it reaches a dead-end, after which it backtracks to explore alternate branches.

---

### Q6. Why does BFS use a Queue data structure?
**Answer:**  
BFS uses a **First-In, First-Out (FIFO) Queue** because nodes must be expanded in the exact order they are discovered. This FIFO ordering guarantees that all nodes at distance $k$ are processed and removed from the queue before any node at distance $k+1$ is expanded.

---

### Q7. Why does DFS use a Stack data structure?
**Answer:**  
DFS uses a **Last-In, First-Out (LIFO) Stack** (or recursion) because it needs to explore the most recently discovered node first. When a dead-end is encountered, popping from the stack naturally backtracks to the previous decision point.

---

### Q8. Which algorithm guarantees finding the shortest path in an unweighted maze?
**Answer:**  
**Breadth-First Search (BFS)**. Because every step in an unweighted maze has an equal cost of 1, BFS explores concentric circles outward from the start. The first time it discovers the goal, it is mathematically guaranteed to be the shortest path in terms of steps.

---

### Q9. Does DFS always find the shortest path? Why or why not?
**Answer:**  
**No, DFS does not guarantee the shortest path.** DFS plunges down whichever branch direction is evaluated first. If that branch happens to reach the goal after a long, meandering detour, DFS will return that path without ever checking if a much shorter shortcut existed along an unexpanded branch.

---

### Q10. What is backtracking in DFS?
**Answer:**  
Backtracking is the process of reversing back up the search path when the algorithm reaches a dead-end (a cell with no unvisited, passable neighbors). In stack terms, this happens when the top node is popped and the algorithm resumes from the previous parent node.

---

### Q11. What is the purpose of a Visited Set?
**Answer:**  
A visited set keeps track of all grid cells that have already been enqueued, pushed, or expanded. This prevents the search algorithm from entering **infinite loops** caused by cycles in the grid (e.g., oscillating back and forth between two adjacent empty cells).

---

### Q12. Why do we store Parent pointers for each node?
**Answer:**  
When an algorithm discovers the goal, it only knows that the goal exists; it does not inherently remember the exact sequence of steps taken to get there. Storing a dictionary mapping each node to its parent (`Parent[child] = parent`) allows us to trace backward from the Goal to the Start to extract the final route.

---

### Q13. How does Path Reconstruction work?
**Answer:**  
Path reconstruction starts at the **Goal** node and repeatedly looks up its parent pointer until it reaches the **Start** node:  
$$\text{Goal} \rightarrow \text{Parent}(\text{Goal}) \rightarrow \text{Parent}(\text{Parent}(\text{Goal})) \rightarrow \dots \rightarrow \text{Start}$$  
This sequence is then reversed to produce the chronological path:  
$$\text{Start} \rightarrow \dots \rightarrow \text{Goal}$$

---

### Q14. What are the Time and Space Complexities of BFS on a 2D grid maze?
**Answer:**  
- **Time Complexity:** $\mathcal{O}(V + E)$, where $V = \text{Rows} \times \text{Cols}$ is the total number of cells, and $E \le 4V$ is the number of valid orthogonal edges. In the worst case, BFS visits every reachable cell once.
- **Space Complexity:** $\mathcal{O}(V)$, because the visited set and the FIFO queue frontier can hold up to $\mathcal{O}(V)$ cells in memory simultaneously.

---

### Q15. What are the Time and Space Complexities of DFS on a 2D grid maze?
**Answer:**  
- **Time Complexity:** $\mathcal{O}(V + E)$, visiting all accessible cells in the worst case.
- **Space Complexity:** $\mathcal{O}(V)$ with a visited set. In a pure tree search without a visited set, DFS space is $\mathcal{O}(b \cdot m)$, where $b$ is the branching factor and $m$ is maximum depth.

---

### Q16. What are the main limitations of BFS?
**Answer:**  
The main limitation of BFS is **high memory consumption**. Because BFS expands level by level, the size of the queue (the frontier) grows exponentially with depth in high-branching search spaces, which can exhaust RAM on very large problems.

---

### Q17. What are the main limitations of DFS?
**Answer:**  
1. **Non-optimal:** It rarely finds the shortest path.
2. **Susceptibility to infinite paths:** In infinite or deep graphs without cycle checking, DFS can get trapped down an endless branch and never terminate.

---

### Q18. Why is solving a maze considered an AI problem?
**Answer:**  
A maze solver represents a **Goal-Based Problem-Solving Agent**. The agent must formulate a problem (State Space, Actions, Transition Model, Goal Test, Path Cost) and systematically search through alternative candidate futures to reach an objective without human intervention. This embodies the foundational principles of automated reasoning and planning in AI.

---

### Q19. What happens if no path exists between Start and Goal?
**Answer:**  
Both BFS and DFS will systematically explore all reachable open cells until their respective frontiers (queue or stack) become completely empty. When the frontier empties without ever encountering the Goal, the algorithm terminates gracefully, sets `path_found = False`, and alerts the user that no path exists.

---

### Q20. How can this project be extended or improved?
**Answer:**  
1. **Informed Search:** Implement **$A^*$ Search** and **Greedy Best-First Search** using the **Manhattan Distance** heuristic ($|x_1 - x_2| + |y_1 - y_2|$) to show how heuristics speed up goal discovery.
2. **Weighted Terrain:** Implement **Dijkstra's Algorithm** for cells with varied movement costs (e.g., mud, water).
3. **Dynamic Mazes:** Add moving obstacles that force dynamic path replanning.
