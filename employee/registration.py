# registration.py
from validate_user import UserValidator, ValidationError


class Registration:
    def __init__(self):
        self.validator = UserValidator()

    def register_user(self):
        user_data = {}

        # User data collection
        user_data["first_name"] = self.get_input(
            "Enter your first name: ", "first_name"
        )
        user_data["last_name"] = self.get_input("Enter your last name: ", "last_name")
        user_data["birthday"] = self.get_input(
            "Enter your birthday (Format: DD/MM/YYYY): ", "birthday"
        )
        user_data["email"] = self.get_input("Enter your email: ", "email")
        user_data["password"] = self.get_input("Enter your password: ", "password")
        user_data["phone_number"] = self.get_input(
            "Enter your phone number with landcode: ", "phone_number"
        )
        user_data["address"] = {
            "street": self.get_input("Enter your street name: ", "address.street"),
            "house_number": self.get_input(
                "Enter your house number: ", "address.house_number"
            ),
            "city": self.get_input("Enter your city: ", "address.city"),
            "zip_code": self.get_input("Enter your ZIP code: ", "address.zip_code"),
            "country": self.get_input("Enter your country: ", "address.country"),
        }

        # Validate user data
        try:
            validated_data = self.validator.validate(user_data)
            print("User registered successfully.")
        except ValidationError as e:
            print(f"Validation failed: {e}")
            return False

        return True

    def get_input(self, prompt, field):
        """Prompts the user for input until it passes validation."""
        while True:
            user_input = input(prompt)
            try:
                # Validate input for the specific field
                user_data = {field: user_input}
                self.validator.validator.validate(user_data)
                return user_input
            except ValidationError as e:
                print(f"Invalid input for {field}. Please try again.")
