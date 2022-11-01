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
        main_tags = ["SELECT", "FROM", "JOIN", "ON", "WHERE"]
        existing_tags = [item for item in main_tags if item in sql.split(" ")]
        join_amount = sql.count("JOIN")
        if join_amount > 1:
            self.handle_multiple_joins(existing_tags, join_amount)
            sql = self.sql
        raw_split = sql.replace(",", "").split(" ")
        existing_tags_positions = [raw_split.index(item) for item in existing_tags]
        sorted_existing_tag_positions_dict = dict(sorted(
            {existing_tags[i]: existing_tags_positions[i] for i in range(len(existing_tags))}
            .items(), key=lambda item: item[1]))
        keys = list(sorted_existing_tag_positions_dict.keys())
        values = self.split_using_multiple_separators(sql, list(sorted_existing_tag_positions_dict.keys()))
        return dict(zip(keys, values))

    @staticmethod
    def minor_split(key: str, value: str) -> Union[list[str], list[list[Union[str, Any]]]]:
        if key in {"SELECT", "FROM"}:
            aux = value.split(",")
            for index, item in enumerate(aux):
                aux[index] = item.replace(" ", "")
            return aux
        elif key == "WHERE":
            split_string = value.split(" ")
            operators = [" = ", " > ", " < ", " <= ", " >= ", " <> ", " AND ", " IN ", " NOT IN "]
            # existing_operators = {item for piece, item in itertools.product(split_string, operators) if item in piece}
            existing_operators = [item for item in operators if item in value]
            main_list = value.split(" AND ") if " AND " in existing_operators else [value]
            instruction_pool = []
            for item in main_list:
                instruction_operator = [operator for operator in existing_operators if operator in item][0]
                instruction_split = item.split(instruction_operator)
                final_instruction = [instruction_split[0], instruction_operator, instruction_split[1]]
                for index, i in enumerate(final_instruction):
                    final_instruction[index] = i.replace(" ", "")
                instruction_pool.append(final_instruction)
            return instruction_pool
        elif "JOIN" in key:
            return value.split(",") if "," in value else [value.replace(" ", "")]
        elif "ON" in key:
            first_split = value.replace(" ", "").split("AND")
            operators = ["=", ">", "<", "<=", ">=", "<>"]
            existing_operators = list({item
                                       for piece, item in itertools.product(first_split, operators) if item in piece})
            output_pot = []
            for item in first_split:
                instruction_operator = [operator for operator in existing_operators if operator in item][0]
                instruction_split = item.split(instruction_operator)
                final_instruction = [instruction_split[0], instruction_operator, instruction_split[1]]
                output_pot.append(final_instruction)
            return output_pot

    def handle_multiple_joins(self, tag_list: list[str], join_amount: int = 2):
        for index, item in enumerate(tag_list):
            if item == "JOIN":
                tag_list[index] = "JOIN_A"
            elif item == "ON":
                tag_list[index] = "ON_A"
        join_indexes = list(range(2, join_amount)) if join_amount != 2 else [2]
        for item in join_indexes:
            new_letter = chr(item + 64)
            new_join = f"JOIN_{new_letter}"
            new_on = f"ON_{new_letter}"
            tag_list.insert(-1, new_join)
            tag_list.insert(-1, new_on)
        structured_sql = self.sql.replace(",", "").split(" ")
        current_index = 0
        for index, item in enumerate(structured_sql):
            if item == "JOIN":
                current_index += 1
                structured_sql[index] = f"JOIN_{chr(current_index + 64)}"
            elif item == "ON":
                structured_sql[index] = f"ON_{chr(current_index + 64)}"
        for replace_index, _ in enumerate(range(1, join_amount + 1)):
            join_position = self.sql.find(" JOIN ") + 5
            struct_sql = list(self.sql)
            struct_sql.insert(join_position, f"_{chr(replace_index + 65)}")
            self.sql = "".join(struct_sql)
            on_position = self.sql.find(" ON ") + 3
            struct_sql = list(self.sql)
            struct_sql.insert(on_position, f"_{chr(replace_index + 65)}")
            self.sql = "".join(struct_sql)
        return


def get_sql_instruction_example_A():
    return "SELECT LNAME FROM EMPLOYEE, WORKS_ON, PROJECT " \
           "WHERE PNAME='WVX3B8W3NR' AND PNUMBER=PNO AND ESSN=SSN AND BIRTHDATE>'1999-12-31"


def get_sql_instruction_example_B():
    return "SELECT NAME, BIRTHDATE, DESCRIPTION, OPENING_BALANCE " \
           "FROM USER " \
           "JOIN ACCOUNT " \
           "ON USER.USER_ID = ACCOUNT.FK_USER_ID " \
           "WHERE OPENING_BALANCE >= 235 AND UF = 'CE' AND ZIP_CODE <> '62930000'"


def get_sql_instruction_example_C():
    return "SELECT USER_ID, NAME, BIRTHDATE, DESCRIPTION, OPENING_BALANCE, UF, ACCOUNT_TYPE_DESCRIPTION " \
           "FROM USER " \
           "JOIN ACCOUNT " \
           "ON USER.USER_ID = ACCOUNT.FK_USER_ID " \
           "JOIN ACCOUNT_TYPE " \
           "ON ACCOUNT_TYPE.ACCOUT_TYPE_ID = ACCOUNT.FK_ACCOUNT_TYPE_ID " \
           "WHERE OPENING_BALANCE >= 300 AND UF = 'CE' AND DESCRIPTION <> 'Conta Corrente' AND USER_ID > 70"


def get_sql_instruction_example_D():
    return "SELECT NAME, BIRTHDATE, DESCRIPTION, OPENING_BALANCE " \
           "FROM USER " \
           "JOIN ACCOUNT " \
           "ON USER.USER_ID = ACCOUNT.FK_USER_ID " \
           "WHERE OPENING_BALANCE >= 235 AND UF = 'CE' AND ZIP_CODE <> '23522-883' "


def get_split_example():
    rat = RelationalAlgebraSplitter()
    sql_instruction = get_sql_instruction_example_C()
    sql_d = get_sql_instruction_example_D()
    return rat.split_pipeline(sql_instruction)


def __main():
    aux = get_split_example()
    # Create a regex to match infinite words separated by commas
    regex = re.compile(r"(\w+)(,\s*\w+)*")
    return


if __name__ == "__main__":
    __main()
