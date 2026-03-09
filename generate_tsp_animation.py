import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# -----------------------------
# Configuration
# -----------------------------
SEED = 42
N_POINTS = 12
FPS = 2

# -----------------------------
# Utilities
# -----------------------------
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

def build_distance_matrix(points):
    n = len(points)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i, j] = euclidean_distance(points[i], points[j])
    return dist

def tour_cost(tour, dist):
    cost = 0.0
    for i in range(len(tour) - 1):
        cost += dist[tour[i], tour[i + 1]]
    cost += dist[tour[-1], tour[0]]
    return cost

def nearest_neighbor(dist, start=0):
    n = len(dist)
    visited = [False] * n
    visited[start] = True
    tour = [start]
    current = start

    while len(tour) < n:
        best = None
        best_d = float("inf")
        for j in range(n):
            if not visited[j] and dist[current, j] < best_d:
                best_d = dist[current, j]
                best = j
        visited[best] = True
        tour.append(best)
        current = best
    return tour

def two_opt_once(tour, dist):
    n = len(tour)
    best_tour = tour[:]
    best_cost = tour_cost(best_tour, dist)

    for i in range(1, n - 1):
        for k in range(i + 1, n):
            candidate = tour[:]
            candidate[i:k + 1] = reversed(candidate[i:k + 1])
            c = tour_cost(candidate, dist)
            if c < best_cost:
                return candidate, True
    return best_tour, False

def two_opt_steps(tour, dist, max_iter=100):
    steps = [tour[:]]
    current = tour[:]

    for _ in range(max_iter):
        current, improved = two_opt_once(current, dist)
        if improved:
            steps.append(current[:])
        else:
            break
    return steps

# -----------------------------
# Animation helpers
# -----------------------------
def draw_base(ax, points, title):
    ax.clear()
    ax.scatter(points[:, 0], points[:, 1], s=60)
    for i, (x, y) in enumerate(points):
        ax.text(x + 0.01, y + 0.01, str(i), fontsize=10)
    ax.set_title(title)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)

def animate_construction(points, steps, output_file, title_prefix):
    fig, ax = plt.subplots(figsize=(6, 6))

    def update(frame):
        draw_base(ax, points, f"{title_prefix} — Step {frame + 1}/{len(steps)}")
        tour = steps[frame]

        if len(tour) >= 2:
            path = points[tour]
            ax.plot(path[:, 0], path[:, 1], marker="o")

        if frame == len(steps) - 1 and len(tour) == len(points):
            closed = points[tour + [tour[0]]]
            ax.plot(closed[:, 0], closed[:, 1], marker="o")

    ani = FuncAnimation(fig, update, frames=len(steps), interval=1000 // FPS, repeat=False)
    ani.save(output_file, writer=PillowWriter(fps=FPS))
    plt.close(fig)

# -----------------------------
# Main
# -----------------------------
def main():
    np.random.seed(SEED)
    points = np.random.rand(N_POINTS, 2)
    dist = build_distance_matrix(points)

    # NN construction steps
    nn_tour = nearest_neighbor(dist, start=0)
    nn_steps = [nn_tour[:i] for i in range(1, len(nn_tour) + 1)]

    animate_construction(
        points,
        nn_steps,
        "tsp_nn_demo.gif",
        "Nearest Neighbor Tour Construction"
    )

    # 2-opt refinement steps
    opt_steps = two_opt_steps(nn_tour, dist)
    animate_construction(
        points,
        opt_steps,
        "tsp_nn_2opt_demo.gif",
        "Nearest Neighbor + 2-opt Refinement"
    )

    print("Generated:")
    print("- tsp_nn_demo.gif")
    print("- tsp_nn_2opt_demo.gif")
    print(f"Initial NN cost: {tour_cost(nn_tour, dist):.3f}")
    print(f"Final 2-opt cost: {tour_cost(opt_steps[-1], dist):.3f}")

if __name__ == "__main__":
    main()