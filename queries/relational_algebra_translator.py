import random
from functools import reduce

from queries.relational_algebra_splitter import get_split_example, get_sql_instruction_example_A


class RelationalAlgebraTranslator:
    def __init__(self, sql_instructions: dict):
        self.split_sql = sql_instructions

    def translate_sql(self) -> str:
        projection = self.__extract_projection()
        selection = self.__extract_selection()
        cartesian_product = self.__extract_cartesian_product()
        on_values = self.__extract_on()
        merged_selection = f"({selection} ^ {on_values})" if on_values else selection
        return f"{projection}({merged_selection}({cartesian_product}))"

    def __extract_projection(self):
        return ["π[" + ", ".join(self.split_sql["SELECT"]) + "]"][0]

    def __extract_selection(self):
        where_values = self.split_sql["WHERE"]

        def selection_notation(item): return f"σ[{item[0]}{item[1]}{item[2]}]"

        new_where_values = [selection_notation(item) for item in where_values]

        def selection_two_items(x, y): return f"{x} ^ {y}"

        return reduce(selection_two_items, new_where_values)

    def __get_join_values(self):  # sourcery skip: use-next
        joins = []
        for key in self.split_sql.keys():
            if key.startswith("JOIN"):
                joins.extend(self.split_sql[key])
        return joins

    def __extract_cartesian_product(self):
        from_values = self.split_sql["FROM"]
        join_values = self.__get_join_values()
        full_values = from_values + join_values

        def cartesian_join(x, y): return f"({x} ⨯ {y})"

        return reduce(cartesian_join, full_values)

    def __extract_on(self):
        if "ON_A" in self.split_sql:
            on_values = [value[0] for key, value in self.split_sql.items() if key.startswith("ON")]
        else:
            on_values = self.split_sql["ON"]
        on_pot = []
        for instruction in on_values:
            new_instruction = f"σ[{instruction[0]}{instruction[1]}{instruction[2]}]"
            on_pot.append(new_instruction)
        return on_pot[0] if len(on_pot) == 1 else " ^ ".join(on_pot)


def __main():
    split_example = get_split_example()
    rat = RelationalAlgebraTranslator(split_example)
    aux = rat.translate_sql()
    return


if __name__ == "__main__":
    __main()
