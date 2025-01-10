import json


class UserExistsError(Exception):
    """Exception raised when attempting to add a user who already exists."""

    pass


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    pass


class UsersNotFoundError(Exception):
    """Exception raised when no users are found during a search."""

    pass


class MockUserManager:
    """
    Mock version of a user manager to simulate a database.
    This version uses a JSON file to persist data.
    """

    def __init__(self, db_path="mock_users_database.json"):
        self.db_path = db_path
        self.load_data()

    def load_data(self):
        """Load data from the mock database file."""
        try:
            with open(self.db_path, "r") as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = []

    def save_data(self):
        """Save current user data back to the mock database file."""
        with open(self.db_path, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, user_data):
        """Add a new user to the database."""
        if self.find_user(user_data["email"]):
            raise UserExistsError(
                f"User with email {user_data['email']} already exists."
            )
        self.users.append(user_data)
        self.save_data()

    def get_all_users(self):
        """Return all users in the mock database."""
        return self.users

    def find_user(self, email):
        """Find a user by email."""
        for user in self.users:
            if user["email"] == email:
                return user
        return None

    def search_users(self, criteria):
        """Search for users matching given criteria."""
        results = [
            user
            for user in self.users
            if all(user.get(key) == value for key, value in criteria.items())
        ]
        if not results:
            raise UsersNotFoundError("No users matching the given criteria were found.")
        return results

    def update_user(self, email, update_data):
        """Update a user's details."""
        user = self.find_user(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found.")

        # Ensure None values are not overwriting existing data
        for key, value in update_data.items():
            if value is not None:
                user[key] = value
        self.save_data()

    def delete_user(self, email):
        """Delete a user by email."""
        user = self.find_user(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found.")

        self.users.remove(user)
        self.save_data()


# Example usage and testing

# Initialize MockUserManager
mock_user_manager = MockUserManager()

# Example user data
user_data1 = {
    "first_name": "Carla",
    "last_name": "Estrada",
    "birthday": "01.01.1990",
    "email": "carla@example.com",
    "password": "mypassword123",
    "phone_number": "+1 1234567890",
    "address": {
        "street": "123 Main St",
        "house_number": "123",
        "city": "New York",
        "zip_code": "10001",
        "country": "USA",
    },
}

user_data2 = {
    "first_name": "Pedro",
    "last_name": "Canales",
    "birthday": "01.01.1994",
    "email": "canales@example.com",
    "password": "mypassword1111",
    "phone_number": "+1 1234567890",
    "address": {
        "street": "124 Main St",
        "house_number": "173",
        "city": "New York",
        "zip_code": "10001",
        "country": "USA",
    },
}

# Add user
try:
    mock_user_manager.add_user(user_data1)
    print(f"Added user: {user_data1['first_name']} {user_data1['last_name']}")
except UserExistsError as e:
    print(f"Error adding user: {e}")

# Add another user
try:
    mock_user_manager.add_user(user_data2)
    print(f"Added user: {user_data2['first_name']} {user_data2['last_name']}")
except UserExistsError as e:
    print(f"Error adding user: {e}")


# Update user
update_data = {"first_name": "Karla", "last_name": "Estrada"}
try:
    mock_user_manager.update_user(user_data1["email"], update_data)
    updated_user = mock_user_manager.find_user(user_data1["email"])
    print(f"Updated user: {updated_user['first_name']} {updated_user['last_name']}")
except UserNotFoundError as e:
    print(f"Error updating user: {e}")

# Search user by criteria
search_criteria = {"first_name": "Karla"}
try:
    found_users = mock_user_manager.search_users(search_criteria)
    for user in found_users:
        print(
            f"Found user: {user['first_name']} {user['last_name']} with email {user['email']}"
        )
except UsersNotFoundError as e:
    print(f"Error searching users: {e}")

# Delete user
try:
    mock_user_manager.delete_user(user_data1["email"])
    print(f"Deleted user with email: {user_data1['email']}")
except UserNotFoundError as e:
    print(f"Error deleting user: {e}")

# Delete other users
try:
    mock_user_manager.delete_user(user_data2["email"])
    print(f"Deleted user with email: {user_data2['email']}")
except UserNotFoundError as e:
    print(f"Error deleting user: {e}")
