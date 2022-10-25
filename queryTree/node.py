import re

import pandas as pd

from queries.relational_algebra_processor import RelationalAlgebraProcessor


class Node:
    def __init__(self, input_relational_instruction: str = "", input_processor: RelationalAlgebraProcessor = None):
        self.processor = input_processor
        self.content: pd.DataFrame = pd.DataFrame()
        self.left_children = None
        self.right_children = None
        self.father = None
        self.sibling = None
        self.relational_instruction = input_relational_instruction
        self.size = len(self.content)

    def analyze_node_instruction(self):
        # sourcery skip: use-getitem-for-re-match-groups, use-named-expression
        """Use regex to analyze the input instruction and return the operation and the tables involved
        If the instruction follows the format word1 ⨯ word2, then the operation is cartesian product
         and the tables are word1 and word2"""
        cartesian_match = re.search(r"(\w+) ⨯ (\w+)", self.relational_instruction)
        selection_match = re.search(r"σ\[(\w+)([<>=!]+)([\'\w]+)", self.relational_instruction)
        projection_match = re.search(r"π\[(\w+)", self.relational_instruction)
        if cartesian_match:
            table_a, table_b = cartesian_match.groups()
            self.cartesian_operation(table_a, table_b)
        if selection_match:
            column, operator, value = selection_match.groups()
            self.selection_operation(column, operator, value)
        if projection_match:
            column = projection_match.groups()[0]
            self.projection_operation(column)

    def projection_operation(self, column: str):
        new_content = self.processor.projection(self.content, [column])
        self.content = new_content
        self.size = len(self.content)

    def selection_operation(self, column: str, operator: str, value: str):
        if '' in column:
            column = column.replace("'", "")
        if '' in value:
            value = value.replace("'", "")
        new_content = self.processor.selection(self.content, column, operator, value)
        self.content = new_content
        self.size = len(self.content)

    def cartesian_operation(self, table_a: str, table_b: str):
        if self.left_children is None and table_a != "SELF":
            new_table_a = self.processor.load_table(table_a)
            self.create_left_children(new_table_a)
        if self.right_children is None and table_b != "SELF":
            new_table_b = self.processor.load_table(table_b)
            self.create_right_children(new_table_b)
        new_content = self.processor.cartesian_product(self.left_children.content, self.right_children.content)
        self.content = new_content
        self.size = len(self.content)
        self.relational_instruction = "SELF"

    def create_left_children(self, content: pd.DataFrame):
        self.left_children = Node(input_processor=self.processor)
        self.left_children.father = self
        self.left_children.content = content
        self.left_children.size = len(content)
        self.left_children.sibling = self.right_children

    def create_right_children(self, content: pd.DataFrame):
        self.right_children = Node(input_processor=self.processor)
        self.right_children.father = self
        self.right_children.content = content
        self.right_children.size = len(content)
        self.right_children.sibling = self.left_children

    def create_father(self, relational_instruction: str):
        self.father = Node(input_relational_instruction=relational_instruction, input_processor=self.processor)
        self.father.content = self.content
        self.father.left_children = self
        self.father.right_children = self.sibling


def __main():
    n1 = Node('EMPLOYEE ⨯ WORKS_ON')
    n1.analyze_node_instruction()
    n1.create_father('SELF ⨯ PROJECT')

    n2 = n1.father
    n2.analyze_node_instruction()
    n2.create_father("σ[PNAME='TWWPPHHHS1']")

    n3 = n2.father
    n3.analyze_node_instruction()
    n3.create_father("σ[PNUMBER=PNO]")

    n4 = n3.father
    n4.analyze_node_instruction()
    n4.create_father("σ[ESSN=SSN]")

    n5 = n4.father
    n5.analyze_node_instruction()
    n5.create_father("σ[BIRTHDATE>'1957-12-31']")

    n6 = n5.father
    n6.analyze_node_instruction()
    n6.create_father("π[LNAME]")

    n7 = n6.father
    n7.analyze_node_instruction()
    return


if __name__ == "__main__":
    __main()
