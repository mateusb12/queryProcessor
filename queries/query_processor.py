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
        intersection_test = self.intersection("employee", "project")
        # first = self.cross_product("employee", "works_on")
        # second = self.cross_product(first, "project")
        # third = self.selection(second, "PNAME = TWWPPHHHS1")
        # fourth = self.selection(third, "ESSN = SSN")
        # fifth = self.selection(fourth, "BIRTHDATE > '01/01/1996'")
        return

    def cross_product(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame:
        original_table_a = self.load_table(table_a)
        original_table_b = self.load_table(table_b)
        return pd.merge(original_table_a, original_table_b, how="cross")

    @staticmethod
    def check_compatible_tables(table_a: pd.DataFrame, table_b: pd.DataFrame) -> tuple[bool, str]:
        # sourcery skip: assign-if-exp, reintroduce-else, swap-if-expression
        a_shape, b_shape = table_a.shape[1], table_b.shape[1]
        a_type, b_type = list(table_a.dtypes), list(table_b.dtypes)
        condition_1 = a_shape == b_shape
        if not condition_1:
            return False, f"Tables must have the same number of columns." \
                          f" Table A has {a_shape} columns, Table B has {b_shape} columns"
        condition_2 = a_type == b_type
        if not condition_2:
            return False, f"Tables must have the same column types." \
                          f" Table A has {a_type}, Table B has {b_type}"
        return True, "Tables are compatible"

    def union(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame or None:
        """Performs a union on two tables. The final table should have the same columns as the first table.
        Both tables should be compatible."""
        original_table_a = self.load_table(table_a)
        original_table_b = self.load_table(table_b)
        compatible_test, compatible_tag = self.check_compatible_tables(original_table_a, original_table_b)
        if not compatible_test:
            return compatible_tag
        original_table_b.columns = original_table_a.columns
        return pd.concat([original_table_a, original_table_b], ignore_index=True).drop_duplicates()

    def intersection(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame or str:
        """Returns all rows that are in both tables. Both tables should be compatible"""
        d1 = {"FN": ["Tom", "Amy", "Alicia", "Ernest"],
              "LN": ["Ford", "Jones", "Smith", "Gilbert"]}
        d2 = {"FName": ["Amy", "John", "Alicia"],
              "Lname": ["Jones", "Brown", "Smith"]}
        original_table_a = self.load_table(table_a)
        original_table_b = self.load_table(table_b)
        compatible_test, compatible_tag = self.check_compatible_tables(original_table_a, original_table_b)
        if not compatible_test:
            return compatible_tag
        original_table_b.columns = original_table_a.columns
        return pd.merge(original_table_a, original_table_b, how="inner")

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
