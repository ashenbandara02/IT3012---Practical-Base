"""Lab 05: generate, evaluate, pool and prune local beam successors."""

import random


def local_beam_search(initial_states, k, max_iters, objective_fn):
    """Maximize objective_fn while keeping the best k pooled successors."""
    current_states = initial_states
    for iteration in range(max_iters):
        all_successors = []
        for state in current_states:
            for _ in range(5):
                neighbor = state + random.uniform(-10, 10)
                fit = objective_fn(neighbor)
                all_successors.append((neighbor, fit))
        all_successors.sort(key=lambda item: item[1], reverse=True)
        current_states = [item[0] for item in all_successors[:k]]
    return max(current_states, key=objective_fn)


# The supplied PDF runner ends after random.seed(42).
# This separate check supplies the missing parabola test.
if __name__ == "__main__":
    random.seed(42)

    def objective(x):
        return -(x - 50) ** 2 + 100

    best = local_beam_search([0, 25, 100], 3, 100, objective)
    print(f"Best state: {best:.6f}")
    print(f"Best objective value: {objective(best):.6f}")
    assert abs(best - 50) < 2, "Result must be within 2 of the parabola maximum."
    print("SUCCESS: Local Beam Search reached the parabola maximum within tolerance.")
