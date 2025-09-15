# Breadth-First Search explores all nodes at the current depth before moving to the next level. It uses a queue (FIFO) to keep track of nodes, ensuring that the shortest path is found in an unweighted graph.

# Key Features:
    # Guarantees the shortest path if the cost is uniform.
    # Uses more memory as it stores all child nodes.\
    # Code Implementation:

# The bfs() function finds the shortest path in a 2D maze using the Breadth-First Search (BFS) algorithm.
    # It starts from a given position and explores neighbors (up, down, left, right).
    # A queue stores positions along with the path taken.
    # A visited set prevents revisiting positions.
    # If the goal is reached, the function returns the complete path; otherwise, it returns None.
# The visualize_maze() function displays the maze and the found path using Matplotlib.
    # Different colors represent open paths, obstacles, start, goal, and the solution path.
    # imshow() displays the maze, and scatter() marks key positions.

import networkx as nx
import matplotlib.pyplot as plt
import heapq

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def uniform_cost_search(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, Node(start))
    explored = set()
    path = []
    
    while frontier:
        node = heapq.heappop(frontier)
        
        if node.state == goal:
            path = reconstruct_path(node)
            break
        
        explored.add(node.state)
        
        for (cost, result_state) in graph[node.state]:
            if result_state not in explored:
                child_cost = node.path_cost + cost
                child_node = Node(result_state, node, None, child_cost)
                if not any(frontier_node.state == result_state and 
                           frontier_node.path_cost <= child_cost for frontier_node in frontier):
                    heapq.heappush(frontier, child_node)
                    
    return path

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def visualize_graph(graph, path=None):
    G = nx.DiGraph()
    labels = {}
    for node, edges in graph.items():
        for cost, child_node in edges:
            G.add_edge(node, child_node, weight=cost)
            labels[(node, child_node)] = cost
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
    
    plt.show()

# Define the graph
graph = {
    'A': [(1, 'B'), (3, 'C')],
    'B': [(2, 'D')],
    'C': [(5, 'D'), (2, 'B')],
    'D': []
}

start = 'A'
goal = 'D'
path = uniform_cost_search(graph, start, goal)

visualize_graph(graph, path)
print("Path from", start, "to", goal, ":", path)