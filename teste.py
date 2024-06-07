import pandas as pd

# Carregar os dados dos clientes, suas compras e informações sobre a primeira e última compra
clientes_df = pd.read_csv('planilhas/customers.csv', delimiter=';')
compras_df = pd.read_csv('planilhas/orders.csv')
first_purchase_df = pd.read_csv('planilhas/first_purchase.csv')
last_purchase_df = pd.read_csv('planilhas/last_purchase.csv')

# Converter colunas de datas para o formato datetime
compras_df['order_date'] = pd.to_datetime(compras_df['order_date'])
first_purchase_df['first_order_date'] = pd.to_datetime(first_purchase_df['first_order_date'])
last_purchase_df['last_order_date'] = pd.to_datetime(last_purchase_df['last_order_date'])

# Filtrar clientes que não realizaram compras desde o último dia de abril de 1997
clientes_sem_compra_desde_abril_1997 = clientes_df[~clientes_df['customer_id'].isin(compras_df[compras_df['order_date'] < '1997-05-01']['customer_id'])]

# Filtrar clientes que fizeram sua primeira compra a partir de primeiro de maio de 1997
clientes_primeira_compra_maio_1997 = clientes_df[clientes_df['customer_id'].isin(first_purchase_df[first_purchase_df['first_order_date'] >= '1997-05-01']['customer_id'])]

# Criar uma tabela com todos os clientes que não estão em nenhuma das duas listas
clientes_nao_em_lista = clientes_df[~clientes_df['customer_id'].isin(clientes_sem_compra_desde_abril_1997['customer_id']) & ~clientes_df['customer_id'].isin(clientes_primeira_compra_maio_1997['customer_id'])]

# Remover os clientes que estão presentes em ambas as tabelas 1 e 2
clientes_sem_compra_desde_abril_1997 = clientes_sem_compra_desde_abril_1997[~clientes_sem_compra_desde_abril_1997['customer_id'].isin(clientes_primeira_compra_maio_1997['customer_id'])]

# Print das tabelas
print("Tabela 1: Clientes que não fazem compras desde o último dia de abril de 1997")
print(clientes_sem_compra_desde_abril_1997[['customer_id', 'company_name']])
print("\nTabela 2: Clientes que fizeram sua primeira compra a partir de primeiro de maio de 1997")
print(clientes_primeira_compra_maio_1997[['customer_id', 'company_name']])
print("\nTabela 3: Clientes que não estão em nenhuma das duas listas")
print(clientes_nao_em_lista[['customer_id', 'company_name']])
