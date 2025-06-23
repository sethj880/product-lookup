import pandas as pd

# Load the Excel file and sheet
file_path = "Inventory_Level_-_Batch_(INVT018).xlsx"
sheet_name = "Inventory Level - Batch"

# Read the sheet
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Show the original column names
print("Available columns:", df.columns.tolist())

# Rename columns to simple names
df = df.rename(columns={
    'Product Code': 'product_code',
    'Product Description': 'description',
    'Batch Number': 'batch_code'
})

# Filter the relevant columns
data = df[['product_code', 'description', 'batch_code']]

# Preview the data
print(data.head())

# Save to CSV
data.to_csv("cleaned_inventory.csv", index=False)
print("✅ Saved cleaned_inventory.csv")
