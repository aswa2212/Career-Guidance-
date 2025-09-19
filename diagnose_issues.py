#!/usr/bin/env python3
"""
Diagnostic script to check database and API issues
"""
import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

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
        error_body = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_body)
        except:
            error_data = error_body
        return {
            'status': e.code,
            'error': error_data
        }
    except Exception as e:
        return {
            'status': 0,
            'error': str(e)
        }

def test_backend_health():
    """Test backend health"""
    print("🔍 Testing backend health...")
    result = make_request(f"{BASE_URL}/health")
    
    if result['status'] == 200:
        print("✅ Backend is healthy!")
        return True
    else:
        print(f"❌ Backend health check failed: {result}")
        return False

def test_colleges_endpoint():
    """Test colleges endpoint to see if SNS college is there"""
    print("\n🏫 Testing colleges endpoint...")
    result = make_request(f"{BASE_URL}/colleges/")
    
    if result['status'] == 200:
        colleges = result['data']
        print(f"✅ Found {len(colleges)} colleges")
        
        # Look for SNS college
        sns_colleges = [c for c in colleges if 'SNS' in c.get('name', '').upper()]
        if sns_colleges:
            print(f"✅ Found SNS college(s): {[c['name'] for c in sns_colleges]}")
        else:
            print("❌ No SNS college found in the data")
            print("Available colleges:")
            for college in colleges[:5]:  # Show first 5
                print(f"   - {college.get('name', 'Unknown')}")
        return True
    else:
        print(f"❌ Failed to get colleges: {result}")
        return False

def test_login_and_interests():
    """Test login and interests functionality"""
    print("\n🔐 Testing login...")
    
    # Try login
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
    
    # Test interests with authentication
    auth_headers = {'Authorization': f'Bearer {token}'}
    
    print("\n💡 Testing interests endpoint...")
    interests_result = make_request(f"{BASE_URL}/users/me/interests", headers=auth_headers)
    
    if interests_result['status'] == 200:
        interests_data = interests_result['data']
        print(f"✅ Interests loaded successfully: {interests_data.get('interests', [])}")
        return True
    else:
        print(f"❌ Failed to load interests: {interests_result}")
        return False

def test_user_profile():
    """Test user profile endpoint"""
    print("\n👤 Testing user profile...")
    
    # Login first
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
        print(f"❌ Login failed for profile test")
        return False
    
    token = login_result['data'].get('access_token')
    auth_headers = {'Authorization': f'Bearer {token}'}
    
    # Get user profile
    profile_result = make_request(f"{BASE_URL}/users/me", headers=auth_headers)
    
    if profile_result['status'] == 200:
        user_data = profile_result['data']
        print(f"✅ User profile loaded:")
        print(f"   Email: {user_data.get('email')}")
        print(f"   Name: {user_data.get('full_name')}")
        print(f"   Interests: {user_data.get('interests', [])}")
        return True
    else:
        print(f"❌ Failed to load user profile: {profile_result}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔧 Running diagnostic tests...\n")
    
    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not healthy. Please check if it's running.")
        return False
    
    # Test colleges endpoint
    test_colleges_endpoint()
    
    # Test login and interests
    test_login_and_interests()
    
    # Test user profile
    test_user_profile()
    
    print("\n🎯 Diagnostic complete!")
    return True

if __name__ == "__main__":
    main()
