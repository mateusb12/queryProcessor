import itertools
import re
from typing import Union, List, Any


class RelationalAlgebraSplitter:
    def split_pipeline(self, sql: str) -> dict:
        raw_dict = self.major_split(sql)
        for key, value in raw_dict.items():
            adjusted = self.minor_split(key, value)
            raw_dict[key] = adjusted
        return raw_dict

    @staticmethod
    def split_using_multiple_separators(input_str: str, separators: list[str]) -> list[str]:
        # sourcery skip: use-fstring-for-formatting
        return [z for y in (re.split('|'.join(r'\b{}\b'.format(x)
                                              for x in separators), z) for z in [input_str]) for z in y if z]

    def major_split(self, sql: str) -> dict:  # sourcery skip: use-fstring-for-formatting
        main_tags = ["SELECT", "FROM", "WHERE", "JOIN", "ON"]
        splitters = [item for item in main_tags if item in sql.split(" ")]
        fragments = self.split_using_multiple_separators(sql, splitters)
        return dict(zip(splitters, fragments))

    @staticmethod
    def minor_split(key: str, value: str) -> Union[list[str], list[list[Union[str, Any]]]]:
        if key in {"SELECT", "FROM"}:
            aux = value.split(",")
            for index, item in enumerate(aux):
                aux[index] = item.replace(" ", "")
            return aux
        elif key == "WHERE":
            split_string = value.split(" ")
            operators = ["=", ">", "<", "<=", ">=", "<>", "AND", "IN", "NOT IN"]
            existing_operators = {item for piece, item in itertools.product(split_string, operators) if item in piece}
            main_list = value.split("AND") if "AND" in existing_operators else [value]
            instruction_pool = []
            for item in main_list:
                instruction_operator = [operator for operator in existing_operators if operator in item][0]
                instruction_split = item.split(instruction_operator)
                final_instruction = [instruction_split[0], instruction_operator, instruction_split[1]]
                for index, i in enumerate(final_instruction):
                    final_instruction[index] = i.replace(" ", "")
                instruction_pool.append(final_instruction)
            return instruction_pool


def __main():
    rat = RelationalAlgebraSplitter()
    sql_instruction = "SELECT LNAME FROM EMPLOYEE, WORKS_ON, PROJECT " \
                      "WHERE PNAME='AQUARIUS' AND PNUMBER=PNO AND ESSN=SSN AND BDATE>'1957-12-31"
    aux = rat.split_pipeline(sql_instruction)
    return


if __name__ == "__main__":
    __main()
