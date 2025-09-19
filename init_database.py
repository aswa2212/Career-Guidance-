#!/usr/bin/env python3
"""
Initialize database with test user
"""

import requests
import json

def create_test_user():
    """Create a test user via API"""
    print("🔧 Creating test user via API...")
    
    base_url = "http://127.0.0.1:8000"
    
    # Test user data
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    
    try:
        # Try to register the user
        response = requests.post(f"{base_url}/auth/register", json=user_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Test user created successfully!")
            print(f"   Email: test@example.com")
            print(f"   Password: password123")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("✅ Test user already exists!")
            print(f"   Email: test@example.com")
            print(f"   Password: password123")
            return True
        else:
            print(f"❌ Failed to create user: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

def test_login():
    """Test login with the test user"""
    print("\n🔐 Testing login...")
    
    base_url = "http://127.0.0.1:8000"
    
    # Login data
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/login", 
            data=login_data,  # Use form data for OAuth2
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"   Access token: {data.get('access_token', 'N/A')[:20]}...")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing login: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing database and testing authentication...")
    
    # Create test user
    user_created = create_test_user()
    
    if user_created:
        # Test login
        login_success = test_login()
        
        if login_success:
            print("\n🎉 Authentication system is working!")
            print("\nYou can now:")
            print("1. Go to http://localhost:3000")
            print("2. Login with:")
            print("   Email: test@example.com")
            print("   Password: password123")
        else:
            print("\n❌ Authentication test failed")
    else:
        print("\n❌ Failed to create test user")
