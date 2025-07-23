import streamlit as st
import sqlite3
import pandas as pd
import datetime
from database import get_db_connection

def debt_management():
    st.title("💳 Debt Management")

    conn = get_db_connection()
    c = conn.cursor()

    # Add New Debt
    with st.form("add_debt_form"):
        st.subheader("Add New Debt")
        customer_name = st.text_input("Customer Name")
        phone_number = st.text_input("Phone Number")
        amount = st.number_input("Amount", min_value=0.0)
        if st.form_submit_button("Add Debt"):
            c.execute("INSERT INTO debts (customer_name, phone_number, amount, date) VALUES (?, ?, ?, ?)",
                      (customer_name, phone_number, amount, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success("Debt added successfully!")

    # View Debts
    st.subheader("Debts List")
    c.execute("SELECT * FROM debts")
    debts = c.fetchall()
    if debts:
        st.write(pd.DataFrame(debts, columns=["ID", "Customer Name", "Phone Number", "Amount", "Date"]))
    else:
        st.info("No debts found.")

    conn.close()