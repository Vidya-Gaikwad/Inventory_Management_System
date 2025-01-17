# This module 'inventory_manager.py' is a part of 'Inventory Management System' Projects
# This module handles operations related to managing inventory which consists of different products

import json
from pathlib import Path
from inventory.product import Product
import re


class InventoryManager:
    ''' This class provides objects for management, ie "manager" of inventory'''

    def __init__(self, file_path="product_catalog.json"):
        self.database = Path(file_path)
        self.json_file_available = False
        self.product_data = {}

    def read_product_data(self):
        '''Reads the product data from the JSON file.'''

        if not self.database.exists():
            print("Product catalog file does not exist. Returning an empty inventory.")
            return {}  # Return an empty dictionary if the file doesn't exist or self.product_data

        try:
            with open(self.database, "r") as file:
                self.json_file_available = True  # The file is available and has been read successfully.
                self.product_data = json.load(file)
                return self.product_data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading the file: {e}")
            return {}  # Return an empty dictionary in case of errors

    def save_product(self):
        '''This method will be called to save changes made to database.
        Here changes to database are, like add_product, update_product'''

        with open(self.database, "w") as file:
            json.dump(self.product_data, file, indent=4)

    def add_product(self, product_id: str, product: Product):
        '''With this method, manager can add product of type Product to database'''

        self.product_data = self.read_product_data()
        if product_id not in self.product_data and self.valid_product_id(product_id):
            if self.validate_product(product):
                self.product_data[product_id] = product.to_dict()
                self.save_product()
                print("\n")
                print(f"Product with ID '{product_id}' added successfully.")
                print("\n")
        else:
            print("Something went wrong, product cannot be added")

    def update_product(self, product_id: str, updated_product: Product):
        '''With this method already present product in daabase can be modified/updated'''

        self.product_data = self.read_product_data()
        if product_id not in self.product_data:
            print(f"There is no product with given product_id '{product_id}'")
            return False
        elif not (isinstance(updated_product, Product)):
            raise TypeError("updated_product must be of type 'Product'")
        elif self.validate_product(updated_product):
            # self.product_data[product_id] = vars(updated_product)
            data = updated_product.to_dict()
            self.product_data[product_id] = data
            self.save_product()
            return True
        else:
            print("Something went wrong, product cannot be updated")

    def valid_product_id(self, product_id: str):
        '''Each product has a unique Id, which should follow given pattern'''

        pattern = r"^[A-Z]\d{3}$"
        if re.match(pattern, product_id):
            return True
        raise ValueError("Product ID must be a valid product ID.")

    def validate_product(self, product: Product):
        '''This methods validates product by checking: if name follows given pattern,
        if quantity, and price is of float type, and category is from the given list
        '''

        pattern = r"^[A-Za-z]+[_\d\s-]*[A-Za-z\d]+$"
        # ex. 'iphone', 'Iphone10', 'iphone-10', 'iphone_10', 'my iphone' ..ect

        category_list = ["Electronics", "electronics", "Furniture", "furniture", "Clothes", "clothes", "Footwear", "footware"]

        if not (isinstance(product, Product)):
            raise TypeError("Type of product is not 'Product'")
        # Makes sure quantity and quality is not zero 
        elif not (product.product_name and product.quantity and product.price and product.category):
            raise TypeError("Product can not be empty")
        elif not (re.match(pattern, product.product_name)):
            raise NameError("product_name does not follow required pattern")
        elif product.category not in category_list:
            raise NameError("Category not in list")
        elif not ((isinstance(product.price, float)) and (isinstance(product.quantity, float))):
            raise TypeError("price and quantity should be of type float")
        else:
            return True

    def search_product_by_name(self, product_name: str):
        ''' This method searches product in "product_catalog.json" by name of product'''

        self.product_data = self.read_product_data()
        for product_id, product in self.product_data.items():
            if product_name.lower() == (product["product_name"]).lower():
                return product
        else:
            return False

    def get_total_inventory_value(self):
        ''' This method provides total value of inventory '''

        if not self.database:
            print("Error: The product catalog file is not available. Cannot calculate total inventory value.")
            return 0  # Return 0 since we can't calculate the total value 
        total_value: float = 0.0
        self.product_data = self.read_product_data()
        for product_id, product in self.product_data.items():
            total_value += product["price"] * product["quantity"]
        return total_value

    def remove_product(self, product_id: str):
        ''' This method removes a product from inventory, when given correct product_id.
        And also updates 'product_catalog.json'
        '''
        if not self.database:
            print("Error: The product catalog file is not available. Cannot remove product.")
            return
        self.product_data = self.read_product_data()
        if product_id in self.product_data:
            del self.product_data[product_id]
            self.save_product()
            print(f"Product with ID {product_id} has been removed from the inventory.")
        else:
            print(f"Product with ID {product_id} not found.")

    def filter_product_by_price(self):
        ''' This method filters product by price (between 0 and given price)'''

        self.product_data = self.read_product_data()
        print("products will be filtered between 0 and price provided")
        price = float(input("Please enter your price: "))
        filtered = list(filter(lambda x: x[1]["price"] < price, self.product_data.items()))
        return filtered

    def filter_product_by_category(self):
        ''' This method filters product by category. 
        User needs to type numbers like 1, 2..ect corresponding to category
        '''
        self.product_data = self.read_product_data()
        try:
            category = input("Please enter your option for category\n1 -Electronics \n2 -Furniture \n3 -Footwear \n4 -Clothes\nCategory: ").strip()
            if category == "1":
                filtered_category = list(filter(lambda x: x[1]["category"] == "Electronics", self.product_data.items()))
                result = filtered_category
            elif category == "2":
                filtered_category = list(filter(lambda x: x[1]["category"] == "Furniture", self.product_data.items()))
                result = filtered_category
            elif category == "3":
                filtered_category = list(filter(lambda x: x[1]["category"] == "Footwear", self.product_data.items()))
                result = filtered_category
            elif category == "4":
                filtered_category = list(filter(lambda x: x[1]["category"] == "Clothes", self.product_data.items()))
                result = filtered_category
            else:
                print("Category not in list! Please enter no between (1 - 4)")
            return result
        except Exception as e:
            print(f"Error: {e}")

    def filter_product_with_low_quantity(self):
        ''' This method provides list of products with low available quantity (below 5)'''

        self.product_data = self.read_product_data()
        products_with_minimum_quantity = list(filter(lambda x: x[1]["quantity"] < 5, self.product_data.items()))
        result = products_with_minimum_quantity
        if len(result) > 0:
            return result
        else:
            print("All products have quantity more than minimum required!!")
