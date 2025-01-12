import bcrypt
from users_database import UserManager
from validate_user import ValidationError


class Login:
    """User login, password, and recovery options."""

    def __init__(self, user_manager):
        self.user_manager = user_manager

    def hash_password(self, password):
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def validate_password(self, input_password, stored_hashed_password):
        """
        Validate the input password by comparing its hash with the stored hash.
        """
        # bcrypt will handle the hashing and comparison internally
        return bcrypt.checkpw(input_password.encode(), stored_hashed_password)

    def validate_email_password(self, email, password):
        """
        Validate the email and password against the database.
        Return True if valid, otherwise False.
        """
        for user in self.user_manager.get_all_users():
            if user["email"] == email:
                # Check the password against the stored hashed password
                if self.validate_password(password, user["password"]):
                    return True
        return False

    def login(self):
        """
        Handle user login with a maximum of 5 attempts.
        """
        attempts = 0
        max_attempts = 5

        while attempts < max_attempts:
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()

            if self.validate_email_password(email, password):
                print("Login successful.")
                return True
            else:
                attempts += 1
                print(
                    f"Invalid email or password. Attempts left: {max_attempts - attempts}"
                )

        print("Too many failed login attempts. Try again later.")
        return False


class ManagerAccessControl:
    def __init__(self, user_data):
        self.user_data = user_data

    def can_crud(self):
        """Check if the logged-in user has CRUD permissions (Manager only)."""
        if self.user_data.get("role") == "Manager":
            return True
        return False
