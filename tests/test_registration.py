# Test if the user gets registered in the database
# Test if the user already exists in the database and raise an error


import pytest
import registration
import json


class TestRegistration:
    
    registration = Registration("test_users_data.json")

    # Test Fullname
    def test_set_fullname(self):
        # register a user in the database
        registration.set_fullname("Hans Peters")
        users_data = registration.read_users_data()
        result = users_data.get("Hans Peters")
        assert result["fullname"] == "Hans Peters"
                      
                
        # avoid duplicates      
        if user in users_data:
        with pytest.raises(ValueError, match="User already registered"):
            registertration.fullname("Hans Peters")
        print(f"User {fullname} already exists in database")
        
        # avoid empty enteries
        elif user in users_data:
        with pytest.raises(ValueError, match="Full name cannot be empty."):
            registration.fullname("")
        print("Full name cannot be empty.")
    
    
    # Test Email Registration
    def test_set_email(self):
        # register a user in the database
        registration.set_email("peters@example.com")
        users_data = registration.read_users_data()
        result = users_data.get("peters@example.com")
        assert result["email"] == "peters@example.com"
        
        if email in users_data:
            with pytest.raises(ValueError, match="Email already registered"):
                registration.email("peters@example.com")
                print(f"Email {email} already exists in database")
                
        if email in users_data:
            with pytest.raises(ValueError, match="Email is empty."):
                registration.email(" ")
                print("Email cannot be empty.")
                
    
    def test_set_password(self):
        registration.set_password("Peters1234!")
        users_data = registration.read_users_data()
        result = users_data.get("Peters1234!")
        assert result["password"] == "Peters1234!"
        
        if password in users_data:
            with pythest.raises(ValueError, match="Password is empty"):
                registration.password(" ")
                print("Password cannot be empty.")
                
    def test_set_birthday(self):
        register.set_birthday("10.12.1991")
        users_data = registration.read_users_data()
        result = users_data.get("10.12.1991")
        assert result["birthday"] == "10.12.1991"
        
        if birthday in users_data:
            with pytest.raises(ValueError, match="Birthday is empty."):
                registration.birthday(" ")
                print("Birthday cannot be empty.")
                
    def test_set_phone_number(self):
        registration.set_phone_number("+491511678653")
        users_data = registration.read_users_data()
        result = users_data.get("+491511678653")
        assert result["phone_number"] == "+491511678653"
        
        if phone_number in users_data:
            with pytest.raises(ValueError, match="Phone number already exists."):
                registration.phone_number("+491511678653")
                print(f"Phone number {phone_number} already exists in database")
                
        if phone_number in users_data:
            with pytest.raises(ValueError, match="Phone number is empty."):
                registration.phone_number(" ")
                print("Phone number cannot be empty.")
                
        def test_set_address(self):
            registration.set_address("Musterstraße 12, 12345 Musterstadt, Germany")
            users_data = registration.read_users_data()
            result = users_data.get("Musterstraße 12, 12345 Musterstadt,Germany")
            assert result["address"] == "Musterstraße 12, 12345 Musterstadt, Germany"
            
            if address in users_data:
                with pytest.raises(ValueError, match="Address is empty."):
                    registration.address(" ")
                    print("Address cannot be empty.")
            
        
            
        