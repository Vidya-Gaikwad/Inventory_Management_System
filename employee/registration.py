class Registration:
    def __init__(self, user_manager, user_validator):
        self.user_manager = user_manager
        self.user_validator = user_validator

    def prompt_user_input(self):
        """Prompt the user for their registration details."""

        print("Welcome to the Registration System!")

        # Prompt for basic user details (first name, last name, etc.)
        first_name = input("Enter your first name: ").strip()
        last_name = input("Enter your last name: ").strip()
        birthday = input("Enter your birthday (Format: DD/MM/YYYY): ").strip()
        email = input("Enter your email: ").strip()
        password = input(
            "Enter your password (min 1 uppercase, min 1 lowercase, 8 characters and 1 symbol): "
        ).strip()
        phone_number = input("Enter your phone number with landcode: ").strip()

        # Prompt for address details
        street = input("Enter your street name: ").strip()
        house_number = input("Enter your house number: ").strip()
        city = input("Enter your city: ").strip()
        zip_code = input("Enter your ZIP code: ").strip()
        country = input("Enter your country: ").strip()

        # Display role choices
        print("\nChoose a role from the following options:")
        print("1. Manager")
        print("2. Sales Employee")
        print("3. Logistics Employee")

        # Prompt the user to select a role
        role_choice = input(
            "Enter the number corresponding to your desired role: "
        ).strip()

        # Validate and map the role choice
        role = self.get_role_from_choice(role_choice)

        if role is None:
            print("Invalid role choice. Please try again.")
            return

        # Collect the user data into a dictionary
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "birthday": birthday,
            "address": {
                "street": street,
                "house_number": house_number,
                "city": city,
                "zip_code": zip_code,
                "country": country,
            },
            "role": role,
        }

        # Validate the user input data
        try:
            validated_data = self.user_validator.validate(user_data)
            self.user_manager.add_user(validated_data)  # Save the user data
            print("Registration successful!")
        except ValidationError as e:
            print(f"Validation failed: {e}")

    def get_role_from_choice(self, choice):
        """Validate the role selection."""
        if choice == "1":
            return "Manager"
        elif choice == "2":
            return "Sales Employee"
        elif choice == "3":
            return "Logistics Employee"
        else:
            return None
