from validate_user import UserValidator, ValidationError
import bcrypt


class Registration:
    """Register and save user data to the database."""

    def __init__(self, user_manager):
        """Initialize with user manager and validator."""
        self.user_manager = user_manager  # Store the user manager instance
        self.validator = UserValidator()

    def prompt_user_input(self):
        """Prompt the user for input and return a dictionary of user data."""
        return {
            "first_name": input("Enter your first name: ").strip().capitalize(),
            "last_name": input("Enter your last name: ").strip().capitalize(),
            "birthday": input("Enter your birthday (Format: DD/MM/YYYY): ").strip(),
            "email": input("Enter your email: ").strip(),
            "password": input(
                "Enter your password (min 1 uppercase, min 1 lowercase, 8 characters and 1 symbol): "
            ).strip(),
            "phone_number": input("Enter your phone number with landcode: ").strip(),
            "address": {
                "street": input("Enter your street name: ").strip().capitalize(),
                "house_number": input("Enter your house number: ").strip(),
                "city": input("Enter your city: ").strip().capitalize(),
                "zip_code": input("Enter your ZIP code: ").strip(),
                "country": input("Enter your country: ").strip().capitalize(),
            },
        }

    def hash_password(self, password):
        """Hash a password using bcrypt and convert to string (UTF-8)."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")  # Convert bytes to string (UTF-8)

    def validate_fields(self, user_data):
        """Validate user input fields individually."""
        failed_field = None
        for field, value in user_data.items():
            if isinstance(value, dict):  # For nested address dictionary
                nested_failed_field = self.validate_fields(value)
                if nested_failed_field:
                    failed_field = f"{field}.{nested_failed_field}"
                    break
            else:
                if not self.validator.validator.validate({field: value}):
                    failed_field = field
                    break
        return failed_field

    def register_user(self, user_data=None):
        """Register a user after prompting for input and validation."""
        if user_data is None:
            user_data = self.prompt_user_input()  # Prompt if no data is provided

        # Validate user data
        failed_field = self.validate_fields(user_data)
        if failed_field:
            print(f"Validation failed for field: {failed_field}")
            return False

        # Hash the password and update the validated user data
        user_data["password"] = self.hash_password(user_data["password"])

        # Add the user to the database
        try:
            self.user_manager.add_user(user_data)
            print("User has been registered successfully.")
            return True
        except Exception as e:
            print(f"Registration failed: {e}")
            return False
