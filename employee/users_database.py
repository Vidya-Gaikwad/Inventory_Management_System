import base64
import json
import bcrypt


class UserManager:
    """Handles user management and storage in a JSON database."""

    def __init__(self, db_file="users.json"):
        self.db_file = db_file
        self.users = self.load_users()

    def load_users(self):
        """Load users from the JSON file."""
        try:
            with open(self.db_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Return an empty list if the file does not exist

    def save_users(self):
        """Save users to the JSON file."""
        with open(self.db_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, user_data):
        """Add a new user to the users list."""
        self.users.append(user_data)
        self.save_users()

    def get_all_users(self):
        """Get all users."""
        return self.users

    def get_user_by_email(self, email):
        """Get a user by email."""
        for user in self.users:
            if user["email"] == email:
                return user
        return None

    def hash_password(self, password):
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return base64.b64encode(hashed_password).decode(
            "utf-8"
        )  # Convert to base64 string

    def store_password(self, password):
        """Store the password in base64 format."""
        return self.hash_password(password)
