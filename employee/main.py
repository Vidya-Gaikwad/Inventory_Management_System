from registration import Registration
from users_database import UserManager, UserExistsError, UserNotFoundError
from manager import Manager
import bcrypt


class Main:
    """Main program to manage the Inventory Manager system."""

    def __init__(self):
        self.user_manager = UserManager()

    def display_main_menu(self):
        """Display the main menu."""
        while True:
            print("\nWelcome to Inventory Manager")
            print("1. Register a user")
            print("2. Login (users and employees)")
            print("3. Exit")

            choice = input("Enter your choice (1-3): ").strip()
            if choice == "1":
                self.register_new_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def register_new_user(self):
        """Register a new user."""
        registration = Registration(self.user_manager)  # Create an instance
        try:
            success = registration.register_user()  # Calls register_user with validation
            if success:
                print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def login_user(self):
        """Handle user login."""
        try:
            login_data = {
                "email": input("Enter your email: ").strip(),
                "password": input("Enter your password: ").strip(),
            }
            user = self.user_manager.find_user(login_data["email"])

            if user and bcrypt.checkpw(
                login_data["password"].encode(), user["password"].encode()
            ):
                print("Login successful!")
                # Handle user roles if required
            else:
                print("Invalid email or password.")
        except Exception as e:
            print(f"Error during login: {e}")


if __name__ == "__main__":
    main = Main()
    main.display_main_menu()

