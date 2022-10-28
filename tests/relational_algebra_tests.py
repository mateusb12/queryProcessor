# Create Tests

import unittest

import pandas as pd

from queries.relational_algebra_processor import RelationalAlgebraProcessor


def get_selection_example() -> pd.DataFrame:
    content = {"FName": ["Tom", "Amy", "Alicia", "Frank"],
               "LName": ["Ford", "Jones", "Smith", "Smith"],
               "Salary": [30000, 20000, 40000, 38000],
               "DNo": [3, 2, 2, 3]}
    return pd.DataFrame(content)


def get_projection_example() -> pd.DataFrame:
    content = {"FName": ["Tom", "Amy"],
               "LName": ["Ford", "Jones"],
               "Salary": [30000, 20000],
               "DNo": [3, 2]}
    return pd.DataFrame(content)


def get_union_example() -> tuple[pd.DataFrame, pd.DataFrame]:
    content_a = {"FName": ["Tom", "Amy", "Alicia", "Ernest"],
                 "LName": ["Ford", "Jones", "Smith", "Gilbert"]}
    content_b = {"FName": ["Amy", "John", "Alicia"],
                 "LName": ["Jones", "Brown", "Smith"]}
    return pd.DataFrame(content_a), pd.DataFrame(content_b)


def get_cross_product_example() -> tuple[pd.DataFrame, pd.DataFrame]:
    content_a = {"A": [101, 102, 103],
                 "B": [104, 105, 106]}
    content_b = {"C": ["p", "q"],
                 "D": ["a", "b"],
                 "E": ["x", "y"]}
    return pd.DataFrame(content_a), pd.DataFrame(content_b)


def get_junction_example() -> tuple[pd.DataFrame, pd.DataFrame]:
    content_a = {"DName": ["Research", "Finance"],
                 "DNo": [2, 5],
                 "Msg_SSN": [553621425, 996856974]}
    content_b = {"SSN": [123658974, 553621425, 996856974, 859689742],
                 "FName": ["Alex", "Fred", "Elsa", "Peter"],
                 "LName": ["Smith", "Scott", "David", "Willians"],
                 "DNo": [2, 5, 5, 2]}
    return pd.DataFrame(content_a), pd.DataFrame(content_b)


class TestRelationalAlgebraProcessor(unittest.TestCase):

    def test_selection(self):
        processor = RelationalAlgebraProcessor()
        example = get_selection_example()
        first_selection = processor.selection(input_table=example, column="DNo", operator="=", value="2")
        output = processor.selection(input_table=example, column="Salary", operator=">", value="30000")
        output.reset_index(drop=True, inplace=True)
        desired_content = {"FName": ["Alicia", "Frank"],
                           "LName": ["Smith", "Smith"],
                           "Salary": [40000, 38000],
                           "DNo": [2, 3]}
        desired_output = pd.DataFrame(desired_content)
        comparison = output.equals(desired_output)
        self.assertTrue(comparison)

    def test_projection(self):
        processor = RelationalAlgebraProcessor()
        example = get_projection_example()
        output = processor.projection(input_table=example, desired_columns=["FName", "LName"])
        output.reset_index(drop=True, inplace=True)
        desired_content = {"FName": ["Tom", "Amy"],
                           "LName": ["Ford", "Jones"]}
        desired_output = pd.DataFrame(desired_content)
        comparison = output.equals(desired_output)
        self.assertTrue(comparison)

    def test_union(self):
        processor = RelationalAlgebraProcessor()
        example_a, example_b = get_union_example()
        output = processor.union(table_a=example_a, table_b=example_b)
        output.reset_index(drop=True, inplace=True)
        desired_content = {"FName": ["Tom", "Amy", "Alicia", "Ernest", "Amy", "John", "Alicia"],
                           "LName": ["Ford", "Jones", "Smith", "Gilbert", "Jones", "Brown", "Smith"]}
        desired_output = pd.DataFrame(desired_content)
        comparison = output.equals(desired_output)
        self.assertTrue(comparison)

    def test_intersection(self):
        processor = RelationalAlgebraProcessor()
        example_a, example_b = get_union_example()
        output = processor.intersection(table_a=example_a, table_b=example_b)
        output.reset_index(drop=True, inplace=True)
        desired_content = {"FName": ["Amy", "Alicia"],
                           "LName": ["Jones", "Smith"]}
        desired_output = pd.DataFrame(desired_content)
        comparison = output.equals(desired_output)
        self.assertTrue(comparison)

    def test_cross_product(self):
        processor = RelationalAlgebraProcessor()
        example_a, example_b = get_cross_product_example()
        output = processor.cartesian_product(table_a=example_a, table_b=example_b)
        output.reset_index(drop=True, inplace=True)
        desired_content = {"A": [101, 101, 101, 101, 102, 102, 102, 102, 103, 103, 103, 103],
                           "B": [104, 104, 104, 104, 105, 105, 105, 105, 106, 106, 106, 106],
                           "C": ["p", "p", "p", "p", "q", "q", "q", "q", "p", "p", "p", "p"],
                           "D": ["a", "a", "a", "a", "b", "b", "b", "b", "a", "a", "a", "a"],
                           "E": ["x", "x", "x", "x", "y", "y", "y", "y", "x", "x", "x", "x"]}
        desired_output = pd.DataFrame(desired_content)
        comparison = output.equals(desired_output)
        self.assertTrue(comparison)

    def test_join(self):
        processor = RelationalAlgebraProcessor()
        example_a, example_b = get_junction_example()
        output = processor.join(table_a=example_a, table_b=example_b, column_a="Msg_SSN", column_b="SSN")
        output.reset_index(drop=True, inplace=True)
        desired_content = {"DName": ["Research", "Finance"],
                           "DNo_x": [2, 5],
                           "Msg_SSN": [553621425, 996856974],
                           "SSN": [553621425, 996856974],
                           "FName": ["Fred", "Elsa"],
                           "LName": ["Scott", "David"],
                           "DNo_y": [5, 5]}
        desired_output = pd.DataFrame(desired_content)
        comparison = output.equals(desired_output)
        self.assertTrue(comparison)


def __main():
    rap = RelationalAlgebraProcessor()


if __name__ == "__main__":
    __main()
