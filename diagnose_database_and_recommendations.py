#!/usr/bin/env python3
"""
Comprehensive diagnostic script for database fetching and recommendations
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

def test_database_endpoints():
    """Test all database endpoints to see if they fetch real data"""
    print("🗄️ Testing Database Endpoints...")
    print("=" * 50)
    
    # Test colleges
    print("\n1. Testing Colleges Endpoint:")
    colleges_result = make_request(f"{BASE_URL}/colleges/")
    if colleges_result['status'] == 200:
        colleges = colleges_result['data']
        print(f"✅ Found {len(colleges)} colleges in database")
        if colleges:
            print("   Sample colleges:")
            for i, college in enumerate(colleges[:3]):
                print(f"   {i+1}. {college.get('name', 'Unknown')} - {college.get('city', 'Unknown')}")
        else:
            print("   ⚠️ No colleges found in database")
    else:
        print(f"❌ Failed to fetch colleges: {colleges_result}")
    
    # Test courses
    print("\n2. Testing Courses Endpoint:")
    courses_result = make_request(f"{BASE_URL}/courses/")
    if courses_result['status'] == 200:
        courses = courses_result['data']
        print(f"✅ Found {len(courses)} courses in database")
        if courses:
            print("   Sample courses:")
            for i, course in enumerate(courses[:3]):
                print(f"   {i+1}. {course.get('title', 'Unknown')} - {course.get('category', 'Unknown')}")
        else:
            print("   ⚠️ No courses found in database")
    else:
        print(f"❌ Failed to fetch courses: {courses_result}")
    
    # Test careers
    print("\n3. Testing Careers Endpoint:")
    careers_result = make_request(f"{BASE_URL}/careers/")
    if careers_result['status'] == 200:
        careers = careers_result['data']
        print(f"✅ Found {len(careers)} careers in database")
        if careers:
            print("   Sample careers:")
            for i, career in enumerate(careers[:3]):
                print(f"   {i+1}. {career.get('title', 'Unknown')} - {career.get('field', 'Unknown')}")
        else:
            print("   ⚠️ No careers found in database")
    else:
        print(f"❌ Failed to fetch careers: {careers_result}")

def test_recommendations():
    """Test recommendation system"""
    print("\n\n🎯 Testing Recommendation System...")
    print("=" * 50)
    
    # First login to get token
    print("\n1. Logging in...")
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
    auth_headers = {'Authorization': f'Bearer {token}'}
    print("✅ Login successful!")
    
    # Test user interests
    print("\n2. Checking user interests...")
    interests_result = make_request(f"{BASE_URL}/users/me/interests", headers=auth_headers)
    if interests_result['status'] == 200:
        interests = interests_result['data'].get('interests', [])
        print(f"✅ User interests: {interests}")
    else:
        print(f"❌ Failed to get interests: {interests_result}")
        return False
    
    # Test recommendations endpoint
    print("\n3. Testing recommendations endpoint...")
    rec_result = make_request(f"{BASE_URL}/recommendations/?limit=5", headers=auth_headers)
    
    if rec_result['status'] == 200:
        rec_data = rec_result['data']
        recommendations = rec_data.get('recommendations', [])
        user_interests = rec_data.get('user_interests', [])
        
        print(f"✅ Recommendations endpoint working!")
        print(f"   User interests used: {user_interests}")
        print(f"   Number of recommendations: {len(recommendations)}")
        
        if recommendations:
            print("   Sample recommendations:")
            for i, rec in enumerate(recommendations[:3]):
                print(f"   {i+1}. {rec.get('course_name', 'Unknown')} ({rec.get('match_percentage', 0)}% match)")
                print(f"      {rec.get('description', 'No description')}")
        else:
            print("   ⚠️ No recommendations generated")
            print("   This might be due to:")
            print("   - No courses in database")
            print("   - ML model not working")
            print("   - User interests not matching any courses")
        
        return True
    else:
        print(f"❌ Recommendations failed: {rec_result}")
        return False

def test_search_functionality():
    """Test search endpoints"""
    print("\n\n🔍 Testing Search Functionality...")
    print("=" * 50)
    
    # Test college search
    print("\n1. Testing college search (SNS)...")
    search_result = make_request(f"{BASE_URL}/colleges/search?query=SNS")
    if search_result['status'] == 200:
        results = search_result['data']
        print(f"✅ Found {len(results)} colleges matching 'SNS'")
        for college in results:
            print(f"   - {college.get('name')} in {college.get('city')}")
    else:
        print(f"❌ College search failed: {search_result}")
    
    # Test course search
    print("\n2. Testing course search (Engineering)...")
    course_search_result = make_request(f"{BASE_URL}/courses/search?q=Engineering")
    if course_search_result['status'] == 200:
        results = course_search_result['data']
        print(f"✅ Found {len(results)} courses matching 'Engineering'")
        for course in results[:3]:
            print(f"   - {course.get('title', 'Unknown')}")
    else:
        print(f"❌ Course search failed: {course_search_result}")

def check_ml_data_files():
    """Check if ML recommendation data files exist"""
    print("\n\n🤖 Checking ML Data Files...")
    print("=" * 50)
    
    import os
    
    data_files = [
        'data/courses.csv',
        'data/user_aptitude.csv', 
        'data/user_interests.json'
    ]
    
    for file_path in data_files:
        full_path = os.path.join(os.path.dirname(__file__), 'career-tracking-backend', file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path} exists")
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if file_path.endswith('.csv'):
                        lines = content.split('\n')
                        print(f"   Contains {len(lines)} lines")
                    elif file_path.endswith('.json'):
                        data = json.loads(content)
                        print(f"   Contains {len(data)} entries")
            except Exception as e:
                print(f"   ⚠️ Error reading file: {e}")
        else:
            print(f"❌ {file_path} missing")

def main():
    """Run all diagnostic tests"""
    print("🔧 Comprehensive Database & Recommendations Diagnostic")
    print("=" * 60)
    
    # Test database endpoints
    test_database_endpoints()
    
    # Test recommendations
    test_recommendations()
    
    # Test search functionality
    test_search_functionality()
    
    # Check ML data files
    check_ml_data_files()
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY & RECOMMENDATIONS:")
    print("=" * 60)
    print("1. If colleges/courses show 0 results:")
    print("   → Your database tables are empty")
    print("   → Add sample data or import your data")
    print()
    print("2. If recommendations don't work:")
    print("   → Check if courses exist in database")
    print("   → Verify ML data files are present")
    print("   → Ensure user has interests set")
    print()
    print("3. To add new data to database:")
    print("   → Use database admin tools")
    print("   → Or create API endpoints for data upload")
    print("   → Data will appear immediately in frontend")

if __name__ == "__main__":
    main()
