# benchmark.py
import time
import random
import csv
from typing import List, Dict, Any
import pygame

from .maze_generator import MazeGenerator
from .blob_obstacle_generator import BlobObstacleGenerator
from .grid_map import GridMap
from .maze_visualizer import GridMapPathFindingVisualizer
from .bfs_path_finder import BFS_Path_Finder
from .dfs_path_finder import DFS_Path_Finder
from .dijkstra_path_finder import Dijkstra_Path_Finder
from .a_star_path_finder import A_Star_Path_Finder
from .theta_star_path_finder import ThetaStarPathFinder
from .lazy_theta_star_path_finder import Lazy_Theta_star_Path_Finder

# --- Benchmark Configuration ---
NUM_RUNS = 2000
ROWS, COLS = 101, 201
ROWS, COLS = 151, 251

# --- Visualization Configuration ---
VISUALIZE = False # Set to True to visualize a single run
VISUALIZE_ALGORITHM = "ALL" # Choose all: "ALL" (OR) Choose one: "BFS", "DFS", "Dijkstra", "A*", "Theta*", "Lazy Theta*"
VISUALIZATION_MODE = "ANIMATED" # "ANIMATED" or "STATIC"
CELL_SIZE = 6 # For visualization

SHOW_RESULT_FOR_SEC = 1
ANIMATION_SPEED = 200
def run_visualization():
    """
    Runs a single instance of a pathfinder with visualization.
    """
    print(f"Running {VISUALIZATION_MODE} visualization for {VISUALIZE_ALGORITHM} for {NUM_RUNS} runs...")

    pathfinders_to_test = {
        # "DFS": DFS_Path_Finder,
        "BFS": BFS_Path_Finder,
        "Dijkstra": Dijkstra_Path_Finder,
        "A*": A_Star_Path_Finder,
        "Theta*": ThetaStarPathFinder,
        # "Lazy Theta*": Lazy_Theta_star_Path_Finder,
    }

    planners_to_run = []
    if VISUALIZE_ALGORITHM == "ALL":
        planners_to_run = list(pathfinders_to_test.items())
    else:
        planner_class = pathfinders_to_test.get(VISUALIZE_ALGORITHM)
        if not planner_class:
            print(f"Error: Algorithm '{VISUALIZE_ALGORITHM}' not found.")
            return
        planners_to_run = [(VISUALIZE_ALGORITHM, planner_class)]

    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
    clock = pygame.time.Clock()
    path_vis = GridMapPathFindingVisualizer(screen, CELL_SIZE)

    for name, planner_class in planners_to_run:
        for run_num in range(1, NUM_RUNS + 1):
            print(f"--- Visualizing {name}, Run {run_num}/{NUM_RUNS} ---")
            pygame.display.set_caption(f"Pathfinding Visualization: {name} (Run {run_num}/{NUM_RUNS})")

            # Generate a maze
            maze_seed = random.randint(0, 2**32 - 1)
            maze_gen = BlobObstacleGenerator(ROWS, COLS, seed=maze_seed)
            # Generate a temporary grid to find random start/goal
            # The grid is initialized by BlobObstacleGenerator's generate method
            # We need a grid map to find walkable cells
            temp_gen = BlobObstacleGenerator(ROWS, COLS, seed=maze_seed) # Use same seed for reproducibility
            temp_gen._init_grid() # Initialize with just perimeter walls
            temp_grid_map = temp_gen.get_grid_map()

            available_cells = list(temp_grid_map.walkable_cells()) # Convert to list to use random.choice and remove
            
            # Ensure start and goal are distinct and not on the very edge (walls)
            if len(available_cells) < 2:
                print(f"Warning: Not enough walkable cells to select start/goal for {name} on run {run_num}. Skipping.")
                continue

            start_node = random.choice(available_cells)
            available_cells.remove(start_node)
            goal_node = random.choice(available_cells)

            # Now generate the maze with actual obstacles, keeping start/goal clear
            grid_map = maze_gen.generate(
                num_blobs=60, 
                avg_blob_size=40, 
                blob_size_variation= 0.9,
                expansion_prob = 0.9,
                keep_clear=[start_node, goal_node]
            )
            
            path_vis.set_grid(grid_map, start=start_node, goal=goal_node)
            path_gen = planner_class(grid_map, start_node, goal_node)

            if VISUALIZATION_MODE == "ANIMATED":
                path_gen.start()

                running_search = True
                while running_search:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    for _ in range(ANIMATION_SPEED):
                        if not path_gen.step():
                            running_search = False
                    
                    path_vis.draw(
                        frontier=getattr(path_gen, 'frontier', None),
                        current=path_gen.current,
                        path=path_gen.path,
                        searched=getattr(path_gen, 'came_from', None)
                    )
                    clock.tick(240)

            elif VISUALIZATION_MODE == "STATIC":
                path_gen.find_path()

            # Show final path for a few seconds
            start_time = time.time()
            while time.time() - start_time < SHOW_RESULT_FOR_SEC:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                path_vis.draw(path=path_gen.path, searched=getattr(path_gen, 'came_from', None))
                pygame.display.flip()
                clock.tick(60)
        
    pygame.quit()
    print("All visualization runs complete.")


