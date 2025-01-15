import json
from pathlib import Path


class UserNotFoundError(Exception):
    pass


class UserExistsError(Exception):
    pass


class UserManager:
    def __init__(self, db_path="users_database.json"):
        self.db_path = Path(db_path)  # Use pathlib for path handling
        self._ensure_db_exists()  # Ensure the file exists when initializing

    def _ensure_db_exists(self):
        """Ensure that the database file exists. If not, create it with an empty list."""
        if not self.db_path.exists():
            with open(self.db_path, "w") as db_file:
                json.dump([], db_file, indent=4)
        else:
            # Ensure the file contains a list and not malformed data
            with open(self.db_path, "r") as db_file:
                try:
                    data = json.load(db_file)
                    if not isinstance(data, list):
                        raise ValueError("Database file is not a valid list.")
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error: {e}")
                    print("Resetting database to empty list.")
                    with open(self.db_path, "w") as db_file:
                        json.dump([], db_file, indent=4)

    def _load_db(self):
        """Load the database from the file."""
        with open(self.db_path, "r") as db_file:
            return json.load(db_file)

    def _save_db(self, db_data):
        """Save the database to the file."""
        with open(self.db_path, "w") as db_file:
            json.dump(db_data, db_file, indent=4)

    def get_all_users(self):
        """Get all users from the database."""
        return self._load_db()

    def find_user(self, email):
        """Find a user by email."""
        users = self._load_db()
        return next((user for user in users if user["email"] == email), None)

    def add_user(self, user_data):
        """Add a new user to the database."""
        try:
            if self.find_user(user_data["email"]):
                raise UserExistsError(
                    f"User with email {user_data['email']} already exists."
                )

            users = self._load_db()
            users.append(user_data)
            self._save_db(users)
            return "User added successfully."

        except Exception as e:
            print(f"Error adding user: {e}")
            raise

    def update_user(self, email, update_data):
        """Update an existing user's information."""
        users = self._load_db()
        user = self.find_user(email)

        if not user:
            raise UserNotFoundError(f"User with email {email} not found.")

        # Update the user data
        for key, value in update_data.items():
            user[key] = value

        self._save_db(users)
        return "User updated successfully."

    def delete_user(self, email):
        """Delete a user by email."""
        users = self._load_db()
        user = self.find_user(email)

        if not user:
            raise UserNotFoundError(f"User with email {email} not found.")

        users.remove(user)
        self._save_db(users)
        return "User deleted successfully."

    def search_users(self, criteria):
        """Search for users matching given criteria."""
        users = self._load_db()
        results = [
            user
            for user in users
            if all(user.get(key) == value for key, value in criteria.items())
        ]

        if not results:
            raise UserNotFoundError("No users matching the given criteria were found.")

        return results
