import random
from typing import Optional, Deque, List, Set
from .grid_map import Grid, Coord, GridMap

# --------------------------------------------------
# Maze Generator
# --------------------------------------------------


class MazeGenerator:
    """
    Maze / map generator using DFS, BFS or Wilson's algorithm carving.

    Grid convention:
        1 = wall
        0 = walkable
    """

    def __init__(self, rows: int, cols: int):
        if rows % 2 == 0 or cols % 2 == 0:
            raise ValueError("Rows and columns must be odd numbers")

        self.rows = rows
        self.cols = cols
        self.grid: Grid = [[1 for _ in range(cols)] for _ in range(rows)]

        self.frontier: Deque[Coord] = Deque()
        self.current: Optional[Coord] = None
        self.mode: Optional[str] = None

        # For Wilson's algorithm
        self.cells: List[Coord] = []
        self.unvisited: Set[Coord] = set()
        self.current_walk: List[Coord] = []

    def start(self, start: Coord, mode: str = "DFS") -> None:
        """
        Start generating a map.

        mode: "EMPTY", "DFS", "BFS", "WILSON"
        """        

        self.mode = mode.upper()

        if self.mode == "EMPTY":
            for r in range(1, self.rows - 1):
                for c in range(1, self.cols - 1):
                    self.grid[r][c] = 0
            return

        if self.mode == "WILSON":
            self._start_wilson()
            return

        r, c = start

        # Snap to odd coordinates
        r = r if r % 2 == 1 else r - 1
        c = c if c % 2 == 1 else c - 1

        pos: Coord = (r, c)

        if not self._in_bounds(pos):
            raise ValueError("Start position out of bounds")

        self.grid[r][c] = 0
        self.frontier.clear()
        self.frontier.append(pos)
        self.current = pos

    def step(self) -> bool:
        """
        Perform ONE carving step.
        Returns False when generation is complete.
        """

        if self.mode == "EMPTY":
            return False

        if self.mode == "WILSON":
            return self._step_wilson()

        if not self.frontier:
            return False

        if self.mode == "DFS":
            pos = self.frontier.pop()
        elif self.mode == "BFS":
            pos = self.frontier.popleft()
        else:
            raise ValueError(f"Invalid mode: {self.mode}")

        self.current = pos
        neighbors = list(self._unvisited_neighbors(pos))

        if neighbors:
            nxt = random.choice(neighbors)
            wall = self._midpoint(pos, nxt)

            self.grid[wall[0]][wall[1]] = 0
            self.grid[nxt[0]][nxt[1]] = 0

            self.frontier.append(pos)
            self.frontier.append(nxt)

        return True

    def generate_full(self, start: Coord, mode: str = "DFS") -> GridMap:
        """
        Generate the full map in one go (no stepping).
        """
        self.start(start, mode)
        while self.step():
            pass
        return GridMap(self.grid)

    # --------------------------------------------------
    # Wilson's Algorithm
    # --------------------------------------------------

    def _start_wilson(self):
        self.cells = []
        for r in range(1, self.rows, 2):
            for c in range(1, self.cols, 2):
                self.cells.append((r, c))

        self.unvisited = set(self.cells)

        # 1. Pick a random cell, mark as visited.
        first_cell = random.choice(self.cells)
        self.grid[first_cell[0]][first_cell[1]] = 0
        self.unvisited.remove(first_cell)

        self.current_walk.clear()
        self.current = None
        self.frontier.clear()

    def _step_wilson(self) -> bool:
        if not self.unvisited:
            self.current = None
            self.frontier.clear()
            self.current_walk.clear()
            return False

        if not self.current_walk:
            # Start a new walk from a random unvisited cell
            walk_start = random.choice(list(self.unvisited))
            self.current_walk.append(walk_start)
            self.current = walk_start
            self.frontier.append(walk_start)
            return True

        current_pos = self.current_walk[-1]

        neighbors = self._get_all_neighbors(current_pos)
        next_pos = random.choice(neighbors)

        self.current = next_pos

        if next_pos in self.current_walk:
            # Loop detected, erase it
            idx = self.current_walk.index(next_pos)

            # Remove from frontier for visualization
            for i in range(idx + 1, len(self.current_walk)):
                self.frontier.remove(self.current_walk[i])

            self.current_walk = self.current_walk[: idx + 1]
        else:
            self.current_walk.append(next_pos)
            self.frontier.append(next_pos)

        # Check if the walk has hit the maze
        if self.grid[next_pos[0]][next_pos[1]] == 0:
            # Carve path into the maze
            for i in range(len(self.current_walk) - 1):
                pos_a = self.current_walk[i]
                pos_b = self.current_walk[i + 1]

                self.grid[pos_a[0]][pos_a[1]] = 0
                wall = self._midpoint(pos_a, pos_b)
                self.grid[wall[0]][wall[1]] = 0
                self.unvisited.discard(pos_a)

            self.unvisited.discard(self.current_walk[-1])

            self.current_walk.clear()
            self.frontier.clear()

        return True

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _get_all_neighbors(self, pos: Coord) -> List[Coord]:
        r, c = pos
        neighbors = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nxt = (r + dr, c + dc)
            if self._in_bounds(nxt):
                neighbors.append(nxt)
        return neighbors

    def _unvisited_neighbors(self, pos: Coord):
        r, c = pos
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nxt = (r + dr, c + dc)
            if self._in_bounds(nxt) and self.grid[nxt[0]][nxt[1]] == 1:
                yield nxt

    def _in_bounds(self, pos: Coord) -> bool:
        r, c = pos
        return 1 <= r < self.rows - 1 and 1 <= c < self.cols - 1

    @staticmethod
    def _midpoint(a: Coord, b: Coord) -> Coord:
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2

    def get_grid_map(self) -> GridMap:
        return GridMap(self.grid)