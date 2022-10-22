import re


class Tree:
    def __init__(self, full_expression: str):
        raw_expressions = re.split(r"\(|\)", full_expression)
        expressions = [item for item in raw_expressions if item != ""]
        self.full_expression = full_expression
        expression_pot = full_expression.split(")")
        print("original expression_pot: ", expression_pot)

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


if __name__ == "__main__":
    __main()
