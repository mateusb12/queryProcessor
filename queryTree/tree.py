import re


class Tree:
    def __init__(self, full_expression: str):
        raw_expressions = re.split(r"\(|\)", full_expression)
        self.expressions = [item for item in raw_expressions if item != ""]
        self.all_expressions_fix(self.expressions)

    def all_expressions_fix(self, input_expressions: list[str]):
        for item in input_expressions:
            self.single_expression_fix(item)

    def single_expression_fix(self, input_str):
        multiple_selection_match = self.multiple_selections_check(input_str)
        incomplete_cross_product_match = self.incomplete_cross_product_check(input_str)
        if multiple_selection_match:
            groups = self.multiple_selections_split(input_str)
            for item in groups:
                item = item.replace("'", "").replace(" ", "")
            current_expression_index = self.expressions.index(input_str)
            self.expressions.remove(input_str)
            self.expressions[current_expression_index:current_expression_index] = groups
        if incomplete_cross_product_match:
            group = input_str.replace(" ", "").split("⨯")[1]
            new_expression = f"SELF ⨯ {group}"
            current_expression_index = self.expressions.index(input_str)
            self.expressions.remove(input_str)
            self.expressions[current_expression_index:current_expression_index] = [new_expression]
        return

    @staticmethod
    def incomplete_cross_product_check(input_str: str):
        """Incomplete cross product is when we have ⨯ but only 1 word after it"""
        if "⨯" not in input_str:
            return False
        formatted_str = input_str.replace(" ", "")
        test = formatted_str.split("⨯")
        test = [item for item in test if item != ""]
        return len(test) != 2

    @staticmethod
    def multiple_selections_check(string: str):
        """If the string has σ and ^ then it has multiple selections"""
        return "σ" in string and "^" in string

    @staticmethod
    def multiple_selections_split(string: str):
        """Split the string into multiple selections by using the ^ character"""
        return string.split("^")


def __main():
    t = Tree("π[LNAME](σ[PNAME='AQUARIUS'] ^ σ[PNUMBER=PNO] ^ σ[ESSN=SSN] ^ σ[BDATE>'1957-12-31']"
             "((((EMPLOYEE ⨯ WORKS_ON) ⨯ PROJECT))))")
    return


if __name__ == "__main__":
    __main()
