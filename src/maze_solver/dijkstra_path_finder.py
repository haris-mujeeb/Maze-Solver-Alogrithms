from typing import Tuple, Dict, Optional, List
from .grid_map import Coord, GridMap
from .base_path_finder import BasePlanner, Path
import heapq

COST_PER_CELL = 1

class Dijkstra_Path_Finder(BasePlanner):
    def __init__(self, grid_map: GridMap, start: Coord, goal: Coord):
        super().__init__(grid_map, start, goal)

        self.frontier: List[Tuple[int, Coord]] = []
        
        self.cost_so_far: Dict[Coord, int] = {}
        self.came_from: Dict[Coord, Optional[Coord]] = {}

        self.current: Optional[Coord] = None
        self.path: Optional[Path] = None

    def start(self):
        self.frontier.clear()
        self.cost_so_far.clear()
        self.came_from.clear()
        
        heapq.heappush(self.frontier, (0, self.start_coord))
        self.cost_so_far[self.start_coord] = 0
        self.came_from[self.start_coord] = None
        
        self.current = None
        self.path = None


    def step(self) -> bool:
        if not self.frontier:
            return False

        current_cost, current = heapq.heappop(self.frontier)
        
        if current_cost > self.cost_so_far.get(current, float("inf")):
            return True
        
        self.current = current

        if current == self.goal_coord:
            self.path = self._reconstruct_path()
            return False

        for n in self.grid_map.neighbours(self.current):
            if not self.grid_map.is_walkable(n):
                continue

            new_cost = current_cost + COST_PER_CELL

            if (n not in self.cost_so_far or new_cost < self.cost_so_far[n]):
                self.cost_so_far[n] = new_cost
                self.came_from[n] = self.current
                heapq.heappush(self.frontier, (new_cost, n))
        
        return True
    

    def find_path(self) -> Path | None:
        self.start()
        while self.step():
            pass
        return self.path


    def _reconstruct_path(self) -> Optional[Path]:
        path : Path = []
        cur: Optional[Coord] = self.goal_coord
        while cur is not None:
            path.append(cur)
            cur = self.came_from.get(cur)

        path.reverse()
        return path
