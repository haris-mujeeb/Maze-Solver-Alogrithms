from typing import Dict, Optional
from .grid_map import Coord
from .base_path_finder import BasePlanner, Path


class BFS_Path_Finder(BasePlanner):
    def start(self):
        self.frontier.append(self.start_coord)
        self.came_from: Dict[Coord, Optional[Coord]] = {self.start_coord: None}
        self.path: Optional[Path] = []
        self.current = self.start_coord

    def step(self) -> bool:
        if not self.frontier:
            return False

        self.current = self.frontier.popleft()
        if self.current == self.goal_cood:
            self.path = self._reconstruct_path()
            return False

        for n in self.grid_map.neighbours(self.current):
            if n not in self.came_from and self.grid_map.is_walkable(n):
                self.came_from[n] = self.current
                self.frontier.append(n)
        return True

    def find_path(self) -> Path | None:
        self.start()
        while self.step():
            pass
        return self.path

    def _reconstruct_path(self) -> Optional[Path]:
        path = []
        cur: Optional[Coord] = self.goal_cood
        while cur is not None:
            path.append(cur)
            cur = self.came_from.get(cur)

        path.reverse()
        return path
