import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from database import get_db_connection

def dashboard():
    st.title("📊 Dashboard")

    # Fetch data from the database
    conn = get_db_connection()
    c = conn.cursor()

    # Expenses Pie Chart
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    expenses_data = c.fetchall()
    if expenses_data:
        expenses_df = pd.DataFrame(expenses_data, columns=["Category", "Amount"])
        fig_expenses = px.pie(expenses_df, values="Amount", names="Category", title="Expenses by Category")
        st.plotly_chart(fig_expenses, use_container_width=True)
    else:
        st.warning("No expenses data found.")

    # Stock Pie Chart
    c.execute("SELECT category, SUM(stock) FROM products GROUP BY category")
    stock_data = c.fetchall()
    if stock_data:
        stock_df = pd.DataFrame(stock_data, columns=["Category", "Stock"])
        fig_stock = px.pie(stock_df, values="Stock", names="Category", title="Stock by Category")
        st.plotly_chart(fig_stock, use_container_width=True)
    else:
        st.warning("No stock data found.")

    # Sales Pie Chart
    c.execute("SELECT p.category, SUM(s.quantity) FROM sales s JOIN products p ON s.product_id = p.id GROUP BY p.category")
    sales_data = c.fetchall()
    if sales_data:
        sales_df = pd.DataFrame(sales_data, columns=["Category", "Quantity"])
        fig_sales = px.pie(sales_df, values="Quantity", names="Category", title="Sales by Category")
        st.plotly_chart(fig_sales, use_container_width=True)
    else:
        st.warning("No sales data found.")

    conn.close()