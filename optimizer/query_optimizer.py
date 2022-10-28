from queries.relational_algebra_splitter import get_sql_instruction_example_C
from queries.relational_algebra_wrapper import relational_algebra_wrapper


class QueryOptimizer:
    def __init__(self, instruction_list: list[str]):
        self.instructions = instruction_list


def __main():
    instruction_example = get_sql_instruction_example_C()
    instruction_set = relational_algebra_wrapper(instruction_example)
    qo = QueryOptimizer(instruction_set)
    return


if __name__ == "__main__":
    __main()
