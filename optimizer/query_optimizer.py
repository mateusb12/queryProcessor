import re

from queries.relational_algebra_processor import RelationalAlgebraProcessor
from queries.relational_algebra_splitter import get_sql_instruction_example_C, get_sql_instruction_example_D
from queries.relational_algebra_wrapper import relational_algebra_wrapper


class QueryOptimizer:
    def __init__(self, instruction_list: list[str], column_dict: dict):
        self.instructions = instruction_list
        self.column_dict = column_dict
        self.instruction_dict = {}
        self.used_tables = set()
        self.used_columns = set()

    def optimizer_pipeline(self):
        self.__analyze_instructions()
        self.avoid_all_cross_products()
        self.heuristic_reduce_tuples()
        self.heuristic_attribute_reduce()
        return self.instructions

    def __analyze_instructions(self):
        for item in self.instructions:
            if "⨯" in item:
                if "cross_product" not in self.instruction_dict:
                    self.instruction_dict["cross_product"] = [item]
                else:
                    self.instruction_dict["cross_product"].append(item)
            if "σ" in item:
                if "selection" not in self.instruction_dict:
                    self.instruction_dict["selection"] = [item]
                else:
                    self.instruction_dict["selection"].append(item)
            if "π" in item:
                trimmed = item[2:-1]
                captured_columns = [item.replace(" ", "") for item in trimmed.split(",")]
                self.used_columns.update(captured_columns)
                if "projection" not in self.instruction_dict:
                    self.instruction_dict["projection"] = [item]
                else:
                    self.instruction_dict["projection"].append(item)
            if join_match := re.match("\σ\[(\w+)\.(\w+)\=(\w+)\.(\w+)\]", item):
                left_table, left_column, right_table, right_column = join_match.groups()
                self.used_tables.add(left_table)
                self.used_tables.add(right_table)
                self.used_columns.add(left_column)
                self.used_columns.add(right_column)
                if "join" not in self.instruction_dict:
                    self.instruction_dict["join"] = [item]
                else:
                    self.instruction_dict["join"].append(item)
        self.instruction_dict["cross_product"] = list(reversed(self.instruction_dict["cross_product"]))
        self.instruction_dict["selection"] = list(reversed(self.instruction_dict["selection"]))
        self.instruction_dict["projection"] = list(reversed(self.instruction_dict["projection"]))
        return

    def avoid_all_cross_products(self):
        for instruction in self.instruction_dict["cross_product"]:
            self.heuristic_avoid_cross_product(instruction)

    def heuristic_avoid_cross_product(self, cross_product_instruction: str):
        """ This heuristic is used to avoid cross product operations, in order to reduce the number of tuples.
        It merges 1 selection operation with 1 cross product operation in order to create 1 join operation."""
        table_a, table_b = [item.replace(" ", "") for item in cross_product_instruction.split("⨯")]
        for instruction in self.instruction_dict["join"]:
            regex_match = re.match("\σ\[(\w+)\.(\w+)\=(\w+)\.(\w+)\]", instruction)
            left_table, left_column, right_table, right_column = regex_match.groups()
            table_pot = [table_a, table_b, left_table, right_table]
            if table_a == "SELF" or table_b == "SELF":
                condition = left_table in table_pot or right_table in table_pot
            else:
                condition = left_table == table_a and right_table == table_b
            if condition:
                new_instruction = f"({left_table} ⋈ •{left_column}={right_column}• {right_table})"
                self.instructions.remove(instruction)
                self.instruction_dict["join"].remove(instruction)
                index = self.instructions.index(cross_product_instruction)
                self.instructions[index] = new_instruction
        return

    def __find_table_by_selection_instruction(self, selection: str):
        regex_match = re.match(r"σ\[(\w+)([<>=!]+)(.*)\]", selection)
        if regex_match is not None:
            column, operator, value = regex_match.groups()
            return self.__find_table_by_column_name(column)

    def __find_table_by_column_name(self, column_name: str) -> str:
        for key, value in self.column_dict.items():
            if column_name in value:
                return key.upper()

    def heuristic_reduce_tuples(self):
        """ This heuristic is used to reduce the number of tuples by altering selection positions.
        It basically moves selection operations closer to the bottom of the query plan."""
        selection_pot = [item for item in self.instructions if "σ" in item]
        for instruction in selection_pot:
            index = self.instructions.index(instruction)
            popped = self.instructions.pop(index)
            self.instructions.append(popped)

        selection_values = [self.__find_table_by_selection_instruction(item) for item in selection_pot]
        selection_dict = dict(zip(selection_pot, selection_values))
        ordered_selection_dict = dict(sorted(selection_dict.items(), key=lambda item: item[1]))
        non_selection_instructions = [item for item in self.instructions if "σ" not in item]
        non_selection_instructions.extend(ordered_selection_dict.keys())
        for index, item in enumerate(non_selection_instructions):
            if "σ" in item:
                table = selection_dict[item]
                non_selection_instructions[index] = f"{item}•{table}•"
        self.instructions = non_selection_instructions

    def __get_desirable_columns(self, table_name: str) -> list[str]:
        table_columns = self.column_dict[table_name]
        return [column for column in table_columns if column in self.used_columns]

    def heuristic_attribute_reduce(self):
        """ This heuristic is used to reduce the number of attributes by altering projection positions.
        It basically moves projection operations closer to the bottom of the query plan."""
        desirable_dict = {key: self.__get_desirable_columns(key.lower()) for key in self.used_tables}
        for key, value in desirable_dict.items():
            if len(value) == 0:
                continue
            new_instruction = f"π[{','.join(value)}]•{key}•"
            found = False
            for index, item in enumerate(self.instructions):
                if "σ" in item:
                    table_name = item.split("•")[1]
                    if table_name == key:
                        self.instructions.insert(index, new_instruction)
                        found = True
                        break
            if not found:
                for index_, item_ in enumerate(self.instructions):
                    if regex_join_match := re.match(r"\((\w+) ⋈ •(\w+)=(\w+)• (\w+)\)", item_):
                        left_table, left_column, right_column, right_table = regex_join_match.groups()
                        if key in [left_table, right_table]:
                            self.instructions.insert(index_+1, new_instruction)
                            found = True
                            break
        return

    def export_query_plan_in_tree_format(self) -> dict:
        """This function exports the query plan in a tree format, composed by main path, left path and right path."""
        main_path = []
        left_path = []
        right_path = []
        for index, item in enumerate(self.instructions):
            if "full" not in main_path:
                main_path.append(item)
                if "⋈" in item:
                    main_path.append("full")
                continue
            if "full" not in left_path:
                left_path.append(item)
                if "•" in item:
                    left_path.append("full")
                continue
            if "full" not in right_path:
                right_path.append(item)
                if "•" in item:
                    right_path.append("full")
                continue
        return {"left_path": left_path[:-1], "right_path": right_path[:-1], "main_path": main_path[:-1]}


def get_optimized_example() -> list[str]:
    qt = RelationalAlgebraProcessor()
    column_dict = qt.export_all_columns()
    instruction_example = get_sql_instruction_example_C()
    instruction_set = relational_algebra_wrapper(instruction_example)
    qo = QueryOptimizer(instruction_set, column_dict)
    return qo.optimizer_pipeline()


def __main():
    aux = get_optimized_example()
    return


if __name__ == "__main__":
    __main()
