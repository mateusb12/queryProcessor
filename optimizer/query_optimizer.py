import re

from queries.relational_algebra_processor import RelationalAlgebraProcessor
from queries.relational_algebra_splitter import get_sql_instruction_example_C, get_sql_instruction_example_D
from queries.relational_algebra_wrapper import relational_algebra_wrapper


class QueryOptimizer:
    def __init__(self, instruction_list: list[str], column_dict: dict):
        self.instructions = instruction_list
        self.column_dict = column_dict
        self.instruction_dict = {}

    def optimizer_pipeline(self):
        self.__analyze_instructions()
        if "cross_product" in self.instruction_dict.keys():
            self.avoid_cross_product()
        self.reduce_tuples()
        return self.instructions

    def __analyze_instructions(self):
        for item in self.instructions:
            if "⨯" in item:
                self.instruction_dict["cross_product"] = item

    def avoid_cross_product(self):
        main_value = self.instruction_dict["cross_product"]
        table_a, table_b = [item.replace(" ", "") for item in main_value.split("⨯")]
        removed_instruction, new_instruction = "", ""
        for instruction in self.instructions:
            if instruction.startswith("σ") and table_a in instruction and table_b in instruction:
                operators = ["=", "<", ">", "<=", ">=", "<>"]
                existing_operator = [operator for operator in operators if operator in instruction][0]
                raw_condition = instruction.split(existing_operator)
                left_condition, right_condition = [item.replace("σ[", "").replace("]", "") for item in raw_condition]
                removed_instruction = instruction
                new_instruction = f"({table_a} ⋈ •{left_condition}{existing_operator}{right_condition}• {table_b})"
                break
        if removed_instruction in self.instructions:
            self.instructions.remove(removed_instruction)
        for index, instruction in enumerate(self.instructions):
            if instruction == main_value:
                self.instructions[index] = new_instruction
                break
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

    def __merge_common_selections(self):
        selection_dict = {}
        for instruction in self.instructions:
            if selection_match := re.match(r"σ\[(\w+)([<>=!]+)(.*)\]•(\w+)•", instruction):
                column, operator, value, table = selection_match.groups()
                if table not in selection_dict.keys():
                    selection_dict[table] = []
                selection_dict[table].append(f"σ[{column}{operator}{value}]")
        for key, value in selection_dict.items():
            if len(value) > 1:
                new_selection = " ∧ ".join(value)
                for item in value:
                    if f"{item}•{key}•" in self.instructions:
                        self.instructions.remove(f"{item}•{key}•")
                self.instructions.append(f"({new_selection})•{key}•")

    def reduce_tuples(self):
        join_instructions = self.__get_join_instructions()
        if not join_instructions:
            return
        selection_pot = [item for item in self.instructions if "σ" in item]
        current_instruction = join_instructions[0]
        join_match = re.match(r"\((\w+) ⋈ •(.*)• (\w+)\)", current_instruction)
        left_table, restriction, right_table = join_match.groups()
        self.__reorder_selections()
        self.__rename_selection_instructions(left_table, right_table, selection_pot)
        self.__merge_common_selections()
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
