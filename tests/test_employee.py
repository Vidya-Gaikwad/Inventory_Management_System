import pytest
from employee import Employee


# Mock version of the UserManager class for testing purposes
class MockUserManager:
    def __init__(self):
        # Simulate a database with a list of dictionaries
        self.users = []

    def add_user(self, user_data):
        # Check for duplicate emails
        for user in self.users:
            if user["email"] == user_data["email"]:
                raise Exception(f"User with email {user_data['email']} already exists.")
        self.users.append(user_data)

    def find_user(self, email):
        # Find a user by email
        for user in self.users:
            if user["email"] == email:
                return user
        return None

    def update_user(self, email, update_data):
        # Update user details
        for i, user in enumerate(self.users):
            if user["email"] == email:
                self.users[i].update(update_data)
                return "User updated successfully."
        raise Exception(f"User with email {email} not found.")

    def delete_user(self, email):
        # Delete a user by email
        for i, user in enumerate(self.users):
            if user["email"] == email:
                del self.users[i]
                return "User deleted successfully."
        raise Exception(f"User with email {email} not found.")


# Fixture to create a mock user manager
@pytest.fixture
def mock_user_manager():
    return MockUserManager()


# Fixture to define employee data (which simulates the input data for an employee)
@pytest.fixture
def employee_data():
    return {
        "first_name": "Graciela",
        "last_name": "Pereira",
        "email": "graciela@example.com",
        "phone_number": "+1234567890",
        "address": {"street": "123 Main St", "house_number": "5A", "city": "New York"},
        "birthday": "10/05/1990",
    }


# The actual test class
class TestEmployee:

    # Test case for adding an employee
    def test_add_employee(self, mock_user_manager, employee_data):
        # Create an employee instance
        employee = Employee(
            user_data=employee_data,
            hiring_date="10/05/2022",
            salary=45300,
            db_manager=mock_user_manager,
        )

        # Save the employee to the "mock" database
        employee.save_to_database()

        # Retrieve the employee from the mock database
        result = mock_user_manager.find_user(employee_data["email"])

        # The expected result after saving the employee
        expected_value = {
            "first_name": "Graciela",
            "last_name": "Pereira",
            "email": "graciela@example.com",
            "phone_number": "+1234567890",
            "address": {
                "street": "123 Main St",
                "house_number": "5A",
                "city": "New York",
            },
            "birthday": "10/05/1990",
            "hiring_date": "10/05/2022",
            "salary": 45300,
        }

        # Assert that the result matches the expected value
        assert result == expected_value

    # Test case for updating an employee
    def test_update_employee(self, mock_user_manager, employee_data):
        # Create an employee instance
        employee = Employee(
            user_data=employee_data,
            hiring_date="10/05/2022",
            salary=47000,
            db_manager=mock_user_manager,
        )

        # Save the employee to the mock database
        employee.save_to_database()

        # Now update the employee's data
        updated_data = {
            "birthday": "15/06/1990",  # Update birthday as an example
            "salary": 47000,  # New salary
        }

        # Update the employee in the database
        employee.update_to_database()

        # Retrieve the updated employee from the mock database
        result = mock_user_manager.find_user(employee_data["email"])

        # The expected updated result
        expected_value = {
            "first_name": "Graciela",
            "last_name": "Pereira",
            "email": "graciela@example.com",
            "phone_number": "+1234567890",
            "address": {
                "street": "123 Main St",
                "house_number": "5A",
                "city": "New York",
            },
            "birthday": "10/05/1990",  # Updated birthday
            "hiring_date": "10/05/2022",
            "salary": 47000,  # Updated salary
        }

        # Assert that the updated data matches the expected result
        assert result == expected_value
