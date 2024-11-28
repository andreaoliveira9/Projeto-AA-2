import os
from matplotlib import pyplot as plt
from utils import import_data, EDGES_DENSITY


def plot_number_operations_vs_number_of_vertices(
    results, name, k, log=False, save=False, show=False
):
    for max_edges in EDGES_DENSITY:
        x = []
        y = []
        for size in range(k, 256):
            try:
                y.append(results[k][max_edges][size]["operations_count"])
            except KeyError:
                break
            x.append(size)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")

        plt.xlabel("Number of vertices")
        plt.ylabel("Number of operations")
        plt.title(f"Number of Operations vs Number of Vertices for k={k}")
        plt.legend()
        plt.grid(True)

    if save:
        plt.savefig(
            f"../charts/{name}/k{k}_number_operations_vs_number_of_vertices.png"
        )
    if show:
        plt.show()

    plt.close()


def plot_time_vs_number_of_vertices(
    results, name, k, log=False, save=False, show=False
):
    for max_edges in EDGES_DENSITY:
        x = []
        y = []
        for size in range(k, 256):
            try:
                y.append(results[k][max_edges][size]["time"])
            except KeyError:
                break
            x.append(size)

        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Time (s)")
        plt.title(f"Time Taken vs Number of Vertices for k={k}")
        plt.legend()
        plt.grid(True)

    if save:
        plt.savefig(f"../charts/{name}/k{k}_time_vs_number_of_vertices.png")
    if show:
        plt.show()
    plt.close()


def plot_number_of_solutions_tested_vs_graph_size(
    results, name, k, log=False, save=False, show=False
):
    for max_edges in EDGES_DENSITY:
        x = []
        y = []
        for size in range(k, 256):
            try:
                y.append(results[k][max_edges][size]["solution_tested"])
            except KeyError:
                break
            x.append(size)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Number of solutions tested")
        plt.title(f"Number of Solutions Tested vs Number of Vertices for k={k}")
        plt.legend()
        plt.grid(True)

    if save:
        plt.savefig(
            f"../charts/{name}/k{k}_number_of_solutions_tested_vs_graph_size.png"
        )
    if show:
        plt.show()
    plt.close()


def precision_greedy_results(results, name):
    total = 0
    valid_results = 0

    for k in results:
        for max_edges in results[k]:
            for size in results[k][max_edges]:
                try:
                    result = results[k][max_edges][size]["valid_result"]
                    if result == True or result == False:
                        total += 1
                        if result:
                            valid_results += 1
                except KeyError:
                    continue

    return valid_results / total * 100


def main():
    k_values = [5, 10, 15]
    # Open all the files that start with results_adaptive_randomized_vertex_cover
    files = [f for f in os.listdir("../results/pickle") if f.endswith(".pickle")]

    # Load all the files
    results = [import_data(f"../results/pickle/{file}") for file in files]

    # Plot all the files as different lines where each one is a different algorithm
    for result, file in zip(results, files):
        if "exhaustive_clique_search" not in file:
            precision = precision_greedy_results(result, file.replace(".pickle", ""))
            print(f"Precision for {file.replace(".pickle", "")}: {precision}%")

        for k in k_values:
            plot_number_of_solutions_tested_vs_graph_size(
                result,
                file.replace(".pickle", ""),
                k,
                log=True,
                save=True,
                show=False,
            )
            plot_time_vs_number_of_vertices(
                result,
                file.replace(".pickle", ""),
                k,
                log=True,
                save=True,
                show=False,
            )
            plot_number_operations_vs_number_of_vertices(
                result,
                file.replace(".pickle", ""),
                k,
                log=True,
                save=True,
                show=False,
            )


if __name__ == "__main__":
    main()
