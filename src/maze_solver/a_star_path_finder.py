from typing import Tuple, List, Dict, Optional
import heapq
from .base_path_finder import BasePlanner, Path, GridMap, Coord


COST_PER_CELL = 1

class A_Star_Path_Finder(BasePlanner):
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

        _ , current = heapq.heappop(self.frontier)
                
        self.current = current
        current_cost_g = self.cost_so_far[current]

        if current == self.goal_coord:
            self.path = self._reconstruct_path()
            return False

        for n in self.grid_map.neighbours(self.current):
            if not self.grid_map.is_walkable(n):
                continue
            

            g_new = current_cost_g + COST_PER_CELL

            if (n not in self.cost_so_far or g_new < self.cost_so_far[n]):
                # distance = self._get_euclidean_distance(current, self.goal_coord)
                distance = self._get_manhattan_distance(n, self.goal_coord)
                self.cost_so_far[n] = g_new
                self.came_from[n] = self.current

                h = self._get_manhattan_distance(n, self.goal_coord)
                f = g_new + h
                heapq.heappush(self.frontier, (f, n))
        
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

    @staticmethod
    def _get_euclidean_distance(source : Coord, target : Coord) -> int:
        return ((target[0] - source[0])**2 + (target[1] - source[1])**2)**0.5

    @staticmethod
    def _get_manhattan_distance(source : Coord, target : Coord) -> int:
        return  (abs(target[0] - source[0]) + abs(target[1] - source[1]))