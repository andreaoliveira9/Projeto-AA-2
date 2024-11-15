import os
from pprint import pprint

from matplotlib import pyplot as plt
from utils import MAXIMUM_NUMBER_EDGES, NUMBER_OF_ITERATIONS, import_data


def plot_number_operations_vs_number_of_vertices(
    results, name, log=False, save=False, show=False
):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 256):
            x.append(size)
            y.append(results[max_edges][size].operations)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Number of operations")
        # plt.title(f"Number of operations vs number of vertices for {name} algorithm")
        plt.legend()

    if save:
        plt.savefig(f"../charts/{name}_number_operations_vs_number_of_vertices.png")
    if show:
        plt.show()

    plt.close()


def plot_time_vs_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 256):
            x.append(size)
            y.append(results[max_edges][size].time)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Time (s)")
        # plt.title(f"Time taken vs number of vertices for {name} algorithm")
        plt.legend()

    if save:
        plt.savefig(f"../charts/{name}_time_vs_number_of_vertices.png")
    if show:
        plt.show()
    plt.close()


def plot_number_of_solutions_tested_vs_graph_size(
    results, name, log=False, save=False, show=False
):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 256):
            x.append(size)
            y.append(results[max_edges][size].solution_counter)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Number of solutions tested")
        # plt.title(f"Number of solutions tested vs number of vertices for {name} algorithm")
        plt.legend()

    if save:
        plt.savefig(f"../charts/{name}_number_of_solutions_tested_vs_graph_size.png")
    if show:
        plt.show()
    plt.close()


def plot_number_of_solutions_with_fixed_edges_and_different_iterations(
    algorithm_name_file, name, max_edges, log=False, save=False, show=False
):
    x = []
    y = []
    # open all the files that start with results_adaptive_randomized_vertex_cover
    files = [f for f in os.listdir("../results") if f.startswith(algorithm_name_file)]

    # load all the files
    results = [import_data(f"../results/{file}") for file in files]
    for size in range(4, 256):
        # plot all the files as different lines where each one is a different iteration
        for result in results:
            x.append(size)
            y.append(result[max_edges][size].solution_counter)
        if log:
            plt.semilogy(x, y, label=f"size: {size}")
        else:
            plt.plot(x, y, label=f"size: {size}")
        x = []
        y = []
    plt.xlabel("Number of iterations")
    plt.ylabel("Number of solutions tested")
    # plt.title(f"Number of solutions tested vs number of iterations for {name} algorithm")
    plt.legend()
    if save:
        plt.savefig(
            f"../charts/{name}_number_of_solutions_tested_vs_number_of_iterations.png"
        )
    if show:
        plt.show()
    plt.close()


def plot_full_results(results, name, log=False, save=False, show=False):
    plot_number_operations_vs_number_of_vertices(
        results, name, log=log, show=show, save=save
    )
    plot_time_vs_number_of_vertices(results, name, log=log, show=show, save=save)
    plot_number_of_solutions_tested_vs_graph_size(
        results, name, log=log, show=show, save=save
    )


def main():
    # Open all the files that start with results_adaptive_randomized_vertex_cover
    files = [
        f
        for f in os.listdir("../results")
        if f.startswith("results_adaptive_randomized_vertex_cover_")
    ]

    # Load all the files
    results = [import_data(f"../results/{file}") for file in files]

    # Plot all the files as different lines where each one is a different algorithm
    for result, file in zip(results, files):
        plot_full_results(
            result,
            file.replace("results_", "").replace(".pickle", ""),
            log=True,
            save=True,
            show=False,
        )


if __name__ == "__main__":
    main()
