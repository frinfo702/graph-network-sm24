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
                new_v = random.choice([node for node in self.graph.nodes() if node != u and not self.graph.has_edge(u, node)])
            else:
                new_v = v
                new_u = random.choice([node for node in self.graph.nodes() if node != v and not self.graph.has_edge(node, v)])

            self.graph.add_edge(new_u, new_v)
        
        return self.graph
    


        
# 使用例
if __name__ == "__main__":
    swn = SmallWorldNetwork(n_nodes=100, k_neighbors=4)
    print(swn.calculate_metrics)