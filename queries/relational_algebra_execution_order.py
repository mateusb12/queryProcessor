import re


class RelationalAlgebraExecutionOrder:
    def __init__(self, full_expression: str):
        self.full_expression = full_expression
        self.expressions = None

    def export_execution_order(self) -> list[str]:
        self.expressions = self.__raw_order(self.full_expression)
        self.__all_expressions_fix(self.expressions)
        return self.expressions

    @staticmethod
    def __raw_order(input_string: str) -> list[str]:
        """This function splits instructions by parenthesis and order then by executing the most inner ones first"""
        parenthesis_pot = []
        instruction_dict = {}
        for character in input_string:
            if character == "(":
                parenthesis_pot.append(True)
            elif character == ")":
                parenthesis_pot.pop()
            else:
                location = len(parenthesis_pot)
                if location not in instruction_dict:
                    instruction_dict[location] = []
                instruction_dict[location].append(character)
        for key, value in instruction_dict.items():
            instruction_dict[key] = "".join(value)
        return [value for key, value in sorted(instruction_dict.items(), key=lambda item: item[0])]

    def __all_expressions_fix(self, input_expressions: list[str]):
        for item in input_expressions:
            self.__single_expression_fix(item)

    def __single_expression_fix(self, input_str):
        multiple_selection_match = self.__multiple_selections_check(input_str)
        incomplete_cross_product_match = self.__incomplete_cross_product_check(input_str)
        if multiple_selection_match:
            groups = self.__multiple_selections_split(input_str)
            for index, item in enumerate(groups):
                groups[index] = item.replace("'", "").replace(" ", "")
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
    def __incomplete_cross_product_check(input_str: str):
        """Incomplete cross product is when we have ⨯ but only 1 word after it"""
        if "⨯" not in input_str:
            return False
        formatted_str = input_str.replace(" ", "")
        test = formatted_str.split("⨯")
        test = [item for item in test if item != ""]
        return len(test) != 2

    @staticmethod
    def __multiple_selections_check(string: str):
        """If the string has σ and ^ then it has multiple selections"""
        return "σ" in string and "^" in string

    @staticmethod
    def __multiple_selections_split(string: str):
        """Split the string into multiple selections by using the ^ character"""
        return string.split("^")


def __main():
    projection = "π[USER_ID, NAME, BIRTHDATE, DESCRIPTION, OPENING_BALANCE, UF, ACCOUNT_DESCRIPTION]"
    selection = "(σ[OPENING_BALANCE>=300] ^ σ[UF='CE'] ^ σ[ACCOUNT_DESCRIPTION<>'ContaCorrente'] ^ σ[USER_ID>3]"
    cartesian = "(((USER ⨯ ACCOUNT) ⨯ ACCOUNT_TYPE)))"
    full_relational = f"{projection} {selection} {cartesian}"
    t = RelationalAlgebraExecutionOrder(full_relational)
    order = t.export_execution_order()
    return


if __name__ == "__main__":
    __main()
