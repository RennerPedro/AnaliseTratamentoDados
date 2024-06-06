import pandas as pd

# Carregar os dados das tabelas orders e employees, especificando o delimitador correto
orders_df = pd.read_csv('orders.csv', delimiter=',')
employees_df = pd.read_csv('employees.csv', delimiter=';')

# Preencher os valores ausentes na coluna 'employee_id' com -1
employees_df['employee_id'].fillna(-1, inplace=True)

# Juntar as tabelas orders e employees usando a coluna employee_id como chave
merged_df = pd.merge(orders_df, employees_df, how='inner', left_on='employee_id', right_on='employee_id')

# Converter a coluna order_date para o tipo datetime
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])

# Extrair o mês da coluna order_date e criar uma nova coluna chamada 'order_month'
merged_df['order_month'] = merged_df['order_date'].dt.to_period('M')

# Calcular o churn mensal de cada employee
churn_per_employee_month = merged_df.groupby(['employee_id', 'order_month']).size().reset_index(name='NumOrders')

# Exportar os resultados para um novo CSV
churn_per_employee_month.to_csv('churn.csv', index=False)

# Visualizar o churn mensal de cada employee
print(churn_per_employee_month)
