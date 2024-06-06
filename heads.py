import pandas as pd

# Carregar o arquivo employees.csv em um DataFrame
employees_df = pd.read_csv('employees.csv')
orders_df = pd.read_csv('orders.csv')

# Visualizar as primeiras linhas do DataFrame
print(employees_df.head())
print(orders_df.head())

