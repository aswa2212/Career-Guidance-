#!/usr/bin/env python3
"""
Test script to debug interests functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_interests():
    """Test user interests functionality"""
    
    # First, let's try to login with a test user
    login_data = {
        "username": "test@example.com",  # Using email as username
        "password": "testpassword"
    }
    
    try:
        # Login
        print("🔐 Attempting login...")
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token_data = login_response.json()
        token = token_data.get("access_token")
        
        if not token:
            print("❌ No access token received")
            return
        
        print("✅ Login successful!")
        
        # Set up headers for authenticated requests
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test getting current user
        print("\n👤 Getting current user...")
        user_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            print(f"✅ User data: {json.dumps(user_data, indent=2)}")
            print(f"Current interests: {user_data.get('interests', [])}")
        else:
            print(f"❌ Failed to get user: {user_response.status_code}")
            print(f"Response: {user_response.text}")
            return
        
        # Test getting user interests
        print("\n💡 Getting user interests...")
        interests_response = requests.get(f"{BASE_URL}/users/me/interests", headers=headers)
        
        if interests_response.status_code == 200:
            interests_data = interests_response.json()
            print(f"✅ Interests data: {json.dumps(interests_data, indent=2)}")
        else:
            print(f"❌ Failed to get interests: {interests_response.status_code}")
            print(f"Response: {interests_response.text}")
        
        # Test updating interests
        print("\n📝 Updating user interests...")
        new_interests = ["Data Science", "Machine Learning", "Web Development", "AI"]
        update_data = {"interests": new_interests}
        
        update_response = requests.put(
            f"{BASE_URL}/users/me/interests", 
            headers=headers,
            json=update_data
        )
        
        if update_response.status_code == 200:
            updated_user = update_response.json()
            print(f"✅ Interests updated successfully!")
            print(f"New interests: {updated_user.get('interests', [])}")
        else:
            print(f"❌ Failed to update interests: {update_response.status_code}")
            print(f"Response: {update_response.text}")
        
        # Test recommendations
        print("\n🎯 Getting recommendations...")
        rec_response = requests.get(f"{BASE_URL}/recommendations/?limit=5", headers=headers)
        
        if rec_response.status_code == 200:
            rec_data = rec_response.json()
            print(f"✅ Recommendations received!")
            print(f"User interests from API: {rec_data.get('user_interests', [])}")
            print(f"Number of recommendations: {len(rec_data.get('recommendations', []))}")
            
            # Show first recommendation
            recommendations = rec_data.get('recommendations', [])
            if recommendations:
                first_rec = recommendations[0]
                print(f"First recommendation: {first_rec.get('course_name')} ({first_rec.get('match_percentage')}% match)")
        else:
            print(f"❌ Failed to get recommendations: {rec_response.status_code}")
            print(f"Response: {rec_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_user_interests()
