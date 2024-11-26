import random
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import networkx as nx


class NetworkGenerator(ABC):
    """
    Abstract base class for network generation.
    Defines the interface for creating different types of networks.
    """

    @abstractmethod
    def generate(self) -> nx.Graph:
        """
        Abstract method to generate a network.
        Returns:
            nx.Graph: Generated network
        """
        pass


class WattsStrogatzNetwork(NetworkGenerator):
    def __init__(self, n_nodes, k_neighbors, p_rewiring=1e-1):
        self.n = n_nodes  # number of nodes
        self.k = k_neighbors  # number of nearest neighbors
        self.p = p_rewiring  # probability of rewiring
        self.graph = nx.Graph()

    def generate(self) -> nx.Graph:
        """create a small-world network"""
        # initialize
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.n))

        # create simple connection
        for i in range(self.n):
            self.graph.add_edge(i, (i + 1) % self.n)

        # rewire k-nearest neighbors
        half_k = self.k // 2
        for i in range(self.n):
            for j in range(1, half_k + 1):
                self.graph.add_edge(i, (i + j) % self.n)
                self.graph.add_edge(i, (i - j) % self.n)

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
        nx.draw(G, pos, node_size=30, node_color="red")
        plt.axis("off")
        plt.show()


class LatticeNetwork(NetworkGenerator):
    def __init__(self, width, height):
        """
        Initialize a lattice graph generator
        Args:
        width (int): Width of the lattice grid
        height (int): Height of the lattice grid
        """
        self.width = width
        self.height = height
        self.graph = nx.Graph

    def generate(self) -> nx.Graph:
        """create a lattice graph"""
        self.graph = nx.Graph()

        # create array of all possible grid coordinates
        all_points = [(x, y) for x in range(self.width) for y in range(self.height)]

        # select n nodes randomly

        # add selected points as nodes
        for x, y in all_points:
            self.graph.add_node((x, y))

        # 行方向にエッジを追加
        for x, y in all_points:
            neighbor = (x, y + 1)
            if neighbor in all_points:
                self.graph.add_edge((x, y), neighbor)

        # 列方向にエッジを追加
        for x, y in all_points:
            neighbor = (x + 1, y)
            if neighbor in all_points:
                self.graph.add_edge((x, y), neighbor)

        return self.graph

    def draw(self, G: nx.Graph):
        # LatticeGraph用の描画方法
        pos = {node: node for node in G.nodes()}
        nx.draw(G, pos, node_size=30, node_color="blue", with_labels=False)
        plt.axis("off")
        plt.show()


class PartialLatticeNetwork(NetworkGenerator):

    def __init__(self, width, height, num_node):
        """
        Initialize a patial lattice graph generator
        Args:
        width (int): Width of the lattice grid
        height (int): Height of the lattice grid
        """
        self.num_node = num_node  # a number of node
        self.width = width
        self.height = height
        self.graph = nx.Graph

    def generate(self) -> nx.Graph:
        """create a partial lattice graph"""
        self.graph = nx.Graph()

        # create array of all possible grid coordinates
        all_points = [(x, y) for x in range(self.width) for y in range(self.height)]

        # select n nodes randomly
        all_points = random.sample(all_points, min(self.num_node, len(all_points)))

        # add selected points as nodes
        for point in all_points:
            self.graph.add_node(point)

        # 行方向にエッジを追加
        for x, y in all_points:
            neighbor = (x, y + 1)
            if neighbor in all_points:
                self.graph.add_edge((x, y), neighbor)

        # 列方向にエッジを追加
        for x, y in all_points:
            neighbor = (x + 1, y)
            if neighbor in all_points:
                self.graph.add_edge((x, y), neighbor)

        return self.graph

    def draw(self, G: nx.Graph):
        # LatticeGraph用の描画方法
        pos = {node: node for node in G.nodes()}
        nx.draw(G, pos, node_size=30, node_color="blue", with_labels=False)
        plt.axis("off")
        plt.show()


class RandomGraphNetwork(NetworkGenerator):
    """
    Generates a random graph network where edges are added with a given probability.
    The network follows the Erdős-Rényi random graph model (G(n,p) model).
    """

    def __init__(self, n_nodes: int, p_wiring: float = 1e-1):
        """
        Initialize the random graph network generator.

        Args:
            n_nodes (int): Number of nodes in the network
            p_wiring (float): Probability of adding an edge between any pair of nodes (default: 0.1)
        """
        self.n = n_nodes
        self.p = p_wiring
        self.graph = nx.Graph()

    def generate(self) -> nx.Graph:
        """
        Create a random network by adding edges with probability p_wiring.

        Returns:
            nx.Graph: Generated random network
        """
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.n))

        for node1 in range(self.n):
            for node2 in range(node1 + 1, self.n):
                if random.random() < self.p:
                    self.graph.add_edge(node1, node2)
        return self.graph

    def draw(self, G: nx.Graph):
        """
        Visualize the network using a circular layout.

        Args:
            G (nx.Graph): Network to visualize
        """
        pos = nx.circular_layout(G)
        nx.draw(G, pos, node_size=30, node_color="red")
        plt.axis("off")
        plt.show()
