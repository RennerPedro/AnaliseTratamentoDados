import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados dos arquivos CSV
combined_df = pd.read_csv('combined_df.csv')
first_purchase = pd.read_csv('first_purchase.csv')
last_purchase = pd.read_csv('last_purchase.csv')
purchase_count = pd.read_csv('purchase_count.csv')

# Visualizar os dados de combined_df
print("Visualizando dados de combined_df:")
print(combined_df)
print()

# Visualizar os dados de first_purchase
print("Visualizando dados de first_purchase:")
print(first_purchase)
print()

# Visualizar os dados de last_purchase
print("Visualizando dados de last_purchase:")
print(last_purchase)
print()

# Visualizar os dados de purchase_count
print("Visualizando dados de purchase_count:")
print(purchase_count)
print()

# Plotar gráfico para combined_df
plt.figure(figsize=(10, 6))
plt.plot(combined_df['customer_id'], combined_df['first_order_date'], label='First Purchase')
plt.plot(combined_df['customer_id'], combined_df['last_order_date'], label='Last Purchase')
plt.xlabel('Customer ID')
plt.ylabel('Order Date')
plt.title('First and Last Purchase Dates by Customer')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Plotar gráfico para first_purchase
plt.figure(figsize=(10, 6))
plt.plot(first_purchase['customer_id'], first_purchase['first_order_date'], label='First Purchase')
plt.xlabel('Customer ID')
plt.ylabel('Order Date')
plt.title('First Purchase Date by Customer')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Plotar gráfico para last_purchase
plt.figure(figsize=(10, 6))
plt.plot(last_purchase['customer_id'], last_purchase['last_order_date'], label='Last Purchase')
plt.xlabel('Customer ID')
plt.ylabel('Order Date')
plt.title('Last Purchase Date by Customer')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Plotar gráfico para purchase_count
plt.figure(figsize=(10, 6))
plt.bar(purchase_count['employee_name'], purchase_count['first/last_ratio'])
plt.xlabel('Employee Name')
plt.ylabel('First/Last Purchase Ratio')
plt.title('First/Last Purchase Ratio by Employee')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
