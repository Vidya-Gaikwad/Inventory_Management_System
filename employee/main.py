import bcrypt
from users_database import UserManager
from login import Login
from manager import Manager
from employee import Employee


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
            print("3. Exit")

            choice = input("Enter your choice (1-3): ").strip()
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def register_user(self):
        """Register a new user."""
        try:
            registration = Registration(
                self.user_manager
            )  # Assuming Registration is defined elsewhere
            registration.register_user()  # Call register_user() on the instance
            print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def login_user(self):
        """Handle user login."""
        try:
            login = Login(
                self.user_manager
            )  # Instantiate the Login class with UserManager
            if login.login():  # Check if login is successful
                email = input("Enter your email: ").strip()
                user = self.user_manager.get_user_by_email(email)

                if user["role"] == "Manager":
                    manager = Manager(user)
                    self.manager_menu(manager)
                else:
                    employee = Employee(user)
                    self.employee_menu(employee)
            else:
                print("Login failed, returning to main menu.")
        except KeyError:
            print("User not found.")

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

    def manage_inventory(self, manager):
        """Manager CRUD menu for inventory."""
        print("\nInventory Management Menu:")
        print("1. Add a product to inventory")
        print("2. Update a product in inventory")
        print("3. Delete a product from inventory")
        print("4. View inventory")
        print("5. Back to manager menu")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            manager.add_to_inventory()
        elif choice == "2":
            manager.update_inventory()
        elif choice == "3":
            manager.delete_from_inventory()
        elif choice == "4":
            print("Displaying inventory...")
            # self.inventory.display_inventory()
        elif choice == "5":
            return
        else:
            print("Invalid choice. Returning to main menu.")

    def manage_products(self, manager):
        """Manager CRUD menu for products."""
        print("\nProduct Management Menu:")
        print("1. Add a product")
        print("2. Update a product")
        print("3. Delete a product")
        print("4. View all products")
        print("5. Back to manager menu")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            manager.add_product()
        elif choice == "2":
            manager.update_product()
        elif choice == "3":
            manager.delete_product()
        elif choice == "4":
            print("Displaying products...")
            # self.product.display_products()
        elif choice == "5":
            return
        else:
            print("Invalid choice. Returning to main menu.")


if __name__ == "__main__":
    main = Main()
    main.display_main_menu()
