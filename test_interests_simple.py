#!/usr/bin/env python3
"""
Simple test script using urllib to test interests functionality
"""
import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8000"

def make_request(url, data=None, headers=None, method='GET'):
    """Make HTTP request using urllib"""
    if headers is None:
        headers = {}
    
    if data is not None:
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        elif isinstance(data, str):
            data = data.encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return {
                'status': response.status,
                'data': json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        return {
            'status': e.code,
            'error': e.read().decode('utf-8')
        }
    except Exception as e:
        return {
            'status': 0,
            'error': str(e)
        }

def test_backend_health():
    """Test if backend is running"""
    print("🔍 Testing backend health...")
    result = make_request(f"{BASE_URL}/health")
    
    if result['status'] == 200:
        print("✅ Backend is running!")
        return True
    else:
        print(f"❌ Backend health check failed: {result}")
        return False

def test_registration_and_interests():
    """Test user registration and interests functionality"""
    
    if not test_backend_health():
        return False
    
    # Test user registration
    print("\n📝 Testing user registration...")
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    reg_result = make_request(f"{BASE_URL}/auth/register", user_data, method='POST')
    
    if reg_result['status'] in [200, 201]:
        print("✅ User registration successful!")
    elif reg_result['status'] == 400 and 'already registered' in reg_result.get('error', ''):
        print("ℹ️ User already exists, continuing...")
    else:
        print(f"❌ Registration failed: {reg_result}")
    
    # Test login
    print("\n🔐 Testing login...")
    login_data = urllib.parse.urlencode({
        'username': 'testuser@example.com',
        'password': 'testpassword123'
    })
    
    login_result = make_request(
        f"{BASE_URL}/auth/login", 
        login_data, 
        {'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST'
    )
    
    if login_result['status'] != 200:
        print(f"❌ Login failed: {login_result}")
        return False
    
    token = login_result['data'].get('access_token')
    if not token:
        print("❌ No access token received")
        return False
    
    print("✅ Login successful!")
    
    # Set up authenticated headers
    auth_headers = {'Authorization': f'Bearer {token}'}
    
    # Test getting current user
    print("\n👤 Testing get current user...")
    user_result = make_request(f"{BASE_URL}/users/me", headers=auth_headers)
    
    if user_result['status'] == 200:
        user_info = user_result['data']
        print(f"✅ User info retrieved: {user_info.get('email')}")
        print(f"   Current interests: {user_info.get('interests', [])}")
    else:
        print(f"❌ Failed to get user info: {user_result}")
        return False
    
    # Test updating interests
    print("\n💡 Testing interests update...")
    interests_data = {
        "interests": ["Data Science", "Machine Learning", "Web Development", "AI", "Python"]
    }
    
    interests_result = make_request(
        f"{BASE_URL}/users/me/interests", 
        interests_data, 
        auth_headers, 
        method='PUT'
    )
    
    if interests_result['status'] == 200:
        updated_user = interests_result['data']
        print(f"✅ Interests updated successfully!")
        print(f"   New interests: {updated_user.get('interests', [])}")
    else:
        print(f"❌ Failed to update interests: {interests_result}")
        return False
    
    # Test getting interests
    print("\n🔍 Testing get interests...")
    get_interests_result = make_request(f"{BASE_URL}/users/me/interests", headers=auth_headers)
    
    if get_interests_result['status'] == 200:
        interests_info = get_interests_result['data']
        print(f"✅ Interests retrieved: {interests_info.get('interests', [])}")
    else:
        print(f"❌ Failed to get interests: {get_interests_result}")
    
    # Test recommendations
    print("\n🎯 Testing recommendations...")
    rec_result = make_request(f"{BASE_URL}/recommendations/?limit=3", headers=auth_headers)
    
    if rec_result['status'] == 200:
        rec_data = rec_result['data']
        print(f"✅ Recommendations received!")
        print(f"   User interests: {rec_data.get('user_interests', [])}")
        print(f"   Number of recommendations: {len(rec_data.get('recommendations', []))}")
        
        recommendations = rec_data.get('recommendations', [])
        if recommendations:
            first_rec = recommendations[0]
            print(f"   First recommendation: {first_rec.get('course_name')} ({first_rec.get('match_percentage')}% match)")
    else:
        print(f"❌ Failed to get recommendations: {rec_result}")
    
    print(f"\n🎉 All tests completed! You can now login to the frontend with:")
    print(f"   Email: testuser@example.com")
    print(f"   Password: testpassword123")
    
    return True

if __name__ == "__main__":
    success = test_registration_and_interests()
    if success:
        print("\n✅ Backend interests functionality is working!")
    else:
        print("\n❌ Some tests failed. Check the backend logs.")
    
    sys.exit(0 if success else 1)
