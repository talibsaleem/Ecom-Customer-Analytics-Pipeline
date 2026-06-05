import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

print(" Feature Engineering and ML Model training started...")

# 1. SQL Database se data parhna
conn = sqlite3.connect('data/ecommerce.db')

query = '''
SELECT 
    c.customer_id,
    c.join_date,
    t.transaction_date,
    t.total_amount
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
'''
df_raw = pd.read_sql_query(query, conn)

# Dates ko sahi format mein convert karna
df_raw['join_date'] = pd.to_datetime(df_raw['join_date'])
df_raw['transaction_date'] = pd.to_datetime(df_raw['transaction_date'])

# 2. FEATURE ENGINEERING (Har customer ka behavior nikalna)
# Hum farz kar rahay hain ke aaj ki tareeq 2026-06-01 hai
current_date = pd.to_datetime('2026-06-01')

# Har customer ke liye metrics calculate karna
customer_features = df_raw.groupby('customer_id').agg(
    total_spend=('total_amount', 'sum'),
    total_transactions=('transaction_date', 'count'),
    last_purchase_date=('transaction_date', 'max'),
    join_date=('join_date', 'first')
).reset_index()

# NaNs ko zero karna (agar kisi ne kuch nahi khareeda)
customer_features['total_spend'] = customer_features['total_spend'].fillna(0)
customer_features['total_transactions'] = customer_features['total_transactions'].fillna(0)

# Recency: Customer ne aakhri baar kitne din pehle khareedari ki
customer_features['recency_days'] = (current_date - customer_features['last_purchase_date']).dt.days
# Agar kisi ki purchase date nahi hai, to join date se calculate karein
customer_features['recency_days'] = customer_features['recency_days'].fillna((current_date - customer_features['join_date']).dt.days)

# 3. LABELLING (Kaun chor gaya?)
# Agar kisi customer ne 90 din se koi khareedari nahi ki, to woh CHURN (1) hai, warna ACTIVE (0) hai
customer_features['churn'] = np.where(customer_features['recency_days'] > 90, 1, 0)

# 4. MACHINE LEARNING MODEL TRAINING
# Features (X) aur Target (Y) select karna
X = customer_features[['total_spend', 'total_transactions', 'recency_days']]
y = customer_features['churn']

# Data ko Train aur Test mein split karna
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model train karna (Random Forest)
model = RandomForestClassifier(random_state=42, n_estimators=50) # Chota n_estimators taakay RAM friendly rahe
model.fit(X_train, y_train)

# Har customer ke liye Churn ki Probability (imkaan) nikalna
# predict_proba hamein 0 se 1 ke darmiyan score deta hai (e.g. 0.85 matlab 85% chance hai ke chor jaye ga)
customer_features['churn_probability'] = model.predict_proba(X)[:, 1]
customer_features['churn_probability'] = customer_features['churn_probability'].round(2)

print(f"-> Model trained successfully. Accuracy score: {model.score(X_test, y_test)*100:.2f}%")

# 5. PREDICTIONS KO SQL MEIN SAVE KARNA
# Hum sirf ID aur Churn Scores save karein ge taakay database heavy na ho
df_predictions = customer_features[['customer_id', 'churn_probability', 'churn']]

# SQL mein nayi table banana
df_predictions.to_sql('churn_predictions', conn, if_exists='replace', index=False)
df_predictions.to_csv('data/churn_predictions.csv', index=False)

conn.close()
print("\nCongratulations! predictions are saved in the 'churn_predictions' table of the database.")