from pathlib import Path

ref = Path(__file__).parent.parent


def get_table_path():
    return Path(ref, "placeholder_generator", "outputs")


def __main():
    print(get_table_path())


if __name__ == "__main__":
    __main()
