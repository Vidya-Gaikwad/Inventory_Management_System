import unittest
from unittest.mock import patch, mock_open
from inventory.inventory_manager import InventoryManager
import json
import os

class TestInventoryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the real mock_products.json file with initial data
        print("setUpClass")
        mock_data = {
            "E101": {"product_name": "Smartphone", "price": 150.0, "category": "Electronics", "quantity": 50},
            "E102": {"product_name": "Laptop", "price": 200.0, "category": "Electronics", "quantity": 10},
        }
        with open("mock_products.json", "w") as f:
            json.dump(mock_data, f, indent=4)

    @classmethod
    def tearDownClass(cls):
        # Clean up the file after all tests run
        print("tearDownClass")
        if os.path.exists("mock_products.json"):
            os.remove("mock_products.json")

    def setUp(self):
        # Initialize the InventoryManager, which will read from the real mock_products.json
        self.inventory_manager = InventoryManager("mock_products.json")

    @patch("builtins.print")  # Mock print to suppress output during tests
    def test_remove_existing_product(self, mock_print):
        product_id = "E101"

        # Check that the product exists
        self.assertIn(product_id, self.inventory_manager.product_data)

        # Remove the product
        self.inventory_manager.remove_product(product_id)

        # Ensure the product is removed from the inventory
        self.assertNotIn(product_id, self.inventory_manager.product_data)

        # Check if the inventory was saved after removal
        with open("mock_products.json", "r") as f:
            product_data = json.load(f)
            self.assertNotIn(product_id, product_data)

        # Ensure print was called to confirm removal 
        mock_print.assert_called_once_with(f"Product with ID {product_id} has been removed from the inventory.")

    @patch("builtins.print")  
    def test_remove_non_existing_product(self, mock_print):
        product_id = "999"

        # Check product doesn't exist
        self.assertNotIn(product_id, self.inventory_manager.product_data)

        # Remove a non-existent product
        self.inventory_manager.remove_product(product_id)

        # Check that the inventory was not modified
        with open("mock_products.json", "r") as f:
            product_data = json.load(f)
            self.assertNotIn(product_id, product_data)

        # Ensure print was called to confirm product not found
        mock_print.assert_called_once_with(f"Product with ID {product_id} not found.")


    @patch("builtins.print") 
    def test_get_product_info(self, mock_print):
        product_id = "E101"

        # Check product exists in inventory
        self.assertIn(product_id, self.inventory_manager.product_data)

        # Get product info
        self.inventory_manager.get_product_info(product_id)

        # Check the correct print statement was called 
        mock_print.assert_called_once_with(f"Product ID: {product_id}, Name: Smartphone, Price: 150.0, Category: Electronics, Quantity: 50")


    @patch("builtins.print")
    def test_get_non_existant_product_info(self, mock_print):
        product_id = "99"

        # Check product doesn't exist in inventory
        self.assertNotIn(product_id, self.inventory_manager.product_data)

        # Get product info
        self.inventory_manager.get_product_info(product_id)

        # Check the correct print statement was called 
        mock_print.assert_called_once_with(f"Product with ID {product_id} not found.")


    @patch("builtins.print")
    def test_get_total_inventory_value(self, mock_print):
        # Expected total value: (150 * 50) + (200 * 10) = 7500 + 2000 = 9500
        expected_total = (150.0 * 50) + (200.0 * 10)

        # Get total inventory value
        total_value = self.inventory_manager.get_total_inventory_value()

        # Assert the total value is correct
        self.assertEqual(total_value, expected_total)

if __name__ == '__main__':
    unittest.main()
