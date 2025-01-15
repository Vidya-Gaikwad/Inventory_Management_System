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
                "regex": r"^[a-zA-ZÀ-ÿ\s]+$",
                "required": True,
            },
            "last_name": {
                "type": "string",
                "regex": r"^[a-zA-ZÀ-ÿ\s]+$",
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
        }
        self.validator = Validator(self.schema)

    def validate(self, data):
        """Validate data against the schema."""
        if not self.validator.validate(data):
            raise ValidationError(self.validator.errors)
        # Additional custom validation
        self.validate_birthday(data.get("birthday"))
        return data

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



