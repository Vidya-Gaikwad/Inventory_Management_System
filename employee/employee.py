from users_database import UserManager, UserExistsError, UserNotFoundError


class Employee:
    def __init__(
        self, user_data: dict, hiring_date: str, salary: float, db_manager: UserManager
    ):
        self.first_name = user_data["first_name"]
        self.last_name = user_data["last_name"]
        self.email = user_data["email"]
        self.phone_number = user_data.get("phone_number")
        self.address = user_data.get("address")
        self.birthday = user_data.get("birthday")
        self.hiring_date = hiring_date
        self.salary = salary
        self.db_manager = db_manager

    def save_to_database(self):
        """Save the employee to the database as a dictionary."""
        user_data = self.to_dict()  # Convert employee to dict
        try:
            # Add the user to the database using the UserManager
            return self.db_manager.add_user(user_data)
        except (Exception, UserExistsError) as e:
            print(f"Error saving user, user already exits: {e}")
            return None

    def update_to_database(self):
        """Update the employee information in the database."""
        update_data = self.to_dict()  # Get the updated employee data as a dict
        try:
            # Update the user in the database using UserManager
            return self.db_manager.update_user(self.email, update_data)
        except (Exception, UserNotFoundError) as e:
            print(f"Error updating user, user not found: {e}")
            return None

    def to_dict(self) -> dict:
        """Convert the employee object to a dictionary."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "birthday": self.birthday,
            "hiring_date": self.hiring_date,
            "salary": self.salary,
        }

    def __str__(self):
        return f"Employee {self.first_name} {self.last_name} (Email: {self.email}, Birthday: {self.birthday}, Hiring Date: {self.hiring_date}, Salary: {self.salary})"


# Initialize UserManager in the Json database
# db_manager = UserManager("users_database.json")

# Create user data dictionary
# user_data = {
# "first_name": "Leon",
# "last_name": "Camarena",
# "email": "Camarene@example.com",
# "phone_number": "+1234567891",
# "address": {"street": "1235 Main St", "house_number": "6A", "city": "New York"},
# }

# Employee object containing: user data, hiring date, salary, and db_manager
# employee = Employee(
# user_data=user_data,
# hiring_date="11/01/2024",
# salary=48000.00,
# db_manager=db_manager,
# )

# print(f"Employee: {employee}")

# Save the employee to the database
# save_message = employee.save_to_database()
# if save_message:
#    print("Employee saved successfully to the database.")

# Update the employee's information
# employee.birthday = "20/06/1995"
# employee.hiring_date = "11/03/2024"
# employee.salary = 58500.00

# Update the employee in the database
# update_message = employee.update_to_database()
# if update_message:
#   print("Employee updated successfully in the database.")

# Print the updated employee
# print("\nEmployee updated:")
# print(employee)

# Print the employee's dictionary representation
# print("\nEmployee data as dictionary:")
# print(employee.to_dict())
