import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados dos arquivos CSV
first_purchase = pd.read_csv('planilhas/first_purchase.csv')
last_purchase = pd.read_csv('planilhas/last_purchase.csv')

# Plotar gráfico de barras para as datas de primeira compra
plt.figure(figsize=(10, 6))
plt.bar(first_purchase['customer_id'], first_purchase['first_order_date'], color='blue')
plt.xlabel('Customer ID')
plt.ylabel('Order Date')
plt.title('First Purchase Date by Customer')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotar gráfico de barras para as datas de última compra
plt.figure(figsize=(10, 6))
plt.bar(last_purchase['customer_id'], last_purchase['last_order_date'], color='green')
plt.xlabel('Customer ID')
plt.ylabel('Order Date')
plt.title('Last Purchase Date by Customer')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
