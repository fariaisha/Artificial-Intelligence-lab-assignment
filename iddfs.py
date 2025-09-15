# Iterative Deepening Depth-First Search (IDDFS) combines Breadth-First Search (BFS) and Depth First Search (DFS) by running Depth First Search (DFS) with increasing depth limits until a solution is found.

# Key Features:
    # Ensures completeness and optimality like Breadth-First Search (BFS).
    # Uses less memory than Breadth-First Search (BFS).

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from typing import List, Optional, Tuple, Set

Coord = Tuple[int, int]
Maze = np.ndarray


def get_neighbors(maze: Maze, node: Coord) -> List[Coord]:
    r, c = node
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1] and maze[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors


def depth_limited_search(maze: Maze, start: Coord, goal: Coord, limit: int) -> Optional[List[Coord]]:
    """Helper DLS used by IDDFS. Keeps visited as a stack-style set to allow revisits across branches."""
    def dls(node: Coord, depth: int, path: List[Coord], visited: Set[Coord]) -> Optional[List[Coord]]:
        if depth > limit:
            return None
        if node == goal:
            return path + [node]
        visited.add(node)
        for n in get_neighbors(maze, node):
            if n in visited:
                continue
            res = dls(n, depth + 1, path + [node], visited)
            if res is not None:
                return res
        visited.remove(node)
        return None

    return dls(start, 0, [], set())


def iddfs(maze: Maze, start: Coord, goal: Coord, max_depth: int = 50) -> Optional[List[Coord]]:
    """Iterative deepening: run DLS with increasing limits until goal found or max_depth reached."""
    for depth in range(max_depth + 1):
        res = depth_limited_search(maze, start, goal, depth)
        if res is not None:
            return res
    return None


# Visualization (same simple visualizer used across files)
def visualize_maze(maze: Maze, start: Coord, goal: Coord, path: Optional[List[Coord]] = None, title: str = 'IDDFS'):
    cmap = ListedColormap(['white', 'black'])
    fig, ax = plt.subplots()
    ax.imshow(maze, cmap=cmap, origin='upper')
    ax.set_title(title)
    ax.scatter(start[1], start[0], color='yellow', marker='o', s=80, label='Start')
    ax.scatter(goal[1], goal[0], color='purple', marker='o', s=80, label='Goal')
    if path:
        for node in path[1:-1]:
            ax.scatter(node[1], node[0], color='green', marker='o', s=30)
        ys = [p[0] for p in path]
        xs = [p[1] for p in path]
        ax.plot(xs, ys, linewidth=2, linestyle='-', alpha=0.8)
    ax.legend()
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == '__main__':
    maze = np.array([
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ])

    start = (0, 0)
    goal = (4, 4)

    print("Running IDDFS (iterative deepening)...")
    path = iddfs(maze, start, goal, max_depth=20)
    print("Path found?", bool(path))
    if path:
        print("Path length:", len(path))
    visualize_maze(maze, start, goal, path, title='IDDFS (max_depth=20)')
