import requests
import json

# Test with a fresh user
print("🧪 Testing Authentication with Fresh User...")

# Register new user
print("\n1. Registering new user...")
register_data = {
    "email": "freshuser@example.com",
    "password": "freshpass123",
    "full_name": "Fresh User"
}

try:
    r1 = requests.post('http://localhost:8000/auth/register', json=register_data)
    print(f"Register Status: {r1.status_code}")
    if r1.status_code == 201:
        print("✅ Registration successful!")
    else:
        print(f"❌ Registration failed: {r1.text}")
except Exception as e:
    print(f"❌ Registration error: {e}")

# Test login
print("\n2. Testing login...")
login_data = {
    "username": "freshuser@example.com",
    "password": "freshpass123"
}

try:
    r2 = requests.post('http://localhost:8000/auth/login', data=login_data)
    print(f"Login Status: {r2.status_code}")
    if r2.status_code == 200:
        response_data = r2.json()
        print("✅ Login successful!")
        print(f"Token received: {response_data.get('access_token', 'No token')[:50]}...")
        
        # Test protected route
        print("\n3. Testing protected route...")
        headers = {"Authorization": f"Bearer {response_data['access_token']}"}
        r3 = requests.get('http://localhost:8000/users/me', headers=headers)
        print(f"Protected Route Status: {r3.status_code}")
        if r3.status_code == 200:
            print("✅ Protected route access successful!")
            user_data = r3.json()
            print(f"User: {user_data.get('full_name')} ({user_data.get('email')})")
        else:
            print(f"❌ Protected route failed: {r3.text}")
    else:
        print(f"❌ Login failed: {r2.text}")
except Exception as e:
    print(f"❌ Login error: {e}")

print("\n🏁 Authentication test completed!")
