import pandas as pd
import plotly.express as px

# Carregar os dados dos arquivos CSV
combined_df = pd.read_csv('planilhas/combined_df.csv')
purchase_count = pd.read_csv('planilhas/purchase_count.csv')

# Converter as colunas de data para datetime
combined_df['first_order_date'] = pd.to_datetime(combined_df['first_order_date'])
combined_df['last_order_date'] = pd.to_datetime(combined_df['last_order_date'])

# Extrair o mês de cada data
combined_df['first_order_month'] = combined_df['first_order_date'].dt.to_period('M').dt.to_timestamp()
combined_df['last_order_month'] = combined_df['last_order_date'].dt.to_period('M').dt.to_timestamp()

# Contagem de clientes por mês de primeira e última compra
first_order_counts = combined_df.groupby('first_order_month')['customer_id'].count().reset_index()
first_order_counts.columns = ['month', 'first_orders']

last_order_counts = combined_df.groupby('last_order_month')['customer_id'].count().reset_index()
last_order_counts.columns = ['month', 'last_orders']

# Combinar as contagens em um único DataFrame
order_counts = pd.merge(first_order_counts, last_order_counts, on='month', how='outer').fillna(0)

# Plotar gráfico de áreas empilhadas para combined_df com meses no eixo y
fig = px.area(order_counts, y='month', x=['first_orders', 'last_orders'],
              labels={'value': 'Number of Orders', 'month': 'Month', 'variable': 'Order Type'},
              title='First and Last Purchase Dates by Customer',
              template='plotly_dark',
              color_discrete_sequence=['#1f77b4', '#ff7f0e'],
              width=800, height=500)

fig.update_layout(
    font=dict(family="Arial, sans-serif", size=12, color="white"),
    title_font=dict(size=18),
    yaxis_title_font=dict(size=14),
    xaxis_title_font=dict(size=14),
    legend_title_font=dict(size=14),
    legend_font=dict(size=12),
    yaxis_tickangle=-45,
    margin=dict(l=80, r=80, t=80, b=80),
    plot_bgcolor='#23272c',
    paper_bgcolor='#23272c'
)

fig.show()

# Plotar gráfico para purchase_count
fig = px.bar(purchase_count, x='employee_name', y='first/last_ratio',
             labels={'first/last_ratio': 'First/Last Purchase Ratio'},
             title='First/Last Purchase Ratio by Employee',
             template='plotly_dark',
             color='employee_name',
             color_continuous_scale=px.colors.qualitative.Pastel,
             width=800, height=500)

fig.update_layout(
    font=dict(family="Arial, sans-serif", size=12, color="white"),
    title_font=dict(size=18),
    xaxis_title_font=dict(size=14),
    yaxis_title_font=dict(size=14),
    legend_title_font=dict(size=14),
    legend_font=dict(size=12),
    xaxis_tickangle=-45,
    margin=dict(l=80, r=80, t=80, b=80),
    plot_bgcolor='#23272c',
    paper_bgcolor='#23272c'
)

fig.show()
