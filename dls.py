# Depth Limited Search (DLS) is a variation of Depth First Search (DFS) that limits the depth of exploration to prevent infinite loops in large or infinite search spaces.

# Key Features:
    # Useful when the goal depth is known.
    # Cannot find solutions beyond the depth limit.


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
    """Performs Depth-Limited Search (DFS with a depth cap).
    Returns path (list of coordinates) from start to goal inclusive, or None if not found within limit.
    """
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
        # allow node to be revisited in other branches
        visited.remove(node)
        return None

    return dls(start, 0, [], set())


# Simple visualizer (same coordinate convention as the search code)
def visualize_maze(maze: Maze, start: Coord, goal: Coord, path: Optional[List[Coord]] = None, title: str = 'DLS'):
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

    limit = 6  # try different limits; small limits may fail
    print(f"Running DLS with limit={limit}...")
    path = depth_limited_search(maze, start, goal, limit)
    print("Path found?", bool(path))
    if path:
        print("Path length:", len(path))
    visualize_maze(maze, start, goal, path, title=f'DLS (limit={limit})')
