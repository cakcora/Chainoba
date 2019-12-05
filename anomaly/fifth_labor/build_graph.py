
#networkx version 2.4
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.max_columns = 20
import numpy as np
rng = np.random.RandomState(seed=5)
ints = rng.randint(1, 11, size=(3,2))
a = ['A', 'B', 'C']
b = ['D', 'A', 'E']
df = pd.DataFrame(ints, columns=['weight', 'cost'])
df[0] = a
df['b'] = b
df[['weight', 'cost', 0, 'b']]




G = nx.from_pandas_edgelist(df, 0, 'b', ['weight', 'cost'])
G['E']['C']['weight']

G['E']['C']['cost']

edges = pd.DataFrame({'source': [0, 1, 2],
                      'target': [2, 2, 3],
                      'weight': [3, 4, 5],
                      'color': ['red', 'blue', 'blue']})
G = nx.from_pandas_edgelist(edges, edge_attr=True, create_using=nx.MultiDiGraph())
# G[0][2]['color']

plt.subplot(121)

nx.draw(G, with_labels=True, font_weight='bold')
plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()