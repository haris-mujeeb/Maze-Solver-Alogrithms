# tests/test_path_finding.py
import pytest
from maze_solver.grid_map import GridMap
from maze_solver.bfs_path_finder import BFS_Path_Finder

@pytest.fixture
def pathfinding_grid():
    """Returns a grid with a clear path for testing pathfinding."""
    grid_data = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    return GridMap(grid_data)

def test_bfs_finds_path(pathfinding_grid):
    start = (1, 1)
    goal = (1, 3)
    
    path_finder = BFS_Path_Finder(pathfinding_grid, start, goal)
    path = path_finder.find_path()
    
    assert path is not None
    assert path == [(1, 1), (2, 1), (2, 2), (2, 3), (1, 3)]
