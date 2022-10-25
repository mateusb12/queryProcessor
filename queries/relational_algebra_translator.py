import random
from functools import reduce

from queries.relational_algebra_splitter import get_split_example, get_split_instruction_example


class RelationalAlgebraTranslator:
    def __init__(self, sql_instruction: str):
        # self.original_instruction = get_split_instruction_example()
        self.original_instruction = sql_instruction
        self.split_sql = get_split_example()

    def translate_sql(self) -> str:
        projection = self.__extract_projection()
        selection = self.__extract_selection()
        cartesian_product = self.__extract_cartesian_product()
        return f"{projection}({selection}({cartesian_product}))"

    def __extract_projection(self):
        return ["π[" + ", ".join(self.split_sql["SELECT"]) + "]"][0]

    def __extract_selection(self):
        where_values = self.split_sql["WHERE"]

        def selection_notation(item): return f"σ[{item[0]}{item[1]}{item[2]}]"

        new_where_values = [selection_notation(item) for item in where_values]

        def selection_two_items(x, y): return f"{x} ^ {y}"

        return reduce(selection_two_items, new_where_values)

    def __extract_cartesian_product(self):
        from_values = self.split_sql["FROM"]

        def cartesian_join(x, y): return f"({x} ⨯ {y})"

        return reduce(cartesian_join, from_values)


def __main():
    rat = RelationalAlgebraTranslator(get_split_instruction_example())
    aux = rat.translate_sql()
    return


if __name__ == "__main__":
    __main()
