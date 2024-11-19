from utils import generate_random_graph
from algorithms import (
    exhaustive_clique_search,
)

k = 5
print("Criando grafo...")
G = generate_random_graph(seed=107637, size=20, maximum_number_edges=0.5)

print("Executando algoritmo exhaustive_clique_search...")
print(exhaustive_clique_search(graph=G, clique_size=k))
