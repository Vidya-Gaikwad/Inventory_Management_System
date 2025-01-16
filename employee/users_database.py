import json
import bcrypt


class UserExistsError(Exception):
    """Raised when trying to add a user that already exists."""

    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""

    pass


class UserManager:
    """Handles user management and storage in a JSON database."""

    def __init__(self, db_file="users_database.json"):
        self.db_file = db_file
        self.users = self.load_users()

    def load_users(self):
        """Load users from the JSON file."""
        try:
            with open(self.db_file, "r") as file:
                content = file.read().strip()
                if content:  # Only try to load if the file isn't empty
                    return json.loads(content)
                else:
                    return []  # Return an empty list if the file is empty
        except FileNotFoundError:
            return []  # Return an empty list if the file does not exist
        except json.JSONDecodeError:
            print(
                "Error: The users database file is corrupted or contains invalid JSON."
            )
            return []  # Return an empty list if the file contains invalid JSON

    def save_users(self):
        """Save users to the JSON file."""
        with open(self.db_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, user_data):
        """Add a new user to the users list."""
        # Check if the user already exists
        existing_user = self.find_user(user_data["email"])
        if existing_user:
            raise UserExistsError(
                f"User with email {user_data['email']} already exists."
            )

        # Add the new user data to the list
        self.users.append(user_data)
        self.save_users()

    def get_all_users(self):
        """Get all users."""
        return self.users

    def find_user(self, email):
        """Find user by email in a case-insensitive way."""
        email = email.strip().lower()

        for user in self.users:
            if user["email"].strip().lower() == email:
                return user
        return None
