import random

from placeholder_generator.table_importer import random_table, mail_suffix


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


if __name__ == "__main__":
    __main()
