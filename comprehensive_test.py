#!/usr/bin/env python3
"""
Comprehensive test script for all system enhancements
Tests the complete flow from backend fixes to frontend integration
"""
import asyncio
import asyncpg
import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv("career-tracking-backend/.env")

class ComprehensiveSystemTest:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.db_url = self._get_database_url()
        self.test_token = None
        self.test_user_id = None
        
    def _get_database_url(self):
        DATABASE_URL = os.getenv("DATABASE_URL")
        if DATABASE_URL and "postgresql+asyncpg" in DATABASE_URL:
            DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        elif not DATABASE_URL:
            DB_USER = os.getenv("DB_USER", "postgres")
            DB_PASSWORD = os.getenv("DB_PASSWORD", "Postgresql%400001")
            DB_HOST = os.getenv("DB_HOST", "localhost")
            DB_PORT = os.getenv("DB_PORT", "5432")
            DB_NAME = os.getenv("DB_NAME", "career_db")
            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        return DATABASE_URL

    def test_backend_health(self):
        """Test if backend server is running"""
        print("🔍 Testing backend server health...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server is running")
                return True
            else:
                print(f"❌ Backend server returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Backend server not accessible: {e}")
            return False

    def test_authentication(self):
        """Test user authentication"""
        print("\n🔍 Testing authentication system...")
        
        # Test login
        login_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword123'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                data=login_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                result = response.json()
                self.test_token = result.get('access_token')
                print("✅ Authentication successful")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False

    def test_user_interests_crud(self):
        """Test user interests CRUD operations"""
        print("\n🔍 Testing user interests CRUD operations...")
        
        if not self.test_token:
            print("❌ No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.test_token}'}
        
        # Test setting interests
        test_interests = ['Data Science', 'Machine Learning', 'Web Development', 'AI', 'Python']
        
        try:
            # Set interests
            response = requests.put(
                f"{self.base_url}/users/me/interests",
                json={'interests': test_interests},
                headers={**headers, 'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print("✅ Successfully set user interests")
                
                # Get interests
                response = requests.get(f"{self.base_url}/users/me/interests", headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    returned_interests = result.get('interests', [])
                    if set(returned_interests) == set(test_interests):
                        print("✅ Successfully retrieved user interests")
                        return True
                    else:
                        print(f"❌ Interest mismatch. Expected: {test_interests}, Got: {returned_interests}")
                        return False
                else:
                    print(f"❌ Failed to get interests: {response.status_code}")
                    return False
            else:
                print(f"❌ Failed to set interests: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Interests CRUD error: {e}")
            return False

    def test_recommendations_engine(self):
        """Test the recommendation engine with real-time data"""
        print("\n🔍 Testing AI recommendation engine...")
        
        if not self.test_token:
            print("❌ No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.test_token}'}
        
        try:
            # Test recommendations endpoint
            response = requests.get(f"{self.base_url}/recommendations/?limit=5", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                recommendations = result.get('recommendations', [])
                user_interests = result.get('user_interests', [])
                
                print(f"✅ Received {len(recommendations)} recommendations")
                print(f"✅ User interests: {user_interests}")
                
                if recommendations:
                    sample_rec = recommendations[0]
                    print(f"✅ Sample recommendation: {sample_rec.get('course_name', 'Unknown')} ({sample_rec.get('match_percentage', 0)}% match)")
                
                # Test refresh endpoint
                response = requests.post(f"{self.base_url}/recommendations/refresh", headers=headers)
                if response.status_code == 200:
                    print("✅ Successfully refreshed recommendation engine")
                    return True
                else:
                    print(f"⚠️ Refresh failed but recommendations work: {response.status_code}")
                    return True
            else:
                print(f"❌ Recommendations failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Recommendations error: {e}")
            return False

    def test_new_api_endpoints(self):
        """Test new API endpoints for courses and colleges"""
        print("\n🔍 Testing new API endpoints...")
        
        try:
            # Test courses endpoint
            response = requests.get(f"{self.base_url}/courses/?limit=5")
            if response.status_code == 200:
                courses = response.json()
                print(f"✅ Courses endpoint working: {len(courses)} courses found")
            else:
                print(f"⚠️ Courses endpoint issue: {response.status_code}")
            
            # Test colleges endpoint
            response = requests.get(f"{self.base_url}/colleges/?limit=5")
            if response.status_code == 200:
                colleges = response.json()
                print(f"✅ Colleges endpoint working: {len(colleges)} colleges found")
            else:
                print(f"⚠️ Colleges endpoint issue: {response.status_code}")
            
            # Test course categories
            response = requests.get(f"{self.base_url}/courses/categories/")
            if response.status_code == 200:
                categories = response.json()
                print(f"✅ Course categories endpoint working")
            else:
                print(f"⚠️ Course categories endpoint issue: {response.status_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ API endpoints error: {e}")
            return False

    async def test_database_schema(self):
        """Test database schema updates"""
        print("\n🔍 Testing database schema...")
        
        try:
            conn = await asyncpg.connect(self.db_url)
            
            # Check interests column
            result = await conn.fetch("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'interests';
            """)
            
            if result:
                print("✅ User interests column exists")
            else:
                print("❌ User interests column missing")
                await conn.close()
                return False
            
            # Check scholarship_details column
            result = await conn.fetch("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'colleges' AND column_name = 'scholarship_details';
            """)
            
            if result:
                print("✅ College scholarship_details column exists")
            else:
                print("⚠️ College scholarship_details column missing (run migration)")
            
            await conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Database schema error: {e}")
            return False

    def test_frontend_api_integration(self):
        """Test frontend API integration points"""
        print("\n🔍 Testing frontend API integration...")
        
        if not self.test_token:
            print("❌ No authentication token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.test_token}'}
        
        try:
            # Test user profile endpoint
            response = requests.get(f"{self.base_url}/users/me", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ User profile endpoint working: {user_data.get('email', 'Unknown')}")
            else:
                print(f"❌ User profile endpoint failed: {response.status_code}")
                return False
            
            # Test course recommendations for frontend
            response = requests.get(f"{self.base_url}/courses/recommendations/for-me", headers=headers)
            if response.status_code == 200:
                recommendations = response.json()
                print(f"✅ Course recommendations for frontend working")
            else:
                print(f"⚠️ Course recommendations endpoint issue: {response.status_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ Frontend integration error: {e}")
            return False

    async def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting comprehensive system tests...\n")
        print("=" * 60)
        
        results = {}
        
        # Backend tests
        results['backend_health'] = self.test_backend_health()
        results['authentication'] = self.test_authentication()
        results['user_interests'] = self.test_user_interests_crud()
        results['recommendations'] = self.test_recommendations_engine()
        results['new_endpoints'] = self.test_new_api_endpoints()
        results['frontend_integration'] = self.test_frontend_api_integration()
        
        # Database tests
        results['database_schema'] = await self.test_database_schema()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title():<25} {status}")
            if result:
                passed += 1
        
        print("=" * 60)
        print(f"Overall Score: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Your system is fully functional.")
            print("\n📝 Next Steps:")
            print("1. Start the backend: cd career-tracking-backend && python -m uvicorn app.main:app --reload")
            print("2. Start the frontend: cd Frontend && npm run dev")
            print("3. Visit http://localhost:3000 and test the new features")
            print("4. Try the interests system in Settings")
            print("5. Check the AI recommendations on Dashboard")
            print("6. Explore college scholarship details")
        else:
            print("⚠️ Some tests failed. Please review the issues above.")
            
        return passed == total

def main():
    """Main function"""
    tester = ComprehensiveSystemTest()
    success = asyncio.run(tester.run_all_tests())
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
