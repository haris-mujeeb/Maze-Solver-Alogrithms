from typing import Tuple, Dict, Optional, List
from .grid_map import Coord, GridMap
from .base_path_finder import BasePlanner, Path
import heapq


class Lazy_Theta_star_Path_Finder(BasePlanner):
  def __init__(self, grid_map : GridMap, start : Coord, goal : Coord):
    super().__init__(grid_map, start, goal)
    
    self.frontier: List[Tuple[float, Coord]] = []

    self.cost_so_far: Dict[Coord, float] = {}
    self.came_from: Dict[Coord, Optional[Coord]] = {}
    self.closed_set: set[Coord] = set()

    self.current: Optional[Coord] = None
    self.path: Optional[Path] = None

  def start(self):
    self.frontier.clear()
    self.cost_so_far.clear()
    self.came_from.clear()
    self.closed_set.clear()

    heapq.heappush(self.frontier, (0.0, self.start_coord))
    self.cost_so_far[self.start_coord] = 0.0
    self.came_from[self.start_coord] = None

    self.current = None
    self.path = None
  
  def step(self) -> bool:
    if not self.frontier:
      return False
    
    _, current = heapq.heappop(self.frontier)

    if current in self.closed_set:
      return True

    self.current = current
    self.closed_set.add(current)

    if current == self.goal_coord:
      self.path = self._reconstruct_path()
      return False
    
    current_cost_g = self.cost_so_far[current]
    
    for n in self.grid_map.neighbours(self.current):
      if not self.grid_map.is_walkable(n):
        continue

      parent = self.came_from[current]

      # Theta*: check if parent can be shortcut
      if parent is not None and self._line_of_sight(parent, n):
        g_new = self.cost_so_far[parent] + self._get_euclidean_distance(parent, n)
        proposed_parent = parent
      else:
        g_new = current_cost_g + self._get_euclidean_distance(current, n)
        proposed_parent = current

      # Relaxation: update if better path found
      if n not in self.cost_so_far or g_new < self.cost_so_far[n]:
        self.cost_so_far[n] = g_new
        self.came_from[n] = proposed_parent
        h = self._get_euclidean_distance(n, self.goal_coord)
        f = g_new + h
        heapq.heappush(self.frontier, (f, n))

    return True


  def find_path(self) -> Optional[Path]:
    self.start()
    while self.step():
      pass
    return self.path
  

  def _reconstruct_path(self) -> Optional[Path]:
    keyframes: Path = []
    cur: Optional[Coord] = self.goal_coord
    while cur is not None:
        keyframes.append(cur)
        cur = self.came_from.get(cur)
    keyframes.reverse()

    if not keyframes:
        return []

    path: Path = [keyframes[0]]
    for i in range(1, len(keyframes)):
        segment = self._bresenham_line(keyframes[i-1], keyframes[i])
        path.extend(segment[1:])

    return path

  @staticmethod
  def _get_euclidean_distance(source : Coord, target : Coord) -> float:
    return ((target[0] - source[0])**2 + (target[1] - source[1])**2)**0.5


  def _bresenham_line(self, a: Coord, b: Coord) -> Path:
    """
    Returns a list of coordinates representing the line from a to b.
    Uses Bresenham's line algorithm.
    """
    x0, y0 = a
    x1, y1 = b
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    points = []
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return points
  
  def _line_of_sight(self, a: Coord, b: Coord) -> bool:
    for x, y in self._bresenham_line(a, b):
      if not self.grid_map.is_walkable((x, y)):
        return False
    return True