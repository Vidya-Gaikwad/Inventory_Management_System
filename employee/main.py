from registration import Registration
from users_database import UserManager


class Main:
    """Main program to manage the Inventory Manager system."""

    def __init__(self):
        self.user_manager = UserManager()  # UserManager to handle user data

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
        registration = Registration(
            self.user_manager
        )  # Pass the user_manager to Registration
        success = registration.register_user()  # Calls register_user with validation
        if success:
            print("Registration successful!")
        else:
            print("Registration failed.")

    def login_user(self):
        """Handle user login."""
        print("Login functionality is not implemented yet.")


if __name__ == "__main__":
    main = Main()
    main.display_main_menu()
