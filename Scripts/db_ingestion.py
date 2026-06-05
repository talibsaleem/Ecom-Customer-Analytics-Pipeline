import pandas as pd
import sqlite3
import os

print("Phase 2: SQL Database setup and Data Ingestion started...")

# 1. Database se connect karna
conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

# 2. Purani tables ko khatam karna (taakay Primary Key ka error na aaye)
cursor.execute("DROP TABLE IF EXISTS transactions;")
cursor.execute("DROP TABLE IF EXISTS customers;")
cursor.execute("DROP TABLE IF EXISTS products;")

# 3. TABLES DOBARA BANANA (Saaf Schema aur Keys ke sath)
cursor.execute('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    join_date TEXT,
    country TEXT
);
''')

cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
);
''')

cursor.execute('''
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    transaction_date TEXT,
    quantity INTEGER,
    total_amount REAL,
    payment_method TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);
''')

conn.commit()
print("-> SQL Tables made successfully.")

# 4. CSV FILES SE DATA PARHNA (RAM Friendly)
df_cust = pd.read_csv('data/customers.csv')
df_prod = pd.read_csv('data/products.csv')
df_trans = pd.read_csv('data/transactions.csv')

# 5. DATA KO IN TABLES MEIN LOAD KARNA
# if_exists='append' ab bina error ke chalay ga kyun ke hum upar tables saaf kar chuke hain
df_cust.to_sql('customers', conn, if_exists='append', index=False)
df_prod.to_sql('products', conn, if_exists='append', index=False)
df_trans.to_sql('transactions', conn, if_exists='append', index=False)

conn.close()
print("\nCongratulations! database setup and data ingestion is complete.")