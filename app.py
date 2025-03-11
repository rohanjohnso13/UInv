from flask import Flask, render_template, request, redirect, url_for, flash
import csv, os

app = Flask(__name__)

# Set a secret key for session and flash messages
app.secret_key = 'your_secret_key'  # In production, you should use a more secure key

FILE_NAME = "inventory.csv"

# Load and save inventory functions
def load_inventory():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, mode='r') as file:
        return list(csv.DictReader(file))

def save_inventory(inventory):
    if inventory:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=inventory[0].keys())
            writer.writeheader()
            writer.writerows(inventory)
    else:
        with open(FILE_NAME, mode='w', newline='') as file:
            # Handle the case when the inventory is empty by writing the header only
            writer = csv.DictWriter(file, fieldnames=["Product ID", "Product Name", "Category", "Price", "Stock", "Total Sales"])
            writer.writeheader()

# Routes for web interface
@app.route('/')
def index():
    inventory = load_inventory()
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['POST'])
def add_product():
    # Get form data
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    category = request.form.get('category')
    price = request.form.get('price')
    stock = request.form.get('stock')

    # Validate form data
    if not product_id or not product_name or not category or not price or not stock:
        flash("All fields are required!", "error")
        return redirect(url_for('index'))

    product = {
        "Product ID": product_id,
        "Product Name": product_name,
        "Category": category,
        "Price": price,
        "Stock": stock,
        "Total Sales": "0"
    }
    
    # Load existing inventory and check if product ID exists
    inventory = load_inventory()
    if any(p['Product ID'] == product['Product ID'] for p in inventory):
        flash("Product ID already exists!", "error")
    else:
        inventory.append(product)
        save_inventory(inventory)
        flash("Product added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/update/<product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    # Load existing inventory
    inventory = load_inventory()
    product = next((p for p in inventory if p['Product ID'] == product_id), None)
    
    # If product not found, flash error and redirect
    if not product:
        flash("Product not found!", "error")
        return redirect(url_for('index'))

    # Handle form submission to update the product
    if request.method == 'POST':
        price = request.form.get('price')
        stock = request.form.get('stock')

        # Validate form data
        if not price or not stock:
            flash("Both Price and Stock are required!", "error")
        else:
            product['Price'] = price
            product['Stock'] = stock
            save_inventory(inventory)
            flash("Product updated successfully!", "success")
            return redirect(url_for('index'))

    # Render update form with product data
    return render_template('update.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)



