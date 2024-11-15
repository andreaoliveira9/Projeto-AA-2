import itertools
from utils import benchmark


def is_clique(graph, nodes):
    """Check if the given set of nodes forms a clique in the graph."""
    return all(graph.has_edge(u, v) for u, v in itertools.combinations(nodes, 2))


@benchmark
def dynamic_programming_clique(graph, clique_size):
    num_nodes = len(graph)
    operations_count = 0
    solutions_tested = 0
    memo = {}

    def is_clique_memoized(subset):
        # Armazena o resultado se ainda não foi calculado
        frozen_subset = frozenset(subset)
        if frozen_subset in memo:
            return memo[frozen_subset]
        is_clique_result = is_clique(graph, subset)
        memo[frozen_subset] = is_clique_result
        return is_clique_result

    # Verifica todas as possíveis subsoluções de tamanhos menores
    for i in range(1 << num_nodes):
        current_clique = [j for j in range(num_nodes) if (i & (1 << j)) > 0]
        operations_count += 1

        if len(current_clique) == clique_size:
            solutions_tested += 1
            # Utiliza a função memoizada
            if is_clique_memoized(current_clique):
                return current_clique, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def exhaustive_clique_search(graph, clique_size):
    node_list = list(graph.nodes)
    solutions_tested = 0
    operations_count = 0

    for subset in itertools.combinations(node_list, clique_size):
        solutions_tested += 1  # Increment tested solutions
        operations_count += 1  # Count this combination check
        if is_clique(graph, subset):
            return subset, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def backtracking_clique(graph, clique_size):
    def find_clique(current_clique, start_index):
        nonlocal operations_count, solutions_tested
        operations_count += 1  # Count this recursive call
        if len(current_clique) == clique_size:
            return current_clique
        for i in range(start_index, len(node_list)):
            solutions_tested += 1  # Increment tested solutions
            new_clique = current_clique + [node_list[i]]
            if is_clique(graph, new_clique):
                result = find_clique(new_clique, i + 1)
                if result:
                    return result
        return None

    node_list = list(graph.nodes)
    operations_count = 0
    solutions_tested = 0
    return find_clique([], 0), operations_count, solutions_tested


@benchmark
def greedy_clique_search(graph, clique_size):
    operations_count = 0
    solutions_tested = 0
    sorted_nodes = sorted(graph.nodes, key=lambda x: graph.degree(x), reverse=True)

    for node in sorted_nodes:
        current_clique = {node}
        for potential_node in sorted_nodes:
            operations_count += 1  # Count the attempt to add a node to the clique
            if potential_node != node and all(
                graph.has_edge(potential_node, v) for v in current_clique
            ):
                current_clique.add(potential_node)

            if len(current_clique) == clique_size:
                solutions_tested += 1
                solution_list = list(current_clique)
                return solution_list, operations_count, solutions_tested

    return None, operations_count, solutions_tested


@benchmark
def branch_and_bound_clique(graph, clique_size):
    def branch(current_clique, candidates):
        nonlocal operations_count, solutions_tested, found_clique
        if len(current_clique) == clique_size:
            found_clique = current_clique[:]
            return True

        if len(current_clique) + len(candidates) < clique_size:
            return False

        for i in range(len(candidates)):
            node = candidates[i]
            new_clique = current_clique + [node]

            solutions_tested += 1  # Increment tested solutions
            operations_count += 1  # Count the candidate evaluation
            if is_clique(graph, new_clique):
                if branch(new_clique, candidates[i + 1 :]):
                    return True

        return False

    node_list = list(graph.nodes)
    operations_count = 0
    solutions_tested = 0
    found_clique = None

    branch([], node_list)
    return found_clique, operations_count, solutions_tested
