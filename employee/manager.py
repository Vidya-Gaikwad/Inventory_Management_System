import bcrypt
from employee import Employee
from users_database import UserManager
from validate_user import UserValidator, ValidationError


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

    def login(self, email, password):
        """Validate the manager's login."""
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

    def hash_password(self, password):
        """Hash a password using bcrypt and convert to string (UTF-8)."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")  # Convert bytes to string (UTF-8)

    def assign_role(self, employee_email: str, role: str):
        """Assign a role to an employee."""
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


# Sample employee data for 3 employees
# manager_data = {
#    "first_name": "Pedro",
#    "last_name": "Pérez",
#    "email": "juan.perez@example.com",
#    "password": "securepassword",  # Password will be hashed
#    "role": "Manager",
#    "phone_number": "555-1234",
#    "address": "Calle Ficticia 123, Ciudad de México, CDMX",
#    "birthday": "15/05/1990",
# }

# inventory_admin_data = {
#    "first_name": "Carlos",
#    "last_name": "Ramirez",
#    "email": "carlos.ramirez@example.com",
#    "password": "password123",  # Password will be hashed
#    "role": "Inventory Admin",
#    "phone_number": "555-5678",
#    "address": "Avenida 2, Ciudad de México, CDMX",
#    "birthday": "20/11/1985",
# }

# logistic_employee_data = {
#    "first_name": "Ana",
#    "last_name": "Gomez",
#    "email": "ana.gomez@example.com",
#    "password": "logistic123",  # Password will be hashed
#    "role": "Logistic Employee",
#    "phone_number": "555-8765",
#    "address": "Calle Falsa 456, Ciudad de México, CDMX",
#    "birthday": "25/03/1992",
# }

# Initialize the user manager (assumes you have a path for the database)
# user_manager = UserManager(db_path="users_database.json")

# Hash the passwords for each employee
# manager_data["password"] = Manager.hash_password(Manager, manager_data["password"])
# inventory_admin_data["password"] = Manager.hash_password(
#    Manager, inventory_admin_data["password"]
# )
# logistic_employee_data["password"] = Manager.hash_password(
#    Manager, logistic_employee_data["password"]
# )

# Create instances for each role
# manager = Manager(manager_data, "01/01/2025", salary=50000, db_manager=user_manager)
# inventory_admin = Manager(
#    inventory_admin_data,
#    "01/01/2025",
#    salary=30000,
#    db_manager=user_manager,
#    role="Inventory Admin",
# )
# logistic_employee = Manager(
#    logistic_employee_data,
#    "01/01/2025",
#    salary=20000,
#    db_manager=user_manager,
#    role="Logistic Employee",
# )

# Add users to the database
# user_manager.add_user(manager_data)
# user_manager.add_user(inventory_admin_data)
# user_manager.add_user(logistic_employee_data)

# Now, login the manager (simulating login process)
# if manager.login("juan.perez@example.com", "securepassword"):
# Assign a role to an employee (for example)
#    employee_email = "ana.gomez@example.com"  # Example employee email
#    if manager.assign_role(employee_email, "Logistic Employee"):
#        print(f"Role 'Logistic Employee' assigned to {employee_email}.")
#    else:
#        print("Failed to assign role.")
# else:
#    print("Manager login failed.")

# Commented-out sections for reference
# Refactor the Inventory Manager Class with the correct data and methods
# class InventoryManager:
#     def add_product(self, product):
#         print(f"Product added to inventory: {product.product_data}")
#         return True
#
#     def update_product(self, product_id, updated_data):
#         print(f"Product {product_id} updated with data: {updated_data}")
#         return True
#
#     def delete_product(self, product_id):
#         print(f"Product {product_id} deleted from inventory.")
#         return True

# Refactor the Product class with the correct data and methods
# class Product:
#     def __init__(self, product_data):
#         self.product_data = product_data
#         print(f"Product created with data: {product_data}")
#
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
#
#     def add_product(self, product_data):
#         """Add a new product to the inventory."""
#         try:
#             product = Product(product_data)  # Mocked Product class
#             return self.inventory_manager.add_product(product)
#         except Exception as e:
#             print(f"Error adding product: {e}")
#             return None
#
#     def update_product(self, product_id, updated_data):
#         """Update product information in the inventory."""
#         try:
#             return self.inventory_manager.update_product(product_id, updated_data)
#         except Exception as e:
#             print(f"Error updating product: {e}")
#             return None
#
#     def delete_product(self, product_id):
#         """Delete a product from the inventory."""
#         try:
#             return self.inventory_manager.delete_product(product_id)
#         except Exception as e:
#             print(f"Error deleting product: {e}")
#             return None
