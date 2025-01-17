from inventory.inventory_manager import InventoryManager
from inventory.product import Product


print("\n")
print("*"*70)
print("------------ Welcome to Inventory management System ------------")
print("*"*70)

manager = InventoryManager()
while True:
    print("\nInventory Management System")
    print("1. Modify/Update Inventory")
    print("2. Search a Product")  
    print("3. Modify/update Product")  
    print("4. Filter Products")  
    print("5. Exit")  
    print("-"*75)
    choice = input("Enter your choice (1-5):  ").strip()
    print("-"*75)

    if choice == "1":
        submenu_1 = True
        while submenu_1:
            print("\n")
            print(".......... Modify/Update Inventory (menu) ..........")
            print("1. Display all products available in inventory")
            print("2. Get total inventory value")
            print("3. Add Product")  
            print("4. Update Product")  
            print("5. Remove Product")
            print("6. Go back")
            print("-"*75)
            print("You are now in submenu: Modify/Update Inventory")
            choice = input("Enter your choice (1-6):  ").strip()
            print("-"*75)
            if choice == "1":  # Displays all products available in inventory with its price (works ok)
                all_products = manager.read_product_data()
                print("Available products in inventory are: ")
                for item, value in all_products.items():
                    print(f"-- {all_products[item]['product_name']},  -----   Price: ${all_products[item]['price']:.2f}")
                print("\n")
            elif choice == "2":
                print("-"*75)
                print(f"Total inventory value is ${manager.get_total_inventory_value()}")
                print("-"*75)
            elif choice == "3":  # Adds a product to inventory, by validating id and product (works ok)
                product_id = input("Enter Product ID (format: A123): ").strip()
                product_name = input("Enter Product Name: ").strip()
                quantity = float(input("Enter Quantity: ").strip())
                price = float(input("Enter Price: ").strip())
                category = input("Enter Category (Electronics, Furniture, Clothes, Footwear): ").strip()
                product = Product(product_name, quantity, price, category)
                try:
                    manager.add_product(product_id, product)
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == "4":  # updates a product when Product ID is given( works ok)
                product_id = input("Enter Product ID to update: ").strip()
                product_name = input("Enter New Product Name: ").strip()
                quantity = float(input("Enter New Quantity: ").strip())
                price = float(input("Enter New Price: ").strip())
                category = input("Enter New Category: ").strip()
                updated_product = Product(product_name, quantity, price, category)
                try:
                    if manager.update_product(product_id, updated_product):
                        print("Product updated successfully.")
                    else:
                        print("Product not found.")
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == "5":  # Removes a product from inventory, when given correct product_id
                product_id = input("Enter Product ID to remove: ").strip()
                try:
                    manager.remove_product(product_id)
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == "6":  # Goes back to main menu
                submenu_1 = False
            else:
                print("Invalid option! Please Enter a no between (1 - 6)")

    elif choice == "2":
        submenu_2 = True
        while submenu_2:
            print("\n")
            print(".......... Search a Product (menu) ..........")
            print("1. Search Product by ID")
            print("2. Search Product by product_name")  # 1
            print("3. Go back")
            print("-"*75)
            choice = input("Enter your choice (1-3):  ").strip()
            print("-"*75)
            if choice == "1":  # Display Product Info/Search product by ID (works ok)
                product_id = input("Enter Product ID to display: ").strip()
                product_data = manager.read_product_data()
                if product_id in product_data:
                    product_info = product_data[product_id]
                    print(f"Product ID: {product_id}")
                    print(f"Name: {product_info['product_name']}")
                    print(f"Quantity: {product_info['quantity']}")
                    print(f"Price: {product_info['price']}")
                    print(f"Category: {product_info['category']}")
                else:
                    print("Product not found.")

            elif choice == "2":  # can search a product by name (works ok)
                product_name = input("Enter name of product:  ").strip()
                product_found = manager.search_product_by_name(product_name)
                if product_found:
                    print(f"Name: {product_found['product_name']}")
                    print(f"Quantity: {product_found['quantity']}")
                    print(f"Price: {product_found['price']}")
                    print(f"Category: {product_found['category']}")
                else:
                    print("Product not found.")

            elif choice == "3":  # Goes back to main menu
                submenu_2 = False
            else:
                print("Invalid option! Please Enter a no between (1 - 3)")

    elif choice == "3":
        submenu_3 = True
        while submenu_3:
            print("\n")
            print(".......... Modify/Update Product (menu) ..........")
            print("1. update quantity of specific product")  # 2
            print("2. Update price of specific product")  # 2
            print("3. Apply Discount") 
            print("4. Go back")
            print("-"*75)
            choice = input("Enter your choice (1-4):  ").strip()
            print("-"*75)
            if choice == "1":  # Updates quantity of a product, when name is given
                product_name = input("Enter name of product: ").strip()
                product_found = manager.search_product_by_name(product_name)
                if isinstance(product_found, dict):
                    added_quantity = float(input("Enter quantity to be added/subtracted: ").strip())
                    product_obj = Product(**product_found)
                    try:
                        updated_quantity = product_obj.update_quantity(added_quantity)
                        print(f"Quantity of given product '{product_name}' has been updated to {updated_quantity}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Product not found!")
            elif choice == "2":  # # Updates price of a product, when name is given
                product_name = input("Enter name of product: ").strip()
                product_found = manager.search_product_by_name(product_name)
                if isinstance(product_found, dict):
                    updated_price = float(input("Enter new price: ").strip())
                    product_obj = Product(**product_found)
                    try:
                        product_obj.update_price(updated_price)
                        print("\n")
                        print(f"Price of given product '{product_name}' has been updated to '${updated_price}'")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Product not found!")
            elif choice == "3":  # applies discount to a product, when name is given
                product_name = input("Enter name of product: ").strip()
                product_found = manager.search_product_by_name(product_name)
                if isinstance(product_found, dict):
                    product_found_obj = Product(**product_found)
                    discount_percentage = float(input("Enter Discount Percentage: "))
                    try:
                        if product_found:
                            product_found_obj.apply_discount(discount_percentage)
                            print("\n")
                            print(f"Discount applied successfully! New Price: {product_found_obj.price}")
                        else:
                            print("\n")
                            print("Product not found.")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Product not found!")
            elif choice == "4":  # Goes back to main menu
                submenu_3 = False
            else:
                print("Invalid option! Please Enter a no between (1 - 4)")

    elif choice == "4":
        submenu_4 = True
        while submenu_4:
            print("\n")
            print(".......... Filter Products (menu) ..........")
            print("1. Filter products by price")  # 3
            print("2. Filter products by category")  # 3
            print("3. Filter products by low quantity (less than 5)")
            print("4. Go back")
            print("-"*75)
            choice = input("Enter your choice (1-4):  ").strip()
            print("-"*75)
            if choice == "1":  # Provides a list of products with price below given price
                result = manager.filter_product_by_price()
                if result:
                    for items in result:
                        print(f"Product_name: {items[1]['product_name']}--- Product_price: {items[1]['price']}")
                else:
                    print("No product found!")
            elif choice == "2":  # Provides a list of products with choosen category
                products = manager.filter_product_by_category()
                if isinstance(products, list):
                    for items in products:
                        print(f"Product_name: {items[1]['product_name']}--- Product_price: {items[1]['price']}")
                else:
                    print("Category not found!")
            elif choice == "3":  # Provides a list of products with quantity less than 5
                products_found = manager.filter_product_with_low_quantity()
                try:
                    for items in products_found:
                        print(f"Product_name: {items[1]['product_name']}--- Product_quantity: {items[1]['quantity']}")
                except TypeError:
                    print("No need to update quantity of any product")
            elif choice == "4":  # Goes back to main menu
                submenu_4 = False
            else:
                print("Invalid option! Please Enter a no between (1 - 4)")

    elif choice == "5":
        print("Exiting the Inventory Management System.")
        print("\n")
        break
    else:
        print("Invalid choice. Please try again.")
        print("\n")
