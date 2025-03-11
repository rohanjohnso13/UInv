from flask import Flask, render_template, request, redirect, url_for, flash
import csv, os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

FILE_NAME = "inventory.csv"

# Load and save inventory functions
def load_inventory():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, mode='r') as file:
        return list(csv.DictReader(file))

def save_inventory(inventory):
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=inventory[0].keys() if inventory else ["Product ID", "Product Name", "Category", "Price", "Stock", "Total Sales"])
        writer.writeheader()
        writer.writerows(inventory)

# Routes for web interface
@app.route('/')
def index():
    inventory = load_inventory()
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['POST'])
def add_product():
    product = {
        "Product ID": request.form['product_id'],
        "Product Name": request.form['product_name'],
        "Category": request.form['category'],
        "Price": request.form['price'],
        "Stock": request.form['stock'],
        "Total Sales": "0"
    }
    inventory = load_inventory()
    if any(p['Product ID'] == product['Product ID'] for p in inventory):
        flash("Product ID exists!", "error")
    else:
        inventory.append(product)
        save_inventory(inventory)
        flash("Product added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/update/<product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    inventory = load_inventory()
    product = next((p for p in inventory if p['Product ID'] == product_id), None)
    
    if request.method == 'POST':
        product['Price'] = request.form['price']
        product['Stock'] = request.form['stock']
        save_inventory(inventory)
        flash("Product updated successfully!", "success")
        return redirect(url_for('index'))

    return render_template('update.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)

