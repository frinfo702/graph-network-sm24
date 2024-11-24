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
        
        # rewire edges
        # 隣接行列の表を意識して！
        edges = list(self.graph.edges())
        for u, v in edges:
            if random.random() < self.p:
                # remove a edge
                self.graph.remove_edge(u, v)
                # select new endpoint
                while True:
                    new_node = random.randint(0, self.n - 1)
                    if new_node != u and not self.graph.has_edge(u, new_node):
                        break
                self.graph.add_edge(u, new_node)
        
        return self.graph
    
    def draw(self, G: nx.Graph):
        # draw a SmallWorldNetwork 
        pos = nx.circular_layout(G)
        nx.draw(G, pos, node_size=30, node_color='red')
        plt.axis('off')
        plt.show()
    
# 格子グラフ
# TODO: nodeを適当に置きまくって、その距離が1のもの同士を繋げばいいのか。多分これ
class LatticeGraph(NetworkGenerator):
    
    def __init__(self, width, height, num_node):
        """
        Initialize a lattice graph generator
        Args:
        width (int): Width of the lattice grid
        height (int): Height of the lattice grid 
        """
        self.num_node = num_node # a number of node
        self.width = width
        self.height = height
        self.graph = nx.Graph

    def generate(self) -> nx.Graph:
        """create a lattice graph"""
        self.graph = nx.Graph()

        # create array of all possible grid coordinates
        all_points = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        # select n nodes randomly
        selected_points = random.sample(all_points, min(self.num_node, len(all_points)))
        
        # add selected points as nodes
        for point in selected_points:
            self.graph.add_node(point)
                    
        # 行方向にエッジを追加
        for x, y in selected_points:
            neighbor = (x, y + 1)
            if neighbor in selected_points:
                self.graph.add_edge((x, y), neighbor)
        
        # 列方向にエッジを追加
        for x, y in selected_points:
            neighbor = (x + 1, y)
            if neighbor in selected_points:
                self.graph.add_edge((x, y), neighbor)
        
        return self.graph
    
    def draw(self, G: nx.Graph):
        # LatticeGraph用の描画方法
        pos = {node: node for node in G.nodes()}
        nx.draw(G, pos, node_size=30, node_color='blue', with_labels=False)
        plt.axis('off')
        plt.show()     
        
# 使用例
if __name__ == "__main__":
    swn = SmallWorldNetwork(n_nodes=100, k_neighbors=4)
    print(swn.calculate_metrics)
