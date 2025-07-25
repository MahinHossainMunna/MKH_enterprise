# sales_register.py
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from database import get_db_connection

def print_invoice(invoice_id):
    conn = get_db_connection()
    c = conn.cursor()

    # Fetch invoice details
    c.execute("SELECT * FROM sales WHERE invoice_id = ?", (invoice_id,))
    invoice_details = c.fetchall()

    if invoice_details:
        # Custom Header
        st.markdown("<h2 style='text-align: center;'>M/S MKH Enterprise</h2>", unsafe_allow_html=True)

        # Invoice Details
        st.subheader("Invoice Details")
        st.write(f"Invoice ID: {invoice_id}")
        st.write(pd.DataFrame(invoice_details, columns=["ID", "Product ID", "Quantity", "Total Price", "Date", "Cashier", "Discount", "Invoice ID", "Payment Status"]))

        # Custom Footer
        user_name = st.session_state.get("username", "Unknown User")
        st.markdown(f"<div style='text-align: center;'>This invoice is generated by {user_name}</div>", unsafe_allow_html=True)

        # Print Button
        if st.button("Print Invoice"):
            st.success("Invoice printed successfully!")
    else:
        st.error("No invoice found with the given ID.")

    conn.close()

def sales_register():
    st.title("🛒 Sales Register")

    # Initialize session state for the current sale cart
    if "sale_cart" not in st.session_state:
        st.session_state["sale_cart"] = []

    conn = get_db_connection()
    c = conn.cursor()

    # Fetch products and combo packages
    with st.spinner("Loading products and combos..."):
        c.execute("SELECT id, name, mrp_per_unit FROM products")
        products = c.fetchall()
        c.execute("SELECT id, name, total_price FROM combo_packages")
        combo_packages = c.fetchall()

    # Create dictionaries for products and combos
    product_dict = {name: (id, mrp_per_unit) for id, name, mrp_per_unit in products}
    combo_dict = {name: (id, total_price) for id, name, total_price in combo_packages}

    # Product/Combo Selection
    selected_item = st.selectbox("Select Product or Combo", list(product_dict.keys()) + list(combo_dict.keys()))

    if selected_item in product_dict:
        # Product Selection
        product_id, mrp_per_unit = product_dict[selected_item]
        quantity = st.number_input("Quantity", min_value=1)
        discount_type = st.radio("Discount Type", ["Percentage", "Fixed Amount"])
        discount_value = st.number_input("Discount Value", min_value=0.0)

        # Calculate Selling Price
        if discount_type == "Percentage":
            selling_price = mrp_per_unit * quantity * (1 - discount_value / 100)
        else:
            selling_price = (mrp_per_unit * quantity) - discount_value

        if st.button("Add to Cart"):
            with st.spinner("Adding to cart..."):
                st.session_state["sale_cart"].append({
                    "product_id": product_id,
                    "name": selected_item,
                    "quantity": quantity,
                    "total_price": selling_price
                })
                st.success(f"{selected_item} added to cart!")
    elif selected_item in combo_dict:
        # Combo Selection
        combo_id, total_price = combo_dict[selected_item]
        if st.button("Add to Cart"):
            with st.spinner("Adding to cart..."):
                st.session_state["sale_cart"].append({
                    "combo_id": combo_id,
                    "name": selected_item,
                    "quantity": 1,
                    "total_price": total_price
                })
                st.success(f"{selected_item} added to cart!")
    else:
        st.warning("Please select a valid product or combo.")

    # Display Current Sale Cart
    st.subheader("Current Sale Cart")
    if st.session_state["sale_cart"]:
        cart_df = pd.DataFrame(st.session_state["sale_cart"])
        st.write(cart_df)

        # Complete Sale
        if st.button("Complete Sale"):
            with st.spinner("Processing sale..."):
                invoice_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                for item in st.session_state["sale_cart"]:
                    if "product_id" in item:
                        c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item["quantity"], item["product_id"]))
                        c.execute("INSERT INTO sales (product_id, quantity, total_price, date, cashier, discount, invoice_id, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                  (item["product_id"], item["quantity"], item["total_price"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), st.session_state["username"], discount_value, invoice_id, "Paid"))
                    elif "combo_id" in item:
                        c.execute("SELECT product_id, quantity FROM combo_package_items WHERE combo_id = ?", (item["combo_id"],))
                        combo_items = c.fetchall()
                        for product_id, quantity in combo_items:
                            c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
                        c.execute("INSERT INTO sales (combo_id, quantity, total_price, date, cashier, discount, invoice_id, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                  (item["combo_id"], item["quantity"], item["total_price"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), st.session_state["username"], 0, invoice_id, "Paid"))
                conn.commit()
                st.success(f"Sale completed successfully! Invoice ID: {invoice_id}")

                # Print Invoice
                print_invoice(invoice_id)

                st.session_state["sale_cart"] = []

    conn.close()