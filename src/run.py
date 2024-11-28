import signal
from collections import defaultdict
from algorithms import (
    exhaustive_clique_search,
    random_sampling_clique,
    monte_carlo_clique,
    monte_carlo_with_heuristic_clique,
    las_vegas_clique,
    randomized_heuristic_clique,
)
from utils import EDGES_DENSITY, SIZES, log, convert_to_json
import pickle
import json
import os

# Carregar os grafos previamente gerados
graphs = pickle.load(open("../graphs/all_graphs.pickle", "rb"))

# Lista de valores de clique de tamanho k que estamos procurando
k_values = [5, 6, 7, 8, 9, 10, 15]  # Exemplo, ajuste conforme necessário
TIME_LIMIT = 100


# Timeout handler function
def timeout_handler(signum, frame):
    raise TimeoutError("Algoritmo ultrapassou o limite de tempo")


# Função para rodar o algoritmo e armazenar os resultados
def run(algorithm, name):
    if name != "exhaustive_clique_search":
        results_exhaustive = pickle.load(
            open(f"../results/pickle/exhaustive_clique_search.pickle", "rb")
        )

    results = defaultdict(dict)
    for k in k_values:
        for max_edges in EDGES_DENSITY:
            for size in range(1, SIZES + 1):
                if size > 300 and size % 5 != 0:
                    continue

                log.info(
                    f"Running {name} algorithm for graph with size {size}, clique size {k}, and density of edges {max_edges}"
                )
                try:
                    # Start the timer
                    signal.signal(signal.SIGALRM, timeout_handler)
                    if name == "exhaustive_clique_search":
                        signal.alarm(TIME_LIMIT)
                    else:
                        signal.alarm(int(1 / 1700 * size**2 + 0.8))

                    if name == "exhaustive_clique_search":
                        (
                            algorithm_name,
                            result,
                            operations_count,
                            time,
                            solution_tested,
                        ) = algorithm(graphs[max_edges][size], k)
                    else:
                        (
                            algorithm_name,
                            result,
                            operations_count,
                            time,
                            solution_tested,
                        ) = algorithm(
                            graphs[max_edges][size], k, 80 * size**2 + 75000
                        )

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

                    if algorithm_name != "exhaustive_clique_search":
                        try:
                            result_exhaustive = results_exhaustive[k][max_edges][size][
                                "result"
                            ]

                            if result is not None:
                                results[k][max_edges][size]["valid_result"] = (
                                    True if type(result_exhaustive) == tuple else False
                                )
                            else:
                                results[k][max_edges][size]["valid_result"] = (
                                    False if type(result_exhaustive) == tuple else True
                                )
                        except KeyError:
                            results[k][max_edges][size][
                                "valid_result"
                            ] = "No valid result to compare"

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

                    signal.alarm(0)  # Disable any alarm just in case
                    break  # Saia do loop max_edges

    pickle.dump(results, open(f"../results/pickle/{name}.pickle", "wb"))
    convert_to_json(name, results, f"../results/json/{name}.json")
    log.info(f"Results for {name} algorithm saved to pickle and json files")


# Função principal que executa todos os algoritmos
def marathon():
    algorithms = [
        (exhaustive_clique_search, "exhaustive_clique_search"),
        (random_sampling_clique, "random_sampling_clique"),
        (monte_carlo_clique, "monte_carlo_clique"),
        (monte_carlo_with_heuristic_clique, "monte_carlo_with_heuristic_clique"),
        (las_vegas_clique, "las_vegas_clique"),
        (randomized_heuristic_clique, "randomized_heuristic_clique"),
    ]

    # Executar todos os algoritmos
    for algorithm, name in algorithms:
        # run(algorithm, name)
        SWlargeG(algorithm, name)


def SWlargeG(algorithm, name):
    graph = pickle.load(open("../graphs/SWlargeG.pickle", "rb"))

    if name != "exhaustive_clique_search":
        results_exhaustive = pickle.load(
            open(f"../results/pickle/SWlargeG_exhaustive_clique_search.pickle", "rb")
        )

    results = defaultdict(dict)
    for k in k_values:
        log.info(f"Running {name} algorithm for SWlargeG graph with clique size {k}")
        try:
            # Start the timer
            signal.signal(signal.SIGALRM, timeout_handler)
            if name == "exhaustive_clique_search":
                signal.alarm(TIME_LIMIT)
            else:
                signal.alarm(50)

            if name == "exhaustive_clique_search":
                (
                    algorithm_name,
                    result,
                    operations_count,
                    time,
                    solution_tested,
                ) = algorithm(graph, k)
            else:
                (
                    algorithm_name,
                    result,
                    operations_count,
                    time,
                    solution_tested,
                ) = algorithm(graph, k, 80 * graph.size() ** 2 + 75000)

            # Cancel the timer if completed within time limit
            signal.alarm(0)

            # Initialize results dictionary keys if needed
            if k not in results:
                results[k] = {}

            results[k] = {
                "result": result,
                "operations_count": operations_count,
                "time": time,
                "solution_tested": solution_tested,
            }

            if algorithm_name != "exhaustive_clique_search":
                try:
                    result_exhaustive = results_exhaustive[k]["result"]

                    if result is not None:
                        results[k]["valid_result"] = (
                            True if type(result_exhaustive) == tuple else False
                        )
                    else:
                        results[k]["valid_result"] = (
                            False if type(result_exhaustive) == tuple else True
                        )
                except KeyError:
                    results[k]["valid_result"] = "No valid result to compare"

        except TimeoutError:
            log.warning(
                f"{name} algorithm timed out for SWlargeG graph with clique size {k}"
            )

            if k not in results:
                results[k] = {}

            results[k] = {
                "timed_out": True,
            }

            signal.alarm(0)  # Disable any alarm just in case

    pickle.dump(results, open(f"../results/pickle/SWlargeG_{name}.pickle", "wb"))

    file_path = f"../results/pickle/SWlargeG_{name}.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(
            results,
            json_file,
            ensure_ascii=False,
            indent=4,
        )

    log.info(f"Results for {name} algorithm saved to pickle and json files")


if __name__ == "__main__":
    marathon()
