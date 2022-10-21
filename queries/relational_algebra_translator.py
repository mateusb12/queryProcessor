from functools import reduce

from queries.relational_algebra_splitter import get_split_example


class RelationalAlgebraTranslator:
    def __init__(self):
        self.split_info = get_split_example()

    def translate(self):
        projection = self.extract_projection()
        cartesian_product = self.extract_cartesian_product()
        selection = self.extract_selection()
        return 0

    def extract_projection(self):
        return ["π(" + ", ".join(self.split_info["SELECT"]) + ")"]

    def extract_cartesian_product(self):
        from_values = self.split_info["FROM"]
        # Create a lambda function to join two strings and form a cartesian product
        join = lambda x, y: f"({x} ⨯ {y})"
        # Use reduce with join to form the cartesian product
        return [reduce(join, from_values)]

    def extract_selection(self):
        where_values = self.split_info["WHERE"]
        return [f"σ({item[0]}{item[1]}{item[2]})" for item in where_values]


def __main():
    rat = RelationalAlgebraTranslator()
    aux = rat.translate()
    return


if __name__ == "__main__":
    __main()
