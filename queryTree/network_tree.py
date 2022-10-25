from queryTree.tree import Tree, build_example_tree


class NetworkNxTree:
    def __init__(self, input_tree: Tree):
        self.tree = input_tree


def __main():
    example_tree = build_example_tree()
    nxt = NetworkNxTree(example_tree)


if __name__ == "__main__":
    __main()
