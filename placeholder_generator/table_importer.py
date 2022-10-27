import pandas as pd

random_table = pd.read_csv("random_table.csv")
random_street_table = pd.read_csv("random_streets.csv")
mail_suffix = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com", "mail.com", "msn.com", "live.com"]
employee_table = pd.read_csv("outputs/employee.csv")
project_table = pd.read_csv("outputs/project.csv")
account_type_table = pd.read_csv("outputs/account_type.csv")
user_table = pd.read_csv("outputs/user.csv")
print(random_table)