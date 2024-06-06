import pandas as pd

# Carregar o arquivo CSV
employees_df = pd.read_csv('employees.csv')

# Preencher os valores NaN na coluna 'reports_to' com -1
employees_df['reports_to'] = employees_df['reports_to'].fillna(-1)

# Mostrar o DataFrame resultante
print(employees_df)
