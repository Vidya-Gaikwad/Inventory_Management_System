from registration2 import Registration
from users_database import UserManager
from login import Login
from manager import Manager
from employee import Employee
from validate_user import UserValidator, ValidationError
import random
import string


class Main:
    """Main program to manage the Inventory Manager system."""

    def __init__(self):
        self.user_manager = UserManager()  # Manages user database
        self.user_validator = UserValidator()  # Validates user input
        self.manager = None  # Initially, no manager is logged in

    def display_main_menu(self):
        """Display the main menu."""
        while True:
            print("\n................. Welcome to Inventory Manager .................")
            print("1. Register a user")
            print("2. Login (users and employees)")
            print("3. Forgot password")
            print("4. Go back")
            print("-" * 75)

            choice = input("Enter your choice (1-4): ").strip()
            print("-" * 75)
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
            registration = Registration(self.user_manager, self.user_validator)
            registration.register_user()
            print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def login_user(self):
        """Handle user login."""
        try:
            login_data = Login.prompt_user_input()
            user = self.user_manager.find_user(login_data["email"])

            if user is None:
                # If the user is not found, handle the error
                print("User not found.")
                return

            if user["role"] == "Manager":
                self.manager = Manager(
                    user,
                    hiring_date=user.get("hiring_date"),
                    salary=user.get("salary"),
                    db_manager=self.user_manager,
                )
                self.manager_menu(self.manager)  # Now passing the initialized manager
            else:
                employee = Employee(
                    user,
                    hiring_date=user.get("hiring_date"),
                    salary=user.get("salary"),
                    db_manager=self.user_manager,
                )
                self.employee_menu(employee)
        except KeyError:
            print("Error during login process.")

    def forgot_password(self):
        """Handle forgot password scenario."""
        email = input("Enter your email address: ").strip()

        user_data = self.user_manager.find_user(email)

        if user_data:
            print(f"A password reset email has been sent to {email}.")
        else:
            print(f"No user found with that email address.")

    def manager_menu(self, manager):
        """Manager's menu to perform manager-specific actions."""
        while True:
            print("\n.......... Manager's Menu ..........")
            print("1. Manage Employees")
            print("2. Access Inventory")
            print("3. Log out")
            print("-" * 75)

            choice = input("Enter your choice (1-3): ").strip()
            print("-" * 75)

            if choice == "1":
                self.manage_employees(manager)  # Call the method to manage employees
            elif choice == "2":
                self.access_inventory(manager.inventory_manager)  # Access the inventory
            elif choice == "3":
                print("Logging out...")
                self.manager = None  # Log out the manager
                break  # Exit from manager's menu and log out
            else:
                print("Invalid choice. Please try again.")

    def find_employee(self, manager, email):
        """Wrapper method to find an employee via Manager."""
        if manager:
            manager.find_employee(email)

    def manage_employees(self, manager):
        """Manage Employees submenu."""
        while True:
            print("\n................. Manage Employees .................")
            print("1. Add an employee")
            print("2. Update an employee")
            print("3. Delete an employee")
            print("4. Find an employee")
            print("5. Assign an employee role")
            print("6. Go back")
            print("-" * 75)

            choice = input("Enter your choice (1-6): ").strip()
            print("-" * 75)

            if choice == "1":
                self.add_employee(manager)
            elif choice == "2":
                self.update_employee(manager)
            elif choice == "3":
                self.delete_employee(manager)
            elif choice == "4":
                email = input("Enter employee's email: ").strip()
                self.find_employee(
                    manager, email
                )  # Now correctly passing manager to find_employee
            elif choice == "5":
                self.assign_employee_role(manager)
            elif choice == "6":
                break  # Go back to the manager menu
            else:
                print("Invalid choice. Please try again.")

    def generate_random_password(self, length=8):
        """Generate a random password with at least 1 uppercase, 1 lowercase, and 1 special character."""
        if length < 8:
            raise ValueError("Password length must be at least 8 characters.")

        # Define the character sets
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        special_characters = string.punctuation
        digits = string.digits

        # Ensure the password has at least 1 uppercase, 1 lowercase, and 1 special character
        password = [
            random.choice(uppercase_letters),
            random.choice(lowercase_letters),
            random.choice(special_characters),
        ]

        # Fill the remaining characters with a mix of all possible characters
        all_characters = (
            uppercase_letters + lowercase_letters + special_characters + digits
        )
        password += random.choices(all_characters, k=length - len(password))

        # Shuffle the password list to ensure randomness
        random.shuffle(password)

        # Convert the list back to a string and return
        return "".join(password)

    def add_employee(self, manager):
        """Add a new employee with extended data."""
        first_name = input("Enter First Name: ").strip().casefold()
        last_name = input("Enter Last Name: ").strip().casefold()
        email = input("Enter Email: ").strip()
        phone_number = input("Enter Phone Number: ").strip()
        birthday = input("Enter Birthday(Format DD/MM/YYYY): ").strip()
        hiring_date = input("Enter Hiring Date(Format DD/MM/YYYY): ").strip()
        salary = float(input("Enter Salary: ").strip())

        # Collecting address details
        print("\nAddress Information:")
        street = input("Enter Street: ").strip()
        house_number = input("Enter House Number: ").strip()
        city = input("Enter City: ").strip()
        zip_code = input("Enter Zip Code: ").strip()
        country = input("Enter Country: ").strip()

        # Role selection submenu
        print("\nSelect Role for the employee:")
        print("1. Manager")
        print("2. Admin")
        print("3. Logistics Employee")
        print("4. Sales Employee")
        role_choice = input("Enter your choice (1-4): ").strip()

        if role_choice == "1":
            role = "Manager"
        elif role_choice == "2":
            role = "Admin"
        elif role_choice == "3":
            role = "Logistics Employee"
        elif role_choice == "4":
            role = "Sales Employee"
        else:
            print("Invalid choice, defaulting to 'Employee'")
            role = "Employee"  # Default role if the input is invalid

        # Generate a random provisional password
        provisional_password = self.generate_random_password()

        # Create employee data dictionary
        employee_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": provisional_password,
            "phone_number": phone_number,
            "birthday": birthday,
            "address": {
                "street": street,
                "house_number": house_number,
                "city": city,
                "zip_code": zip_code,
                "country": country,
            },
            "role": role,  # Set the chosen role
        }

        # Add the employee to the manager's database
        try:
            self.user_manager.add_user(
                employee_data
            )  # This saves the employee to the database
            print("\nEmployee added successfully!")
            print(
                f"Provisional password for {first_name} {last_name}: {provisional_password}"
            )
        except UserExistsError as e:
            print(f"Error: {e}")

    def update_employee(self, manager):
        """Update employee information."""
        email = input("Enter the email of the employee to update: ").strip()
        updated_data = {}

        # Loop to show the fields to update
        while True:
            print("\n........... Update Employee ..........")
            print("1. Update First Name")
            print("2. Update Last Name")
            print("3. Update Email")
            print("4. Update Phone Number")
            print("5. Update Birthday")
            print("6. Update Address")
            print("7. Update Hiring Date")
            print("8. Update Salary")
            print("9. Update Role")
            print("0. Cancel")
            print("-" * 50)

            choice = input("Enter the number of the field you want to update: ").strip()

            if choice == "1":
                updated_data["first_name"] = input("Enter the new First Name: ").strip()
            elif choice == "2":
                updated_data["last_name"] = input("Enter the new Last Name: ").strip()
            elif choice == "3":
                updated_data["email"] = input("Enter the new Email: ").strip()
            elif choice == "4":
                updated_data["phone_number"] = input(
                    "Enter the new Phone Number: "
                ).strip()
            elif choice == "5":
                updated_data["birthday"] = input(
                    "Enter the new Birthday (DD/MM/YYYY): "
                ).strip()
            elif choice == "6":
                # Address submenu
                updated_data["address"] = self.update_address()
            elif choice == "7":
                updated_data["hiring_date"] = input(
                    "Enter the new Hiring Date (DD/MM/YYYY): "
                ).strip()
            elif choice == "8":
                updated_data["salary"] = float(input("Enter the new Salary: ").strip())
            elif choice == "9":
                updated_data["role"] = input("Enter the new Role: ").strip()
            elif choice == "0":
                print("Update cancelled.")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

        # Proceed to update the employee data
        if updated_data:
            try:
                manager.update_employee(email, updated_data)
                print(f"Employee {email} updated successfully.")
            except Exception as e:
                print(f"Error updating employee {email}: {str(e)}")

    def update_address(self):
        """Prompt the manager to update the address."""
        print("\n........... Update Address ..........")

        address_data = {}  # Initialize empty address data here

        while True:
            print("\n........... Address Submenu ..........")
            print("1. Update Street")
            print("2. Update House Number")
            print("3. Update City")
            print("4. Update Zip Code")
            print("5. Update Country")
            print("6. Go Back")
            print("-" * 50)

            # Get user's choice for updating address
            choice = input(
                "Enter the number of the part of the address to update: "
            ).strip()

            if choice == "1":
                address_data["street"] = input("Enter the new Street: ").strip()
            elif choice == "2":
                address_data["house_number"] = input(
                    "Enter the new House Number: "
                ).strip()
            elif choice == "3":
                address_data["city"] = input("Enter the new City: ").strip()
            elif choice == "4":
                address_data["zip_code"] = input("Enter the new Zip Code: ").strip()
            elif choice == "5":
                address_data["country"] = input("Enter the new Country: ").strip()
            elif choice == "6":
                break  # Go back to the main update menu
            else:
                print("Invalid choice. Please try again.")
                continue

        return address_data

    def assign_employee_role(self, manager):
        """Assign a role to an employee."""
        email = input("Enter the email of the employee to assign a role: ")
        role = input("Enter the role to assign: ")
        manager.assign_role(email, role)

    def access_inventory(self, inventory_manager):
        """Inventory access and modification menu."""
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
                self.modify_inventory(inventory_manager)
            elif choice == "2":
                self.search_product(inventory_manager)
            elif choice == "3":
                self.modify_product(inventory_manager)
            elif choice == "4":
                self.filter_products(inventory_manager)
            elif choice == "5":
                print("Exiting the Inventory Management System.")
                break
            else:
                print("Invalid choice. Please try again.")

    def modify_inventory(self, inventory_manager):
        """Modify/Update inventory submenu."""
        while True:
            print("\n.......... Modify/Update Inventory ..........")
            print("1. Display all products")
            print("2. Get total inventory value")
            print("3. Add Product")
            print("4. Update Product")
            print("5. Remove Product")
            print("6. Go back")
            print("-" * 75)
            choice = input("Enter your choice (1-6): ")
            print("-" * 75)

            if choice == "1":
                all_products = inventory_manager.read_product_data()
                print("Available products in inventory are: ")
                for item, value in all_products.items():
                    print(
                        f"-- {all_products[item]['product_name']}, Price: ${all_products[item]['price']:.2f}"
                    )
            elif choice == "2":
                print("-" * 75)
                print(
                    f"Total inventory value is ${inventory_manager.get_total_inventory_value()}"
                )
            elif choice == "3":
                self.add_product(inventory_manager)
            elif choice == "4":
                self.update_product(inventory_manager)
            elif choice == "5":
                self.remove_product(inventory_manager)
            elif choice == "6":
                break  # Go back to the inventory menu
            else:
                print("Invalid option. Please try again.")

    def add_product(self, inventory_manager):
        """Add a product to the inventory."""
        product_id = input("Enter Product ID (format: A123): ")
        product_name = input("Enter Product Name: ")
        quantity = float(input("Enter Quantity: "))
        price = float(input("Enter Price: "))
        category = input("Enter Category (Electronics, Furniture, Clothes, Footwear): ")
        product = Product(product_name, quantity, price, category)
        try:
            inventory_manager.add_product(product_id, product)
        except Exception as e:
            print(f"Error: {e}")

    def update_product(self, inventory_manager):
        """Update product information."""
        product_id = input("Enter Product ID to update: ")
        product_name = input("Enter New Product Name: ")
        quantity = float(input("Enter New Quantity: "))
        price = float(input("Enter New Price: "))
        category = input("Enter New Category: ")
        updated_product = Product(product_name, quantity, price, category)
        try:
            if inventory_manager.update_product(product_id, updated_product):
                print("Product updated successfully.")
            else:
                print("Product not found.")
        except Exception as e:
            print(f"Error: {e}")

    def remove_product(self, inventory_manager):
        """Remove a product from the inventory."""
        product_id = input("Enter Product ID to remove: ")
        try:
            inventory_manager.remove_product(product_id)
        except Exception as e:
            print(f"Error: {e}")

    def search_product(self, inventory_manager):
        """Search a product by ID or name."""
        while True:
            print("\n1. Search Product by ID")
            print("2. Search Product by Name")
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
                product_found = inventory_manager.search_product_by_name(product_name)
                if product_found:
                    print(f"Name: {product_found['product_name']}")
                    print(f"Quantity: {product_found['quantity']}")
                    print(f"Price: {product_found['price']}")
                    print(f"Category: {product_found['category']}")
                else:
                    print("Product not found.")
            elif choice == "3":
                break  # Go back to the main inventory menu

    def filter_products(self, inventory_manager):
        """Filter products based on certain criteria."""
        while True:
            print("\n1. Filter products by price")
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
                products_found = inventory_manager.filter_product_with_low_quantity()
                try:
                    for items in products_found:
                        print(
                            f"Product_name: {items[1]['product_name']}--- Quantity: {items[1]['quantity']}"
                        )
                except TypeError:
                    print("No products with low quantity found.")
            elif choice == "4":
                break  # Go back to the inventory menu
            else:
                print("Invalid option! Please try again.")


if __name__ == "__main__":
    main = Main()
    main.display_main_menu()
