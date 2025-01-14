import sys
import os

# Add the root directory of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the modules
from employee.manager import Manager
from employee.users_database import UserManager, UserExistsError, UserNotFoundError


class TestManager(unittest.TestCase):
    def setUp(self):
        # Initialize a mock user manager and manager instance
        self.mock_user_manager = UserManager("mock_users_database.json")
        self.manager = Manager(
            user_data={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
            },
            hiring_date="2025-01-01",
            salary=50000,
            db_manager=self.mock_user_manager,
        )

    def test_manager_creation(self):
        """Test that manager is created properly."""
        self.assertEqual(self.manager.role, "Manager")

    def test_assign_role(self):
        """Test role assignment for an employee."""
        self.manager.assign_role("employee@example.com", "Manager")
        # Add assertion based on how your mock user manager works
        # Example: check if the role of the employee is updated

    def test_login_success(self):
        """Test manager login with correct credentials."""
        # Add your mock logic to check login success
        self.assertTrue(self.manager.login("john.doe@example.com", "correct_password"))

    def test_login_failure(self):
        """Test manager login with incorrect credentials."""
        self.assertFalse(
            self.manager.login("wrong.email@example.com", "wrong_password")
        )
