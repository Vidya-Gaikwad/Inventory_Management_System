import json
from pathlib import Path

class Product:
    
    def __init__(self, product_name, quantity, price, category, file_path = "product_catalog.json"):
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.database = Path(file_path)
        self.product_data = {}

    def read_product_data(self):
        # Read the data from the JSON file
        if self.database.exists():
            with open(self.database, "r") as file:
                self.product_data = json.load(file)
                return self.product_data
        else:
            print("File not found. Returning empty data.")
            return {}


    def update_quantity(self, added_quantity):
        # Update the quantity of the product
        self.quantity += added_quantity

        # Find the product by name and update its quantity
        product_found = False
        for product_id, product_info in self.product_data.items():
            if product_info["name"].lower() == self.product_name: 
                self.product_data[product_id]["quantity"] = self.quantity
                product_found = True
                break
        
        
        if not product_found:
            print(f"Product '{self.product_name}' not found in the catalog.")
            return 

        # Save the updated product data back to the JSON file
        self.save_product_data()

    def update_price(self, new_price):
        self.price = new_price

        # Find the product by name and update its price
        product_found = False
        for product_id, product_info in self.product_data.items():
            if product_info["name"].lower() == self.product_name: 
                self.product_data[product_id]["price"] = self.price
                product_found = True
                break
        
        
        if not product_found:
            print(f"Product '{self.product_name}' not found in the catalog.")
            return  

        # Save the updated product data back to the JSON file
        self.save_product_data()


    def display_product_info(self):
        info = (f"Name: {self.product_name}, "
                f"Quantity: {self.quantity}, Price: ${self.price:.2f}, "
                f"Category: {self.category}")
        print(info)
        return info
    
    def is_in_stock(self):
        return self.quantity > 0
    
    def apply_discount(self, discount_percentage):
        if not (0 <= discount_percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100")
        discount = self.price * (discount_percentage / 100)
        self.price = max(0, self.price - discount)

    def save_product_data(self):
        # Save the updated product data back to the JSON file
        with open(self.database, "w") as file:
            json.dump(self.product_data, file, indent=4)

    def to_dict(self):
    #"""Returns the product attributes as a dictionary."""
        data = {
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "category": self.category
            }
        return data