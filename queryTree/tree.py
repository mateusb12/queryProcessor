import re

from optimizer.query_optimizer import get_optimized_example
from queries.relational_algebra_processor import RelationalAlgebraProcessor
from queries.relational_algebra_splitter import get_sql_instruction_example_A, get_sql_instruction_example_C, \
    get_sql_instruction_example_D
from queries.relational_algebra_wrapper import relational_algebra_wrapper
from queryTree.node import Node


class Tree:
    def __init__(self, relational_algebra_expressions: list[str]):
        # self.expressions = relational_algebra_expressions[::-1]
        self.expressions = relational_algebra_expressions
        self.processor = RelationalAlgebraProcessor()
        self.root_node = Node()
        self.current_node = Node()
        self.current_label = "A"
        self.edge_pot = []
        self.join_by_column_dict, join_by_index_dict = self.join_side_analysis(self.expressions)
        self.current_index = 0
        self.consumed_instructions = []
        self.current_instruction = self.expressions[0]

    def build_tree(self):
        root_node = Node(self.current_instruction, self.processor, self.current_label)
        self.increment_instruction(self.current_instruction)
        self.root_node = root_node
        self.current_node = root_node
        self.analyze_instruction(self.current_instruction, self.root_node)
        self.unnest_edge_list()

    def analyze_instruction(self, current_instruction: str, node: Node, desired_table: str = ""):
        # sourcery skip: use-named-expression
        cartesian_match = re.search(r"(\w+) ⨯ (\w+)", current_instruction)
        selection_match = re.search(r"σ\[(\w+)([<>=!]+)(.*)(?:\]\•)(\w+)(?:\•)", current_instruction)
        projection_match = re.search(r"π\[(.*)\](?:\•(\w+)\•)?", current_instruction)
        join_match = re.search(r"\((\w+) ⋈ •(\w+)=(\w+)• (\w+)\)", current_instruction)

        if projection_match:
            column_list, projection_table = projection_match.groups()
            if projection_table is None:
                self.increment_instruction(current_instruction)
                return
            if relatives_test := self.check_for_relatives(projection_table):
                self.create_leaf(current_instruction, node)
                return self.current_instruction
            projection_new_instruction, projection_node = self.create_children_from_instruction(node,
                                                                                                current_instruction)
            projection_output = self.analyze_instruction(projection_new_instruction, projection_node)
            return self.current_instruction
        elif join_match:
            left_table, left_column, right_table, right_column = join_match.groups()
            left_size = len(self.join_by_column_dict[left_table])
            left_instruction, join_node = self.create_children_from_instruction(node, current_instruction)
            if left_size == 1:
                left_output = self.analyze_instruction(left_instruction, join_node)
                self.current_index += 1
                self.current_instruction = self.expressions[self.current_index]
                right_instruction = self.expressions[self.current_index]
            right_size = len(self.join_by_column_dict[right_column])
            if right_size in {1, 2}:
                right_output = self.analyze_instruction(self.current_instruction, join_node)
            print("done!")
        elif selection_match:
            selection_column, selection_operator, selection_value, selection_table = selection_match.groups()
            relatives_test = self.check_for_relatives(selection_table)
            if relatives_test:
                self.create_leaf(current_instruction, node)
                return self.current_instruction
            selection_new_instruction, selection_node = self.create_children_from_instruction(node, current_instruction)
            selection_output = self.analyze_instruction(selection_new_instruction, selection_node)
            return self.current_instruction

    def create_children_from_instruction(self, input_node: Node, next_instruction: str):
        upcoming_instruction = self.expressions[self.current_index + 1]
        new_node = input_node.create_children(input_instruction=next_instruction, input_label=self.current_label)
        self.current_node = new_node
        if next_instruction not in self.consumed_instructions:
            self.consumed_instructions.append(next_instruction)
        self.increment_instruction(upcoming_instruction)
        return upcoming_instruction, new_node

    def check_for_relatives(self, table_tag: str) -> bool:
        possible_corresponding = [item for item in self.expressions if item not in self.consumed_instructions]
        possible_relatives_dict = self.__get_possible_relatives(possible_corresponding)
        try:
            possible_relatives = possible_relatives_dict[table_tag]
        except KeyError:
            return True
        return all((relative in self.consumed_instructions for relative in possible_relatives))

    def create_leaf(self, input_instruction: str, input_node: Node):
        return input_node.create_children(input_instruction, self.current_label)

    def increment_current_label(self):
        current_label = self.current_label
        new_label = chr(len(self.consumed_instructions) + 65)
        self.current_label = new_label
        return self.current_label

    def increment_instruction(self, input_instruction: str):
        self.current_index += 1
        next_instruction = self.expressions[self.current_index]
        self.current_instruction = next_instruction
        if input_instruction in self.consumed_instructions:
            raise ValueError("Instruction already consumed")
        self.consumed_instructions.append(input_instruction)
        self.increment_current_label()

    def unnest_edge_list(self):
        unnested_list = []
        for edge_list in self.edge_pot:
            unnested_list.extend(iter(edge_list))
        self.edge_pot = unnested_list

    @staticmethod
    def __get_possible_relatives(possible_corresponding: list[str]) -> dict:
        possible_relatives = {}
        for j in possible_corresponding:
            if point_regex := re.search(r"(?:.*)\•(\w+)\•", j):
                if point_regex[1] not in possible_relatives:
                    possible_relatives[point_regex[1]] = []
                possible_relatives[point_regex[1]].append(j)
        return possible_relatives

    @staticmethod
    def join_side_analysis(instruction_list: list[str]) -> tuple[dict, dict]:
        reversed_list = instruction_list[::-1]
        join_instructions = [item for item in reversed_list if "⋈" in item]
        join_by_column_dict = {}
        join_by_index_dict = {}
        for index, instruction in enumerate(join_instructions):
            join_regex = re.match(r"\((\w+) ⋈ •(\w+)=(\w+)• (\w+)\)", instruction)
            left_table_, left_column, right_column, right_table_ = join_regex.groups()
            join_by_index_dict[instruction] = index + 1
            if left_table_ not in join_by_column_dict:
                join_by_column_dict[left_table_] = []
            if right_table_ not in join_by_column_dict:
                join_by_column_dict[right_table_] = []
            join_by_column_dict[left_table_].append(instruction)
            join_by_column_dict[right_table_].append(instruction)
        for key, value in join_by_column_dict.items():
            join_by_column_dict[key] = list(reversed(value))
        return join_by_column_dict, join_by_index_dict


def build_example_tree() -> Tree:
    relational_algebra_instructions = get_optimized_example()
    t = Tree(relational_algebra_instructions)
    t.build_tree()
    return t


def __main():
    aux = build_example_tree()
    return


if __name__ == "__main__":
    __main()
