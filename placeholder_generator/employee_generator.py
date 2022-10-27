import random

import pandas as pd

from placeholder_generator.core_generator import generate_random_integer, generate_random_first_name, \
    generate_random_last_name, generate_random_birthdate, generate_random_email, generate_random_telephone, \
    generate_random_project_name, generate_two_random_dates


def generate_random_employee_entry():
    """Create a random entry"""
    ssn = generate_random_integer(1, 100000)
    first_name = generate_random_first_name()
    last_name = generate_random_last_name()
    birthdate = generate_random_birthdate()
    email = generate_random_email(first_name, last_name)
    telephone = generate_random_telephone()
    return f"{ssn}, {first_name},{last_name},{birthdate},{email},{telephone}"


def generate_random_project_entry():
    """Create a random project entry"""
    p_number = generate_random_integer(100, 100000)
    p_name = generate_random_project_name(10)
    p_start, p_end = generate_two_random_dates()
    p_description = generate_random_project_name(100)
    return f"{p_number},{p_name},{p_start},{p_end},{p_description}"


def generate_random_works_on_entry(employee_df: pd.DataFrame, project_df: pd.DataFrame):
    """Create a random auxiliary table"""
    random_user = random.choice(employee_df["SSN"])
    random_project = random.choice(project_df["PNUMBER"])
    return f"{random_user},{random_project}"


def generate_employee_table_csv(size: int = 10000):
    """Create a csv with random employee entries"""
    with open("outputs/employee.csv", "w") as file:
        file.write("SSN,FNAME,LNAME,BIRTHDATE,EMAIL,TELEPHONE\n")
        for _ in range(size):
            file.write(f"{generate_random_employee_entry()}\n")


def generate_project_table_csv(size: int = 10000):
    """Create a csv with random project entries"""
    with open("outputs/project.csv", "w") as file:
        file.write("PNUMBER,PNAME,DSTART,DEND,PDESCRIPTION\n")
        for _ in range(size):
            file.write(f"{generate_random_project_entry()}\n")


def generate_works_on_csv(size: int = 100000):
    """Create a csv with random auxiliary table entries"""
    refreshed_employee_df = pd.read_csv("outputs/employee.csv")
    refreshed_project_df = pd.read_csv("outputs/project.csv")
    with open("outputs/works_on.csv", "w") as file:
        file.write("ESSN,PNO\n")
        for _ in range(size):
            file.write(f"{generate_random_works_on_entry(refreshed_employee_df, refreshed_project_df)}\n")


def generate_unique_indexes():
    employee_df = pd.read_csv("outputs/employee.csv")
    project_df = pd.read_csv("outputs/project.csv")
    size = len(employee_df)
    employee_first_index = generate_random_integer(150000, 700000)
    project_df_first_index = generate_random_integer(150, 20000)
    employee_range = list(range(employee_first_index, employee_first_index + size))
    project_df_range = list(range(project_df_first_index, project_df_first_index + size))
    employee_df["SSN"] = employee_range
    project_df["PNUMBER"] = project_df_range
    employee_df.to_csv("outputs/employee.csv", index=False)
    project_df.to_csv("outputs/project.csv", index=False)


def __full_pipeline(size: int = 10000):
    generate_employee_table_csv(size)
    generate_project_table_csv(size)
    generate_unique_indexes()
    generate_works_on_csv(size*6)


def __main():
    __full_pipeline(10)
