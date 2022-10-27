import random

from placeholder_generator.core_generator import generate_random_integer, generate_random_street_name, \
    generate_random_house_number, generate_random_birthdate


def generate_random_user_table():
    """Create a csv with random user entries"""
    ufs = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE",
           "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    user_id = generate_random_integer(1, 100000)
    address = generate_random_street_name()
    number = generate_random_integer(100000, 500000)
    district = generate_random_house_number()
    zip_code = f"{generate_random_integer(10000, 99999)}-{generate_random_integer(100, 999)}"
    uf = random.choice(ufs)
    birthdate = generate_random_birthdate()
    return f"{user_id},{address},{number},{district},{zip_code},{uf},{birthdate}"


def __main():
    aux = generate_random_user_table()
    return


if __name__ == "__main__":
    __main()
