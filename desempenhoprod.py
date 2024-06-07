import pandas as pd
import plotly.express as px

def load_data():
    orders_df = pd.read_csv('orders.csv')
    order_details_df = pd.read_csv('order_details.csv')
    products_df = pd.read_csv('products.csv', sep=';')
    categories_df = pd.read_csv('categories.csv', sep=';')
    
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
    
    return orders_df, order_details_df, products_df, categories_df

def process_data(orders_df, order_details_df, products_df, categories_df):
    orders_details_merged = pd.merge(order_details_df, orders_df, on='order_id')
    orders_details_merged = pd.merge(orders_details_merged, products_df, on='product_id')
    orders_details_merged = pd.merge(orders_details_merged, categories_df, on='category_id')

    orders_details_merged['year_month'] = orders_details_merged['order_date'].dt.to_period('M').astype(str)

    sales_per_category_month = orders_details_merged.groupby(['category_name', 'year_month']).agg({'quantity': 'sum'}).reset_index()
    sales_per_category_month = sales_per_category_month.sort_values(by=['category_name', 'year_month'])
    
    return sales_per_category_month

def visualize_sales_by_category(sales_per_category_month):
    fig = px.line(
        sales_per_category_month, 
        x='year_month', 
        y='quantity', 
        color='category_name', 
        title='Sales Performance Over Time by Category',
        labels={'year_month': 'Year-Month', 'quantity': 'Quantity Sold', 'category_name': 'Category'},
    )

    fig.update_layout(
        xaxis_title='Year-Month',
        yaxis_title='Quantity Sold',
        legend_title='Category',
        template='plotly_white',
        hovermode='x unified',
        xaxis=dict(
            tickmode='array',
            tickvals=sales_per_category_month['year_month'].unique(),  # Ensure all unique year-month values are shown
            tickangle=-45,  # Rotate the x-axis labels to prevent overlap
        ),
        margin=dict(l=40, r=40, t=40, b=80),  # Adjust margins for better spacing
        plot_bgcolor='rgba(0,0,0,0)',  # Make the plot background transparent
    )

    fig.update_traces(
        mode='lines+markers',  # Add markers to the lines for better visibility
        marker=dict(size=6)    # Size of the markers
    )

    fig.show()

def main():
    orders_df, order_details_df, products_df, categories_df = load_data()
    sales_per_category_month = process_data(orders_df, order_details_df, products_df, categories_df)
    
    print("Sales Performance by Category Over Time:")
    print(sales_per_category_month)
    
    visualize_sales_by_category(sales_per_category_month)

if __name__ == "__main__":
    main()
