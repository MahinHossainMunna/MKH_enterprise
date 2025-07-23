# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("store.db", check_same_thread=False)
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT)''')
    
    # Products Table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    category TEXT,
                    subcategory TEXT,
                    manufacturer TEXT,
                    bulk_buy_price REAL,
                    mrp_per_unit REAL,
                    stock INTEGER,
                    barcode TEXT)''')
    
    # Sales Table
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    quantity INTEGER,
                    total_price REAL,
                    date TEXT,
                    cashier TEXT,
                    discount REAL,
                    invoice_id TEXT,
                    payment_status TEXT)''')
    
    # Expenses Table
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    amount REAL,
                    category TEXT,
                    date TEXT)''')
    
    # Debt Table
    c.execute('''CREATE TABLE IF NOT EXISTS debts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    phone_number TEXT,
                    amount REAL,
                    date TEXT)''')
    
    # Combo Packages Table
    c.execute('''CREATE TABLE IF NOT EXISTS combo_packages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    description TEXT,
                    total_price REAL)''')
    
    # Combo Package Items Table
    c.execute('''CREATE TABLE IF NOT EXISTS combo_package_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    combo_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY(combo_id) REFERENCES combo_packages(id),
                    FOREIGN KEY(product_id) REFERENCES products(id))''')
    
    conn.commit()
    conn.close()

def init_super_admin():
    conn = sqlite3.connect("store.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", ("DON",))
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ("DON", "mh.DON", "Super Admin"))
        conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect("store.db", check_same_thread=False)