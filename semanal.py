import pandas as pd

# Carregar os dados dos arquivos CSV
orders_df = pd.read_csv('planilhas/orders.csv')
order_details_df = pd.read_csv('planilhas/order_details.csv')

# Converter coluna 'ano_mes' para datetime
order_details_df['ano_mes'] = pd.to_datetime(order_details_df['ano_mes'])

# Combinar os dados de pedidos com os detalhes dos pedidos
merged_df = pd.merge(orders_df, order_details_df, on='order_id')

# Extrair o mês e o ano para cada linha
merged_df['ano_mes'] = pd.to_datetime(merged_df['ano_mes'])
merged_df['ano'] = merged_df['ano_mes'].dt.year
merged_df['mes'] = merged_df['ano_mes'].dt.month

# Definir a data de início de cada semana como o primeiro dia do mês
merged_df['week_start'] = merged_df['ano_mes'] - pd.to_timedelta(merged_df['ano_mes'].dt.day - 1, unit='D')

# Calcular o número da semana dentro do mês (1 a 4)
merged_df['week_of_month'] = ((merged_df['ano_mes'].dt.day - 1) // 7) + 1

# Agrupar por ano, mês e semana do mês e calcular as maiores vendas por semana
weekly_sales = merged_df.groupby(['ano', 'mes', 'week_of_month']).agg({'total_sale': 'sum'}).reset_index()

# Renomear as colunas
weekly_sales.rename(columns={'ano': 'ano', 'mes': 'mes', 'week_of_month': 'semana_do_mes'}, inplace=True)

# Salvar os resultados das maiores vendas por semana em um arquivo CSV
output_csv = 'maiores_vendas_por_semana.csv'
weekly_sales.to_csv(output_csv, index=False)

print(f"Os resultados foram salvos em '{output_csv}'.")
