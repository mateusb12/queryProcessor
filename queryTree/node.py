import re
from typing import Tuple, List, Union, Any, Optional

import pandas as pd

from queries.relational_algebra_processor import RelationalAlgebraProcessor


class Node:
    def __init__(self, input_relational_instruction: str = "", input_processor: RelationalAlgebraProcessor = None,
                 input_label: str = "A"):
        self.processor = input_processor
        self.content: pd.DataFrame = pd.DataFrame()
        self.left_children = None
        self.right_children = None
        self.father = None
        self.sibling = None
        self.relational_instruction = input_relational_instruction
        self.size = len(self.content)
        self.label = input_label
        self.edges = None
        self.current_table = None

    def analyze_node_instruction(self):
        # sourcery skip: use-getitem-for-re-match-groups, use-named-expression
        """Use regex to analyze the input instruction and return the operation and the tables involved
        If the instruction follows the format word1 ⨯ word2, then the operation is cartesian product
         and the tables are word1 and word2"""
        cartesian_match = re.search(r"(\w+) ⨯ (\w+)", self.relational_instruction)
        selection_match = re.search(r"σ\[(\w+)([<>=!]+)(.*)(?:\]\•)(\w+)(?:\•)", self.relational_instruction)
        projection_match = re.search(r"π\[((.*))\](?:\•(\w+))?", self.relational_instruction)
        # projection_match = re.search(r"π\[(\w+)", self.relational_instruction)
        join_match = re.search(r"(\w+) ⋈ •(.*)• (\w+)", self.relational_instruction)
        if cartesian_match:
            table_a, table_b = cartesian_match.groups()
            self.cartesian_operation(table_a, table_b)
        elif selection_match:
            column, operator, value, table = selection_match.groups()
            self.current_table = table
            self.selection_operation(column, operator, value, desired_table=table)
        elif projection_match:
            projection_groups = projection_match.groups()
            column_list = projection_groups[0].split(",")
            if len(projection_groups) == 3:
                self.current_table = projection_groups[2]
            self.projection_operation(column_list)
        elif join_match:
            table_a, restriction, table_b = join_match.groups()
            restriction_match = re.search(r"(\w+)\.(.*)([<>=!]+)(\w+)\.(.*)", restriction)
            left_table, left_column, operator, right_table, right_column = restriction_match.groups()
            self.join_operation(table_a, table_b, left_column, right_column)
        self.edges = self.get_edge_list()

    def projection_operation(self, column_list: list[str]):
        new_content = self.processor.projection(self.content, column_list)
        self.content = new_content
        self.size = len(self.content)

    def selection_operation(self, column: str, operator: str, value: str, desired_table: str = ""):
        if "'" in column:
            column = column.replace("'", "")
        if "'" in value:
            value = value.replace("'", "")
        if self.left_children is None and self.right_children is None:
            chosen_content = self.processor.load_table(desired_table.lower())
            self.create_left_children(chosen_content)
        else:
            chosen_content = self.content
        new_content = self.processor.selection(chosen_content, column, operator, value)
        self.content = new_content
        self.size = len(self.content)

    def get_self_content(self):
        if self.left_children is not None:
            return self.left_children.content
        if self.right_children is not None:
            return self.right_children.content

    def merge_preparation(self, table_a, table_b):
        if self.left_children is None and table_a != "SELF":
            new_table_a = self.processor.load_table(table_a)
            self.create_left_children(content=new_table_a)
        if self.right_children is None and table_b != "SELF":
            new_table_b = self.processor.load_table(table_b)
            self.create_right_children(content=new_table_b)
        left_content = self.left_children.content if table_a != "SELF" else self.get_self_content()
        right_content = self.right_children.content if table_b != "SELF" else self.get_self_content()
        return left_content, right_content

    def cartesian_operation(self, table_a: str, table_b: str):
        left_content, right_content = self.merge_preparation(table_a, table_b)
        new_content = self.processor.cartesian_product(left_content, right_content)
        self.content = new_content
        self.size = len(self.content)
        self.relational_instruction = "SELF"

    def join_operation(self, table_a: str, table_b: str, column_a: str, column_b: str):
        left_content, right_content = self.merge_preparation(table_a, table_b)
        new_content = self.processor.join(left_content, right_content, column_a, column_b)
        self.content = new_content
        self.size = len(self.content)

    def create_new_children(self, content: pd.DataFrame, label: str = "A"):
        new_node = Node(input_processor=self.processor, input_label=label)
        new_node.father = self
        new_node.content = content
        new_node.size = len(content)
        return new_node

    def create_left_children(self, content: pd.DataFrame):
        new_label = chr(ord(self.label) - 2)
        self.left_children = self.create_new_children(content, new_label)
        self.left_children.sibling = self.right_children

    def create_right_children(self, content: pd.DataFrame):
        new_label = chr(ord(self.label) - 1)
        self.right_children = self.create_new_children(content, new_label)
        self.right_children.sibling = self.left_children

    def create_father(self, relational_instruction: str, label: str = "A"):
        self.father = Node(input_relational_instruction=relational_instruction, input_processor=self.processor,
                           input_label=label)
        self.father.content = self.content
        self.father.left_children = self
        self.father.right_children = self.sibling

    def get_edge_list(self):
        if self.right_children is None:
            alternative_label = chr(ord(self.label) - 1)
            self.left_children.label = alternative_label
        left_children_label = self.left_children.label if self.left_children else None
        right_children_label = self.right_children.label if self.right_children else None
        left_edge = [self.label, left_children_label] if left_children_label else None
        right_edge = [self.label, right_children_label] if right_children_label else None
        if left_edge == right_edge:
            return [left_edge]
        if left_edge and right_edge:
            return [left_edge, right_edge]
        elif left_edge:
            return [left_edge]
        elif right_edge:
            return [right_edge]


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
