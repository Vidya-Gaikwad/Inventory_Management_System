import bcrypt
import json
from employee.employee import Employee
from employee.users_database import UserManager, UserExistsError, UserNotFoundError

# Example imports (replace later with actual inventory and product modules)
# from inventory_manager import InventoryManager  # Placeholder
# from product import Product  # Placeholder


class Manager(Employee):
    def __init__(
        self,
        user_data: dict,
        hiring_date: str,
        salary: float,
        db_manager: UserManager,
        role: str = "Manager",
    ):
        # Inherit from Employee
        super().__init__(user_data, hiring_date, salary, db_manager)
        self.role = role  # A manager has a specific role

    def assign_role(self, employee_email: str, role: str):
        """Assign a role to an employee. Give credentials to CRUD"""
        if self.role == "Manager":  # Only managers can assign roles
            employee = self.db_manager.find_user(employee_email)
            if employee:
                employee["role"] = role
                self.db_manager.save_users()  # Save the updated user data
                print(f"Role {role} assigned to {employee_email}.")
                return True
            else:
                print(f"User {employee_email} not found.")
                return False
        else:
            print("Only Managers can assign roles.")
            return False

    def manage_employees(self, action, *args, **kwargs):
        """Allow managers to manage employees."""
        if self.role == "Manager":
            if action == "add":
                return self.add_employee(*args, **kwargs)
            elif action == "update":
                return self.update_employee(*args, **kwargs)
            elif action == "delete":
                return self.delete_employee(*args, **kwargs)
        else:
            print("Only Managers can perform this action.")
        return False

    def add_employee(self, employee_data):
        """Add an employee to the system."""
        employee = Employee(
            employee_data,
            hiring_date="01/01/2025",
            salary=50000,
            db_manager=self.db_manager,
        )
        return employee.save_to_database()

    def update_employee(self, email, updated_data):
        """Update an existing employee's information."""
        employee = self.db_manager.find_user(email)
        if employee:
            # Update the employee's data here
            employee.update_to_database()
            return True
        return False

    def delete_employee(self, email):
        """Delete an employee by email."""
        employee = self.db_manager.find_user(email)
        if employee:
            # Delete the employee from the database
            self.db_manager.delete_user(email)
            return True
        return False

    def login(self, email, password):
        """Validate the manager's login by checking if the provided email and password match."""
        user_data = self.db_manager.find_user(email)
        if user_data and self.validate_login(password, user_data["password"]):
            if (
                user_data.get("role") == self.role
            ):  # Check if the user has the "Manager" role
                print(f"Login successful for {email}")
                self.logged_in_user = user_data  # Store the logged-in user
                return True
            else:
                print("Access denied. Only Managers can log in.")
        print("Invalid login. Acces only for Managers")
        return False

    def validate_login(self, entered_password, stored_password) -> bool:
        """Compare entered password with stored password."""
        return bcrypt.checkpw(entered_password.encode(), stored_password.encode())