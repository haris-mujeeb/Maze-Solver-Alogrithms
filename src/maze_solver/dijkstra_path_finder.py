from typing import Deque, Tuple, Dict, Optional, List
from collections import deque
from .grid_map import Coord, GridMap
from .base_path_finder import BasePlanner, Path


class Dijkstra_Path_Finder(BasePlanner):
    def __init__(self, grid_map: GridMap, start: Coord, goal: Coord):
        super().__init__(grid_map, start, goal)
        self.frontier: Deque[Tuple[int, Coord]] = deque()
        self.cost_so_far: Dict[Coord, int] = {}

    def start(self) -> None:
        pass
