from tinydb import TinyDB, Query

# Create a new TinyDB instance and insert data
db = TinyDB("test_db.json")

# Insert a test record
db.insert({"name": "John Doe", "age": 30})

# Query for the record
User = Query()
result = db.search(User.name == "John Doe")

print(result)
