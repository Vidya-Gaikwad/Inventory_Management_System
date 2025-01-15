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
                "regex": r"^[a-zA-ZÀ-ÿ\s'-]+$",
                "required": True,
            },
            "last_name": {
                "type": "string",
                "regex": r"^[a-zA-ZÀ-ÿ\s'-]+$",
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
                        "regex": r"^[a-zA-ZÀ-ÿ\s\-]+$",
                        "required": True,
                    },
                    "country": {
                        "type": "string",
                        "regex": r"^[a-zA-ZÀ-ÿ\s]+$",
                        "required": True,
                    },
                    "zip_code": {
                        "type": "string",
                        "regex": r"^\d{5,8}$",
                        "required": True,
                    },
                },
            },
            "role": {
                "type": "string",
                "allowed": ["Manager", "Logistics Employee", "Sales Employee"],
                "required": True,
            },
        }
        self.validator = Validator(self.schema)

    def validate(self, data):
        """Validate data against the schema."""
        if not self.validator.validate(data):
            raise ValidationError(self.get_error_messages(data))

        # Additional custom validation
        self.validate_birthday(data.get("birthday"))
        return data

    def get_error_messages(self, data):
        """Generate user-friendly error messages."""
        error_messages = []

        # General validation errors (from Cerberus schema)
        for field, errors in self.validator.errors.items():
            for error in errors:
                if field == "first_name":
                    error_messages.append(
                        "First name must contain only letters, spaces, apostrophes, or hyphens."
                    )
                elif field == "last_name":
                    error_messages.append(
                        "Last name must contain only letters, spaces, apostrophes, or hyphens."
                    )
                elif field == "email":
                    error_messages.append(
                        "Please enter a valid email address (e.g., user@example.com)."
                    )
                elif field == "password":
                    error_messages.append(
                        "Password must contain at least one uppercase letter, one lowercase letter, one digit, and be at least 8 characters long."
                    )
                elif field == "phone_number":
                    error_messages.append(
                        "Please enter a valid phone number with the correct format (e.g., +1-555-1234)."
                    )
                elif field == "birthday":
                    error_messages.append(
                        "Please enter a valid birthday in the format DD/MM/YYYY."
                    )
                elif field == "address":
                    for sub_field, sub_errors in self.validator.errors[
                        "address"
                    ].items():
                        if sub_field == "street":
                            error_messages.append(
                                "Street name should only contain letters, numbers, spaces, or hyphens."
                            )
                        elif sub_field == "house_number":
                            error_messages.append(
                                "House number should contain digits and optional letters or hyphens."
                            )
                        elif sub_field == "city":
                            error_messages.append(
                                "City name should only contain letters, spaces, and hyphens."
                            )
                        elif sub_field == "country":
                            error_messages.append(
                                "Country name should only contain letters and spaces."
                            )
                        elif sub_field == "zip_code":
                            error_messages.append("ZIP code should contain 5-8 digits.")

                elif field == "role":
                    error_messages.append(
                        "Role must be one of: Manager, Logistics Employee, or Sales Employee."
                    )

        return error_messages

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
        return birthday
