from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class NetworkGenerator(ABC):
    """ネットワーク生成の基底となるクラス"""
    @abstractmethod
    def generate(self) -> nx.Graph:
        pass

class NetworkAnalyzer:
    """class to analyze networks"""
    def calculate_metrics(self, G: nx.Graph):
        """compute network's metrics"""
        
        # calculate the path fo each of the subgraph
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
    
    def analyze_propaties(self, generator: NetworkGenerator, num_points=10) -> tuple:
        """anylize properties of the network as p changes"""
        p_values = np.logspace(-4, 0, num=num_points)
        L_values = []
        C_values = []
        for p in p_values:
            if hasattr(generator, 'p'):
                generator.p = p
            G = generator.generate()
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


