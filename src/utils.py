import json
from time import time
import networkx as nx
from collections import namedtuple
import logging, pickle

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

EDGES_DENSITY = [0.75, 0.5, 0.25, 0.125]
SEED = 107637
SIZES = 1000

Result = namedtuple(
    "Result", ["function", "result", "operations", "time", "solutions_tested"]
)


def generate_random_graph(seed=SEED, size=10, maximum_number_edges=0.8):
    return nx.fast_gnp_random_graph(size, maximum_number_edges, seed=seed)


def generate_all_graphs():
    all_graphs = {}
    for maximum_number_edges in EDGES_DENSITY:
        all_graphs[maximum_number_edges] = {}
        for size in range(1, 300):
            G = generate_random_graph(SEED, size, maximum_number_edges)
            all_graphs[maximum_number_edges][size] = G
            print(f"Generated graph with {size} nodes and {maximum_number_edges} edges")
        for size in range(300, SIZES + 1, 5):
            G = generate_random_graph(SEED, size, maximum_number_edges)
            all_graphs[maximum_number_edges][size] = G
            print(f"Generated graph with {size} nodes and {maximum_number_edges} edges")
    return all_graphs


def save_graphs():
    graphs = generate_all_graphs()
    pickle.dump(graphs, open("../graphs/all_graphs.pickle", "wb"))


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time()
        result, operations, solutions_tested = func(*args, **kwargs)
        end = time()

        return Result(func.__name__, result, operations, end - start, solutions_tested)

    return wrapper


def import_data(file):
    return pickle.load(open(f"{file}", "rb"))


def convert_to_json(alg_name, data, path, mode="all"):
    new_data = {}
    if mode == "all":
        for k, max_edges_dict in data.items():
            new_data[k] = {}
            for max_edges, sizes_dict in max_edges_dict.items():
                new_data[k][max_edges] = {}
                for size, results in sizes_dict.items():
                    if results.get("timed_out"):
                        # If timed out, only include the timed_out field
                        new_data[k][max_edges][size] = {
                            "timed_out": True,
                        }
                    else:
                        # Otherwise, include all results
                        new_data[k][max_edges][size] = {
                            "result": results["result"],
                            "operations_count": results["operations_count"],
                            "time": results["time"],
                            "solution_tested": results["solution_tested"],
                        }
                        if alg_name != "exhaustive_clique_search":
                            new_data[k][max_edges][size]["valid_result"] = results[
                                "valid_result"
                            ]
    else:
        for k, results in data.items():
            new_data[k] = {
                "result": results["result"],
                "operations_count": results["operations_count"],
                "time": results["time"],
                "solution_tested": results["solution_tested"],
            }

    # Write JSON data to a file
    with open(path, "w") as json_file:
        json.dump(new_data, json_file, indent=4)


if __name__ == "__main__":
    save_graphs()

    """ for size in [10000, 20000, 30000]:
        G = generate_random_graph(SEED, size, 0.25)
        pickle.dump(G, open(f"../graphs/{size}_graph.pickle", "wb")) """
