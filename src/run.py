import signal
from collections import defaultdict
from algorithms import (
    dynamic_programming_clique,
    exhaustive_clique_search,
    backtracking_clique,
    greedy_clique_search,
    branch_and_bound_clique,
)
from utils import EDGES_DENSITY, SIZES, log, convert_to_json
import pickle

# Carregar os grafos previamente gerados
graphs = pickle.load(open("../graphs/all_graphs.pickle", "rb"))

# Lista de valores de clique de tamanho k que estamos procurando
k_values = [5, 6, 7, 8, 9, 10, 15]  # Exemplo, ajuste conforme necessário
TIME_LIMIT = 5  # Defina o limite de tempo em segundos


# Timeout handler function
def timeout_handler(signum, frame):
    raise TimeoutError("Algoritmo ultrapassou o limite de tempo")


# Função para rodar o algoritmo e armazenar os resultados
def run(algorithm, name):
    results = defaultdict(dict)
    for k in k_values:
        timeout_occurred = False
        for max_edges in EDGES_DENSITY:
            for size in range(k, SIZES):
                if timeout_occurred:
                    break  # Saia do loop 'size' se ocorrer timeout
                log.info(
                    f"Running {name} algorithm for graph with size {size}, clique size {k}, and density of edges {max_edges}"
                )
                try:
                    # Start the timer
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(TIME_LIMIT)

                    (
                        algorithm_name,
                        result,
                        operations_count,
                        time,
                        solution_tested,
                    ) = algorithm(graphs[max_edges][size], k)

                    # Cancel the timer if completed within time limit
                    signal.alarm(0)

                    # Initialize results dictionary keys if needed
                    if k not in results:
                        results[k] = {}
                    if max_edges not in results[k]:
                        results[k][max_edges] = {}
                    if size not in results[k][max_edges]:
                        results[k][max_edges][size] = {}

                    results[k][max_edges][size] = {
                        "result": result,
                        "operations_count": operations_count,
                        "time": time,
                        "solution_tested": solution_tested,
                    }
                except TimeoutError:
                    log.warning(
                        f"{name} algorithm timed out for graph with size {size}, clique size {k}, and density of edges {max_edges}"
                    )

                    if k not in results:
                        results[k] = {}
                    if max_edges not in results[k]:
                        results[k][max_edges] = {}
                    if size not in results[k][max_edges]:
                        results[k][max_edges][size] = {}

                    results[k][max_edges][size] = {
                        "timed_out": True,
                    }

                    timeout_occurred = True  # Marcar que o timeout ocorreu
                    signal.alarm(0)  # Disable any alarm just in case
                    break  # Saia do loop max_edges

    pickle.dump(results, open(f"../results/pickle/{name}.pickle", "wb"))
    convert_to_json(results, f"../results/json/{name}.json")
    log.info(f"Results for {name} algorithm saved to pickle and json files")


# Função principal que executa todos os algoritmos
def marathon():
    algorithms = [
        (dynamic_programming_clique, "dynamic_programming_clique"),
        # (exhaustive_clique_search, "exhaustive_clique_search"),
        # (backtracking_clique, "backtracking_clique"),
        # (greedy_clique_search, "greedy_clique_search"),
        # (branch_and_bound_clique, "branch_and_bound_clique"),
    ]

    # Executar todos os algoritmos
    for algorithm, name in algorithms:
        run(algorithm, name)


if __name__ == "__main__":
    marathon()
