import itertools
import random
import math
from utils import benchmark


def is_clique(graph, subset):
    return all(graph.has_edge(u, v) for u, v in itertools.combinations(subset, 2))


@benchmark
def exhaustive_clique_search(graph, clique_size):
    node_list = list(graph.nodes)
    solutions_tested = 0
    operations_count = 0

    for subset in itertools.combinations(node_list, clique_size):
        solutions_tested += 1  # Increment tested solutions
        operations_count += 1 + sum(1 for _ in itertools.combinations(subset, 2))
        if is_clique(graph, subset):
            return subset, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def random_sampling_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)
    operations_count = 0
    solutions_tested = 0

    for _ in range(num_trials):
        subset = random.sample(node_list, clique_size)
        solutions_tested += 1
        operations_count += 1 + sum(1 for _ in itertools.combinations(subset, 2))
        if is_clique(graph, subset):
            return subset, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def monte_carlo_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)
    operations_count = 0
    solutions_tested = 0

    for _ in range(num_trials):
        subset = []
        node = random.choice(node_list)
        subset.append(node)
        neighbors = set(graph.neighbors(node))

        while len(subset) < clique_size:
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
def las_vegas_clique(graph, clique_size, max_restarts=1000):
    node_list = list(graph.nodes)
    operations_count = 0
    solutions_tested = 0

    for _ in range(max_restarts):
        subset = []
        candidate_nodes = node_list[:]
        random.shuffle(candidate_nodes)

        for node in candidate_nodes:
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
def simulated_annealing_clique(
    graph, clique_size, initial_temp=1000, cooling_rate=0.99, max_iter=1000
):
    node_list = list(graph.nodes)
    current_subset = random.sample(node_list, clique_size)
    current_energy = sum(
        1
        for u, v in itertools.combinations(current_subset, 2)
        if not graph.has_edge(u, v)
    )
    temperature = initial_temp
    operations_count = 0

    for _ in range(max_iter):
        if temperature <= 0:
            break

        # Neighbor generation: swap a random node
        new_subset = current_subset[:]
        replace_index = random.randint(0, clique_size - 1)
        new_node = random.choice([n for n in node_list if n not in new_subset])
        new_subset[replace_index] = new_node

        new_energy = sum(
            1
            for u, v in itertools.combinations(new_subset, 2)
            if not graph.has_edge(u, v)
        )
        operations_count += clique_size

        # Decide whether to accept the new state
        if new_energy < current_energy or random.random() < math.exp(
            (current_energy - new_energy) / temperature
        ):
            current_subset, current_energy = new_subset, new_energy

        # Cooling
        temperature *= cooling_rate

        if current_energy == 0 and len(current_subset) == clique_size:
            return current_subset, operations_count, _  # Found solution

    return None, operations_count, max_iter


@benchmark
def genetic_clique(graph, clique_size, population_size=50, generations=100):
    node_list = list(graph.nodes)
    population = [random.sample(node_list, clique_size) for _ in range(population_size)]
    operations_count = 0

    def fitness(subset):
        return sum(
            1 for u, v in itertools.combinations(subset, 2) if graph.has_edge(u, v)
        )

    for _ in range(generations):
        # Evaluate fitness
        population = sorted(population, key=fitness, reverse=True)
        if fitness(population[0]) == clique_size * (clique_size - 1) // 2:
            return population[0], operations_count, _

        # Selection and crossover
        new_population = population[: population_size // 2]
        while len(new_population) < population_size:
            parents = random.sample(new_population[:10], 2)
            crossover_point = random.randint(1, clique_size - 1)
            child = parents[0][:crossover_point] + parents[1][crossover_point:]
            child = list(set(child))  # Ensure no duplicates
            if len(child) < clique_size:
                child.extend(
                    random.sample(
                        [n for n in node_list if n not in child],
                        clique_size - len(child),
                    )
                )
            new_population.append(child)

        # Mutation
        for individual in new_population:
            if random.random() < 0.1:  # Mutation probability
                mutate_index = random.randint(0, clique_size - 1)
                individual[mutate_index] = random.choice(
                    [n for n in node_list if n not in individual]
                )

        population = new_population
        operations_count += population_size * clique_size

    return None, operations_count, generations
