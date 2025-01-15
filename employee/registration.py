from employee.users_database import UserManager, UserExistsError
from employee.validate_user import UserValidator, ValidationError
import bcrypt  # bcrypt algorithm to hash passwords and verify them


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
        

############################### vecchio con modifica mio ########################################

# class Registration:
#     """Register and save user data to the database."""

#     def __init__(self, user_manager):
#         self.user_manager = user_manager
#         self.validator = UserValidator()

#     def prompt_user_input(self):
#         """Prompt the user for input and return a dictionary of user data."""
#         return {
#             "first_name": input("Enter your first name: ").strip().capitalize(),
#             "last_name": input("Enter your last name: ").strip().capitalize(),
#             "birthday": input("Enter your birthday (DD.MM.YYYY): ").strip(),
#             "email": input("Enter your email: ").strip(),
#             "password": input("Enter your password: ").strip(),
#             "phone_number": input("Enter your phone number with landcode: ").strip(),
#             "address": {
#                 "street": input("Enter your street name: ").strip().capitalize(),
#                 "house_number": input("Enter your house number: ").strip(),
#                 "city": input("Enter your city: ").strip().capitalize(),
#                 "zip_code": input("Enter your ZIP code: ").strip(),
#                 "country": input("Enter your country: ").strip().capitalize(),
#             },
#         }

#     # def hash_password(self, password): # old one
#     #     """Hash a password using bcrypt."""
#     #     salt = bcrypt.gensalt()
#     #     return bcrypt.hashpw(password.encode(), salt)
#     # The bcrypt.hashpw() function returns a bytes object, so .decode('utf-8') is used to convert it to a string. This makes the password hash 
#     # suitable for JSON serialization.
#     def hash_password(self, password):
#         """Hash a password using bcrypt and return it as a string."""
#         salt = bcrypt.gensalt()
#         hashed_password = bcrypt.hashpw(password.encode(), salt)
#         return hashed_password.decode('utf-8')  # Convert the byte object to a string


#     def register_user(self, user_data=None):
#         """Register a user after prompting for input and validation."""
#         if user_data is None:
#             user_data = self.prompt_user_input()  # Prompt if no data is provided

#         # Validate user data
#         try:
#             validated_user = self.validator.validate(user_data)
#         except ValidationError as e:
#             print(f"Validation failed. Please check your entries: {e}")
#             return False

#         # Hash the password and update the validated user data
#         validated_user["password"] = self.hash_password(validated_user["password"])

#         # Add the user to the database
#         try:
#             self.user_manager.add_user(validated_user)
#             print("User has been registered successfully.")
#             return True
#         except UserExistsError as e:
#             print(f"Registration failed. User already exists in the database: {e}")
#             return False