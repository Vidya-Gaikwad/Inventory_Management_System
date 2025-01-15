import unittest
from unittest.mock import patch, MagicMock
from inventory.product import Product

class TestProduct(unittest.TestCase):

    def setUp(self):
        """Set up a sample product before each test."""
        self.product = Product(product_name="Laptop", quantity=10, price=1000, category="Electronics")
        self.product.product_data = {
            "E101": {"name": "Laptop", "quantity": 10, "price": 1000, "category": "Electronics"}
        }

    @patch("builtins.open", new_callable=MagicMock)
    def test_update_quantity(self, mock_open):
        """Test the update_quantity method."""
        self.product.update_quantity(5)
        mock_open.assert_called_once_with(self.product.database, "w")

        self.assertEqual(self.product.product_data["E101"]["quantity"], 15)

    @patch("builtins.open", new_callable=MagicMock)
    def test_update_price(self, mock_open):
        """Test the update_price method."""
        self.product.update_price(1200)
        
        mock_open.assert_called_once_with(self.product.database, "w")
        
        self.assertEqual(self.product.product_data["E101"]["price"], 1200)

    def test_display_product_info(self):
        """Test the display_product_info method."""
        info = self.product.display_product_info()
        expected_info = "Name: Laptop, Quantity: 10, Price: $1000.00, Category: Electronics"
        
        self.assertEqual(info, expected_info)

    def test_is_in_stock(self):
        """Test the is_in_stock method."""
        self.assertTrue(self.product.is_in_stock())
        
        self.product.quantity = 0
        self.assertFalse(self.product.is_in_stock())

    def test_apply_discount(self):
        """Test the apply_discount method."""
        self.product.apply_discount(10)
        self.assertEqual(self.product.price, 900.00)
        
        with self.assertRaises(ValueError):
            self.product.apply_discount(110)

    def test_to_dict(self):
        product_dict = self.product.to_dict()
        expected_dict = {
            "product_name": "Laptop",
            "quantity": 10,
            "price": 1000,
            "category": "Electronics"
        }
        self.assertEqual(product_dict, expected_dict)

if __name__ == "__main__":
    unittest.main()
