from .base_path_finder import BasePlanner, Path


class A_star_Path_Finder(BasePlanner):
    def __init__(self, grid_map, start, goal):
        super().__init__(grid_map, start, goal)

    def start(self):
        

    def step(self) -> bool:
        pass

    def find_path(self) -> Path | None:
        pass
