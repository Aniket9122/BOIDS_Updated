# Boids 2‑D Sandbox & Experiments

A Python/Pygame recreation of Craig Reynolds’ flocking (Boids) model extended with interactive world‑building, automatic data collection and a simple genetic‑algorithm optimiser.

---

Statement of Contribution 

Aniket :-
* **GUI and Mapping buttons to boids functionality 
* **Target Seeking 
* **Test 2 Implementation 
* **Github repo management 

Victor:-
* **Main environment functionality 
* **Create Targets / Obstacles 
* **Obstacle Avoidance 
* **GA Implementation 
* **Test 1 Implementation 

---

## 1 Features

* **Real‑time flocking** – alignment, cohesion, separation with adjustable weights.
* **Dynamic environment** – click‑to‑spawn obstacles, toggle wrap‑around goals (targets).
* **Metrics collection** – arrival‑time histograms, per‑target timings, speed calculation.
* **Genetic Algorithm (GA)** – evolves rule weights over successive runs.
* **Matplotlib plots** – bar/pie diagrams of arrival times; speed‑per‑target curves.

---

## 2 Directory structure

```
.
├─ Animats/
│    └─ bird.py            # individual agent logic
├─ Environment/
│    ├─ base_env.py        # common world code
│    ├─ env_1.py           # sample map with obstacles
│    └─ env_2.py           # empty map (baseline)
├─ boids.py                # main interactive sandbox – RUN THIS
├─ boidsTest.py            # scripted experiment & metric plots
├─ geneticAlgorithm.py     # GA wrapper that evolves rule weights
└─ README.md               # this file
```

---

## 3 Requirements

* Python ≥ 3.9
* pygame
* numpy
* matplotlib

Install via:

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install pygame numpy matplotlib
```

---

## 4 Quick start

```bash
python boids.py
```

A 1400 × 1000 window appears populated with 50 birds. Use the on‑screen buttons:

| Button (rounded = env) | Effect                             |
| ---------------------- | ---------------------------------- |
| **Alignment**          | Toggle heading alignment rule      |
| **Cohesion**           | Toggle centre‑seeking rule         |
| **Separation**         | Toggle crowd‑avoidance rule        |
| **Enable targets**     | Spawn/clear two green goal circles |
| **Add obstacle**       | Drop one random obstacle           |
| **Clear obstacles**    | Remove all obstacles               |
| *Left‑click anywhere*  | Add a new bird at cursor           |

Birds wrap around screen edges and automatically avoid obstacles. When ≥ 80 % of the flock reaches a target, a new one is spawned and arrival‑time statistics are logged.

---

## 5 Running experiments

\### 5.1 Speed & timing study

```bash
python boidsTest.py
```

* 30 target cycles on the obstacle map (Env1)
* Calculates per‑target speed & arrival‑time buckets (\[5,10,15,20,25,30] s)
* Saves `arrival_bar.png` (bar chart of arrival counts)
* Prints average speed to console

\### 5.2 Genetic‑algorithm optimiser

```bash
python geneticAlgorithm.py
```

* 30 generations × 5 runs each
* Offspring produced by simple crossover; 3 best genomes carried forward
* Fitness = average speed to target over 45 s run
* Plots best/average fitness curves at the end

> **Tip**  : GA spawns its own Pygame windows; close them automatically by waiting or manually via *X*.

---

## 6 Packaging into an executable

Create a one‑file binary (Windows example):

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole boids.py \
           --add-data "Environment;Environment" --add-data "Animats;Animats"
```

Resulting `dist/boids.exe` runs on machines without Python.

---

## Git repo : https://github.com/Aniket9122/BOIDS_Updated.git