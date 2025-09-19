#!/usr/bin/env python3
"""
Test script to verify interests are working in main frontend
"""
import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:8000"

def test_interests_flow():
    """Test the complete interests flow"""
    print("🧪 Testing Interests in Main Frontend")
    print("=" * 50)
    
    # Step 1: Login
    print("\n1. Logging in...")
    login_data = urllib.parse.urlencode({
        'username': 'testuser@example.com',
        'password': 'testpassword123'
    })
    
    try:
        login_req = urllib.request.Request(f"{BASE_URL}/auth/login", 
                                         data=login_data.encode(), 
                                         headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with urllib.request.urlopen(login_req) as response:
            login_result = json.loads(response.read().decode())
            token = login_result.get('access_token')
            print("✅ Login successful!")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return
    
    auth_headers = {'Authorization': f'Bearer {token}'}
    
    # Step 2: Set some interests
    print("\n2. Setting user interests...")
    test_interests = ['Data Science', 'Machine Learning', 'Web Development', 'AI', 'Python']
    
    try:
        interests_data = json.dumps({'interests': test_interests}).encode()
        interests_req = urllib.request.Request(f"{BASE_URL}/users/me/interests", 
                                             data=interests_data,
                                             headers={**auth_headers, 'Content-Type': 'application/json'},
                                             method='PUT')
        with urllib.request.urlopen(interests_req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ Interests set: {result.get('interests', [])}")
    except Exception as e:
        print(f"❌ Failed to set interests: {e}")
        return
    
    # Step 3: Test recommendations endpoint
    print("\n3. Testing recommendations with interests...")
    try:
        rec_req = urllib.request.Request(f"{BASE_URL}/recommendations/?limit=3", 
                                       headers=auth_headers)
        with urllib.request.urlopen(rec_req) as response:
            rec_result = json.loads(response.read().decode())
            
            user_interests = rec_result.get('user_interests', [])
            recommendations = rec_result.get('recommendations', [])
            
            print(f"✅ User interests returned: {user_interests}")
            print(f"✅ Number of recommendations: {len(recommendations)}")
            
            if recommendations:
                print("📋 Sample recommendations:")
                for i, rec in enumerate(recommendations[:2]):
                    print(f"   {i+1}. {rec.get('course_name', 'Unknown')} ({rec.get('match_percentage', 0)}% match)")
            
            if rec_result.get('error'):
                print(f"⚠️ Note: {rec_result['error']}")
                
    except Exception as e:
        print(f"❌ Failed to get recommendations: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🎯 FRONTEND TESTING INSTRUCTIONS")
    print("=" * 50)
    print("1. Open your main frontend: http://localhost:3001")
    print("2. Login with: testuser@example.com / testpassword123")
    print("3. Go to Dashboard - you should see:")
    print("   ✅ 'Recommended for You' section")
    print("   ✅ 'Based on your interests:' with blue tags")
    print("   ✅ Interest tags: Data Science, Machine Learning, etc.")
    print("4. Go to Settings - you should see:")
    print("   ✅ 'My Interests' section with your interests")
    print("   ✅ Ability to add/remove interests")
    print("5. After changing interests in Settings:")
    print("   ✅ Go back to Dashboard")
    print("   ✅ Click refresh button in recommendations")
    print("   ✅ New interests should appear")

if __name__ == "__main__":
    test_interests_flow()
