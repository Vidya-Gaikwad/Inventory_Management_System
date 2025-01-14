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


# if __name__ == "__main__":
#    user_data = {
#        "first_name": "Miguel",
#        "last_name": "Estrada",
#        "email": "Miguel@example.com",
#        "password": "StrongPass1",
#        "phone_number": "+1234567890",
#        "address": {
#            "street": "123 Main St",
#            "house_number": "5A",
#            "city": "New York",
#            "country": "USA",
#            "zip_code": "10001",
#        },
#        "birthday": "25/05/1995",
#    }

#    validator = UserValidator()
#    try:
#        validated_user = validator.validate(user_data)
#        print("User data is valid.")
#    except ValidationError as e:
#        print(f"Validation failed: {e}")
