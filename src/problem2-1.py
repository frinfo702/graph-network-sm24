# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx
import scipy as sp
# %%
def create_cycle_graph(n):
    G = networkx.Graph()
    for i in range(n):
        G.add_edge(i, (i + 1) % n)
    return G

# サイクルグラフの作成
n = 100
G = create_cycle_graph(n)
pos = networkx.circular_layout(G) # set circle layout
networkx.draw(G, pos=pos, node_size=10, node_color='blue')
plt.title("Watts-Strogatz Small-World Network")
plt.show()
# %%
def expand_cycle_graph(G, k):
    n = G.number_of_nodes()
    half_k = k // 2
    for i in range(n):
        for j in range(1, half_k + 1):
            G.add_edge(i, (i + j) % n)
            G.add_edge(i, (i - j) % n)
    return G

# グラフの拡張
k = 4
G = expand_cycle_graph(G, k)
networkx.draw(G, pos=pos, node_size=10, node_color='blue')
plt.show()
# %%
# 枝の張り替え確率pを設定
p = 0.5
# %%
import random

def rewire_graph(G, p):
    n = G.number_of_nodes()
    edges = list(G.edges())
    num_edges = len(edges)
    num_rewire = int(num_edges * p)

    for edge in random.sample(edges, num_rewire):
        u, v = edge
        G.remove_edge(u, v)
        
        # 張替えの方向を決定
        if random.random() < 0.5:
            new_u = u
            new_v = random.choice([node for node in G.nodes() if node != u and not G.has_edge(u, node)])
        else:
            new_v = v
            new_u = random.choice([node for node in G.nodes() if node != v and not G.has_edge(node, v)])
        
        G.add_edge(new_u, new_v)
    return G

# 枝の張替え
G = rewire_graph(G, p)

networkx.draw(G, pos=pos, node_size=10, node_color='blue')
plt.show()
# %%
