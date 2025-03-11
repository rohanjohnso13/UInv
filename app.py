import tkinter as tk
from tkinter import messagebox
import csv, os

FILE_NAME = "inventory.csv"

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

def add_product():
    product = {
        "Product ID": product_id_entry.get(),
        "Product Name": product_name_entry.get(),
        "Category": category_entry.get(),
        "Price": price_entry.get(),
        "Stock": stock_entry.get(),
        "Total Sales": "0"
    }
    inventory = load_inventory()
    if any(p['Product ID'] == product['Product ID'] for p in inventory):
        messagebox.showerror("Error", "Product ID exists!")
    else:
        inventory.append(product)
        save_inventory(inventory)
        messagebox.showinfo("Success", "Product added!")

root = tk.Tk()
root.title("Inventory Management System")

tk.Label(root, text="Product ID").grid(row=0, column=0)
product_id_entry = tk.Entry(root)
product_id_entry.grid(row=0, column=1)

tk.Label(root, text="Product Name").grid(row=1, column=0)
product_name_entry = tk.Entry(root)
product_name_entry.grid(row=1, column=1)

tk.Label(root, text="Category").grid(row=2, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=2, column=1)

tk.Label(root, text="Price").grid(row=3, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1)

tk.Label(root, text="Stock").grid(row=4, column=0)
stock_entry = tk.Entry(root)
stock_entry.grid(row=4, column=1)

add_button = tk.Button(root, text="Add Product", command=add_product)
add_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
