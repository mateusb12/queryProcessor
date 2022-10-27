from pathlib import Path

ref = Path(__file__).parent.parent


def get_table_path():
    return Path(ref, "placeholder_generator", "main_table")


def __main():
    print(get_table_path())


if __name__ == "__main__":
    __main()
