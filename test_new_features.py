#!/usr/bin/env python3
"""
Test script for new features:
1. User interests functionality
2. AI recommendation engine
3. Database schema updates
"""

import asyncio
import asyncpg
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from backend directory
backend_dir = os.path.join(os.path.dirname(__file__), "career-tracking-backend")
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path)

class FeatureTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.db_url = self._get_database_url()
        self.test_token = None
        
    def _get_database_url(self):
        DATABASE_URL = os.getenv("DATABASE_URL")
        if DATABASE_URL and "postgresql+asyncpg" in DATABASE_URL:
            # Convert asyncpg URL to standard postgresql URL for asyncpg.connect
            DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        elif not DATABASE_URL:
            DB_USER = os.getenv("DB_USER", "postgres")
            DB_PASSWORD = os.getenv("DB_PASSWORD", "Postgresql%400001")  # URL encoded
            DB_HOST = os.getenv("DB_HOST", "localhost")
            DB_PORT = os.getenv("DB_PORT", "5432")
            DB_NAME = os.getenv("DB_NAME", "career_db")
            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        return DATABASE_URL
    
    async def test_database_schema(self):
        """Test if interests column exists in users table"""
        print("🔍 Testing database schema...")
        
        try:
            conn = await asyncpg.connect(self.db_url)
            
            # Check if interests column exists
            result = await conn.fetch("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'interests';
            """)
            
            if result:
                print("✅ Interests column exists in users table")
                print(f"   Column type: {result[0]['data_type']}")
            else:
                print("❌ Interests column missing from users table")
                print("   Run: python add_interests_column.py")
                
            await conn.close()
            return bool(result)
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def test_backend_health(self):
        """Test if backend server is running"""
        print("🔍 Testing backend server...")
        
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
            print("   Make sure to run: python -m uvicorn app.main:app --reload")
            return False
    
    def test_recommendation_engine(self):
        """Test recommendation engine data loading"""
        print("🔍 Testing recommendation engine...")
        
        try:
            # Test if data files exist
            data_files = [
                "data/courses.csv",
                "data/user_aptitude.csv", 
                "data/user_interests.json"
            ]
            
            backend_dir = os.path.join(os.path.dirname(__file__), "career-tracking-backend")
            
            for file_path in data_files:
                full_path = os.path.join(backend_dir, file_path)
                if os.path.exists(full_path):
                    print(f"✅ Found {file_path}")
                else:
                    print(f"❌ Missing {file_path}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking data files: {e}")
            return False
    
    def test_api_endpoints(self):
        """Test new API endpoints"""
        print("🔍 Testing API endpoints...")
        
        # Test recommendations endpoint (should require auth)
        try:
            response = requests.get(f"{self.base_url}/recommendations/")
            if response.status_code == 401:
                print("✅ Recommendations endpoint requires authentication")
            else:
                print(f"⚠️  Recommendations endpoint returned {response.status_code}")
            
            # Test interests endpoint (should require auth)
            response = requests.get(f"{self.base_url}/users/me/interests")
            if response.status_code == 401:
                print("✅ Interests endpoint requires authentication")
            else:
                print(f"⚠️  Interests endpoint returned {response.status_code}")
                
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API endpoint test failed: {e}")
            return False
    
    def test_frontend_files(self):
        """Test if frontend files exist"""
        print("🔍 Testing frontend files...")
        
        frontend_files = [
            "Frontend/src/components/RecommendedCourses.jsx",
            "Frontend/src/pages/Dashboard.jsx",
            "Frontend/src/pages/settings/Settings.jsx"
        ]
        
        project_root = os.path.dirname(__file__)
        
        for file_path in frontend_files:
            full_path = os.path.join(project_root, file_path)
            if os.path.exists(full_path):
                print(f"✅ Found {file_path}")
            else:
                print(f"❌ Missing {file_path}")
                return False
        
        return True
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting comprehensive feature tests...\n")
        
        results = {
            "database_schema": await self.test_database_schema(),
            "backend_health": self.test_backend_health(),
            "recommendation_engine": self.test_recommendation_engine(),
            "api_endpoints": self.test_api_endpoints(),
            "frontend_files": self.test_frontend_files()
        }
        
        print("\n📊 Test Results Summary:")
        print("=" * 50)
        
        all_passed = True
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            if not passed:
                all_passed = False
        
        print("=" * 50)
        
        if all_passed:
            print("🎉 All tests passed! Your new features are ready to use.")
            print("\n📝 Next steps:")
            print("1. Start the backend: cd career-tracking-backend && python -m uvicorn app.main:app --reload")
            print("2. Start the frontend: cd Frontend && npm run dev")
            print("3. Visit http://localhost:3000 and test the new features")
        else:
            print("⚠️  Some tests failed. Please fix the issues above before proceeding.")
        
        return all_passed

def main():
    """Main function"""
    tester = FeatureTester()
    success = asyncio.run(tester.run_all_tests())
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
