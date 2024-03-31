import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, nx_graph=None, multi_graph=False, di_graph=False):
        if nx_graph:
            self.g = nx_graph
        elif multi_graph:
            self.g = nx.MultiGraph()
        elif di_graph:
            self.g = nx.DiGraph()
        else:
            self.g = nx.Graph()

    def add_node_list(self, node_list):
        self.g.add_weighted_edges_from(node_list)

    def node_count(self):
        return self.g.number_of_nodes()

    def edge_count(self):
        return self.g.number_of_edges()

    def get_edges(self):
        return self.g.edges

    def get_edge_weight(self, node1, node2):
        return self.g.get_edge_data(node1, node2)["weight"]

    def get_nodes(self):
        return self.g.nodes

    def get_degree(self):
        return self.g.degree

    def add_edge(self, node1, node2, weight=None):
        if weight:
            self.g.add_edge(node1, node2, weight=weight)
        else:
            self.g.add_edge(node1, node2)

    def has_edge(self, node1, node2):
        return self.g.has_edge(node1, node2)

    def remove_node(self, node):
        return self.g.remove_node(node)

    def get_graph(self):
        return self.g

    def plot_graph(self, output_path):
        pos = nx.spring_layout(self.g)
        nx.draw(self.g, pos, with_labels=True)
        # labels
        if isinstance(self.g, nx.MultiGraph):
            labels = {}
        else:
            labels = {e: str(self.get_edge_weight(e[0], e[1])) for e in self.g.edges}
        nx.draw_networkx_edge_labels(self.g, pos, edge_labels=labels, font_size=5)

        if isinstance(self.g, nx.DiGraph):
            nx.draw_networkx_edges(self.g, pos, edgelist=self.g.edges, arrows=True)
        plt.savefig(output_path)
        plt.close()

    def get_euler_tour(self, source_node):
        return nx.algorithms.eulerian_circuit(self.g, source=source_node)
