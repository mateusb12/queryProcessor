import itertools
import re
from typing import Union, List, Any


class RelationalAlgebraSplitter:
    def __init__(self):
        self.sql = ""

    def split_pipeline(self, sql: str) -> dict:
        self.sql = sql
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
        existing_tags = [item for item in main_tags if item in sql.split(" ")]
        raw_split = sql.replace(",", "").split(" ")
        existing_tags_positions = [raw_split.index(item) for item in existing_tags]
        sorted_existing_tag_positions_dict = dict(sorted(
            {existing_tags[i]: existing_tags_positions[i] for i in range(len(existing_tags))}
            .items(), key=lambda item: item[1]))
        values = self.split_using_multiple_separators(sql, list(sorted_existing_tag_positions_dict.keys()))
        return dict(zip(sorted_existing_tag_positions_dict.keys(), values))

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
        elif key == "JOIN":
            return value.split(",") if "," in value else [value.replace(" ", "")]
        elif key == "ON":
            first_split = value.split("AND")
            return value.split("=")


def get_sql_instruction_example_A():
    return "SELECT LNAME FROM EMPLOYEE, WORKS_ON, PROJECT " \
           "WHERE PNAME='WVX3B8W3NR' AND PNUMBER=PNO AND ESSN=SSN AND BIRTHDATE>'1999-12-31"


def get_sql_instruction_example_B():
    return "SELECT NAME, BIRTHDATE, DESCRIPTION, OPENING_BALANCE " \
           "FROM USER " \
           "JOIN ACCOUNT " \
           "ON USER.USER_ID = ACCOUNT.FK_USER_ID " \
           "WHERE OPENING_BALANCE >= 235 AND UF = 'CE' AND ZIP_CODE <> '62930000'"


def get_split_example():
    rat = RelationalAlgebraSplitter()
    sql_instruction = get_sql_instruction_example_B()
    return rat.split_pipeline(sql_instruction)


def __main():
    aux = get_split_example()
    return


if __name__ == "__main__":
    __main()
