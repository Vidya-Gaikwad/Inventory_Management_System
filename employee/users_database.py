from tinydb import TinyDB, Query
import json


class UserNotFoundError(Exception):
    pass


class UserExistsError(Exception):
    pass


class UserManager:
    def __init__(self, db_path="users_database.json"):
        self.db = TinyDB(db_path)
        self.user_query = Query()
        self.db_path = db_path  # Store the database path explicitly

    def get_all_users(self):
        """Get all users from the database."""
        return self.db.all()

    def find_user(self, email):
        """Find a user by email."""
        result = self.db.search(self.user_query.email == email)
        return result[0] if result else None

    def add_user(self, user_data):
        """Add a new user to the database."""
        if self.find_user(user_data["email"]):
            raise UserExistsError(f"User with email {user_data['email']} already exists.")
        self.db.insert(user_data)
        # Reformat the file after adding the user (pretty printing)
        self._pretty_print_db()
        return "User added successfully."

    def update_user(self, email, update_data):
        """Update an existing user's information."""
        if not self.find_user(email):
            raise UserNotFoundError(f"User with email {email} not found.")
        self.db.update(update_data, self.user_query.email == email)
        # Reformat the file after updating the user (pretty printing)
        self._pretty_print_db()
        return "User updated successfully."

    def delete_user(self, email):
        """Delete a user by email."""
        if not self.find_user(email):
            raise UserNotFoundError(f"User with email {email} not found.")
        self.db.remove(self.user_query.email == email)
        # Reformat the file after deleting the user (pretty printing)
        self._pretty_print_db()
        return "User deleted successfully."

    def _pretty_print_db(self):
        """Reformat the TinyDB storage to have pretty print with newlines."""
        with open(self.db_path, 'r') as f:  # Use the stored db_path
            db_data = json.load(f)

        # Open the file again for writing with pretty print and indent
        with open(self.db_path, 'w') as f:
            json.dump(db_data, f, indent=4)

    def search_users(self, criteria):
        """Search for users matching given criteria."""
        results = self.db.search(
            lambda user: all(user.get(key) == value for key, value in criteria.items())
        )
        if not results:
            raise UserNotFoundError("No users matching the given criteria were found.")
        return results



# user_manager = UserManager()

# Add a user
# user_data = {
#  "first_name": "Carlos",
# "last_name": "Ramirez",
#  "birthday": "01.01.1990",
#  "email": "Carlos@example.com",
#  "password": "password123",
#  "phone_number": "+1 1234567890",
#  "address": {
#      "street": "123 Main St",
#      "house_number": "123",
#      "city": "New York",
#      "zip_code": "10001",
#      "country": "USA",
#  },
# }

# print(user_data)


# user_manager.add_user(user_data)

# Update a user's information
# update_data = {
#    "first_name": "Carlos",
#    "last_name": "Ramirez",
#    "birthday": "02.02.1990",
#    "email": "Carlos@example.com",
#    "password": "newpassword456",
#    "phone_number": "+1 9876543210",
#    "address": {
#        "street": "456 Elm St",
#        "house_number": "456",
#        "city": "Los Angeles",
#        "zip_code": "90001",
#        "country": "USA",
#    },
# }

# user_manager.update_user(user_data["email"], update_data)

# print(update_data)

# Delete a user
# delete_user = user_manager.delete_user(user_data["email"])

# print(delete_user)

# Search for users
# criteria = {"first_name": "Carlos"}

# try:
#    users = user_manager.search_users(criteria)
#    for user in users:
#        print(user)
# except Exception as e:
#    print(e)