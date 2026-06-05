import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

print("data generation started.")
# ---------------------------------------------------------
# 1. PRODUCTS (CHEENZOON) KA DATA
# ---------------------------------------------------------
# Yeh bohat chota aur RAM friendly dictionary hai
products_data = {
    'product_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'product_name': ['Wireless Mouse', 'Mechanical Keyboard', 'Gaming Monitor', 'USB-C Hub', 
                    'Noise Canceling Headphones', 'Leather Wallet', 'Travel Backpack', 
                    'Water Bottle', 'Running Shoes', 'Smart Fitness Watch'],
    'category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics', 
                 'Fashion', 'Fashion', 'Accessories', 'Fashion', 'Electronics'],
    'price': [25.99, 89.99, 249.99, 34.99, 199.99, 45.00, 65.00, 19.99, 120.00, 150.00]
}
df_products = pd.DataFrame(products_data)

# ---------------------------------------------------------
# 2. CUSTOMERS (GAAHAK) KA DATA
# ---------------------------------------------------------
num_customers = 200  # Sirf 200 customers taakay RAM par bojh na paray
customer_ids = range(1, num_customers + 1)

np.random.seed(42) # Taakay aap ka aur mera data bilkul aik jaisa banay
start_date = datetime(2024, 1, 1)

# Har customer ki sign-up date generate ho rahi hai
join_dates = [start_date + timedelta(days=int(np.random.randint(0, 730))) for _ in customer_ids]

df_customers = pd.DataFrame({
    'customer_id': customer_ids,
    'customer_name': [f"Customer_{i}" for i in customer_ids],
    'email': [f"customer_{i}@email.com" for i in customer_ids],
    'join_date': join_dates,
    'country': np.random.choice(['United States', 'Canada', 'United Kingdom', 'Germany', 'Pakistan'], num_customers)
})

# ---------------------------------------------------------
# 3. TRANSACTIONS (KHAREEDARI) KA DATA (With Churn Pattern)
# ---------------------------------------------------------
# Yahan hum Data Science ka dimag laga rahay hain. Hum kuch customers ko jan boojh kar
# "Inactive" (churned) banayein gay taakay baad mein hamara Machine Learning model unhein pehchan sakay.

transactions_list = []
transaction_id = 10001
end_project_date = datetime(2026, 6, 1)

for idx, row in df_customers.iterrows():
    cust_id = row['customer_id']
    j_date = row['join_date']
    
    # 30% chances hain k customer chor kar chala gaya (Churn ho gaya)
    is_churned = np.random.choice([True, False], p=[0.3, 0.7])
    
    if is_churned:
        max_active_days = np.random.randint(30, 180)
        last_possible_buy_date = j_date + timedelta(days=max_active_days)
    else:
        last_possible_buy_date = end_project_date
        
    num_purchases = np.random.randint(1, 15)
    
    for _ in range(num_purchases):
        days_between = (last_possible_buy_date - j_date).days
        if days_between <= 0:
            days_between = 1
            
        tx_date = j_date + timedelta(days=int(np.random.randint(0, days_between)))
        
        if tx_date > end_project_date:
            continue
            
        # Random product select karna
        prod_row = df_products.sample(n=1).iloc[0]
        quantity = np.random.randint(1, 4)
        total_amount = round(prod_row['price'] * quantity, 2)
        
        transactions_list.append({
            'transaction_id': transaction_id,
            'customer_id': cust_id,
            'product_id': prod_row['product_id'],
            'transaction_date': tx_date.strftime('%Y-%m-%d'),
            'quantity': quantity,
            'total_amount': total_amount,
            'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Crypto', 'Bank Transfer'])
        })
        transaction_id += 1

# List ko DataFrame mein convert karna (Memory efficient tareeqa)
df_transactions = pd.DataFrame(transactions_list)

# ---------------------------------------------------------
# 4. DATA CO CSV FILES MEIN SAVE KARNA
# ---------------------------------------------------------
os.makedirs('data', exist_ok=True) # Agar data folder nahi bana to yeh bana dega

df_products.to_csv('data/products.csv', index=False)
df_customers.to_csv('data/customers.csv', index=False)
df_transactions.to_csv('data/transactions.csv', index=False)


print(f"-> {len(df_products)} Products generated.")
print(f"-> {len(df_customers)} Customers generated.")
print(f"-> {len(df_transactions)} records of transactions is saved in 'data/' folder.")