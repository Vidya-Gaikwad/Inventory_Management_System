import bcrypt
from users_database import UserManager


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
        return bcrypt.checkpw(input_password.encode(), stored_hashed_password)

    def validate_email_password(self, email, password):
        """
        Validate the email and password against the database.
        Return True if valid, otherwise False.
        """
        for user in self.user_manager.get_all_users():
            if user["email"] == email:
                if self.validate_password(password, user["password"]):
                    return True
        return False

    def forgot_password(self):
        """Handle forgot password scenario."""
        email = (
            input("Enter your email address: ").strip().lower()
        )  # Normalize email input
        print(f"Entered email: {email}")  # Debugging output

        # Check if the user exists in the database
        user_data = self.user_manager.find_user(email)

        if user_data:
            print(f"A password reset email has been sent to {email}.")
            # Further actions for password recovery (e.g., sending reset instructions).
        else:
            print(f"No user found with that email address.")

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

    @staticmethod
    def prompt_user_input():
        """
        This is a static method to prompt the user for login credentials.
        You can use this to input email and password directly when logging in.
        """
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        return {"email": email, "password": password}
