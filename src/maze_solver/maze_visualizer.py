import pygame
from typing import Deque, Optional, Dict, Collection, Any
from .grid_map import GridMap, Coord
from .base_path_finder import Path

BLACK = (20, 20, 20)
GREEN = (80, 200, 120)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 0)
RED = (255, 80, 80)
WHITE = (240, 240, 240)
GREY = (192, 192, 192)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)


class MazeGeneratorVisualizer:
    def __init__(self, grid_map: GridMap, cell_size=16):
        self.grid = grid_map.grid
        self.rows = grid_map.rows
        self.cols = grid_map.cols
        self.cell_size = cell_size

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.cols * cell_size, self.rows * cell_size)
        )

    def draw(
        self, frontier: Optional[Deque[Coord]] = None, current: Optional[Coord] = None
    ):
        self.screen.fill(BLACK)

        for r in range(self.rows):
            for c in range(self.cols):
                color = BLACK if self.grid[r][c] else WHITE
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        c * self.cell_size,
                        r * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

        if frontier:
            for r, c in frontier:
                pygame.draw.rect(
                    self.screen,
                    BLUE,
                    (
                        c * self.cell_size,
                        r * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

        if current:
            r, c = current
            pygame.draw.rect(
                self.screen,
                RED,
                (
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                ),
            )

        pygame.display.flip()


class GridMapPathFindingVisualizer:
    def __init__(self, screen, cell_size=16):
        self.screen = screen
        self.cell_size = cell_size
        self.grid = None
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None

    def set_grid(self, grid_map: GridMap, start: Optional[Coord] = None, goal: Optional[Coord] = None):
        self.grid = grid_map.grid
        self.rows = grid_map.rows
        self.cols = grid_map.cols
        self.start = start
        self.goal = goal

    def draw(
        self,
        frontier: Optional[Collection[Any]] = None,
        current: Optional[Coord] = None,
        path: Optional[Path] = None,
        searched: Optional[Dict[Coord, Optional[Coord]]] = None,
    ):
        self.screen.fill(WHITE)
        self._draw_maze()

        if searched:
            for r, c in searched:
                pygame.draw.rect(
                    self.screen,
                    GREY,
                    (
                        c * self.cell_size,
                        r * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

        if frontier:
            coords_to_draw = []
            # Make a copy to safely inspect the first item
            frontier_items = list(frontier)
            if frontier_items:
                first_item = frontier_items[0]
                # Check if it looks like Dijkstra's frontier: (cost, (r, c))
                if (
                    isinstance(first_item, tuple)
                    and len(first_item) == 2
                    and isinstance(first_item[1], tuple)
                ):
                    coords_to_draw = [item[1] for item in frontier_items if isinstance(item, tuple) and len(item) == 2]
                else:  # Assumes BFS/DFS frontier of (r, c)
                    coords_to_draw = [item for item in frontier_items if isinstance(item, tuple) and len(item) == 2]

            for r, c in coords_to_draw:
                pygame.draw.rect(
                    self.screen,
                    BLUE,
                    (
                        c * self.cell_size,
                        r * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

        if current:
            r, c = current
            pygame.draw.rect(
                self.screen,
                RED,
                (
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                ),
            )

        if path:
            for p in path:
                r, c = p
                pygame.draw.rect(
                    self.screen,
                    YELLOW,
                    (
                        c * self.cell_size,
                        r * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )
        
        if self.start:
            r, c = self.start
            start_size = self.cell_size * 5
            offset = (start_size - self.cell_size) // 2
            pygame.draw.rect(
                self.screen,
                ORANGE,
                (
                    c * self.cell_size - offset,
                    r * self.cell_size - offset,
                    start_size,
                    start_size,
                ),
            )

        if self.goal:
            r, c = self.goal
            goal_size = self.cell_size * 5
            offset = (goal_size - self.cell_size) // 2
            pygame.draw.rect(
                self.screen,
                PURPLE,
                (
                    c * self.cell_size - offset,
                    r * self.cell_size - offset,
                    goal_size,
                    goal_size,
                ),
            )

        pygame.display.flip()

    def _draw_maze(self):
        for r in range(self.rows):
            for c in range(self.cols):
                color = GREEN if self.grid[r][c] else BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        c * self.cell_size,
                        r * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )
