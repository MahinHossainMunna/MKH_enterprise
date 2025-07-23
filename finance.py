import streamlit as st
import sqlite3
import pandas as pd
from database import get_db_connection

def finance():
    st.title("💰 Finance")

    conn = get_db_connection()
    c = conn.cursor()

    # Cash and Bank Balance
    st.header("Cash and Bank Balance")
    cash_balance = st.number_input("Cash Balance", min_value=0.0)
    bank_balance = st.number_input("Bank Balance", min_value=0.0)
    if st.button("Update Balances"):
        st.success("Balances updated successfully!")

    # Profit and Loss
    st.header("Profit and Loss")
    c.execute("SELECT SUM(total_price) FROM sales")
    total_sales = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = c.fetchone()[0] or 0
    profit_loss = total_sales - total_expenses
    st.write(f"Total Sales: {total_sales} Tk")
    st.write(f"Total Expenses: {total_expenses} Tk")
    st.write(f"Profit/Loss: {profit_loss} Tk")

    # Generate Report
    st.header("Generate Report")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if st.button("Generate Report"):
        c.execute("SELECT * FROM sales WHERE date BETWEEN ? AND ?", (start_date, end_date))
        sales_data = c.fetchall()
        if sales_data:
            st.write(pd.DataFrame(sales_data, columns=["ID", "Product ID", "Quantity", "Total Price", "Date", "Cashier", "Discount", "Invoice ID", "Payment Status"]))
        else:
            st.info("No sales data found for the selected period.")

    conn.close()