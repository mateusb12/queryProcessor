from queries.relational_algebra_splitter import get_sql_instruction_example_C, get_sql_instruction_example_D
from queries.relational_algebra_wrapper import relational_algebra_wrapper


class QueryOptimizer:
    def __init__(self, instruction_list: list[str]):
        self.instructions = instruction_list
        self.instruction_dict = {}
        self.optimizer_pipeline()

    def optimizer_pipeline(self):
        self.__analyze_instructions()
        if "cross_product" in self.instruction_dict.keys():
            self.avoid_cross_product()
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


def get_optimized_example() -> list[str]:
    instruction_example = get_sql_instruction_example_D()
    instruction_set = relational_algebra_wrapper(instruction_example)
    qo = QueryOptimizer(instruction_set)
    return qo.optimizer_pipeline()


def __main():
    aux = get_optimized_example()
    return


if __name__ == "__main__":
    __main()
