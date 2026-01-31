.PHONY: all run lint format test install clean

PYTHON := python

all: run

run: 
	$(PYTHON) -m src.maze_solver.main

lint:
	ruff src

format:
	black src

test:
	pytest

install:
	$(PYTHON) -m pip install .
	
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*__pycache__" -delete
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
