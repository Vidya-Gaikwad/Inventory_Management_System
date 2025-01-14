from users_database import UserManager, UserExistsError
from validate_user import UserValidator, ValidationError
import bcrypt


class Registration:
    """Register and save user data to the database."""

    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.validator = UserValidator()  # Create an instance of UserValidator

    def prompt_user_input(self):
        """Prompt the user for input and return a dictionary of user data."""
        user_data = {
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
        return user_data

    def hash_password(self, password):
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def register_user(self, user_data=None):
        """Register a user after prompting for input and validation."""
        if user_data is None:
            user_data = self.prompt_user_input()  # Prompt if no data is provided

        # Validate each field one by one
        while True:
            failed_field = self.validate_fields(user_data)
            if failed_field is None:
                break
            else:
                print(f"Please correct the '{failed_field}' field.")
                # If the field is a sub-field (like address), handle it accordingly
                if "." in failed_field:
                    field, sub_field = failed_field.split(".")
                    user_data[field][sub_field] = input(
                        f"Enter your {sub_field}: "
                    ).strip()
                else:
                    user_data[failed_field] = input(
                        f"Enter your {failed_field}: "
                    ).strip()

        # Hash the password and update the validated user data
        user_data["password"] = self.hash_password(user_data["password"]).decode(
            "utf-8"
        )  # Convert bytes to str

        # Add the user to the database
        try:
            self.user_manager.add_user(user_data)
            print("User has been registered successfully.")
            return True
        except UserExistsError as e:
            print(f"Registration failed. User already exists in the database: {e}")
            return False

    def validate_fields(self, user_data):
        """Validate each field in the user data and return the first failed field."""
        # Validate main fields (first_name, last_name, etc.)
        for field, value in user_data.items():
            if isinstance(
                value, dict
            ):  # If it's an address dictionary, validate nested fields
                for sub_field, sub_value in value.items():
                    if not self.validator.validator.validate({sub_field: sub_value}):
                        return f"{field}.{sub_field}"  # Return nested field as "field.sub_field"
            else:
                if not self.validator.validator.validate({field: value}):
                    return field
        return None
