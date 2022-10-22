import re
from pathlib import Path

import pandas as pd

from path_reference.paths import get_table_path


class RelationalAlgebraProcessor:
    def __init__(self):
        self.tables = self.map_all_tables()
        self.convert_datetime_format()

    @staticmethod
    def map_all_tables() -> dict:
        """ This function maps all tables in the table folder to a dictionary.
         The key is the table name and the value is the table itself"""
        table_dict = {}
        table_folder = Path(get_table_path())
        for table in table_folder.glob("*.csv"):
            table_name = table.stem
            table_dict[table_name] = pd.read_csv(table)
        return table_dict

    def convert_datetime_format(self):
        """Converts all datetime columns to datetime format"""
        for table in self.tables.values():
            for column in table.columns:
                first_value = str(table[column].iloc[0])
                if re.match(r"\d{2}/\d{2}/\d{4}", first_value):
                    table[column] = pd.to_datetime(table[column], format='%d/%m/%Y')

    def load_table(self, table_tag: str or pd.DataFrame) -> pd.DataFrame:
        if isinstance(table_tag, str):
            table_tag = table_tag.lower()
        return self.tables[table_tag] if isinstance(table_tag, str) else table_tag

    def set_up_query_example(self):
        first = self.cartesian_product("employee", "works_on")
        second = self.cartesian_product(first, "project")
        third = self.selection(input_table=second, column="PNAME", operator="=", value="TWWPPHHHS1")
        fourth = self.selection(third, "ESSN = SSN")
        return self.selection(fourth, "BIRTHDATE > '01/01/1996'")

    def cartesian_product(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame:
        """Returns a cross product of two tables. The final table should have the same columns as the first table"""
        original_table_a = self.load_table(table_a)
        original_table_b = self.load_table(table_b)
        return pd.merge(original_table_a, original_table_b, how="cross")

    @staticmethod
    def check_compatible_tables(table_a: pd.DataFrame, table_b: pd.DataFrame) -> tuple[bool, str]:
        # sourcery skip: assign-if-exp, reintroduce-else, swap-if-expression
        """ Checks if two tables are compatible.
        Returns a tuple of a boolean and a string. If the boolean is True, the tables are compatible."""
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

    def prepare_compatible_tables(self, table_a: str or pd.DataFrame,
                                  table_b: str or pd.DataFrame) -> pd.DataFrame or str:
        """ Returns two tables that are compatible with each other. If they are not compatible, returns a string"""
        original_table_a = self.load_table(table_a)
        original_table_b = self.load_table(table_b)
        compatible_test, compatible_tag = self.check_compatible_tables(original_table_a, original_table_b)
        if not compatible_test:
            return compatible_test, compatible_tag
        original_table_b.columns = original_table_a.columns
        return original_table_a, original_table_b

    def union(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame or None:
        """Performs a union on two tables. The final table should have the same columns as the first table.
        Both tables should be compatible."""
        prepared_table_a, prepared_table_b = self.prepare_compatible_tables(table_a, table_b)
        return pd.concat([prepared_table_a, prepared_table_b], ignore_index=True).drop_duplicates()

    def intersection(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame or str:
        """Returns all rows that are in both tables. Both tables should be compatible"""
        prepared_table_a, prepared_table_b = self.prepare_compatible_tables(table_a, table_b)
        prepared_table_b.columns = prepared_table_a.columns
        return pd.merge(prepared_table_a, prepared_table_b, how="inner")

    def difference(self, table_a: str or pd.DataFrame, table_b: str or pd.DataFrame) -> pd.DataFrame or str:
        """Returns all rows that are in table_a but not in table_b. Both tables should be compatible"""
        prepared_table_a, prepared_table_b = self.prepare_compatible_tables(table_a, table_b)
        return pd.merge(prepared_table_a, prepared_table_b, how="left",
                        indicator=True).query("_merge == 'left_only'").drop(columns=['_merge'])

    def projection(self, input_table: str or pd.DataFrame, desired_columns: list[str]) -> pd.DataFrame:
        """Returns a table with only the desired columns"""
        original_table = self.load_table(input_table)
        return original_table[desired_columns]

    def selection(self, input_table: str or pd.DataFrame, column: str, operator: str = "=", value: str = ""):
        """Returns a table with only the rows that satisfy the instruction"""
        original_table = self.load_table(input_table)
        alL_columns = original_table.columns
        right_value = value if value not in alL_columns else original_table[value]
        if operator == "=":
            return original_table[original_table[column] == right_value]
        elif operator == ">":
            return original_table[original_table[column] > right_value]
        elif operator == "<":
            return original_table[original_table[column] < right_value]


def __main():
    qt = RelationalAlgebraProcessor()
    aux = qt.set_up_query_example()
    return


if __name__ == "__main__":
    __main()
