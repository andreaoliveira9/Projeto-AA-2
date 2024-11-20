import itertools
import random
from utils import benchmark
from time import time


def is_clique(graph, subset):
    return all(graph.has_edge(u, v) for u, v in itertools.combinations(subset, 2))


@benchmark
def exhaustive_clique_search(graph, clique_size):
    node_list = list(graph.nodes)
    solutions_tested = 0
    operations_count = 0

    for subset in itertools.combinations(node_list, clique_size):
        solutions_tested += 1
        operations_count += 1 + sum(1 for _ in itertools.combinations(subset, 2))
        if is_clique(graph, subset):
            return subset, operations_count, solutions_tested  # Stop immediately

    return None, operations_count, solutions_tested


@benchmark
def random_sampling_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)
    operations_count = 0
    solutions_tested = 0

    for _ in range(num_trials):
        if operations_count > 150 * graph.size() ** 2 + 100000:
            break
        subset = random.sample(node_list, clique_size)
        solutions_tested += 1
        operations_count += 1 + sum(1 for _ in itertools.combinations(subset, 2))
        if is_clique(graph, subset):
            return subset, operations_count, solutions_tested  # Stop immediately

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
            return subset, operations_count, solutions_tested  # Stop immediately

    return None, operations_count, solutions_tested


@benchmark
def monte_carlo_with_heuristic(graph, clique_size, num_trials=1000):
    """
    Algoritmo Monte Carlo que combina geração aleatória com heurísticas.
    """
    node_list = list(graph.nodes)
    solutions_tested = set()
    operations_count = 0  # Contador de operações

    for _ in range(num_trials):
        subset = []
        # Inicia com um nó aleatório
        node = random.choice(node_list)
        subset.append(node)
        neighbors = set(graph.neighbors(node))
        operations_count += 1  # Escolha do nó inicial

        # Usa heurísticas para expandir o subconjunto
        while len(subset) < clique_size:
            if not neighbors or operations_count > 150 * graph.size() ** 2 + 100000:
                break
            # Ordena vizinhos por grau (heurística) e seleciona o melhor
            neighbors = sorted(
                neighbors, key=lambda x: len(list(graph.neighbors(x))), reverse=True
            )
            operations_count += len(neighbors)  # Operação de ordenação
            candidate = random.choice(neighbors[: max(1, len(neighbors) // 2)])
            subset.append(candidate)
            neighbors.intersection_update(graph.neighbors(candidate))
            operations_count += 1  # Atualização do conjunto de vizinhos

        # Evita redundâncias
        subset_id = tuple(sorted(subset))
        operations_count += len(subset)  # Operação de ordenação
        if subset_id in solutions_tested:
            continue
        solutions_tested.add(subset_id)
        operations_count += 1  # Adiciona ao conjunto

        # Verifica se a solução é válida
        if len(subset) == clique_size and is_clique(graph, subset):
            operations_count += sum(
                1 for _ in itertools.combinations(subset, 2)
            )  # Checagem do clique
            return subset, operations_count, len(solutions_tested)  # Para imediatamente

    return None, operations_count, len(solutions_tested)


@benchmark
def las_vegas_clique(graph, clique_size, num_trials=1000):
    node_list = list(graph.nodes)
    operations_count = 0
    solutions_tested = 0

    for _ in range(num_trials):
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
            return subset, operations_count, solutions_tested  # Stop immediately

    return None, operations_count, solutions_tested


@benchmark
def randomized_heuristic_clique(graph, clique_size, num_trials=1000):
    """
    Combina geração aleatória com heurísticas para encontrar um clique.
    """
    node_list = list(graph.nodes)
    tested_solutions = set()
    operations_count = 0  # Contador de operações

    def heuristic(node):
        """Heurística: Retorna o número de vizinhos de um nó."""
        return len(list(graph.neighbors(node)))

    def generate_candidate():
        """
        Gera uma solução candidata usando um misto de randomização
        e heurísticas.
        """
        nonlocal operations_count
        # Ordena nós com base na heurística (nós com mais vizinhos primeiro)
        sorted_nodes = sorted(node_list, key=heuristic, reverse=True)
        operations_count += len(node_list)  # Operação de ordenação
        # Seleciona aleatoriamente, mas com viés para os primeiros (mais conectados)
        subset = random.sample(sorted_nodes[: len(sorted_nodes) // 2], clique_size)
        operations_count += clique_size  # Operação de seleção
        return subset

    for iteration in range(num_trials):
        if operations_count > 150 * graph.size() ** 2 + 100000:
            break
        # Gera uma solução candidata
        candidate = generate_candidate()
        candidate_id = tuple(sorted(candidate))
        operations_count += len(candidate)  # Operação de ordenação
        if candidate_id in tested_solutions:
            continue
        tested_solutions.add(candidate_id)
        operations_count += 1  # Adiciona ao conjunto

        # Avalia a solução
        if is_clique(graph, candidate):
            operations_count += sum(
                1 for _ in itertools.combinations(candidate, 2)
            )  # Checagem do clique
            return (
                candidate,
                iteration,
                operations_count,
                len(tested_solutions),
            )  # Para imediatamente

    return None, None, operations_count, len(tested_solutions)
