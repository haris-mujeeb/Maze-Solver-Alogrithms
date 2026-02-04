# Path Planning Algorithms

This document provides a detailed overview of the path planning algorithms implemented in this project.

## A* (A-Star)

A* is an informed search algorithm, or a "best-first search", meaning that it is formulated in terms of weighted graphs: starting from a specific starting node of a graph, it aims to find a path to the given goal node having the smallest cost (least distance travelled, shortest time, etc.). It does this by maintaining a tree of paths originating at the start node and extending those paths one edge at a time until its termination criterion is satisfied.

At each iteration of its main loop, A* needs to determine which of its paths to extend. It does so based on the cost of the path and an estimate of the cost required to extend the path all the way to the goal. Specifically, A* selects the path that minimizes `f(n) = g(n) + h(n)` where `n` is the next node on the path, `g(n)` is the cost of the path from the start node to `n`, and `h(n)` is a heuristic function that estimates the cost of the cheapest path from `n` to the goal.

## Breadth-First Search (BFS)

Breadth-First Search (BFS) is an algorithm for traversing or searching tree or graph data structures. It starts at the tree root (or some arbitrary node of a graph, sometimes referred to as a 'search key') and explores the neighbor nodes first, before moving to the next level neighbors.

BFS is an uninformed search algorithm that does not use any heuristics. It explores all paths of a certain length before moving on to explore paths of a greater length. This guarantees that BFS will find the shortest path in terms of the number of edges, but not necessarily the optimal path in terms of cost.

## Depth-First Search (DFS)

Depth-First Search (DFS) is an algorithm for traversing or searching tree or graph data structures. The algorithm starts at the root node (selecting some arbitrary node as the root node in the case of a graph) and explores as far as possible along each branch before backtracking.

DFS is an uninformed search algorithm. It can be implemented using a stack. The algorithm may not find the shortest path.

## Dijkstra's Algorithm

Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a graph, which may represent, for example, road networks. It was conceived by computer scientist Edsger W. Dijkstra in 1956 and published three years later.

The algorithm exists in many variants. Dijkstra's original algorithm found the shortest path between two given nodes, but a more common variant fixes a single node as the "source" node and finds shortest paths from the source to all other nodes in the graph, producing a shortest-path tree.

## Theta*

Theta* is a variant of A* that can find shorter paths than A* on grids because it is not restricted to moving between adjacent grid cells. Theta* can propagate information along grid edges without constraining the paths to be formed by those edges. It does this by considering any two vertices in the grid graph to be reachable from one another if they are in line-of-sight.

When choosing the successor of a node, Theta* considers the parent of the current node. If the parent is in line-of-sight to the successor, the path is shortened by bypassing the current node.

## Lazy Theta*

Lazy Theta* is a variant of Theta* that is optimized for speed. It's "lazy" in the sense that it doesn't perform line-of-sight checks for every neighbor of the current node. Instead, it assumes there is a line-of-sight and only performs the check when it expands a node from the open list. If the line-of-sight check fails, it finds a new parent for the node and updates its cost. This can save a significant amount of computation, especially in open areas of the map.

## Rapidly-exploring Random Tree (RTT)

The Rapidly-exploring Random Tree (RRT) is a data structure and algorithm that is designed for efficiently searching non-convex, high-dimensional spaces. RRTs are constructed incrementally in a way that biases the search towards unexplored portions of the space.

The algorithm is particularly well-suited for path planning problems where the environment has obstacles and constraints. It builds a tree from a random starting point, and incrementally adds new nodes from random samples in the search space.

## RTT* (RRT-Star)

RTT* is an optimized version of the RRT algorithm. While RRT is designed to efficiently find a feasible path, it does not guarantee that the path will be optimal. RTT* introduces a "rewiring" step that continuously improves the quality of the paths in the tree.

After a new node is added to the tree, RTT* checks if there are any existing nodes in the vicinity that could be reached via a shorter path through the new node. If so, it rewires the tree to connect them through the new node. Additionally, it checks if the new node can be connected to a different parent for a shorter path to the root. This process helps the algorithm to converge towards an optimal path as more samples are added.
