import re

from queries.relational_algebra_processor import RelationalAlgebraProcessor
from queries.relational_algebra_splitter import get_sql_instruction_example_C, get_sql_instruction_example_D
from queries.relational_algebra_wrapper import relational_algebra_wrapper


class QueryOptimizer:
    def __init__(self, instruction_list: list[str], column_dict: dict):
        self.instructions = instruction_list
        self.column_dict = column_dict
        self.instruction_dict = {}
        self.used_join_columns = []
        self.left_table = ""
        self.right_table = ""
        self.left_table_columns = []
        self.right_table_columns = []

    def optimizer_pipeline(self):
        self.__analyze_instructions()
        if "cross_product" in self.instruction_dict.keys():
            self.heuristic_avoid_cross_product()
        self.heuristic_reduce_tuples()
        self.heuristic_attribute_reduce()
        return self.instructions

    def __analyze_instructions(self):
        for item in self.instructions:
            if "⨯" in item:
                self.instruction_dict["cross_product"] = item

    def heuristic_avoid_cross_product(self):
        main_value = self.instruction_dict["cross_product"]
        table_a, table_b = [item.replace(" ", "") for item in main_value.split("⨯")]
        removed_instruction, new_instruction = "", ""
        for instruction in self.instructions:
            if instruction.startswith("σ") and table_a in instruction and table_b in instruction:
                operators = ["=", "<", ">", "<=", ">=", "<>"]
                existing_operator = [operator for operator in operators if operator in instruction][0]
                raw_condition = instruction.split(existing_operator)
                left_condition, right_condition = [item.replace("σ[", "").replace("]", "") for item in raw_condition]
                self.used_join_columns.append(left_condition.split(".")[-1])
                self.used_join_columns.append(right_condition.split(".")[-1])
                self.left_table = left_condition.split(".")[0]
                self.right_table = right_condition.split(".")[0]
                removed_instruction = instruction
                new_instruction = f"({table_a} ⋈ •{left_condition}{existing_operator}{right_condition}• {table_b})"
                break
        if removed_instruction in self.instructions:
            self.instructions.remove(removed_instruction)
        for index, instruction in enumerate(self.instructions):
            if instruction == main_value:
                self.instructions[index] = new_instruction
                break
        self.left_table_columns = self.column_dict[self.left_table.lower()]
        self.right_table_columns = self.column_dict[self.right_table.lower()]
        return

    def __get_join_instructions(self):
        if join_instructions := [item for item in self.instructions if "⋈" in item]:
            return join_instructions
        return None

    @staticmethod
    def __get_suitable_columns_for_selection_trim(selection_pot: list[str], column_pot: list[str]) -> list[str]:
        suitable_selections = []
        for selection in selection_pot:
            selection_match = re.match(r"σ\[(\w+)([<>=!]+)(.*)\]", selection)
            column, operator, value = selection_match.groups()
            if column in column_pot:
                suitable_selections.append(selection)
        return suitable_selections

    def __rename_selection_instructions(self, left_table, right_table, selection_pot):
        left_columns, right_columns = self.column_dict[left_table.lower()], self.column_dict[right_table.lower()]
        left_suitable = self.__get_suitable_columns_for_selection_trim(selection_pot, left_columns)
        right_suitable = self.__get_suitable_columns_for_selection_trim(selection_pot, right_columns)
        old_instructions = left_suitable + right_suitable
        for j in old_instructions:
            new_instruction = ""
            if j in left_suitable:
                new_instruction = f"{j}•{left_table}•"
            elif j in right_suitable:
                new_instruction = f"{j}•{right_table}•"
            old_instruction_index = self.instructions.index(j)
            self.instructions[old_instruction_index] = new_instruction

    def __reorder_selections(self):
        selections = [item for item in self.instructions if "σ" in item]
        for selection in selections:
            index = self.instructions.index(selection)
            self.instructions.append(self.instructions.pop(index))

    def __handle_multiple_selections_of_the_same_table(self):
        selection_dict = {}
        for item in self.instructions:
            if "•" in item and "σ" in item:
                table = item.split("•")[1]
                if table in selection_dict:
                    selection_dict[table].append(item)
                else:
                    selection_dict[table] = [item]
        for value in selection_dict.values():
            if len(value) > 1:
                to_be_trimmed_pot = value[:-1]
                for to_be_trimmed in to_be_trimmed_pot:
                    index = self.instructions.index(to_be_trimmed)
                    trimmed = to_be_trimmed.split("•")[0]
                    self.instructions[index] = trimmed
        return

    def heuristic_reduce_tuples(self):
        join_instructions = self.__get_join_instructions()
        if not join_instructions:
            return
        selection_pot = [item for item in self.instructions if "σ" in item]
        current_instruction = join_instructions[0]
        join_match = re.match(r"\((\w+) ⋈ •(.*)• (\w+)\)", current_instruction)
        left_table, restriction, right_table = join_match.groups()
        self.__rename_selection_instructions(left_table, right_table, selection_pot)
        self.__reorder_selections()
        self.__handle_multiple_selections_of_the_same_table()
        return

    def heuristic_attribute_reduce(self):
        column_pot = []
        column_pot.extend(self.used_join_columns)
        projection_instructions = [item for item in self.instructions if "π" in item]
        for projection in projection_instructions:
            projection_match = re.match(r"π\[(.*)\]", projection)
            columns = projection_match.groups()[0].split(",")
            trimmed_columns = [item.replace(" ", "") for item in columns]
            column_pot.extend(trimmed_columns)
        left_table_columns = self.column_dict[self.left_table.lower()]
        right_table_columns = self.column_dict[self.right_table.lower()]
        left_table_projection = [item for item in left_table_columns if item in column_pot]
        right_table_projection = [item for item in right_table_columns if item in column_pot]
        return


def get_optimized_example() -> list[str]:
    qt = RelationalAlgebraProcessor()
    column_dict = qt.export_all_columns()
    instruction_example = get_sql_instruction_example_D()
    instruction_set = relational_algebra_wrapper(instruction_example)
    qo = QueryOptimizer(instruction_set, column_dict)
    return qo.optimizer_pipeline()


def __main():
    aux = get_optimized_example()
    return


if __name__ == "__main__":
    __main()
