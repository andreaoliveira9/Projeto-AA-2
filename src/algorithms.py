import itertools
from utils import benchmark
from time import time as tim


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
