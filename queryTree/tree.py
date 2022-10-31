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
        self.root_node = None
        self.current_label = "A"
        self.edge_pot = []
        self.join_by_column_dict, join_by_index_dict = self.join_side_analysis(self.expressions)
        self.root_none = Node()
        self.current_index = 0
        self.consumed_instructions = []
        self.current_instruction = self.expressions[0]

    def build_tree(self):
        root_node = Node(self.current_instruction, self.processor, self.current_label)
        self.root_node = root_node
        count = 1
        while count != 5:
            self.analyze_instruction(self.current_instruction, self.root_node)
            count += 1

        # for index, instruction in enumerate(self.expressions):
        #     self.current_index = index
        #     if index == 0:
        #         continue
        #     self.analyze_instruction(instruction, current_node)
        #     self.consumed_instructions.append(instruction)
        # current_node.create_father(relational_instruction=instruction, label=new_label)
        # old_table = current_node.current_table
        # old_content = current_node.content
        # current_node = current_node.father
        # current_node.analyze_node_instruction()
        # self.edge_pot.append(current_node.edges)
        # new_content = current_node.content
        # new_table = current_node.current_table
        self.unnest_edge_list()

    def analyze_instruction(self, next_instruction: str, node: Node, desired_table: str = ""):
        cartesian_match = re.search(r"(\w+) ⨯ (\w+)", next_instruction)
        selection_match = re.search(r"σ\[(\w+)([<>=!]+)(.*)(?:\]\•)(\w+)(?:\•)", next_instruction)
        projection_match = re.search(r"π\[(.*)\](?:\•(\w+)\•)?", next_instruction)
        join_match = re.search(r"\((\w+) ⋈ •(\w+)=(\w+)• (\w+)\)", next_instruction)

        if projection_match:
            column_list, projection_table = projection_match.groups()
            if projection_table is None:
                self.increment_instruction(next_instruction)
                return
            possible_corresponding = self.expressions[self.current_index:]
            possible_relatives_dict = self.__get_possible_relatives(possible_corresponding)
            possible_relatives = possible_relatives_dict[projection_table]
            if all(relative in self.consumed_instructions for relative in possible_relatives):
                return 0
        elif join_match:
            left_table, left_column, right_take, right_column = join_match.groups()
            left_size = len(self.join_by_column_dict[left_table])
            following_instruction = self.expressions[self.current_index + 1]
            if left_size == 1:
                new_children = node.create_children(input_instruction=following_instruction)
                self.increment_instruction(following_instruction)
                left_output = self.analyze_instruction(following_instruction, new_children)
            right_size = len(self.join_by_column_dict[right_column])
            if right_size == 2:
                self.increment_instruction(self.current_instruction)
                current_instruction = self.expressions[self.current_index]
                new_children = node.create_children(input_instruction=current_instruction)
                self.consumed_instructions.append(following_instruction)
                right_output = self.analyze_instruction(current_instruction, new_children)
            pass

    def increment_current_label(self):
        self.current_label = chr(ord(self.current_label) + 1)
        return self.current_label

    def increment_instruction(self, input_instruction: str):
        self.current_index += 1
        self.current_instruction = self.expressions[self.current_index]
        self.consumed_instructions.append(input_instruction)

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
    # instruction_example = get_sql_instruction_example_D()
    # relational_algebra_instructions = relational_algebra_wrapper(instruction_example)
    relational_algebra_instructions = get_optimized_example()
    t = Tree(relational_algebra_instructions)
    t.build_tree()
    return t


def __main():
    aux = build_example_tree()
    return


if __name__ == "__main__":
    __main()
