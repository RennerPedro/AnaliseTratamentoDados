import pandas as pd

def clean_csv(file_path):
    cleaned_file_path = 'cleaned_' + file_path
    
    with open(file_path, 'r', encoding='utf-8') as infile, open(cleaned_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned_line = line.replace('"', '').replace(',', '.')
            outfile.write(cleaned_line)
    
    return cleaned_file_path

def read_csv_safely(file_path):
    cleaned_file_path = clean_csv(file_path)
    return pd.read_csv(cleaned_file_path, delimiter=',')

try:
    orders = read_csv_safely('orders.csv')
    order_details = read_csv_safely('order_details.csv')
    
    print("CSV files loaded successfully.")
except Exception as e:
    print("Failed to load one or both of the CSV files.")
    print(e)
