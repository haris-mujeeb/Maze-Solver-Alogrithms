# tests/test_grid_map.py
import pytest
from maze_solver.grid_map import GridMap

@pytest.fixture
def simple_grid():
    """Returns a simple 3x3 grid for testing."""
    # 1 is wall, 0 is path
    grid_data = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    return GridMap(grid_data)

def test_in_bounds(simple_grid):
    assert simple_grid.in_bounds((1, 1)) is True
    assert simple_grid.in_bounds((0, 0)) is True
    assert simple_grid.in_bounds((3, 3)) is False
    assert simple_grid.in_bounds((-1, 1)) is False

def test_is_walkable(simple_grid):
    assert simple_grid.is_walkable((1, 1)) is True
    assert simple_grid.is_walkable((0, 0)) is False
