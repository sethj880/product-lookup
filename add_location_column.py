import sqlite3

conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Add the new column
cursor.execute("ALTER TABLE products ADD COLUMN location TEXT")

conn.commit()
conn.close()

print("✅ 'location' column added to products table")
