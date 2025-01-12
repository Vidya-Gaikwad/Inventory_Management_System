import bcrypt
import json
from employee import Employee
from users_database import UserManager, UserExistsError, UserNotFoundError

# Example imports (replace later with actual inventory and product modules)
# from inventory_manager import InventoryManager  # Placeholder
# from product import Product  # Placeholder

import bcrypt
from users_database import UserManager, UserNotFoundError


class Manager(Employee):
    def __init__(
        self,
        user_data: dict,
        hiring_date: str,
        salary: float,
        db_manager: UserManager,
        role: str = "Manager",
    ):
        super().__init__(user_data, hiring_date, salary, db_manager)
        self.role = role

    def assign_role(self, employee_email: str, role: str):
        """Assign a role to an employee. Give credentials to CRUD."""
        if self.role != "Manager":
            print("Only Managers can assign roles.")
            return False

        employee = self.db_manager.find_user(employee_email)
        if not employee:
            print(f"User {employee_email} not found.")
            return False

        employee["role"] = role
        self.db_manager.save_users()  # Save the updated user data
        print(f"Role {role} assigned to {employee_email}.")
        return True

    def login(self, email, password):
        """Validate the manager's login by checking if the provided email and password match."""
        try:
            user_data = self.db_manager.find_user(email)
            if not user_data:
                print(f"User with email {email} not found.")
                return False

            if self.validate_login(password, user_data["password"]):
                if user_data.get("role") == "Manager":
                    print(
                        f"Login successful for {user_data['first_name']} {user_data['last_name']}"
                    )
                    self.logged_in_user = user_data
                    return True
                else:
                    print("Access denied. Only Managers can log in.")
                    return False
            else:
                print("Incorrect password.")
                return False

        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def validate_login(self, entered_password, stored_password) -> bool:
        """Compare entered password with stored password."""
        return bcrypt.checkpw(entered_password.encode(), stored_password.encode())

    # Refactor the Inventory Manager Class with the correct data and methods
    # class InventoryManager:
    #     def add_product(self, product):
    #         print(f"Product added to inventory: {product.product_data}")
    #         return True

    #     def update_product(self, product_id, updated_data):
    #         print(f"Product {product_id} updated with data: {updated_data}")
    #         return True

    #     def delete_product(self, product_id):
    #         print(f"Product {product_id} deleted from inventory.")
    #         return True

    # Refactor the Product class with the correct data and methods
    # class Product:
    #     def __init__(self, product_data):
    #         self.product_data = product_data
    #         print(f"Product created with data: {product_data}")

    #     def manage_inventory(self, action, *args, **kwargs):
    #         """Allow only managers to perform inventory-related actions."""
    #         if self.can_crud():
    #             if action == "add":
    #                 return self.add_product(*args, **kwargs)
    #             elif action == "update":
    #                 return self.update_product(*args, **kwargs)
    #             elif action == "delete":
    #                 return self.delete_product(*args, **kwargs)
    #         else:
    #             print("Only Managers can perform this action.")

    #     def add_product(self, product_data):
    #         """Add a new product to the inventory."""
    #         try:
    #             product = Product(product_data)  # Mocked Product class
    #             return self.inventory_manager.add_product(product)
    #         except Exception as e:
    #             print(f"Error adding product: {e}")
    #             return None

    #     def update_product(self, product_id, updated_data):
    #         """Update product information in the inventory."""
    #         try:
    #             return self.inventory_manager.update_product(product_id, updated_data)
    #         except Exception as e:
    #             print(f"Error updating product: {e}")
    #             return None

    #     def delete_product(self, product_id):
    #         """Delete a product from the inventory."""
    #         try:
    #             return self.inventory_manager.delete_product(product_id)
    #         except Exception as e:
    #             print(f"Error deleting product: {e}")
    #             return None


# Define user_data
# user_data = {
#    "first_name": "Juan",
#    "last_name": "Pérez",
#    "email": "juan.perez@example.com",
#    "password": "securepassword",
#    "role": "Manager",
#    "phone_number": "555-1234",
#    "address": "Calle Ficticia 123, Ciudad de México, CDMX",
#    "birthday": "15/05/1990",
# }

# Initialize the user manager
# user_manager = UserManager(db_path="users_database.json")

# Create a manager instance with the user_data
# manager = Manager(user_data, "01/01/2025", salary=50000, db_manager=user_manager)

# Now, login the manager (simulating a login process)
# if manager.login("juan.perez@example.com", "securepassword"):
# If login is successful, manager can manage employees
#    manager.assign_role("santos@example.com", "Manager")  # Assign the role of "Manager"

#    employee_data = {
#        "first_name": "Carlos",
#        "last_name": "Santos",
#        "email": "santos@example.com",
#        "password": "securepassword",
#        "role": "Logistics Administrator",
#    }

# Add an employee (only if manager is logged in)
#    manager.manage_employees("add", employee_data)

# Add a product to inventory (mocked)
# product_data = {"product_name": "Laptop", "price": 1000.0, "quantity": 10}
# manager.manage_inventory("add", product_data)
