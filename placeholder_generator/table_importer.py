import pandas as pd

random_table = pd.read_csv("random_table.csv")
mail_suffix = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com", "mail.com", "msn.com", "live.com"]
employee_table = pd.read_csv("outputs/employee.csv")
project_table = pd.read_csv("outputs/project.csv")
print(random_table)