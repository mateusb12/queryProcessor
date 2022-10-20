from pathlib import Path

import pandas as pd

from path_reference.paths import get_table_path


class QueryTest:
    def __init__(self):
        table_path = get_table_path()
        self.employee_table = pd.read_csv(Path(table_path, "employee.csv"))
        self.project_table = pd.read_csv(Path(table_path, "project.csv"))
        self.works_on_table = pd.read_csv(Path(table_path, "works_on.csv"))
        self.employee_table['BIRTHDATE'] = pd.to_datetime(self.employee_table['BIRTHDATE'], format='%d/%m/%Y')
        self.project_table["DSTART"] = pd.to_datetime(self.project_table["DSTART"], format='%d/%m/%Y')
        self.project_table["DEND"] = pd.to_datetime(self.project_table["DEND"], format='%d/%m/%Y')
        self.tables = {"employee": self.employee_table, "project": self.project_table, "works_on": self.works_on_table}

    def load_table(self, table_tag: str or pd.DataFrame) -> pd.DataFrame:
        return self.tables[table_tag] if isinstance(table_tag, str) else table_tag

    def set_up_query(self):
        first = self.cross_product("employee", "works_on")
        second = self.cross_product(first, "project")
        third = self.selection(second, "PNAME = TWWPPHHHS1")
        fourth = self.selection(third, "ESSN = SSN")
        fifth = self.selection(fourth, "BIRTHDATE > '01/01/1996'")
        return

    def cross_product(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame:
        original_table_a = self.load_table(table_a)
        original_table_b = self.load_table(table_b)
        return pd.merge(original_table_a, original_table_b, how="cross")

    def projection(self, input_table: str or pd.DataFrame, desired_columns: list[str]) -> pd.DataFrame:
        original_table = self.load_table(input_table)
        return original_table[desired_columns]

    def selection(self, input_table: str or pd.DataFrame, instruction: str):
        original_table = self.load_table(input_table)
        alL_columns = original_table.columns
        column, operator, value = instruction.split(" ")
        right_value = value if value not in alL_columns else original_table[value]
        if operator == "=":
            return original_table[original_table[column] == right_value]
        elif operator == ">":
            return original_table[original_table[column] > right_value]
        elif operator == "<":
            return original_table[original_table[column] < right_value]


def __main():
    qt = QueryTest()
    qt.set_up_query()


if __name__ == "__main__":
    __main()
