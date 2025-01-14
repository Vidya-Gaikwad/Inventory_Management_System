from cerberus import Validator
import datetime


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class UserValidator:
    """Handles validation of user data using the Cerberus library."""

    def __init__(self):
        self.schema = {
            "first_name": {
                "type": "string",
                "regex": r"^[a-zA-Z]+(?: [a-zA-Z]+)*$",
                "required": True,
            },
            "last_name": {
                "type": "string",
                "regex": r"^[a-zA-Z]+(?: [a-zA-Z]+)*$",
                "required": True,
            },
            "email": {
                "type": "string",
                "regex": r"^\S+@\S+\.\w{2,4}$",
                "required": True,
            },
            "password": {
                "type": "string",
                "regex": r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$",
                "required": True,
            },
            "phone_number": {
                "type": "string",
                "regex": r"^\+?\d{1,3}[-.\s]?\d{9,12}$",
                "required": True,
            },
            "birthday": {
                "type": "string",
                "required": True,
            },
            "address": {
                "type": "dict",
                "required": True,
                "schema": {
                    "street": {
                        "type": "string",
                        "regex": r"^[a-zA-Z0-9\s\-\']+$",
                        "required": True,
                    },
                    "house_number": {
                        "type": "string",
                        "regex": r"^\d{1,5}[a-zA-Z\d\-]*$",
                        "required": True,
                    },
                    "city": {
                        "type": "string",
                        "regex": r"^[a-zA-Z\s\-]+$",
                        "required": True,
                    },
                    "country": {
                        "type": "string",
                        "regex": r"^[a-zA-Z\s]+$",
                        "required": True,
                    },
                    "zip_code": {
                        "type": "string",
                        "regex": r"^\d{5,8}$",
                        "required": True,
                    },
                },
            },
        }
        self.validator = Validator(self.schema)

    def validate(self, data):
        """Validate data against the schema and prompt for invalid fields."""
        valid_data = data.copy()
        errors = self.validator.validate(data)
        if not errors:
            # All fields are valid, check custom validations
            self.validate_birthday(valid_data.get("birthday"))
            return valid_data

        # If there are errors, give user-friendly feedback and reprompt invalid fields
        for field, error_list in self.validator.errors.items():
            for error in error_list:
                print(f"Error with {field}: {self.get_error_message(field, error)}")
                valid_data[field] = self.prompt_for_field(field, valid_data)
        return valid_data

    def validate_birthday(self, birthday):
        """Validate birthday to ensure user is at least 18 years old."""
        try:
            birth_date = datetime.datetime.strptime(birthday, "%d/%m/%Y")
            today = datetime.datetime.now()
            age = (
                today.year
                - birth_date.year
                - ((today.month, today.day) < (birth_date.month, birth_date.day))
            )
            if age < 18:
                raise ValidationError("User must be at least 18 years old.")
        except ValueError:
            raise ValidationError("Invalid birthday format. Use DD/MM/YYYY.")

    def get_error_message(self, field, error):
        """Provide a user-friendly error message based on the field and error."""
        messages = {
            "first_name": "First name should only contain letters and spaces.",
            "last_name": "Last name should only contain letters and spaces.",
            "email": "Email must follow the format: example@domain.com.",
            "password": (
                "Password must be at least 8 characters long, include at least one uppercase letter, "
                "one lowercase letter, and one digit."
            ),
            "phone_number": "Phone number must be in a valid format, such as +1234567890.",
            "birthday": "Birthday must be in the format DD/MM/YYYY.",
            "address.street": "Street name should only contain letters, numbers, and spaces.",
            "address.house_number": "House number can contain numbers and letters.",
            "address.city": "City name should only contain letters and spaces.",
            "address.country": "Country name should only contain letters and spaces.",
            "address.zip_code": "ZIP code must contain 5-8 digits.",
        }
        return messages.get(f"{field}", error)

    def prompt_for_field(self, field, data):
        """Prompt user for input for the field if invalid, using the current data."""
        while True:
            input_value = input(f"Enter a valid {field}: ").strip()
            # Update the input in the data dictionary and validate
            data[field] = input_value
            try:
                self.validate(data)
                return input_value
            except ValidationError:
                print(f"Please enter a valid value for {field}.")
                continue


# Example usage:

#user_data = {
#    "first_name": "Miguel",
#    "last_name": "Estrada",
#    "email": "Miguel@example.com",
#    "password": "StrongPass1",
#    "phone_number": "+1234567890",
#    "address": {
#        "street": "123 Main St",
#        "house_number": "5A",
#        "city": "New York",
#        "country": "USA",
#        "zip_code": "10001",
#    },
#    "birthday": "25/05/1995",
#}

#validator = UserValidator()
#try:
#    validated_user = validator.validate(user_data)
#    print("User data is valid.")
#except ValidationError as e:
#    print(f"Validation failed: {e}")
