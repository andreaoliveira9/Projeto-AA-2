# ficheiro pickle
import pickle

# Abra o ficheiro pickle em modo de leitura binária
with open(
    "/Users/andreoliveira/Documents/GitHub/Projeto-AA-2/graphs/SWlargeG.pickle",
    "rb",
) as f:
    dados = pickle.load(f)

print(dados)
