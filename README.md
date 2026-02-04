# Maze Solver and Visualizer

This project is a Python application that generates and solves mazes, with a visual representation of the algorithms provided by Pygame.

This document also serves as a personal guide to the industrial-standard Python development practices that have been set up for this project.

## Features

*   **Maze Generation**: Procedurally generates mazes.
*   **Pathfinding Visualization**: Visualizes various pathfinding algorithms as they explore the maze, providing a clear understanding of how they work.
*   **Multiple Algorithms**: Implements a variety of pathfinding algorithms, from simple searches to more advanced, optimized techniques.
*   **Customizable Visualization**: The start and goal points are rendered as distinct circular shapes for easy identification.

## Pathfinding Algorithms

This project includes the following pathfinding algorithms:

*   A* (A-Star)
*   Breadth-First Search (BFS)
*   Depth-First Search (DFS)
*   Dijkstra's Algorithm
*   Theta*
*   Lazy Theta*
*   Rapidly-exploring Random Tree (RRT)
*   RTT* (RRT-Star)

For a detailed explanation of each algorithm, please see the [developer notes on path planners](src/README.md).

## Development Setup

This project is configured with a modern Python development environment. The following steps have been completed to ensure code quality, maintainability, and ease of development.

### 1. Project Structure (`src` layout)

-   **What was done**: The Python source code has been moved into a `src/maze_solver` directory. This directory is a Python package (it contains an `__init__.py` file).
-   **Why**: This separates the application code from other project files like tests, documentation, and configuration, which is a standard practice for maintainable projects.

### 2. Dependency Management (`pyproject.toml`)

-   **What was done**: A `pyproject.toml` file was created in the root directory. It defines the project's name, version, and dependencies.
-   **Why**: This is the modern, standardized way to manage Python project dependencies and metadata, replacing older files like `requirements.txt` for this purpose.
-   **How to use**: To install the dependencies (like `pygame`) into your virtual environment, run the following command from the project root:
    ```bash
    pip install .
    ```

### 3. Linting and Formatting (`ruff` & `black`)

-   **What was done**: `ruff` and `black` were installed for linting and code formatting.
-   **Why**: `black` automatically formats code to a consistent style. `ruff` is an extremely fast linter that checks for errors, potential bugs, and stylistic issues.
-   **How to use**:
    -   To check for linting issues:
        ```bash
        make lint
        # or
        ruff check src/
        ```
    -   To automatically format the code:
        ```bash
        make format
        # or
        black src/
        ```

### 4. Testing (`pytest`)

-   **What was done**: `pytest` was installed, and a `tests/` directory was created for writing tests. The project is configured via `pyproject.toml` to allow `pytest` to discover the source code in `src/`.
-   **Why**: Automated testing is crucial for verifying that your code works correctly and for catching bugs when you make changes.
-   **How to use**:
    -   To run all tests:
        ```bash
        make test
        # or
        pytest
        ```

### 5. Static Type Checking (`mypy`)

-   **What was done**: `mypy` was installed and used to check for type consistency in the code based on the type hints provided. All type errors have been resolved.
-   **Why**: Static type checking helps catch a whole class of bugs before the code is even run, improving reliability and making the code easier to understand.
-   **How to use**:
    -   To run a type check:
        ```bash
        mypy src/
        ```

### 6. Development Automation (`Makefile`)

-   **What was done**: A `Makefile` was created in the root directory to provide simple, memorable commands for common development tasks.
-   **Why**: This simplifies the development workflow, making it easy to run, test, and format the project without having to remember the full commands.
-   **Available commands**:
    -   `make run`: Runs the main application.
    -   `make install`: Installs dependencies from `pyproject.toml`.
    -   `make lint`: Checks the code for linting issues.
    -   `make format`: Formats the code with `black`.
    -   `make test`: Runs the test suite with `pytest`.
    -   `make clean`: Removes temporary Python and build files.

## How to Run the Application

1.  Ensure your virtual environment is activated.
2.  From the project root, run:
    ```bash
    make run
    ```
    Alternatively, you can run the module directly:
    ```bash
    python -m src.maze_solver.main
    ```

---

## Future TODOs

The following are more advanced steps that can be taken as the project grows:

-   **Step 6: Configuration Management**: Implement a system for managing configuration (e.g., using `.env` files or a config file) if the application starts to require settings like API keys, different modes, etc.
-   **Step 7: Documentation**: Set up `Sphinx` to auto-generate a documentation website from the docstrings in the code, making it easier for others (and your future self) to understand the project.
-   **Step 8: CI/CD (Continuous Integration/Continuous Deployment)**: Create a CI/CD pipeline using a tool like GitHub Actions to automatically run tests, linting, and type checks every time code is pushed to the repository.
