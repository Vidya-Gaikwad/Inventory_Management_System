import pytest
from employee.validate_user import UserValidator, ValidationError


class TestValidateUser:

    def test_validate_name(self):
        # Test valid names
        assert Validation.validate_name("Álvaro Pérez") == "Álvaro Pérez"

        # Test invalid names
        with pytest.raises(ValidationError, match="Invalid name. Use only letters."):
            Validation.validate_name("12345")

    def test_validate_email(self):
        # Test valid emails
        assert (
            Validation.validate_email("carla.doe@example.com")
            == "carla.doe@example.com"
        )

        # Test invalid emails
        with pytest.raises(
            ValidationError, match="Invalid email. Use format: example@example.com."
        ):
            Validation.validate_email("invalid_email@@ example..345")

    def test_validate_password(self):
        # Test valid passwords
        assert Validation.validate_password("StrongP@ss1") == "StrongP@ss1"

        # Test invalid passwords
        with pytest.raises(
            ValidationError,
            match="Invalid password. Use uppercase, lowercase, digits, and at least 8 characters.",
        ):
            Validation.validate_password("wea123")

    def test_validate_username(self):
        # Test valid usernames
        assert Validation.validate_username("john_doe123") == "john_doe123"

        # Test invalid usernames
        with pytest.raises(
            ValidationError,
            match="Invalid username. Use only letters, uppercase, lowercase, numbers, and underscores.",
        ):
            Validation.validate_username("john&&& 123")

    def test_validate_phone_number(self):
        # Test valid phone numbers
        assert Validation.validate_phone_number("+1234567890") == "+1234567890"

        # Test invalid phone numbers
        with pytest.raises(
            ValidationError, match="Invalid phone number. Use format: +1234567890."
        ):
            Validation.validate_phone_number("19456??")

    def test_validate_birthday(self):
        # Test valid birthdays
        assert Validation.validate_birthday("01/01/1990") == "01/01/1990"

        # Test invalid birthdays
        with pytest.raises(
            ValidationError, match="Invalid birthday. Use format: DD/MM/YYYY."
        ):
            Validation.validate_birthday("32/12/2000")  # Invalid date
        with pytest.raises(
            ValidationError,
            match="Invalid birthday. User must be at least 18 years old.",
        ):
            Validation.validate_birthday("01/01/2022")  # Under 18

    def test_validate_address(self):
        # Test valid address
        valid_address = {
            "street": "123 Main St",
            "house_number": "A",
            "city": "New York",
            "country": "USA",
            "zip_code": "10001",
        }
        assert Validation.validate_address(valid_address) == valid_address

        # Test invalid address
        invalid_address = {
            "street": "123 Main St",
            "house_number": "123#",  # Invalid house number
            "city": "123City",  # Invalid city
            "country": "U5A",  # Invalid country
            "zip_code": "1",  # Invalid zip code
        }
        with pytest.raises(
            ValidationError, match="Address validation failed: Invalid house number."
        ):
            Validation.validate_address(invalid_address)
