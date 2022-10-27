from queries.relational_algebra_execution_order import RelationalAlgebraExecutionOrder
from queries.relational_algebra_splitter import get_sql_instruction_example_A, RelationalAlgebraSplitter, \
    get_sql_instruction_example_B
from queries.relational_algebra_translator import RelationalAlgebraTranslator


def relational_algebra_wrapper(sql_instruction: str) -> list[str]:
    """
    This function is the wrapper for the relational algebra translator.
    :param sql_instruction: The SQL instruction to be translated.
    :return: The relational algebra instruction.
    """
    splitter = RelationalAlgebraSplitter()
    split_sql = splitter.split_pipeline(sql_instruction)
    translator = RelationalAlgebraTranslator(split_sql)
    relational_algebra_expression = translator.translate_sql()
    order_analyzer = RelationalAlgebraExecutionOrder(relational_algebra_expression)
    return order_analyzer.export_execution_order()


def __main():
    instruction_example = get_sql_instruction_example_B()
    aux = relational_algebra_wrapper(instruction_example)
    return


if __name__ == "__main__":
    __main()
