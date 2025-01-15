from employee.employee import Employee
from employee.login import Login
from employee.registration import Registration
from employee.users_database import UserManager, UserExistsError, UserNotFoundError
from inventory.inventory_manager import InventoryManager
from inventory.product import Product
import bcrypt


def main():
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
                access_inventory(inventory_manager)
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


def access_inventory(inventory_manager):
    while True:
        print("\nInventory Management Menu")
        print("1. Add a new product")
        print("2. Update product details")
        print("3. Delete a product")
        print("4. View inventory value")
        print("5. Update Product Quantity")
        print("6. Update Product Price")
        print("7. View product information")
        print("8. Apply Discount")
        print("9. Filter products by price")
        print("10. Filter products by category")
        print("11. View products with low quantity")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":  # Add a new product
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = float(input("Enter product quantity: "))
            category = input("Enter product category: ")

            product = Product(name, quantity, price, category)
            inventory_manager.add_product(product_id, product)

        elif choice == "2":  # Update product details
            product_id = input("Enter product ID to update: ")
            name = input("Enter new product name: ")
            price = float(input("Enter new product price: "))
            quantity = float(input("Enter new product quantity: "))
            category = input("Enter new product category: ")

            product = Product(name, quantity, price, category)
            inventory_manager.update_product(product_id, product)

        elif choice == "3":  # Delete a product
            product_id = input("Enter product ID to delete: ")
            inventory_manager.remove_product(product_id)

        elif choice == "4":  # View inventory value
            total_value = inventory_manager.get_total_inventory_value()
            print(f"Total inventory value: ${total_value:.2f}")

        elif choice == "5":  # Update Product Quantity
            product_id = input("Enter product ID to update quantity: ")
            added_quantity = float(input("Enter quantity to add: "))
            product = inventory_manager.product_data.get(product_id)
            if product:
                product.update_quantity(added_quantity)
                print(f"Updated quantity of product '{product_id}'.")
            else:
                print(f"Product ID '{product_id}' not found.")

        elif choice == "6":  # Update Product Price
            product_id = input("Enter product ID to update price: ")
            new_price = float(input("Enter new product price: "))
            product = inventory_manager.product_data.get(product_id)
            if product:
                product.update_price(new_price)
                print(f"Updated price of product '{product_id}'.")
            else:
                print(f"Product ID '{product_id}' not found.")

        elif choice == "7":  # View product information
            product_id = input("Enter product ID to view: ")
            product_data = inventory_manager.product_data.get(product_id)

            if product_data:
                # Create a Product instance from the dictionary data
                product = Product(
                    product_name=product_data["product_name"],
                    quantity=product_data["quantity"],
                    price=product_data["price"],
                    category=product_data["category"]
                )
                product.display_product_info()
            else:
                print(f"Product ID '{product_id}' not found.")

        elif choice == "8":  # Apply Discount
            product_id = input("Enter product ID to apply discount: ")
            discount = float(input("Enter discount percentage: "))
            product_data = inventory_manager.product_data.get(product_id)
            print(f"Current product data: {inventory_manager.product_data}")
            if product_data:
                print(f"Found product: {product_data}")
                # Convert to Product instance and ensure float conversion
                product = Product(
                    product_name=product_data["product_name"],
                    quantity=float(product_data["quantity"]),
                    price=float(product_data["price"]),
                    category=product_data["category"],
                )
                product.apply_discount(discount)
                inventory_manager.update_product(product_id, product)
                print(f"Discount applied to product '{product_id}'. New price: ${product.price:.2f}")
            else:
                print(f"Product ID '{product_id}' not found.")


        # elif choice == "8":  # Apply Discount
        #     product_id = input("Enter product ID to apply discount: ")
        #     discount = float(input("Enter discount percentage: "))
        #     inventory_manager.read_product_data()  # Ensure product data is updated
        #     print(f"Current product data: {inventory_manager.product_data}")  # Debugging output
        #     product_data = inventory_manager.product_data.get(product_id)
        #     if product_data:
        #         # Debugging: Confirm product data
        #         print(f"Found product: {product_data}")
        #         # Create a Product instance from the dictionary data
        #         product = Product(
        #             product_name=product_data["product_name"],
        #             quantity=product_data["quantity"],
        #             price=product_data["price"],
        #             category=product_data["category"]
        #         )
        #         product.apply_discount(discount)

        #         # Update the product in inventory
        #         inventory_manager.update_product(product_id, product)
        #         print(f"Discount applied to product '{product_id}'. New price: ${product.price:.2f}")
        #     else:
        #         print(f"Product ID '{product_id}' not found.")

        # elif choice == "8":  # Apply Discount
        #     product_id = input("Enter product ID to apply discount: ")
        #     discount = float(input("Enter discount percentage: "))
        #     inventory_manager.read_product_data()  # Ensure product data is updated
        #     product_data = inventory_manager.product_data.get(product_id)
        #     if product_data:
        #         # Create a Product instance from the dictionary data
        #         product = Product(
        #             product_name=product_data["product_name"],
        #             quantity=product_data["quantity"],
        #             price=product_data["price"],
        #             category=product_data["category"]
        #         )
        #         product.apply_discount(discount)

        #         # Update the product in inventory
        #         inventory_manager.update_product(product_id, product)
        #         print(f"Discount applied to product '{product_id}'. New price: ${product.price:.2f}")
        #     else:
        #         print(f"Product ID '{product_id}' not found.")
            # discount = float(input("Enter discount percentage: "))
            # product = inventory_manager.product_data.get(product_id)
            # if product:
            #     product.apply_discount(discount)
            #     print(f"Discount applied to product '{product_id}'. New price: ${product.price:.2f}")
            # else:
            #     print(f"Product ID '{product_id}' not found.")

        elif choice == "9":  # Filter products by price
            filtered_products = inventory_manager.filter_product_by_price()
            if filtered_products:
                print("Filtered products by price:")
                for product_id, product in filtered_products:
                    print(f"{product_id}: {product['product_name']}, ${product['price']:.2f}")

        elif choice == "10":  # Filter products by category
            filtered_products = inventory_manager.filter_product_by_category()
            if filtered_products:
                print("Filtered products by category:")
                for product_id, product in filtered_products:
                    print(f"{product_id}: {product['product_name']}, Category: {product['category']}")

        elif choice == "11":  # View products with low quantity
            low_quantity_products = inventory_manager.filter_product_with_low_quantity()
            if low_quantity_products:
                print("Products with low quantity:")
                for product_id, product in low_quantity_products:
                    print(f"{product_id}: {product['product_name']}, Quantity: {product['quantity']}")

        elif choice == "12":  # Exit
            print("Exiting Inventory Management...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

############################# Mariana mini #######################################################################################

# from registration import Registration
# from users_database import UserManager, UserExistsError, UserNotFoundError
# from manager import Manager
# import bcrypt


# class Main:
#     """Main program to manage the Inventory Manager system."""

#     def __init__(self):
#         self.user_manager = UserManager()

#     def display_main_menu(self):
#         """Display the main menu."""
#         while True:
#             print("\nWelcome to Inventory Manager")
#             print("1. Register a user")
#             print("2. Login (users and employees)")
#             print("3. Exit")

#             choice = input("Enter your choice (1-3): ").strip()
#             if choice == "1":
#                 self.register_user()
#             elif choice == "2":
#                 self.login_user()
#             elif choice == "3":
#                 print("Goodbye!")
#                 break
#             else:
#                 print("Invalid choice. Please try again.")

#     def register_user(self):
#         """Register a new user."""
#         registration = Registration(self.user_manager)  # Create an instance
#         try:
#             success = registration.register_user()
#             if success:
#                 print("Registration successful!")
#         except ValueError as e:
#             print(f"Error: {e}")

#     def login_user(self):
#         """Handle user login."""
#         try:
#             login_data = {
#                 "email": input("Enter your email: ").strip(),
#                 "password": input("Enter your password: ").strip(),
#             }
#             user = self.user_manager.find_user(login_data["email"])

#             if user and bcrypt.checkpw(
#                 login_data["password"].encode(), user["password"].encode()
#             ):
#                 print("Login successful!")
#                 # Handle user roles if required
#             else:
#                 print("Invalid email or password.")
#         except Exception as e:
#             print(f"Error during login: {e}")


# if __name__ == "__main__":
#     main = Main()
#     main.display_main_menu()

##### Mariana ###########################################################################################################################

# import bcrypt
# from registration import Registration
# from login import Login
# from users_database import UserManager, UserExistsError, UserNotFoundError
# from manager import Manager
# from employee import Employee

# # from inventory import Inventory
# # from product import Product


# class Main:
#     """Main program to manage the Inventory Manager system."""

#     def __init__(self):
#         self.user_manager = UserManager()  # Manages user database
#         # self.inventory_manger = InventoryManager()  # Manages inventory database
#         # self.product = Product()  # Manages product database

#     def display_main_menu(self):
#         """Display the main menu."""
#         while True:
#             print("\nWelcome to Inventory Manager")
#             print("1. Register a user")
#             print("2. Login (users and employees)")
#             print("3. Exit")

#             choice = input("Enter your choice (1-3): ").strip()
#             if choice == "1":
#                 self.register_user()
#             elif choice == "2":
#                 self.login_user()
#             elif choice == "3":
#                 print("Goodbye!")
#                 break
#             else:
#                 print("Invalid choice. Please try again.")

#     def register_user(self):
#         """Register a new user."""
#         try:
#             registration_data = Registration.prompt_user_input()
#             Registration.register_user(registration_data)
#             print("Registration successful!")
#         except ValueError as e:
#             print(f"Error: {e}")

#     def login_user(self):
#         """Handle user login."""
#         try:
#             login_data = Login.prompt_user_input()
#             user = self.user_manager.get_user_by_email(login_data["email"])

#             if bcrypt.checkpw(
#                 login_data["password"].encode(), user["password"].encode()
#             ):
#                 print("Login successful!")

#                 if user["role"] == "Manager":
#                     manager = Manager(user)
#                     self.manager_menu(manager)
#                 else:
#                     employee = Employee(user)
#                     self.employee_menu(employee)
#             else:
#                 print("Incorrect password.")
#                 choice = (
#                     input("Do you want to recover your password? (y/n): ")
#                     .strip()
#                     .lower()
#                 )
#                 if choice == "y":
#                     Login.password_recovery(login_data["email"])
#                 else:
#                     print("Returning to main menu.")
#         except KeyError:
#             print("User not found.")

#     def manager_menu(self, manager):
#         """Menu for managers with CRUD permissions."""
#         print(f"\nWelcome, Manager {manager.user_data['first_name']}!")
#         while True:
#             print("\nManager Menu:")
#             print("1. Manage employees (CRUD)")
#             print("2. Manage inventory (CRUD)")
#             print("3. Manage products (CRUD)")
#             print("4. Logout")

#             choice = input("Enter your choice (1-4): ").strip()
#             if choice == "1":
#                 self.manage_employees(manager)
#             elif choice == "2":
#                 self.manage_inventory(manager)
#             elif choice == "3":
#                 self.manage_products(manager)
#             elif choice == "4":
#                 print("Logging out...")
#                 break
#             else:
#                 print("Invalid choice. Please try again.")

#     def manage_employees(self, manager):
#         """Manager CRUD menu for employees."""
#         print("\nEmployee Management Menu:")
#         print("1. Add an employee")
#         print("2. Update an employee")
#         print("3. Delete an employee")
#         print("4. Find an employee")
#         print("5. Assign an employee role")
#         print("6. Back to main menu")

#         choice = input("Enter your choice (1-6): ").strip()
#         if choice == "1":
#             manager.add_employee()
#         elif choice == "2":
#             manager.update_employee()
#         elif choice == "3":
#             manager.delete_employee()
#         elif choice == "4":
#             manager.find_employee()
#         elif choice == "5":
#             manager.assign_role()
#         elif choice == "6":
#             return
#         else:
#             print("Invalid choice. Returning to main menu.")

#     def manage_inventory(self, manager):
#         """Manager CRUD menu for inventory."""
#         print("\nInventory Management Menu:")
#         print("1. Add a product to inventory")
#         print("2. Update a product in inventory")
#         print("3. Delete a product from inventory")
#         print("4. View inventory")
#         print("5. Back to manager menu")

#         choice = input("Enter your choice (1-5): ").strip()
#         if choice == "1":
#             manager.add_to_inventory()
#         elif choice == "2":
#             manager.update_inventory()
#         elif choice == "3":
#             manager.delete_from_inventory()
#         elif choice == "4":
#             print("Displaying inventory...")
#             # self.inventory.display_inventory()
#         elif choice == "5":
#             return
#         else:
#             print("Invalid choice. Returning to main menu.")
            
        

#     def manage_products(self, manager):
#         """Manager CRUD menu for products."""
#         print("\nProduct Management Menu:")
#         print("1. Add a product")
#         print("2. Update a product")
#         print("3. Delete a product")
#         print("4. View all products")
#         print("5. Back to manager menu")

#         choice = input("Enter your choice (1-5): ").strip()
#         if choice == "1":
#             manager.add_product()
#         elif choice == "2":
#             manager.update_product()
#         elif choice == "3":
#             manager.delete_product()
#         elif choice == "4":
#             print("Displaying products...")
#             # self.product.display_products()
#         elif choice == "5":
#             return
#         else:
#             print("Invalid choice. Returning to main menu.")


# if __name__ == "__main__":
#     main = Main()
#     main.display_main_menu()
