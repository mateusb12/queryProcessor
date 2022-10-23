import random
from functools import reduce

from queries.relational_algebra_splitter import get_split_example, get_split_instruction_example


class RelationalAlgebraTranslator:
    def __init__(self):
        self.original_instruction = get_split_instruction_example()
        self.split_info = get_split_example()

    def translate(self):
        projection = self.extract_projection()
        selection = self.extract_selection()
        cartesian_product = self.extract_cartesian_product()
        full_expression = f"{projection}({selection}({cartesian_product}))"
        return 0

    def extract_projection(self):
        return ["π[" + ", ".join(self.split_info["SELECT"]) + "]"][0]

    def extract_selection(self):
        where_values = self.split_info["WHERE"]

        def selection_notation(item): return f"σ[{item[0]}{item[1]}{item[2]}]"

        new_where_values = [selection_notation(item) for item in where_values]

        def selection_two_items(x, y): return f"{x} ^ {y}"

        return reduce(selection_two_items, new_where_values)

    def extract_cartesian_product(self):
        from_values = self.split_info["FROM"]

        def cartesian_join(x, y): return f"({x} ⨯ {y})"

        return reduce(cartesian_join, from_values)


def __main():
    rat = RelationalAlgebraTranslator()
    aux = rat.translate()
    return


if __name__ == "__main__":
    __main()
