from matplotlib.offsetbox import AnchoredText

from queries.relational_algebra_splitter import get_sql_instruction_example_D, get_sql_instruction_example_C
from queryTree.tree import Tree, build_example_tree
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


class NetworkNxTree:
    def __init__(self, input_tree: Tree):
        self.tree = input_tree
        self.edges = self.tree.collect_all_edges()
        self.instruction_dict = self.tree.instruction_dict
        self.graph = nx.Graph()
        self.graph.add_edges_from(self.edges)

    def draw_graph(self):
        pos = graphviz_layout(self.graph, prog="dot")
        nx.draw(self.graph, pos, with_labels=True, node_color="skyblue", node_size=1500, alpha=0.5, arrows=True,
                edgecolors="black")
        ax = plt.gca()
        legend_text = "".join(f"{key} → {value[:30]}\n" for key, value in self.instruction_dict.items())
        at = self.text_only(plt.gca(), legend_text, loc=1)
        plt.show()
        return

    @staticmethod
    def text_only(ax, txt, fontsize=8, loc=2, *args, **kwargs):
        at = AnchoredText(txt,
                          prop=dict(size=fontsize),
                          frameon=True,
                          loc=loc)
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        ax.add_artist(at)
        return at


def __main():
    example_sql = get_sql_instruction_example_C()
    example_tree = build_example_tree(example_sql)
    nxt = NetworkNxTree(example_tree)
    nxt.draw_graph()
    pass


if __name__ == "__main__":
    __main()
