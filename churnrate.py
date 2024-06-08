import pandas as pd
import plotly.express as px

# Carregar os dados dos clientes, suas compras e informações sobre a primeira e última compra
clientes_df = pd.read_csv('planilhas/customers.csv', delimiter=';')
compras_df = pd.read_csv('planilhas/orders.csv')
first_purchase_df = pd.read_csv('planilhas/first_purchase.csv')
last_purchase_df = pd.read_csv('planilhas/last_purchase.csv')

# Converter colunas de datas para o formato datetime
compras_df['order_date'] = pd.to_datetime(compras_df['order_date'])
first_purchase_df['first_order_date'] = pd.to_datetime(first_purchase_df['first_order_date'])
last_purchase_df['last_order_date'] = pd.to_datetime(last_purchase_df['last_order_date'])

# Filtrar clientes que não realizaram compras desde o último dia de dezembro de 1997
clientes_sem_compra_desde_dezembro_1997 = clientes_df[clientes_df['customer_id'].isin(
    last_purchase_df[last_purchase_df['last_order_date'] <= '1997-12-31']['customer_id'])]

# Filtrar clientes que fizeram sua primeira compra a partir de primeiro de janeiro de 1998
clientes_primeira_compra_janeiro_1998 = clientes_df[clientes_df['customer_id'].isin(
    first_purchase_df[first_purchase_df['first_order_date'] >= '1998-01-01']['customer_id'])]

# Remover os clientes que estão presentes em ambas as tabelas 1 e 2
clientes_sem_compra_desde_dezembro_1997 = clientes_sem_compra_desde_dezembro_1997[
    ~clientes_sem_compra_desde_dezembro_1997['customer_id'].isin(clientes_primeira_compra_janeiro_1998['customer_id'])]

# Criar uma tabela com todos os clientes que não estão em nenhuma das duas listas
clientes_nao_em_lista = clientes_df[
    ~clientes_df['customer_id'].isin(clientes_sem_compra_desde_dezembro_1997['customer_id']) & 
    ~clientes_df['customer_id'].isin(clientes_primeira_compra_janeiro_1998['customer_id'])]

# Print das tabelas
print("Tabela 1: Clientes que não fazem compras desde o último dia de dezembro de 1997")
print(clientes_sem_compra_desde_dezembro_1997[['customer_id', 'company_name']])
print("\nTabela 2: Clientes que fizeram sua primeira compra a partir de primeiro de janeiro de 1998")
print(clientes_primeira_compra_janeiro_1998[['customer_id', 'company_name']])
print("\nTabela 3: Clientes que não estão em nenhuma das duas listas")
print(clientes_nao_em_lista[['customer_id', 'company_name']])

# Contar o número de clientes em cada categoria
num_clientes_sem_compra_desde_dezembro_1997 = len(clientes_sem_compra_desde_dezembro_1997)
num_clientes_primeira_compra_janeiro_1998 = len(clientes_primeira_compra_janeiro_1998)
num_clientes_nao_em_lista = len(clientes_nao_em_lista)

# Dados para o gráfico
data = {
    'Categoria': ['Saída de clientes', 'Novos clientes', 'Clientes retidos'],
    'Número de Clientes': [num_clientes_sem_compra_desde_dezembro_1997, 
                           num_clientes_primeira_compra_janeiro_1998, 
                           num_clientes_nao_em_lista]
}

df = pd.DataFrame(data)

# Criar o gráfico de pizza interativo
fig = px.pie(df, values='Número de Clientes', names='Categoria', 
             title='Churn Rate partindo de 01/1998', color_discrete_sequence=px.colors.qualitative.Set3,
             hover_data=['Número de Clientes'], labels={'Número de Clientes':'Clientes'})

# Atualizações adicionais para tornar o gráfico mais bonito
fig.update_traces(textposition='inside', textinfo='percent+label', 
                  marker=dict(line=dict(color='#000000', width=2)))

fig.update_layout(
    title_font_size=24,
    title_font_family='Arial',
    title_font_color='Black',
    legend_title='Categorias',
    legend_title_font_color='green',
    legend_title_font_size=16,
    legend=dict(
        x=0.8,
        y=0.9,
        traceorder='normal',
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        bgcolor='LightSteelBlue',
        bordercolor='Black',
        borderwidth=2
    )
)

fig.show()

# Exportar dados para CSV
#clientes_sem_compra_desde_dezembro_1997.to_csv('planilhas/clientes_sem_compra_desde_dezembro_1997.csv', index=False)
#clientes_primeira_compra_janeiro_1998.to_csv('planilhas/clientes_primeira_compra_janeiro_1998.csv', index=False)
#clientes_nao_em_lista.to_csv('planilhas/clientes_nao_em_lista.csv', index=False)
