import streamlit as st
import sqlite3
import pandas as pd
from database import get_db_connection

def manage_users():
    st.title("👥 Manage Users")

    if st.session_state["role"] != "Super Admin":
        st.error("You do not have permission to access this section.")
        return

    conn = get_db_connection()
    c = conn.cursor()

    # Add New User
    with st.form("add_user_form"):
        st.subheader("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "Cashier"])
        if st.form_submit_button("Add User"):
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            st.success(f"User {username} added as {role}")

    # View Users
    st.subheader("Users List")
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    if users:
        st.write(pd.DataFrame(users, columns=["ID", "Username", "Password", "Role"]))
    else:
        st.info("No users found.")

    conn.close()