# --- Main Benchmark Function ---

def run_benchmark():
    """
    Runs the pathfinding benchmark and prints the results.
    """
    print("Starting pathfinding benchmark...")

    pathfinders_to_test = [
        # ("DFS", DFS_Path_Finder),
        ("BFS", BFS_Path_Finder),
        ("Dijkstra", Dijkstra_Path_Finder),
        ("A*", A_Star_Path_Finder),
        ("Theta*", ThetaStarPathFinder),
        # ("Lazy Theta*", Lazy_Theta_star_Path_Finder),
    ]

    results: List[Dict[str, Any]] = []

    for run_num in range(1, NUM_RUNS + 1):
        print(f"--- Run {run_num}/{NUM_RUNS} ---")

        # Generate a new maze for each run
        maze_seed = random.randint(0, 2**32 - 1)
        maze_gen = BlobObstacleGenerator(ROWS, COLS, seed=maze_seed)
        
        # Generate a temporary grid to find random start/goal
        temp_gen = BlobObstacleGenerator(ROWS, COLS, seed=maze_seed) # Use same seed for reproducibility
        temp_gen._init_grid()
        temp_grid_map = temp_gen.get_grid_map()

        available_cells = list(temp_grid_map.walkable_cells())
        
        if len(available_cells) < 2:
            print(f"Warning: Not enough walkable cells to select start/goal for benchmark run {run_num}. Skipping.")
            continue
        
        start_node = random.choice(available_cells)
        available_cells.remove(start_node)
        goal_node = random.choice(available_cells)

        grid_map = maze_gen.generate(
            num_blobs=80, 
            avg_blob_size=40, 
            keep_clear=[start_node, goal_node]
        )

        for name, planner_class in pathfinders_to_test:
            print(f"  Testing {name}...")

            planner = planner_class(grid_map, start_node, goal_node)

            start_time = time.perf_counter()
            path = planner.find_path()
            end_time = time.perf_counter()

            execution_time = (end_time - start_time) * 1000  # in milliseconds

            path_found = path is not None
            path_length_nodes = 0
            path_length_dist = 0.0

            if path_found and path:
                path_length_nodes = len(path)
                for i in range(1, len(path)):
                    path_length_dist += ((path[i][0] - path[i-1][0])**2 + (path[i][1] - path[i-1][1])**2)**0.5

            nodes_visited = len(getattr(planner, 'came_from', {}))

            run_data = {
                "run": run_num,
                "algorithm": name,
                "maze_seed": maze_seed,
                "path_found": path_found,
                "path_length_nodes": path_length_nodes,
                "path_length_dist": round(path_length_dist, 2),
                "execution_time_ms": round(execution_time, 2),
                "nodes_visited": nodes_visited,
            }
            results.append(run_data)
            print(f"    Done. Time: {run_data['execution_time_ms']} ms, Path length: {run_data['path_length_nodes']} nodes, Visited: {run_data['nodes_visited']} nodes")

    # --- Save results to CSV ---
    if results:
        keys = results[0].keys()
        with open("benchmark_results.csv", "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
        print("\nBenchmark results saved to benchmark_results.csv")

    # --- Print summary ---
    if results:
        print("\n--- Benchmark Summary ---")
        # Group results by algorithm
        summary_data = {}
        for res in results:
            alg = res['algorithm']
            if alg not in summary_data:
                summary_data[alg] = {
                    'runs': 0,
                    'total_time': 0,
                    'total_visited': 0,
                    'total_path_nodes': 0,
                    'total_path_dist': 0,
                    'successful_runs': 0
                }
            summary_data[alg]['runs'] += 1
            summary_data[alg]['total_time'] += res['execution_time_ms']
            summary_data[alg]['total_visited'] += res['nodes_visited']
            if res['path_found']:
                summary_data[alg]['successful_runs'] += 1
                summary_data[alg]['total_path_nodes'] += res['path_length_nodes']
                summary_data[alg]['total_path_dist'] += res['path_length_dist']

        print(f"{'Algorithm':<15} | {'Avg Time (ms)':>15} | {'Avg Visited':>15} | {'Avg Path Nodes':>15} | {'Avg Path Dist':>15} | {'Success Rate':>15}")
        print("-----------------------------------------------------------------------------------------------------")
        for alg, data in summary_data.items():
            avg_time = round(data['total_time'] / data['runs'], 2)
            avg_visited = round(data['total_visited'] / data['runs'])
            avg_path_nodes = round(data['total_path_nodes'] / data['successful_runs']) if data['successful_runs'] > 0 else 0
            avg_path_dist = round(data['total_path_dist'] / data['successful_runs'], 2) if data['successful_runs'] > 0 else 0
            success_rate = f"{round((data['successful_runs'] / data['runs']) * 100)}%"

            print(f"{alg:<15} | {avg_time:>15} | {avg_visited:>15} | {avg_path_nodes:>15} | {avg_path_dist:>15} | {success_rate:>15}")

if __name__ == "__main__":
    if VISUALIZE:
        run_visualization()
    else:
        run_benchmark()
