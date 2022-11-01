from queryTree.tree import Tree, build_example_tree
import matplotlib.pyplot as plt
import networkx as nx


class NetworkNxTree:
    def __init__(self, input_tree: Tree):
        self.tree = input_tree
        self.edges = self.tree.collect_all_edges()
        self.graph = nx.Graph()
        self.graph.add_edges_from(self.edges)

    def draw_graph(self):
        nx.draw(self.graph, with_labels=True)
        ax = plt.gca()
        plt.show()
        return


def __main():
    example_tree = build_example_tree()
    nxt = NetworkNxTree(example_tree)
    nxt.draw_graph()
    pass


if __name__ == "__main__":
    __main()
