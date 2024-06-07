import pandas as pd

# Função para ler CSV e mostrar mensagens de erro detalhadas
def read_csv_safely(file_path, delimiter, expected_columns):
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
        # Verifica se o número de colunas é igual ao esperado
        if df.shape[1] == expected_columns:
            return df
        else:
            print(f"Expected {expected_columns} columns, but found {df.shape[1]} columns in {file_path}.")
            return None
    except pd.errors.EmptyDataError:
        print(f"No columns to parse from file {file_path}.")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing file {file_path}: {e}")
        return None

# Número esperado de colunas
expected_columns_orders = 15  # Incluindo a nova coluna order_month
expected_columns_order_details = 10  # Ajustado para o número correto de colunas em order_details.csv

# Tentativas de delimitadores comuns
delimiters = [',', ';', '\t']

# Carregar os arquivos CSV com linhas limpas
orders = None
order_details = None

for delimiter in delimiters:
    if orders is None:
        orders = read_csv_safely('orders.csv', delimiter, expected_columns_orders)
    if order_details is None:
        order_details = read_csv_safely('order_details.csv', delimiter, expected_columns_order_details)

# Verificar se ambos os DataFrames foram carregados corretamente
if orders is not None and order_details is not None:
    # Unir os dataframes orders e order_details
    merged_data = pd.merge(orders, order_details, on='order_id')

    # Convertendo colunas que devem ser números para o tipo correto
    merged_data['unit_price'] = merged_data['unit_price'].str.replace(',', '.').astype(float)
    merged_data['discount'] = merged_data['discount'].str.replace(',', '.').astype(float)
    merged_data['total_sale'] = merged_data['unit_price'] * merged_data['quantity'] * (1 - merged_data['discount'])

    # Converter order_date para datetime
    merged_data['order_date'] = pd.to_datetime(merged_data['order_date'], errors='coerce')

    # Filtrar linhas com datas inválidas
    merged_data = merged_data.dropna(subset=['order_date'])

    # Extrair ano e mês
    merged_data['year_month'] = merged_data['order_date'].dt.to_period('M')

    # Calcular a soma mensal das vendas
    monthly_sales = merged_data.groupby('year_month')['total_sale'].sum().reset_index()

    # Contar o número de pedidos por mês
    monthly_orders = merged_data.groupby('year_month')['order_id'].nunique().reset_index()

    # Unir os dois dataframes
    monthly_data = pd.merge(monthly_sales, monthly_orders, on='year_month')

    # Renomear colunas para clareza
    monthly_data.columns = ['year_month', 'total_sales', 'num_orders']

    # Calcular o ticket médio
    monthly_data['average_ticket'] = monthly_data['total_sales'] / monthly_data['num_orders']

    # Exportar os resultados para um novo CSV
    #monthly_data.to_csv('monthly_average_ticket.csv', index=False)

    print(monthly_data)
else:
    print("Failed to load one or both of the CSV files.")
