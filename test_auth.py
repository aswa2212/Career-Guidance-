import requests
import json

# Test authentication endpoints
BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = requests.post(url, json=data)
    print(f"Register Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Registration successful!")
        print(f"Response: {response.json()}")
        return True
    else:
        print(f"❌ Registration failed: {response.text}")
        return False

def test_login():
    """Test user login"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(url, data=data)
    print(f"Login Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login successful!")
        result = response.json()
        print(f"Token received: {result.get('access_token', 'No token')[:50]}...")
        return result.get('access_token')
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_protected_route(token):
    """Test accessing protected route"""
    url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"Protected Route Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Protected route access successful!")
        print(f"User data: {response.json()}")
        return True
    else:
        print(f"❌ Protected route failed: {response.text}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Authentication Flow...")
    print("=" * 50)
    
    # Test registration
    print("\n1. Testing Registration:")
    register_success = test_register()
    
    # Test login
    print("\n2. Testing Login:")
    token = test_login()
    
    # Test protected route
    if token:
        print("\n3. Testing Protected Route:")
        test_protected_route(token)
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")
