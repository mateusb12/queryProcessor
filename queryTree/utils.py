import re


def analyze_adequate_regex(input_sql: str):
    no_join = "JOIN" not in input_sql
    single_join = input_sql.count("JOIN") == 1
    multiple_join = input_sql.count("JOIN") > 1
    current_regex_str = ""
    if single_join:
        current_regex_str = "(SELECT )(.*)( FROM )(.*)( JOIN )(.*)( ON )(.*)( WHERE )(.*)"
    elif multiple_join:
        join_amount = input_sql.count("JOIN")
        current_regex_str = r"(SELECT )(.*)( FROM )(.*)"
        for _ in range(join_amount):
            current_regex_str += r"( JOIN )(.*)( ON )(.*)"
        current_regex_str += r"( WHERE )(.*)"
    elif no_join:
        current_regex_str = "(SELECT )(.*)( FROM )(.*)( WHERE )(.*)"
    return current_regex_str


def break_down_sql_line(input_sql: str):
    adequate_regex = analyze_adequate_regex(input_sql)
    regex = re.compile(adequate_regex)
    groups = list(regex.match(input_sql).groups())
    new_str_pot = ["".join(groups[i:i + 2]) for i in range(0, len(groups), 2)]
    return "\n".join(new_str_pot)


def __main():
    sql_with_single_join = "SELECT * FROM table1 JOIN table2 ON table1.col3 = table2.col3 " \
                           "WHERE table2.col4 = 3 AND table2.col5 = 4"
    sql_with_double_join = "SELECT * FROM table1 JOIN table2 ON table1.col3 = table2.col3 " \
                           "JOIN table3 ON table2.col4 = table3.col4 WHERE table3.col5 = 3 AND table3.col6 = 4"
    sql_without_join = "SELECT * FROM table1 WHERE table1.col4 = 3 AND table1.col5 = 4"
    aux1 = break_down_sql_line(sql_with_single_join)
    aux2 = break_down_sql_line(sql_with_double_join)
    aux3 = break_down_sql_line(sql_without_join)
    return


if __name__ == '__main__':
    __main()
