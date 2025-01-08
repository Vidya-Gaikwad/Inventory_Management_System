import json
from pathlib import Path
from inventory.product import Product
import re


class InventoryManager:
    ''' This class provides objects for management, ie "manager" of inventory'''
    def __init__(self, file_path="product_catalog.json"):
        self.database = Path(file_path)
        self.json_file_available = False # added new 
        self.product_data = {}

    # def read_product_data(self):
    #     '''objects can read complete database. This method displays complete database'''

    #     if not self.database.exists():
    #         raise FileNotFoundError
    #     else:
    #         with open(self.database, "r") as file:
    #             self.product_data = json.load(file)
    #             return self.product_data

    # added new
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

    def add_product(self, product_id, product: Product):
        '''With this method, manager can add product of type Product to database'''
        self.product_data = self.read_product_data()
        if self.validate_product(product_id, product):
            self.product_data[product_id] = product.to_dict()
            self.save_product()
            print(f"Product '{product_id}' added successfully.")
        else:
            print("Something went wrong, product cannot be added")

    def update_product(self, product_id, updated_product: Product):
        '''With this method already present product in daabase can be modified/updated'''
        self.product_data = self.read_product_data()
        if product_id not in self.product_data:
            print(f"There is no product with given product_id '{product_id}'")
            return False
        elif not (isinstance(updated_product, Product)):
            raise TypeError("updated_product must be of type 'Product'")
        else:
            # self.product_data[product_id] = vars(updated_product)
            data = updated_product.to_dict()
            self.product_data[product_id] = data
            self.save_product()

    def valid_product_id(self, product_id):
        '''Each product has a unique Id, which should follow given pattern'''

        pattern = r"^[A-Z]\d{3}$"
        if re.match(pattern, product_id):
            return True
        raise ValueError("Product ID must be a valid product ID.")

    
    def validate_product(self, product_id, product: Product):
        '''This methods validates product by checking: if name follows given pattern,
        if quantity, and price is of float type, and category is from the given list
        '''

        pattern = r"^[A-Za-z]+[_\d\s-]*[A-Za-z\d]+$"
        # ex. 'iphone', 'Iphone10', 'iphone-10', 'iphone_10', 'my iphone' ..ect

        category_list = ["Electronics", "electronics", "Furniture", "furniture", "Clothes", "clothes", "Footware", "footware"]

        if product_id not in self.product_data and self.valid_product_id(product_id):
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
        else:
            print("Product_id already exist")
            return False

    def search_product_by_name(self, product_name):
        self.product_data = self.read_product_data()
        for product_id, product in self.product_data.items():
            #if product_name == self.product_data[product_id]["product_name"]:
            if product_name == product["product_name"]:
                #print(product)
                return product
            

    def get_total_inventory_value(self):
        if not self.database:
            print("Error: The product catalog file is not available. Cannot calculate total inventory value.")
            return 0  # Return 0 since we can't calculate the total value 
        total_value = 0
        for product_id, product in self.product_data.items():
            total_value += product["price"] * product["quantity"]
        return total_value

    def remove_product(self, product_id):
        if not self.database:
            print("Error: The product catalog file is not available. Cannot remove product.")
            return
        if product_id in self.product_data:
            del self.product_data[product_id]
            self.save_product()
            print(f"Product with ID {product_id} has been removed from the inventory.")
        else:
            print(f"Product with ID {product_id} not found.")

    def filter_product_by_price(self):
        pass

    def filter_product_by_category(self):
        pass


# manager = InventoryManager()
# manager.read_product_data()
# product = Product("TV", 500.0, 10, "Electronics")
# manager.add_product("E102", product)


# product1 = Product("TV",500.00, 10, "Electronics")
# person = InventoryManager()
# person.read_product_data()
# person.add_product((product1))