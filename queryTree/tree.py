from optimizer.query_optimizer import get_optimized_example
from queries.relational_algebra_processor import RelationalAlgebraProcessor
from queries.relational_algebra_splitter import get_sql_instruction_example_A, get_sql_instruction_example_C, \
    get_sql_instruction_example_D
from queries.relational_algebra_wrapper import relational_algebra_wrapper
from queryTree.node import Node


class Tree:
    def __init__(self, relational_algebra_expressions: list[str]):
        self.expressions = relational_algebra_expressions[::-1]
        self.processor = RelationalAlgebraProcessor()
        self.root_node = None
        self.current_label = "C"
        self.edge_pot = []

    def build_tree(self):
        first_expression = self.expressions[0]
        first_node = Node(first_expression, self.processor, self.current_label)
        first_node.analyze_node_instruction()
        self.edge_pot.append(first_node.edges)
        current_node = first_node
        self.root_node = first_node
        for instruction in self.expressions[1:]:
            new_label = self.increment_current_label()
            print(f"Label: {new_label}")
            current_node.create_father(relational_instruction=instruction, label=new_label)
            old_content = current_node.content
            current_node = current_node.father
            current_node.analyze_node_instruction()
            self.edge_pot.append(current_node.edges)
            new_content = current_node.content
        self.unnest_edge_list()

    def increment_current_label(self):
        self.current_label = chr(ord(self.current_label) + 1)
        return self.current_label

    def unnest_edge_list(self):
        unnested_list = []
        for edge_list in self.edge_pot:
            unnested_list.extend(iter(edge_list))
        self.edge_pot = unnested_list


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
