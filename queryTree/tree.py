from queries.relational_algebra_processor import RelationalAlgebraProcessor
from queries.relational_algebra_splitter import get_split_instruction_example
from queries.relational_algebra_wrapper import relational_algebra_wrapper
from queryTree.node import Node


class Tree:
    def __init__(self, relational_algebra_expressions: list[str]):
        self.expressions = relational_algebra_expressions[::-1]
        self.processor = RelationalAlgebraProcessor()
        self.root_node = None

    def build_tree(self):
        first_expression = self.expressions.pop(0)
        first_node = Node(first_expression, self.processor)
        first_node.analyze_node_instruction()
        self.root_node = Node(first_expression, self.processor)
        current_node = self.root_node
        for instruction in self.expressions:
            current_node.create_father(instruction)
            current_node = current_node.father
            current_node.analyze_node_instruction()


def __main():
    instruction_example = get_split_instruction_example()
    relational_algebra_instructions = relational_algebra_wrapper(instruction_example)
    t = Tree(relational_algebra_instructions)
    t.build_tree()
    return


if __name__ == "__main__":
    __main()
