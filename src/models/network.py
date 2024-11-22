from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
import random
import icecream as ic
import matplotlib.pyplot as plt

class NetworkGenerator(ABC):
    """ネットワーク生成の基底となるクラス"""
    @abstractmethod
    def generate(self) -> nx.Graph:
        pass

class SmallWorldNetwork(NetworkGenerator):
    def __init__(self, n_nodes, k_neighbors, p_rewiring=1e-2):
        self.n = n_nodes # number of nodes
        self.k = k_neighbors # number of nearest neighbors
        self.p = p_rewiring # probability of rewiring
        self.graph = nx.Graph()

    def generate(self) -> nx.Graph:
        """create a small-world network"""
        # initialize
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.n))

        # TODO
        # このへんの実装をうまいことやる

        # create simple connection
        for i in range(self.n):
            self.graph.add_edge(i, (i+1)%self.n)
        
        # rewire k-nearest neighbors
        half_k = self.k // 2
        for i in range(self.n):
            for j in range(1, half_k+1):
                self.graph.add_edge(i, (i+j) % self.n)  
                self.graph.add_edge(i, (i-j) % self.n)
        
        edges = list(self.graph.edges())
        num_edges = len(edges)
        num_edges = len(edges)
        num_rewire = int(num_edges * self.p)

        for edge in random.sample(edges, num_rewire):
            u, v = edge
            self.graph.remove_edge(u, v)
        
            # define a direction of rewiring
            if random.random() < 0.5:
                new_u = u
                new_v = random.choice([node for node in self.graph.nodes() if node != u and not G.has_edge(u, node)])
            else:
                new_v = v
                new_u = random.choice([node for node in self.graph.nodes() if node != v and not G.has_edge(node, v)])

            self.graph.add_edge(new_u, new_v)
        
        return self.graph
    
    def calculate_metrics(self, G):
        """calculate metrics of the network"""

        # calculate the path of each of the subgraphs (or connected component) and store them in path_temp
        path_temp = []
        weights = []
        for subgraph in (G.subgraph(c).copy() for c in nx.connected_components(G)):
            path_temp.append(nx.average_shortest_path_length(subgraph))
        # create a variable weight that holds the size of each subgraph (or connected component)
        # alternatively I have weighted by graph size but we could use anything to weight the average
        for components in nx.connected_components(G):
            weights.append(len(components))
        # compute the weighted average
        avg_shotest_path = np.average(path_temp,weights = weights) 
        avg_cluster = nx.average_clustering(G)
        
        return avg_shotest_path, avg_cluster

    def analyze_propaties(self, num_points=10) -> tuple:
        """anylize properties of the network as p changes"""
        p_values = np.logspace(-4, 0, num=num_points)
        L_values = []
        C_values = []
        for p in p_values:
            G = self.create_small_world_network(p)
            L, C = self.calculate_metrics(G)
            L_values.append(L)
            C_values.append(C)

        return p_values, np.array(L_values), np.array(C_values)

    def plot_propaties(self, p_values, L_values, C_values):
        """plot propaties of the network"""
        plt.figure(figsize=(12, 4))
        plt.plot(p_values, L_values/L_values[0], label="average shortest path length")
        plt.plot(p_values, C_values/C_values[0], label="average clustering coefficient")
        plt.xscale("log")
        plt.xlabel("rewiring probability")
        plt.ylabel("normalized values of metrics")
        plt.grid(True)
        plt.legend()
        plt.show()

        
# 使用例
if __name__ == "__main__":
    swn = SmallWorldNetwork(n_nodes=100, k_neighbors=4)
    print(swn.calculate_metrics)