import itertools
import random
from utils import benchmark


def is_clique(graph, subset):
    return all(graph.has_edge(u, v) for u, v in itertools.combinations(subset, 2))


def is_small_graph(nodes, clique_size):
    return len(nodes) < clique_size


@benchmark
def exhaustive_clique_search(graph, clique_size):
    node_list = list(graph.nodes)
    solutions_tested = 0
    operations_count = 0

    for subset in itertools.combinations(node_list, clique_size):
        solutions_tested += 1
        operations_count += 1 + sum(1 for _ in itertools.combinations(subset, 2))
        if is_clique(graph, subset):
            return subset, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def random_sampling_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)

    if is_small_graph(node_list, clique_size):
        return None, 0, 0

    operations_count = 0
    solutions_tested = 0

    for _ in range(num_trials):
        if operations_count > 150 * graph.size() ** 2 + 100000:
            break
        subset = random.sample(node_list, clique_size)
        solutions_tested += 1
        operations_count += 1 + sum(1 for _ in itertools.combinations(subset, 2))
        if is_clique(graph, subset):
            return subset, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def monte_carlo_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)

    if is_small_graph(node_list, clique_size):
        return None, 0, 0

    operations_count = 0
    solutions_tested = 0

    for _ in range(num_trials):
        if operations_count > 150 * graph.size() ** 2 + 100000:
            break
        subset = []
        node = random.choice(node_list)
        subset.append(node)
        neighbors = set(graph.neighbors(node))

        while (
            len(subset) < clique_size
            or operations_count < 150 * graph.size() ** 2 + 100000
        ):
            if not neighbors:
                break
            candidate = random.choice(list(neighbors))
            subset.append(candidate)
            neighbors.intersection_update(graph.neighbors(candidate))
            operations_count += 1

        solutions_tested += 1
        if len(subset) == clique_size and is_clique(graph, subset):
            return subset, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def monte_carlo_with_heuristic_clique(graph, clique_size, num_trials=1000):
    """
    Algoritmo Monte Carlo que combina geração aleatória com heurísticas.
    """
    node_list = list(graph.nodes)

    if is_small_graph(node_list, clique_size):
        return None, 0, 0

    solutions_tested = set()
    operations_count = 0  # Contador de operações

    for _ in range(num_trials):
        subset = []
        node = random.choice(node_list)
        subset.append(node)
        neighbors = set(graph.neighbors(node))
        operations_count += 1

        # Usa heurísticas para expandir o subconjunto
        while len(subset) < clique_size:
            if not neighbors or operations_count > 150 * graph.size() ** 2 + 100000:
                break

            neighbors = sorted(
                neighbors, key=lambda x: len(list(graph.neighbors(x))), reverse=True
            )
            operations_count += len(neighbors)
            candidate = random.choice(neighbors[: max(1, len(neighbors) // 2)])
            subset.append(candidate)
            neighbors = set(neighbors).intersection(set(graph.neighbors(candidate)))
            operations_count += 1

        # Evita redundâncias
        subset_id = tuple(sorted(subset))
        operations_count += len(subset)
        if subset_id in solutions_tested:
            continue
        solutions_tested.add(subset_id)
        operations_count += 1

        if len(subset) == clique_size and is_clique(graph, subset):
            operations_count += sum(1 for _ in itertools.combinations(subset, 2))
            return subset, operations_count, len(solutions_tested)

    return None, operations_count, len(solutions_tested)


@benchmark
def las_vegas_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)

    if is_small_graph(node_list, clique_size):
        return None, 0, 0

    operations_count = 0
    solutions_tested = 0

    for _ in range(num_trials):
        if operations_count > 150 * graph.size() ** 2 + 100000:
            break
        subset = []
        candidate_nodes = node_list[:]
        random.shuffle(candidate_nodes)

        for node in candidate_nodes:
            if operations_count > 150 * graph.size() ** 2 + 100000:
                break
            if len(subset) < clique_size and all(
                graph.has_edge(node, v) for v in subset
            ):
                subset.append(node)
                operations_count += len(subset) - 1

        solutions_tested += 1
        if len(subset) == clique_size:
            return subset, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def randomized_heuristic_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)

    if is_small_graph(node_list, clique_size):
        return None, 0, 0

    tested_solutions = set()
    operations_count = 0

    def heuristic(node):
        return len(list(graph.neighbors(node)))

    def generate_candidate():
        nonlocal operations_count
        sorted_nodes = sorted(node_list, key=heuristic, reverse=True)
        operations_count += len(node_list)

        candidate_pool = sorted_nodes[: len(sorted_nodes) // 2]
        if len(candidate_pool) < clique_size:
            return None
        subset = random.sample(candidate_pool, clique_size)
        operations_count += clique_size
        return subset

    for _ in range(num_trials):
        if operations_count > 150 * graph.size() ** 2 + 100000:
            break
        # Gera uma solução candidata
        candidate = generate_candidate()
        if candidate is None:
            continue
        candidate_id = tuple(sorted(candidate))
        operations_count += len(candidate)
        if candidate_id in tested_solutions:
            continue
        tested_solutions.add(candidate_id)
        operations_count += 1

        # Avalia a solução
        if is_clique(graph, candidate):
            operations_count += sum(1 for _ in itertools.combinations(candidate, 2))
            return (
                candidate,
                operations_count,
                len(tested_solutions),
            )

    return None, operations_count, len(tested_solutions)
