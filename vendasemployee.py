import pandas as pd
import plotly.express as px

# Carregar os dados dos arquivos CSV
orders_df = pd.read_csv('planilhas/orders.csv')
employees_df = pd.read_csv('planilhas/employees.csv', sep=';')
customers_df = pd.read_csv('planilhas/customers.csv', sep=';')
order_details_df = pd.read_csv('planilhas/order_details.csv')

# Converter colunas de data para datetime
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])

# Combinar os dados de pedidos com os dados de funcionários
orders_employees_df = pd.merge(orders_df, employees_df, how='left', left_on='employee_id', right_on='employee_id')

# Identificar a primeira e última compra de cada cliente
first_purchase = orders_employees_df.sort_values('order_date').groupby('customer_id').first().reset_index()
last_purchase = orders_employees_df.sort_values('order_date').groupby('customer_id').last().reset_index()

# Renomear colunas para claridade
first_purchase = first_purchase[['customer_id', 'order_date', 'employee_id', 'first_name']]
first_purchase.columns = ['customer_id', 'first_order_date', 'first_employee_id', 'first_employee_first_name']

last_purchase = last_purchase[['customer_id', 'order_date', 'employee_id', 'first_name']]
last_purchase.columns = ['customer_id', 'last_order_date', 'last_employee_id', 'last_employee_first_name']

# Combinar os dados de primeira e última compra
combined_df = pd.merge(first_purchase, last_purchase, on='customer_id')

# Calcular a soma das primeiras compras por vendedor
first_purchase_count = combined_df['first_employee_id'].value_counts().reset_index()
first_purchase_count.columns = ['employee_id', 'first_purchase_count']

# Combinar com os nomes dos funcionários para primeira compra
first_purchase_count = pd.merge(first_purchase_count, employees_df[['employee_id', 'first_name']], on='employee_id', how='left')

# Calcular a soma das últimas compras por vendedor
last_purchase_count = combined_df['last_employee_id'].value_counts().reset_index()
last_purchase_count.columns = ['employee_id', 'last_purchase_count']

# Combinar com os nomes dos funcionários para última compra
last_purchase_count = pd.merge(last_purchase_count, employees_df[['employee_id', 'first_name']], on='employee_id', how='left')

# Exibir o resultado combinado das primeiras e últimas compras
print(combined_df)

# Exibir a soma das primeiras compras por vendedor
print("First Purchase Count by Employee:")
print(first_purchase_count)

# Exibir a soma das últimas compras por vendedor
print("Last Purchase Count by Employee:")
print(last_purchase_count)

# Combinar as contagens de primeiras e últimas compras em uma única tabela
purchase_count = pd.merge(first_purchase_count, last_purchase_count, on='employee_id', how='outer').fillna(0)

# Calcular a porcentagem de primeiras/últimas compras por vendedor
purchase_count['first/last_ratio'] = purchase_count['first_purchase_count'] / purchase_count['last_purchase_count']

# Manter apenas uma coluna de nome de funcionário
purchase_count = purchase_count[['employee_id', 'first_name_x', 'first_purchase_count', 'last_purchase_count', 'first/last_ratio']]
purchase_count.columns = ['employee_id', 'employee_name', 'first_purchase_count', 'last_purchase_count', 'first/last_ratio']

# Ordenar pela razão de primeiras/últimas compras em ordem decrescente
purchase_count = purchase_count.sort_values(by='first/last_ratio', ascending=False)

# Exibir a tabela com a porcentagem de primeiras/últimas compras por vendedor
print("First/Last Purchase Ratio by Employee:")
print(purchase_count)

# Função para calcular o número total de vendas de cada funcionário
def calcular_total_vendas(order_details_df, orders_df, employees_df):
    # Contar o número total de pedidos por funcionário
    total_vendas_por_funcionario = orders_df['employee_id'].value_counts().reset_index()
    total_vendas_por_funcionario.columns = ['employee_id', 'total_sales']
    
    # Combinar com os nomes dos funcionários
    total_vendas_por_funcionario = pd.merge(total_vendas_por_funcionario, employees_df[['employee_id', 'first_name']], on='employee_id')
    
    return total_vendas_por_funcionario

# Calcular o número total de vendas por funcionário
total_vendas_por_funcionario = calcular_total_vendas(order_details_df, orders_df, employees_df)

# Exibir o número total de vendas por funcionário
print("Número Total de Vendas por Funcionário:")
print(total_vendas_por_funcionario)

total_vendas_por_funcionario.to_csv('planilhas/vendasfuncionario.csv', index=False)


# Criar um gráfico de barras do número total de vendas por funcionário
fig = px.bar(total_vendas_por_funcionario, x='first_name', y='total_sales',
             title='Número Total de Vendas por Funcionário', labels={'first_name': 'Funcionário', 'total_sales': 'Total de Vendas'},
             color='total_sales', color_continuous_scale=px.colors.sequential.Plasma)

# Atualizações adicionais para tornar o gráfico mais bonito
fig.update_layout(
    title_font_size=24,
    title_font_family='Arial',
    title_font_color='Black',
    xaxis_title='Funcionário',
    yaxis_title='Total de Vendas',
    coloraxis_colorbar_title='Total de Vendas',
    coloraxis_colorbar_thickness=20,
    coloraxis_colorbar_tickfont=dict(size=12),
    coloraxis_colorbar_title_font=dict(size=16)
)

fig.show()
