from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = "products.db"

def get_products(search=""):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if search:
        search = f"%{search.lower()}%"
        cur.execute("""
            SELECT * FROM products
            WHERE LOWER(product_code) LIKE ?
               OR LOWER(description) LIKE ?
               OR LOWER(batch_code) LIKE ?
        """, (search, search, search))
    else:
        cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return products

@app.route("/", methods=["GET", "POST"])
def index():
    search = request.args.get("search", "")
    products = get_products(search)
    return render_template("index.html", products=products, search=search)

@app.route("/update_location", methods=["POST"])
def update_location():
    product_id = request.form["id"]
    location = request.form["location"]
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE products SET location = ? WHERE id = ?", (location, product_id))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
