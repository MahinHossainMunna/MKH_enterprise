import streamlit as st
import sqlite3
import pandas as pd
from database import get_db_connection

def expenses():
    st.title("💸 Expenses")

    conn = get_db_connection()
    c = conn.cursor()

    # Add New Expense
    with st.form("add_expense_form"):
        st.subheader("Add New Expense")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0)
        category = st.text_input("Category")
        if st.form_submit_button("Add Expense"):
            c.execute("INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
                      (description, amount, category, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success("Expense added successfully!")

    # View Expenses
    st.subheader("Expenses List")
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    if expenses:
        st.write(pd.DataFrame(expenses, columns=["ID", "Description", "Amount", "Category", "Date"]))
    else:
        st.info("No expenses found.")

    conn.close()