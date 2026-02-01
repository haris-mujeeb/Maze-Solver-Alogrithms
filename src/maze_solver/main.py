# main.py
import pygame
from .maze_generator import MazeGenerator
from .blob_obstacle_generator import BlobObstacleGenerator
from .maze_visualizer import MazeGeneratorVisualizer, GridMapPathFindingVisualizer
from .bfs_path_finder import BFS_Path_Finder
from .dfs_path_finder import DFS_Path_Finder
from .dijkstra_path_finder import Dijkstra_Path_Finder
from .a_star_path_finder import A_Star_Path_Finder
from .theta_star_path_finder import ThetaStarPathFinder

# ROWS, COLS = 101, 201
ROWS, COLS = 61, 81
# ROWS, COLS = 41, 61
CELL = 6
VISUALIZE_MAP_GENERATION = True
VISUALIZE_MAP_GENERATION = False

if VISUALIZE_MAP_GENERATION:
    maze = MazeGenerator(ROWS, COLS)
    # maze.start((1, 1), mode="EMPTY")
    # maze.start((1, 1), mode="BFS")
    # maze.start((1, 1), mode="DFS")
    maze.start((1, 1), mode="WILSON")

    vis = MazeGeneratorVisualizer(maze.get_grid_map(), CELL)

    clock = pygame.time.Clock()

    while maze.step():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        vis.draw(maze.frontier, maze.current)
        clock.tick(60)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        vis.draw()
        clock.tick(60)

    pygame.quit()

else:
    # maze = MazeGenerator(ROWS, COLS)
    # maze.generate_full(start=(1, 1), mode="EMPTY")

    # maze = MazeGenerator(ROWS, COLS)
    # maze.generate_full(start=(1, 1), mode="DFS")

    maze = BlobObstacleGenerator(ROWS, COLS)
    maze.generate()

    start_node = (1, 1)
    goal_node = (ROWS - 2, COLS - 2)

    path_vis = GridMapPathFindingVisualizer(maze.get_grid_map(), CELL, start=start_node, goal=goal_node)
    # path_gen = BFS_Path_Finder(maze.get_grid_map(), start_node, goal_node)
    # path_gen = DFS_Path_Finder(maze.get_grid_map(), start_node, goal_node)
    # path_gen = Dijkstra_Path_Finder(maze.get_grid_map(), start_node, goal_node)
    # path_gen = A_Star_Path_Finder(maze.get_grid_map(), start_node, goal_node)
    path_gen = ThetaStarPathFinder(maze.get_grid_map(), start_node, goal_node)

    path_gen.start()
    clock = pygame.time.Clock()

    while path_gen.step():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        path_vis.draw(
            frontier=path_gen.frontier,
            current=path_gen.current,
            path=path_gen.path,
            searched=path_gen.came_from,
        )
        clock.tick(240)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        path_vis.draw(path=path_gen.path, searched=path_gen.came_from)
        clock.tick(10)

    pygame.quit()