import re

from queries.relational_algebra_splitter import get_sql_instruction_example_A, get_sql_instruction_example_B, \
    get_sql_instruction_example_C, get_sql_instruction_example_D


class QueryParser:
    def __init__(self, input_sql: str):
        self.sql = input_sql
        self.parse_pipeline()

    def parse_pipeline(self):
        core_match = self.__core_parser()
        extra_matches = self.__extra_parser()
        if extra_matches == ["WHERE"]:
            core_regex = "(SELECT )(.*)( FROM )(.*)( WHERE )(.*)"
        elif extra_matches == ["WHERE", "JOIN", "ON"]:
            core_regex = "(SELECT )(.*)( FROM )(.*)( JOIN )(.*)"
        else:
            core_regex = ""
        groups = list(re.match(core_regex, self.sql).groups())
        core_sql = "".join(groups[:-2])
        self.core_sql_analyze(core_sql)
        rest_sql = "".join(groups[-2:])
        if "JOIN" in extra_matches:
            rest_sql = self.extract_join(rest_sql)
        self.analyze_where(rest_sql)
        return

    @staticmethod
    def core_sql_analyze(core_sql: str):
        match = re.match("SELECT (\w+)((,\s*\w+)*)? FROM (\w+)((,\s*\w+)*)?", core_sql)
        if match is None:
            raise ValueError("Invalid SQL syntax")

    @staticmethod
    def analyze_where(where_sql: str):
        if " AND " not in where_sql:
            where_match = re.match("(\w+)\.(\w+)(\s*)(=|<|>)(\s*)(\w+)", where_sql)
        else:
            # TODO: implement a correct way of capturing multiple ANDS
            where_match = re.match("(\w+)\.(\w+)(\s*)(=|<|>)(\s*)(\w+)( AND )(.*)", where_sql)
        if where_match is None:
            raise ValueError("Invalid SQL syntax")

    @staticmethod
    def extract_join(join_sql: str):
        match = re.match("^(?: JOIN )(?:.*)(?: ON )(.*)( WHERE)(.*)", join_sql)
        if groups := match.groups():
            return "".join(groups[1:])
        else:
            raise ValueError("Wrong join condition found")

    def __core_parser(self) -> bool:
        core = []
        if "SELECT " in self.sql:
            core.append("SELECT")
        if " FROM " in self.sql:
            core.append("FROM")
        return len(core) == 2

    def __extra_parser(self):
        pot = []
        if "WHERE " in self.sql:
            pot.append("WHERE")
        if " JOIN " in self.sql:
            pot.append("JOIN")
        if " ON " in self.sql:
            pot.append("ON")
        return pot


def __main():
    a_example = get_sql_instruction_example_A()
    b_example = get_sql_instruction_example_B()
    c_example = get_sql_instruction_example_C()
    d_example = get_sql_instruction_example_D()
    qp = QueryParser(b_example)
    return


if __name__ == "__main__":
    __main()
