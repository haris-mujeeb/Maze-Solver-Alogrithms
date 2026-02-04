import random
from typing import List, Set, Tuple, Optional
from .grid_map import GridMap, Grid, Coord
from .a_star_path_finder import A_Star_Path_Finder

class BlobObstacleGenerator:
    """
    Generate a grid with randomly shaped obstacles ("blobs").

    Usage:
        gen = BlobObstacleGenerator(rows=100, cols=100, seed=42)
        grid_map = gen.generate(num_blobs=80, avg_blob_size=40, keep_clear=[start, goal])
    """
    def __init__(self, rows: int, cols: int, seed: Optional[int] = None):
        if rows < 3 or cols < 3:
            raise ValueError("rows and cols must be >= 3")
        self.rows = rows
        self.cols = cols
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        # grid initialized later in generate()
        self.grid: Grid = []

    def _in_bounds(self, p: Coord) -> bool:
        r, c = p
        return 1 <= r < self.rows - 1 and 1 <= c < self.cols - 1

    def _init_grid(self) -> None:
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # perimeter walls
        for r in range(self.rows):
            self.grid[r][0] = 1
            self.grid[r][self.cols - 1] = 1
        for c in range(self.cols):
            self.grid[0][c] = 1
            self.grid[self.rows - 1][c] = 1

    def generate(self,
                 num_blobs: int = 40,
                 avg_blob_size: int = 30,
                 blob_size_variation: float = 0.9,
                 expansion_prob: float = 0.9,
                 attempts_limit: int | None = None,
                 noise_frac: float = 0.01,
                 keep_clear: Optional[List[Coord]] = None,
                 clear_radius: int = 3) -> GridMap:
        """
        num_blobs: approx number of separate obstacles
        avg_blob_size: target avg cells per blob
        blob_size_variation: fraction (0..1) to vary sizes
        expansion_prob: probability to expand to neighbor during growth
        attempts_limit: max total attempts to place blobs (default = num_blobs*10)
        noise_frac: fraction of grid cells turned into sparse noise obstacles
        keep_clear: list of coords to guarantee a clear radius around (e.g., start/goal)
        clear_radius: radius around keep_clear coords to force free cells
        """
        if self.seed is not None:
            random.seed(self.seed)

        if attempts_limit is None:
            attempts_limit = max(100, num_blobs * 10)

        self._init_grid()
        occupied: Set[Coord] = set()
        attempts = 0
        placed = 0

        while placed < num_blobs and attempts < attempts_limit:
            attempts += 1
            r = random.randint(1, self.rows - 2)
            c = random.randint(1, self.cols - 2)
            if (r, c) in occupied:
                continue

            var = int(avg_blob_size * blob_size_variation)
            target = max(1, avg_blob_size + random.randint(-var, var))

            blob: Set[Coord] = set()
            frontier: List[Coord] = [(r, c)]
            blob.add((r, c))

            while frontier and len(blob) < target:
                cur = frontier.pop(random.randrange(len(frontier)))
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    if random.random() > expansion_prob:
                        continue
                    nxt = (cur[0] + dr, cur[1] + dc)
                    if not self._in_bounds(nxt):
                        continue
                    if nxt in blob or nxt in occupied:
                        continue
                    # occasional hole
                    if random.random() < 0.1:
                        continue
                    blob.add(nxt)
                    frontier.append(nxt)
                    if len(blob) >= target:
                        break

            # accept blob if reasonably sized
            if len(blob) >= max(1, target // 4):
                # ensure blob won't fully cover keep_clear areas (if provided)
                if keep_clear:
                    conflict = False
                    for center in keep_clear:
                        cr, cc = center
                        for dx in range(-clear_radius, clear_radius + 1):
                            for dy in range(-clear_radius, clear_radius + 1):
                                if (cr + dx, cc + dy) in blob:
                                    conflict = True
                                    break
                            if conflict:
                                break
                        if conflict:
                            break
                    if conflict:
                        continue

                occupied.update(blob)
                placed += 1

        # write occupied to grid
        for (rr, cc) in occupied:
            self.grid[rr][cc] = 1

        # add sparse noise
        noise_cells = int(self.rows * self.cols * noise_frac)
        for _ in range(noise_cells):
            rr = random.randint(1, self.rows - 2)
            cc = random.randint(1, self.cols - 2)
            self.grid[rr][cc] = 1

        # Check for path, and carve one if necessary
        if keep_clear and len(keep_clear) >= 2:
            start_node, goal_node = keep_clear[0], keep_clear[1]

            path_finder = A_Star_Path_Finder(GridMap(self.grid), start_node, goal_node)
            path = path_finder.find_path()

            if not path:
                empty_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
                for r in range(self.rows):
                    empty_grid[r][0] = 1
                    empty_grid[r][self.cols - 1] = 1
                for c in range(self.cols):
                    empty_grid[0][c] = 1
                    empty_grid[self.rows - 1][c] = 1
                
                empty_grid_map = GridMap(empty_grid)

                ideal_path_finder = A_Star_Path_Finder(empty_grid_map, start_node, goal_node)
                ideal_path = ideal_path_finder.find_path()

                if ideal_path:
                    carve_radius = 2
                    for r_path, c_path in ideal_path:
                        for dr in range(-carve_radius, carve_radius + 1):
                            for dc in range(-carve_radius, carve_radius + 1):
                                r, c = r_path + dr, c_path + dc
                                if 1 <= r < self.rows - 1 and 1 <= c < self.cols - 1:
                                    self.grid[r][c] = 0

        # enforce keep_clear areas
        if keep_clear:
            for center in keep_clear:
                cr, cc = center
                for dr in range(-clear_radius, clear_radius + 1):
                    for dc in range(-clear_radius, clear_radius + 1):
                        rr, cc2 = cr + dr, cc + dc
                        if 1 <= rr < self.rows - 1 and 1 <= cc2 < self.cols - 1:
                            self.grid[rr][cc2] = 0

        return GridMap(self.grid)

    def get_grid_map(self) -> GridMap:
        if not self.grid:
            self._init_grid()
        return GridMap(self.grid)
