from employee import Employee
from login import Login
from registration import Registration
from users_database import UserManager, UserExistsError, UserNotFoundError


import sys
import os


# Add the inventory folder to the sys.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "inventory"))
)

import inventory_manager
import product


class Main:

    def display_main_menu(self):
        user_manager = UserManager()
        login_system = Login(user_manager)
        registration_system = Registration(user_manager)
        inventory_manager = InventoryManager()

        while True:
            print("\nWelcome to the Inventory Management System")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":  # Login
                if login_system.login():
                    print("Login successful!")
                    self.access_inventory(
                        inventory_manager
                    )  # Use self to call instance method
                    break  # Exit after accessing inventory
                else:
                    print("Login failed. Please try again.")

            elif choice == "2":  # Register
                if registration_system.register_user():
                    print("Registration successful! You can now log in.")
                else:
                    print("Registration failed. Please try again.")

            elif choice == "3":
                print("Exiting system...")
                break

            else:
                print("Invalid choice. Please try again.")

    def access_inventory(self, inventory_manager):
        print("\n")
        print("*" * 70)
        print("------------ Welcome to Inventory management System ------------")
        print("*" * 70)

        while True:
            print("\nInventory Management System")
            print("1. Modify/Update Inventory")
            print("2. Search a Product")
            print("3. Modify/Update Product")
            print("4. Filter Products")
            print("5. Exit")
            print("-" * 75)
            choice = input("Enter your choice (1-5):  ")
            print("-" * 75)

            if choice == "1":
                submenu_1 = True
                while submenu_1:
                    print(".......... Modify/Update Inventory menu ..........")
                    print("1. Display all products available in inventory")
                    print("2. Get total inventory value")
                    print("3. Add Product")
                    print("4. Update Product")
                    print("5. Remove Product")
                    print("6. Go back")
                    print("-" * 75)
                    print("You are now in submenu: Modify/Update Inventory")
                    choice = input("Enter your choice (1-6):  ")
                    print("-" * 75)
                    if choice == "1":
                        all_products = inventory_manager.read_product_data()
                        print("Available products in inventory are: ")
                        for item, value in all_products.items():
                            print(
                                f"-- {all_products[item]['product_name']}, Price: ${all_products[item]['price']:.2f}"
                            )
                        print("\n")
                    elif choice == "2":
                        print("-" * 75)
                        print(
                            f"Total inventory value is ${inventory_manager.get_total_inventory_value()}"
                        )
                        print("-" * 75)
                    elif choice == "3":
                        product_id = input("Enter Product ID (format: A123): ")
                        product_name = input("Enter Product Name: ")
                        quantity = float(input("Enter Quantity: "))
                        price = float(input("Enter Price: "))
                        category = input(
                            "Enter Category (Electronics, Furniture, Clothes, Footwear): "
                        )
                        product = Product(product_name, quantity, price, category)
                        try:
                            inventory_manager.add_product(product_id, product)
                        except Exception as e:
                            print(f"Error: {e}")
                    elif choice == "4":
                        product_id = input("Enter Product ID to update: ")
                        product_name = input("Enter New Product Name: ")
                        quantity = float(input("Enter New Quantity: "))
                        price = float(input("Enter New Price: "))
                        category = input("Enter New Category: ")
                        updated_product = Product(
                            product_name, quantity, price, category
                        )
                        try:
                            if inventory_manager.update_product(
                                product_id, updated_product
                            ):
                                print("Product updated successfully.")
                            else:
                                print("Product not found.")
                        except Exception as e:
                            print(f"Error: {e}")
                    elif choice == "5":
                        product_id = input("Enter Product ID to remove: ")
                        try:
                            inventory_manager.remove_product(product_id)
                        except Exception as e:
                            print(f"Error: {e}")
                    elif choice == "6":
                        submenu_1 = False
                    else:
                        print("Invalid option")

            elif choice == "2":
                submenu_2 = True
                while submenu_2:
                    print("1. Search Product by ID")
                    print("2. Search Product by product_name")
                    print("3. Go back")
                    print("-" * 75)
                    choice = input("Enter your choice (1-3):  ")
                    print("-" * 75)
                    if choice == "1":
                        product_id = input("Enter Product ID to display: ")
                        product_data = inventory_manager.read_product_data()
                        if product_id in product_data:
                            product_info = product_data[product_id]
                            print(f"Product ID: {product_id}")
                            print(f"Name: {product_info['product_name']}")
                            print(f"Quantity: {product_info['quantity']}")
                            print(f"Price: {product_info['price']}")
                            print(f"Category: {product_info['category']}")
                        else:
                            print("Product not found.")

                    elif choice == "2":
                        product_name = input("Enter name of product:  ")
                        product_found = inventory_manager.search_product_by_name(
                            product_name
                        )
                        if product_found:
                            print(f"Name: {product_found['product_name']}")
                            print(f"Quantity: {product_found['quantity']}")
                            print(f"Price: {product_found['price']}")
                            print(f"Category: {product_found['category']}")
                        else:
                            print("Product not found.")

                    elif choice == "3":
                        submenu_2 = False

            elif choice == "3":
                submenu_3 = True
                while submenu_3:
                    print("1. Update quantity of specific product")
                    print("2. Update price of specific product")
                    print("3. Apply Discount")
                    print("4. Go back")
                    print("-" * 75)
                    choice = input("Enter your choice (1-4):  ")
                    print("-" * 75)
                    if choice == "1":
                        product_name = input("Enter name of product: ")
                        added_quantity = float(
                            input("Enter quantity to be added/subtracted: ")
                        )
                        product_found = inventory_manager.search_product_by_name(
                            product_name
                        )
                        product_obj = Product(**product_found)
                        try:
                            updated_quantity = product_obj.update_quantity(
                                added_quantity
                            )
                            print(
                                f"Quantity of '{product_name}' updated to {updated_quantity}"
                            )
                        except Exception as e:
                            print(f"Error: {e}")
                    elif choice == "2":
                        product_name = input("Enter name of product: ")
                        updated_price = float(input("Enter new price: "))
                        product_found = inventory_manager.search_product_by_name(
                            product_name
                        )
                        product_obj = Product(**product_found)
                        try:
                            product_obj.update_price(updated_price)
                            print(
                                f"Price of '{product_name}' updated to '${updated_price}'"
                            )
                        except Exception as e:
                            print(f"Error: {e}")
                    elif choice == "3":
                        product_name = input("Enter name of product: ")
                        product_found = inventory_manager.search_product_by_name(
                            product_name
                        )
                        product_obj = Product(**product_found)
                        discount_percentage = float(
                            input("Enter Discount Percentage: ")
                        )
                        try:
                            if product_found:
                                product_obj.apply_discount(discount_percentage)
                                print(
                                    f"Discount applied successfully. New Price: {product_obj.price}"
                                )
                            else:
                                print("Product not found.")
                        except Exception as e:
                            print(f"Error: {e}")
                    elif choice == "4":
                        submenu_3 = False
                    else:
                        print("Invalid option!")

            elif choice == "4":
                submenu_4 = True
                while submenu_4:
                    print("1. Filter products by price")
                    print("2. Filter products by category")
                    print("3. Filter products by low quantity (less than 5)")
                    print("4. Go back")
                    print("-" * 75)
                    choice = input("Enter your choice (1-4):  ")
                    print("-" * 75)
                    if choice == "1":
                        result = inventory_manager.filter_product_by_price()
                        if result:
                            for items in result:
                                print(
                                    f"Product_name: {items[1]['product_name']}--- Price: {items[1]['price']}"
                                )
                        else:
                            print("No product found!")
                    elif choice == "2":
                        products = inventory_manager.filter_product_by_category()
                        for items in products:
                            print(
                                f"Product_name: {items[1]['product_name']}--- Price: {items[1]['price']}"
                            )
                    elif choice == "3":
                        products_found = (
                            inventory_manager.filter_product_with_low_quantity()
                        )
                        try:
                            for items in products_found:
                                print(
                                    f"Product_name: {items[1]['product_name']}--- Quantity: {items[1]['quantity']}"
                                )
                        except TypeError:
                            print("No products with low quantity found.")
                    elif choice == "4":
                        submenu_4 = False
            elif choice == "5":
                print("Exiting the Inventory Management System.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main = Main()
    main.display_main_menu()
