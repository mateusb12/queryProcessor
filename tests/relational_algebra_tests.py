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


def __main():
    rap = RelationalAlgebraProcessor()


if __name__ == "__main__":
    __main()
