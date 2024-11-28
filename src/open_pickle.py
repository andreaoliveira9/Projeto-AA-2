# ficheiro pickle
import pickle

path = input("Introduza o caminho do ficheiro pickle: ")
# Abra o ficheiro pickle em modo de leitura binária
with open(
    path,
    "rb",
) as f:
    dados = pickle.load(f)

print(dados)
