from utils import generate_random_graph
from algorithms import (
    dynamic_programming_clique,
    exhaustive_clique_search,
    backtracking_clique,
    greedy_clique_search,
    branch_and_bound_clique,
)

k = 5
print("Criando grafo...")
G = generate_random_graph(seed=107637, size=20, maximum_number_edges=0.5)

print("Executando algoritmo dynamic_programming_clique...")
print(dynamic_programming_clique(graph=G, clique_size=k))

print("Executando algoritmo exhaustive_clique_search...")
print(exhaustive_clique_search(graph=G, clique_size=k))

print("Executando algoritmo backtracking_clique...")
print(backtracking_clique(graph=G, clique_size=k))

print("Executando algoritmo greedy_clique_search...")
print(greedy_clique_search(graph=G, clique_size=k))

print("Executando algoritmo branch_and_bound_clique...")
print(branch_and_bound_clique(graph=G, clique_size=k))
