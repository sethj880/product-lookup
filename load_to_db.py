import pandas as pd
import sqlite3

# Load the cleaned CSV
df = pd.read_csv("cleaned_inventory.csv")

# Connect to (or create) the SQLite database
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Drop existing table if it exists
cursor.execute("DROP TABLE IF EXISTS products")

# Create a fresh products table
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code TEXT,
    description TEXT,
    batch_code TEXT
)
""")

# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO products (product_code, description, batch_code)
        VALUES (?, ?, ?)
    """, (row['product_code'], row['description'], row['batch_code']))

# Commit and close
conn.commit()
conn.close()

print("✅ Database loaded fresh with all products")
