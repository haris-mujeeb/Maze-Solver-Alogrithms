from typing import TypeAlias, List, Tuple

# --------------------------------------------------
# Type aliases
# --------------------------------------------------

Coord: TypeAlias = Tuple[int, int]
Grid: TypeAlias = List[List[int]]


# --------------------------------------------------
# Grid Map
# --------------------------------------------------


class GridMap:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def in_bounds(self, pos: Coord) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, pos: Coord) -> bool:
        r, c = pos
        return self.grid[r][c] == 0

    def neighbours(self, pos: Coord):
        r, c = pos
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nxt = (r + dr, c + dc)
                if self.in_bounds(nxt):
                    yield nxt

    def walkable_cells(self) -> List[Coord]:
        return [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self.grid[r][c] == 0
        ]
