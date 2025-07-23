# main.py
import streamlit as st
from auth import login, logout
from dashboard import dashboard
from sales_register import sales_register
from stock_register import stock_register
from finance import finance
from debt_management import debt_management
from expenses import expenses
from manage_users import manage_users
from combo_management import combo_management
from database import init_db, init_super_admin

def main():
    # Custom CSS and Header/Footer
    st.markdown("""
        <style>
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stHeader {
                font-size: 2em;
                font-weight: bold;
                color: #4CAF50;
            }
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #f1f1f1;
                color: black;
                text-align: center;
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>M/S MKH Enterprise</h1>", unsafe_allow_html=True)

    # Initialize the database
    init_db()
    init_super_admin()

    # Login and Navigation
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if not st.session_state["logged_in"]:
        login()
    else:
        logout()
        if st.session_state["role"] == "Super Admin":
            menu = ["Dashboard", "Sales Register", "Stock Register", "Finance", "Debt Management", "Expenses", "Manage Users", "Combo Management"]
        elif st.session_state["role"] == "Admin":
            menu = ["Dashboard", "Sales Register", "Stock Register", "Finance", "Debt Management", "Expenses"]
        else:
            menu = ["Sales Register", "Stock Register", "Debt Management"]

        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Dashboard":
            dashboard()
        elif choice == "Sales Register":
            sales_register()
        elif choice == "Stock Register":
            stock_register()
        elif choice == "Finance":
            finance()
        elif choice == "Debt Management":
            debt_management()
        elif choice == "Expenses":
            expenses()
        elif choice == "Manage Users":
            manage_users()
        elif choice == "Combo Management":
            combo_management()

    # Footer
    st.markdown("<div class='footer'>This grocery management software is developed by MenaceAI.ez (Mahin Hossain Munna)</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()