# combo_management.py
import streamlit as st
import sqlite3
import pandas as pd
from database import get_db_connection

def combo_management():
    st.title("📦 Combo Packages Management")

    conn = get_db_connection()
    c = conn.cursor()

    # Fetch all products for combo creation
    c.execute("SELECT id, name FROM products")
    products = c.fetchall()
    product_dict = {name: id for id, name in products}

    # Add New Combo Package
    with st.form("add_combo_form"):
        st.subheader("Add New Combo Package")
        combo_name = st.text_input("Combo Name")
        combo_description = st.text_input("Combo Description")
        total_price = st.number_input("Total Price", min_value=0.0)

        # Add products to combo
        st.subheader("Add Products to Combo")
        selected_products = st.multiselect("Select Products", list(product_dict.keys()))
        quantities = [st.number_input(f"Quantity for {product}", min_value=1) for product in selected_products]

        if st.form_submit_button("Add Combo"):
            # Insert combo package
            c.execute("INSERT INTO combo_packages (name, description, total_price) VALUES (?, ?, ?)",
                      (combo_name, combo_description, total_price))
            combo_id = c.lastrowid

            # Insert combo items
            for product, quantity in zip(selected_products, quantities):
                product_id = product_dict[product]
                c.execute("INSERT INTO combo_package_items (combo_id, product_id, quantity) VALUES (?, ?, ?)",
                          (combo_id, product_id, quantity))
            conn.commit()
            st.success(f"Combo '{combo_name}' added successfully!")

    # View Combo Packages
    st.subheader("Combo Packages List")
    c.execute("SELECT id, name, description, total_price FROM combo_packages")
    combos = c.fetchall()
    if combos:
        st.write(pd.DataFrame(combos, columns=["ID", "Name", "Description", "Total Price"]))
    else:
        st.info("No combo packages found.")

    conn.close()