import re

import pandas as pd

from queries.relational_algebra_processor import RelationalAlgebraProcessor


class Node:
    def __init__(self):
        self.processor = RelationalAlgebraProcessor()
        self.content: pd.DataFrame = pd.DataFrame()
        self.left_children = None
        self.right_children = None
        self.father = None
        self.sibling = None
        self.relational_instruction = 'EMPLOYEE ⨯ WORKS_ON'
        self.size = len(self.content)

    def analyze_node_instruction(self):
        # sourcery skip: use-getitem-for-re-match-groups, use-named-expression
        """Use regex to analyze the input instruction and return the operation and the tables involved
        If the instruction follows the format word1 ⨯ word2, then the operation is cartesian product
         and the tables are word1 and word2"""
        cartesian_regex = r"(\w+) ⨯ (\w+)"
        cartesian_match = re.search(cartesian_regex, self.relational_instruction)
        if cartesian_match:
            table_a, table_b = cartesian_match.groups()
            self.cartesian_operation(table_a, table_b)

    def cartesian_operation(self, table_a: str, table_b: str):
        if self.left_children is None:
            new_table_a = self.processor.load_table(table_a)
            self.create_left_children(new_table_a)
        if self.right_children is None:
            new_table_b = self.processor.load_table(table_b)
            self.create_right_children(new_table_b)
        new_content = self.processor.cartesian_product(self.left_children.content, self.right_children.content)
        self.content = new_content
        self.size = len(self.content)

    def create_left_children(self, content: pd.DataFrame):
        self.left_children = Node()
        self.left_children.father = self
        self.left_children.content = content
        self.left_children.size = len(content)
        self.left_children.sibling = self.right_children

    def create_right_children(self, content: pd.DataFrame):
        self.right_children = Node()
        self.right_children.father = self
        self.right_children.content = content
        self.right_children.size = len(content)
        self.right_children.sibling = self.left_children


def __main():
    n = Node()
    n.analyze_node_instruction()
    return


if __name__ == "__main__":
    __main()
