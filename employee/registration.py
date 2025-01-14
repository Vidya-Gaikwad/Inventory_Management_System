from users_database import UserManager, UserExistsError
from validate_user import UserValidator, ValidationError
import bcrypt


class Registration:
    """Register and save user data to the database."""

    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.validator = UserValidator()

    def prompt_user_input(self):
        """Prompt the user for input and return a dictionary of user data."""
        return {
            "first_name": input("Enter your first name: ").strip().capitalize(),
            "last_name": input("Enter your last name: ").strip().capitalize(),
            "birthday": input("Enter your birthday (DD.MM.YYYY): ").strip(),
            "email": input("Enter your email: ").strip(),
            "password": input("Enter your password: ").strip(),
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
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)


def register_user(self, user_data=None):
    """Register a user after prompting for input and validation."""
    if user_data is None:
        user_data = self.prompt_user_input()  # Prompt if no data is provided

    # Validate user data
    try:
        validated_user = self.validator.validate(user_data)
    except ValidationError as e:
        print(f"Validation failed. Please check your entries: {e}")
        return False

    # Hash the password and update the validated user data
    validated_user["password"] = self.hash_password(validated_user["password"])

    # Add the user to the database
    try:
        self.user_manager.add_user(validated_user)
        print("User has been registered successfully.")
        return True
    except UserExistsError as e:
        print(f"Registration failed. User already exists in the database: {e}")
        return False
