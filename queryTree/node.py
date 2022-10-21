import pandas as pd

from queries.relational_algebra_processor import RelationalAlgebraProcessor


class Node:
    def __init__(self):
        self.processor = RelationalAlgebraProcessor()
        self.content: pd.DataFrame = pd.DataFrame()
        self.left_children = None
        self.right_children = None
        self.father = None
        self.size = len(self.content)

    def cartesian_operation(self, table_a: str, table_b: str):
        if self.left_children is None:
            new_content = self.processor.load_table(table_a)
            self.create_left_children(new_content)
        if self.right_children is None:
            new_content = self.processor.load_table(table_b)
            self.create_right_children(new_content)
        self.content = self.processor.cartesian_product(self.left_children.content, self.right_children.content)
        self.size = len(self.content)

    def create_left_children(self, content: pd.DataFrame):
        self.left_children = Node()
        self.left_children.father = self
        self.left_children.content = content
        self.left_children.size = len(content)

    def create_right_children(self, content: pd.DataFrame):
        self.right_children = Node()
        self.right_children.father = self
        self.right_children.content = content
        self.right_children.size = len(content)


def __main():
    n = Node()
    n.cartesian_operation("employee", "works_on")
    return


if __name__ == "__main__":
    __main()
