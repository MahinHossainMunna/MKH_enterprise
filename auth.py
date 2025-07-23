import streamlit as st
import sqlite3
import pandas as pd
from database import get_db_connection

def login():
    st.sidebar.title("Login")
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()
            if user:
                st.session_state["logged_in"] = True
                st.session_state["role"] = user[3]
                st.session_state["username"] = user[1]
                st.sidebar.success(f"Logged in as {user[3]}")
                st.session_state["force_rerun"] = True  # Force a rerun
            else:
                st.sidebar.error("Invalid credentials")
            conn.close()

def logout():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
        st.session_state["username"] = None
        st.sidebar.success("Logged out successfully")
        st.session_state["force_rerun"] = True  # Force a rerun
        
def manage_users():
    st.title("Manage Users")
    if st.session_state["role"] not in ["Super Admin", "Admin"]:
        st.error("You do not have permission to access this section.")
        return
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Add New User
    with st.form("Add User"):
        st.subheader("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "Cashier"])
        if st.form_submit_button("Add User"):
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            st.success(f"User {username} added successfully!")
    
    # View and Delete Users
    st.subheader("User List")
    c.execute("SELECT id, username, role FROM users")
    users = c.fetchall()
    if users:
        user_df = pd.DataFrame(users, columns=["ID", "Username", "Role"])
        st.write(user_df)
        
        # Delete User (Only Super Admin can delete users)
        if st.session_state["role"] == "Super Admin":
            delete_user_id = st.number_input("Enter User ID to Delete", min_value=1)
            if st.button("Delete User"):
                c.execute("DELETE FROM users WHERE id = ?", (delete_user_id,))
                conn.commit()
                st.success(f"User with ID {delete_user_id} deleted successfully!")
        else:
            st.info("Only Super Admin can delete users.")
    else:
        st.info("No users found.")
    conn.close()