# Statistical Delivery Route Optimizer & Simulator

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)

An end-to-end Python software application designed to solve the **Traveling Salesperson Problem (TSP)** and **Shortest Path Problem (Dijkstra)**, combined with a **stochastic Monte Carlo-inspired simulation** to forecast delivery delays, fuel consumption, and traffic dynamics under uncertain real-world weather and urban traffic conditions.

The simulation models real-world geographic coordinates around **Poços de Caldas - MG, Brazil**.

---

## Key Features

- **Graph Algorithms & Route Optimization**:
  - **Nearest Neighbor Heuristic**: Solves TSP for multi-point delivery route generation.
  - **Dijkstra's Algorithm**: Utilizes min-heaps (`heapq`) for priority-queue-based shortest path calculations between specific nodes.
  - **Haversine Formula**: Calculates real-world spatial distances using geographic coordinates (latitude/longitude).
- **Stochastic Simulation Engine**:
  - Incorporates Gaussian noise to simulate urban traffic variations.
  - Models speed degradation and probability of delivery delays under various weather conditions (*Sunny*, *Fog*, *Heavy Rain*) and peak vs. non-peak traffic hours.
- **Data Persistence**:
  - Stores all historical simulation runs, including path sequences, weather parameters, fuel usage, and delay probabilities, in a local **SQLite** database.
- **Interactive Data Visualization**:
  - Renders a 2D spatial map showing the optimized delivery route sequence and directional vectors.
  - Generates comparative bar charts comparing current run metrics against historical averages using **Matplotlib**.
- **Clean Architecture & OOP**:
  - Fully modular codebase utilizing Python type hints (`typing`), custom `@dataclass` structures, proper error handling (`try/except`), and detailed Docstrings.

---

## Repository Structure

```text
delivery-route-simulator/
├── data_manager.py      # Location database and SQLite persistence layer
├── graph_solver.py      # Graph data structures, Haversine, Dijkstra, and TSP solver
├── simulator.py         # Stochastic statistical simulation engine
├── visualizer.py        # Route mapping and performance visualization
├── main.py              # Interactive Command Line Interface (CLI)
├── requirements.txt     # Python project dependencies
├── SECURITY.md          # Vulnerability reporting guidelines
└── README.md            # Project documentation
