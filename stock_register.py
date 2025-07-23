# stock_register.py
import streamlit as st
import sqlite3
import pandas as pd
from database import get_db_connection

def stock_register():
    st.title("📦 Stock Register")

    conn = get_db_connection()
    c = conn.cursor()

    # Static Categories and Subcategories
    categories = ["Drinks", "Snacks", "Daily Needs"]
    daily_needs_subcategories = ["Solid", "Liquid"]
    units = {
        "Drinks": ["Case", "Litre", "ml"],
        "Snacks": ["Unit"],
        "Daily Needs": {
            "Solid": ["kg", "gram"],
            "Liquid": ["Litre", "ml"]
        }
    }

    # Add New Product Form
    with st.form("add_product_form"):
        st.subheader("Add/Update Product")
        name = st.text_input("Product Name")
        category = st.selectbox("Category", categories)
        if category == "Daily Needs":
            subcategory = st.selectbox("Subcategory", daily_needs_subcategories)
        manufacturer = st.text_input("Manufacturer")
        bulk_buy_price = st.number_input("Bulk Buy Price (Total)", min_value=0.0)
        mrp_per_unit = st.number_input("MRP (Per Unit)", min_value=0.0)

        if st.form_submit_button("Add/Update Product"):
            # Insert or update product
            c.execute("SELECT id FROM products WHERE name = ?", (name,))
            existing_product = c.fetchone()
            if existing_product:
                c.execute("UPDATE products SET category = ?, subcategory = ?, manufacturer = ?, bulk_buy_price = ?, mrp_per_unit = ? WHERE id = ?",
                          (category, subcategory if category == "Daily Needs" else None, manufacturer, bulk_buy_price, mrp_per_unit, existing_product[0]))
            else:
                c.execute("INSERT INTO products (name, category, subcategory, manufacturer, bulk_buy_price, mrp_per_unit, stock) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (name, category, subcategory if category == "Daily Needs" else None, manufacturer, bulk_buy_price, mrp_per_unit, 0))
            conn.commit()
            st.success("Product added/updated successfully!")

    # Display Products
    st.subheader("Product List")
    c.execute("SELECT id, name, category, subcategory, manufacturer, bulk_buy_price, mrp_per_unit, stock FROM products")
    products = c.fetchall()
    if products:
        st.write(pd.DataFrame(products, columns=["ID", "Name", "Category", "Subcategory", "Manufacturer", "Bulk Buy Price", "MRP (Per Unit)", "Stock"]))
    else:
        st.info("No products found.")

    conn.close()