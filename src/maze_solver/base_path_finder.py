from typing import Optional, TypeAlias, List, Any, Deque
from collections import deque
from .grid_map import GridMap, Coord

# --------------------------------------------------
# Type aliases
# --------------------------------------------------

Path: TypeAlias = List[Coord]

# --------------------------------------------------
# Maze Generator
# --------------------------------------------------


class BasePlanner:
    def __init__(self, grid_map: GridMap, start: Coord, goal: Coord):
        self.grid_map = grid_map
        self.start_coord: Coord = start
        self.goal_cood: Coord = goal
        self.frontier: Deque[Any] = deque()
        self.current: Optional[Coord] = None

    def start(self) -> None:
        """Run planning and return path (list of coords) or None."""
        raise NotImplementedError

    def step(self) -> bool:
        """Run planning and return path (list of coords) or None."""
        raise NotImplementedError

    def find_path(self) -> Optional[Path]:
        """Run planning and return path (list of coords) or None."""
        raise NotImplementedError
