import random

import pandas as pd

from placeholder_generator.core_generator import generate_random_integer, generate_random_street_name, \
    generate_random_birthdate, generate_random_project_name, generate_random_tag, generate_random_first_name
from placeholder_generator.table_importer import account_type_table, user_table, transaction_type_table, category_table, \
    account_table


def generate_random_user_table_line():
    """Create a csv with random user entries"""
    ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE",
           "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    user_id = generate_random_integer(100000, 999999)
    name = generate_random_first_name()
    address = generate_random_street_name().replace(",", " ")
    number = generate_random_integer(1000, 9999)
    district = generate_random_tag()
    zip_code = f"{generate_random_integer(10000, 99999)}-{generate_random_integer(100, 999)}"
    uf = random.choice(ufs)
    birthdate = generate_random_birthdate()
    return f"{user_id},{name},{address},{number},{district},{zip_code},{uf},{birthdate}"


def generate_random_account_type_table_line():
    account_type_id = generate_random_integer(100000, 999999)
    description = generate_random_project_name(10)
    return f"{account_type_id},{description}"


def generate_random_account_table_line():
    account_id = generate_random_integer(100000, 999999)
    description = generate_random_project_name(10)
    random_account_type_id = random.choice(account_type_table["ACCOUNT_TYPE_ID"])
    random_user_id = random.choice(user_table["USER_ID"])
    opening_balance = generate_random_integer(1000, 50000)
    return f"{account_id},{description},{random_account_type_id},{random_user_id},{opening_balance}"


def generate_random_transaction_type_table_line():
    transaction_id = generate_random_integer(100000, 999999)
    transaction_description = generate_random_project_name(15)
    return f"{transaction_id},{transaction_description}"


def generate_random_category_table_line():
    category_id = generate_random_integer(100000, 999999)
    category_description = generate_random_project_name(10)
    return f"{category_id},{category_description}"


def generate_random_transaction_table_line():
    transaction_id = generate_random_integer(100000, 999999)
    date = generate_random_birthdate()
    description = generate_random_project_name(20)
    transaction_type_id = random.choice(transaction_type_table["TRANSACTION_TYPE_ID"])
    category_id = random.choice(category_table["CATEGORY_ID"])
    account_id = random.choice(account_table["ACCOUNT_ID"])
    value = generate_random_integer(1000, 50000)
    return f"{transaction_id},{date},{description},{transaction_type_id},{category_id},{account_id},{value}"


def create_user_table_csv(size: int = 10000):
    """Create a csv with random user entries"""
    with open("main_table/user.csv", "w") as file:
        file.write("USER_ID,NAME,ADDRESS,NUMBER,DISTRICT,ZIP_CODE,UF,BIRTHDATE\n")
        for _ in range(size):
            new_line = f"{generate_random_user_table_line()}\n"
            file.write(new_line)
    print("User table created successfully")


def create_account_type_csv(size: int = 10000):
    """Create a csv with random account type entries"""
    with open("main_table/account_type.csv", "w") as file:
        file.write("ACCOUNT_TYPE_ID,ACCOUNT_TYPE_DESCRIPTION\n")
        for _ in range(size):
            file.write(f"{generate_random_account_type_table_line()}\n")


def create_account_csv(size: int = 10000):
    """Create a csv with random account entries"""
    with open("main_table/account.csv", "w") as file:
        file.write("ACCOUNT_ID,DESCRIPTION,FK_ACCOUNT_TYPE_ID,FK_USER_ID,OPENING_BALANCE\n")
        for _ in range(size):
            file.write(f"{generate_random_account_table_line()}\n")


def create_transaction_type_csv(size: int = 10000):
    """Create a csv with random transaction type entries"""
    with open("main_table/transaction_type.csv", "w") as file:
        file.write("TRANSACTION_TYPE_ID,TRANSACTION_TYPE_DESCRIPTION\n")
        for _ in range(size):
            file.write(f"{generate_random_transaction_type_table_line()}\n")


def create_category_csv(size: int = 10000):
    """Create a csv with random category entries"""
    with open("main_table/category.csv", "w") as file:
        file.write("CATEGORY_ID,CATEGORY_DESCRIPTION\n")
        for _ in range(size):
            file.write(f"{generate_random_category_table_line()}\n")


def create_transaction_csv(size: int = 10000):
    """Create a csv with random transaction entries"""
    with open("main_table/transaction.csv", "w") as file:
        file.write("TRANSACTION_ID,DATE,TRANSACTION_DESCRIPTION,"
                   "FK_TRANSACTION_TYPE_ID,FK_CATEGORY_ID,FK_ACCOUNT_ID,VALUE\n")
        for _ in range(size):
            file.write(f"{generate_random_transaction_table_line()}\n")


def recalculate_all_indexes():
    table_dict = {"user": "USER_ID", "account_type": "ACCOUNT_TYPE_ID", "account": "ACCOUNT_ID",
                  "transaction_type": "TRANSACTION_TYPE_ID", "category": "CATEGORY_ID",
                  "transaction": "TRANSACTION_ID"}
    for key, value in table_dict.items():
        recalculate_single_index(key, value)


def recalculate_single_index(table_name: str, index_column: str):
    try:
        table = pd.read_csv(f"main_table/{table_name}.csv")
    except FileNotFoundError:
        print(f"Table {table_name} not found")
        return
    size = len(table)
    table[index_column] = range(1, size + 1)
    table.to_csv(f"main_table/{table_name}.csv", index=False)


def full_pipeline(size: int = 10000):
    create_user_table_csv(size)
    create_account_type_csv(size)
    recalculate_all_indexes()
    create_account_csv(size)
    create_transaction_type_csv(size)
    create_category_csv(size)
    recalculate_all_indexes()
    create_transaction_csv(size)
    recalculate_all_indexes()


def __main():
    full_pipeline(100)


if __name__ == "__main__":
    __main()
