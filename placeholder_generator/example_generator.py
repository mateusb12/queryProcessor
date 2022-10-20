import random

import pandas as pd

from table_generator.table_importer import random_table, mail_suffix, employee_table, project_table


def generate_random_integer(min_range: int, max_range: int):
    """Create a random integer"""
    return random.randint(min_range, max_range)


def generate_random_first_name():
    """Create a random first name"""
    return random.choice(random_table["First Name"])


def generate_random_last_name():
    """Create a random last name"""
    return random.choice(random_table["Last Name"])


def generate_random_project_name(size: int):
    """Create a string of random alphanumeric characters"""
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=size))


def generate_random_birthdate():
    """Create a random birthdate. The person should have between 18 and 45 years old"""
    day = generate_random_integer(1, 30)
    month = generate_random_integer(1, 12)
    random_day = day if day > 9 else f"0{day}"
    random_month = month if month > 9 else f"0{month}"
    random_year = generate_random_integer(1977, 2004)
    return f"{random_day}/{random_month}/{random_year}"


def generate_two_random_dates() -> tuple[str, str]:
    """Create two random dates. The second one should be bigger than the first one"""
    first_day = generate_random_integer(1, 30)
    second_day = generate_random_integer(1, 30)
    first_month = generate_random_integer(1, 12)
    second_month = generate_random_integer(1, 12)
    first_year = generate_random_integer(2000, 2020)
    second_year = generate_random_integer(first_year, 2020)
    formatted_first_day = first_day if first_day > 9 else f"0{first_day}"
    formatted_second_day = second_day if second_day > 9 else f"0{second_day}"
    formatted_first_month = first_month if first_month > 9 else f"0{first_month}"
    formatted_second_month = second_month if second_month > 9 else f"0{second_month}"
    return (
        f"{formatted_first_day}/{formatted_first_month}/{first_year}",
        f"{formatted_second_day}/{formatted_second_month}/{second_year}",
    )


def generate_random_email(first_name: str, last_name: str):
    """Create a random email"""
    random_suffix = random.choice(mail_suffix)
    random_tag = generate_random_integer(1, 100)
    return f"{first_name.lower()[0]}.{last_name.lower()}.{random_tag}@{random_suffix}"


def generate_random_telephone():
    city_code = generate_random_integer(10, 100)
    header = random.choice(["8", "9"])
    first_tag = generate_random_integer(1, 999)
    if first_tag > 100:
        first_tag = f"0{first_tag}"
    elif first_tag > 10:
        first_tag = f"00{first_tag}"
    second_tag = generate_random_integer(1, 9999)
    if second_tag < 1000:
        second_tag = f"0{second_tag}"
    elif second_tag < 100:
        second_tag = f"00{second_tag}"
    elif second_tag < 10:
        second_tag = f"000{second_tag}"
    return f"+55 ({city_code}) 9{header}{first_tag}-{second_tag}"


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


if __name__ == "__main__":
    __main()
