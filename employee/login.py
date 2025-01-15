import bcrypt
import base64
from users_database import UserManager


class Login:
    """User login, password, and recovery options."""

    def __init__(self, user_manager):
        self.user_manager = user_manager

    def validate_password(self, input_password, stored_hashed_password):
        """
        Validate the input password by comparing its hash with the stored hash.
        Ensure both inputs are byte objects before passing to bcrypt.
        """
        # Decode the base64 encoded stored hashed password to bytes
        stored_hashed_password = base64.b64decode(stored_hashed_password)

        # Validate the password using bcrypt
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

    def password_recovery(self, email):
        """Simulate sending a password recovery email."""
        print(f"We sent a password recovery link to {email}.")

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
