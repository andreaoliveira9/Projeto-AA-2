# ficheiro pickle
import pickle

# Abra o ficheiro pickle em modo de leitura binária
with open(
    "/Users/andreoliveira/Library/CloudStorage/OneDrive-UniversidadedeAveiro/1º Semestre/Algoritmos Avançados/Projeto 1/results/pickle/greedy_clique_search.pickle",
    "rb",
) as f:
    dados = pickle.load(f)

print(dados)
