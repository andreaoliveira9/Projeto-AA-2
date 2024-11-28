import networkx as nx
import pickle

lines = []
with open("../graphs/SWlargeG.txt", "r") as f:
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    lines = f.readlines()

G = nx.Graph()
for line in lines:
    line = line.split()
    G.add_edge(int(line[0]), int(line[1]))

pickle.dump(G, open("../graphs/SWlargeG.pickle", "wb"))
