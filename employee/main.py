from registration import Registration
from users_database import UserManager
from login import Login
from manager import Manager
from employee import Employee

# from inventory.inventory_manager import InventoryManager
# from inventory.product import Product


class Main:
    """Main program to manage the Inventory Manager system."""

    def __init__(self):
        self.user_manager = UserManager()  # Manages user database

    def display_main_menu(self):
        """Display the main menu."""
        while True:
            print("\nWelcome to Inventory Manager")
            print("1. Register a user")
            print("2. Login (users and employees)")
            print("3. Forgot password")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ").strip()
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                self.forgot_password()  # New option to change password if forgotten
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def register_user(self):
        """Register a new user."""
        try:
            registration = Registration(
                self.user_manager
            )  # Create instance of Registration class
            registration.register_user()  # Call register_user() on the instance
            print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def login_user(self):
        """Handle user login."""
        try:
            login_data = Login.prompt_user_input()
            user = self.user_manager.find_user(login_data["email"])

            if bcrypt.checkpw(
                login_data["password"].encode(), user["password"].encode()
            ):
                print("Login successful!")

                if user["role"] == "Manager":
                    manager = Manager(user, hiring_date, salary, self.user_manager)
                    self.manager_menu(manager)
                else:
                    employee = Employee(user)
                    self.employee_menu(employee)
            else:
                print("Incorrect password.")
                choice = (
                    input("Do you want to recover your password? (y/n): ")
                    .strip()
                    .lower()
                )
                if choice == "y":
                    self.forgot_password()  # Call password recovery
                else:
                    print("Returning to main menu.")
        except KeyError:
            print("User not found.")

    def forgot_password(self):
        """Handle forgot password scenario."""
        email = input(
            "Enter your email address: "
        ).strip()  # Strip any extra whitespace

        # Check if the user exists in the database
        user_data = self.user_manager.find_user(email)

        if user_data:
            print(f"A password reset email has been sent to {email}.")
            # Here, you can implement further actions for password recovery (e.g., reset link, etc.)
            # For now, let's just simulate sending an email.
        else:
            print(f"No user found with that email address.")

    def manager_menu(self, manager):
        """Menu for managers with CRUD permissions."""
        print(f"\nWelcome, Manager {manager.user_data['first_name']}!")
        while True:
            print("\nManager Menu:")
            print("1. Manage employees (CRUD)")
            print("2. Manage inventory (CRUD)")
            print("3. Manage products (CRUD)")
            print("4. Logout")

            choice = input("Enter your choice (1-4): ").strip()
            if choice == "1":
                self.manage_employees(manager)
            elif choice == "2":
                self.manage_inventory(manager)
            elif choice == "3":
                self.manage_products(manager)
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_employees(self, manager):
        """Manager CRUD menu for employees."""
        print("\nEmployee Management Menu:")
        print("1. Add an employee")
        print("2. Update an employee")
        print("3. Delete an employee")
        print("4. Find an employee")
        print("5. Assign an employee role")
        print("6. Back to main menu")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            manager.add_employee()
        elif choice == "2":
            manager.update_employee()
        elif choice == "3":
            manager.delete_employee()
        elif choice == "4":
            manager.find_employee()
        elif choice == "5":
            manager.assign_role()
        elif choice == "6":
            return
        else:
            print("Invalid choice. Returning to main menu.")

    def access_inventory(self, inventory_manager):

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