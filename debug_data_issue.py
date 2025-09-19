#!/usr/bin/env python3
"""
Debug script to check why updated data is not showing in frontend
"""
import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def make_request(url):
    """Make HTTP request with cache busting"""
    try:
        # Add timestamp to prevent caching
        import time
        cache_bust_url = f"{url}{'&' if '?' in url else '?'}_t={int(time.time())}"
        
        req = urllib.request.Request(cache_bust_url)
        req.add_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        req.add_header('Pragma', 'no-cache')
        req.add_header('Expires', '0')
        
        with urllib.request.urlopen(req) as response:
            return {
                'status': response.status,
                'data': json.loads(response.read().decode('utf-8'))
            }
    except Exception as e:
        return {
            'status': 0,
            'error': str(e)
        }

def check_backend_data():
    """Check what data is actually in the backend"""
    print("🔍 Checking Backend Data (Fresh Request)")
    print("=" * 50)
    
    # Check colleges
    print("\n1. Colleges in Backend:")
    colleges_result = make_request(f"{BASE_URL}/colleges/")
    if colleges_result['status'] == 200:
        colleges = colleges_result['data']
        print(f"   Total colleges: {len(colleges)}")
        if colleges:
            for i, college in enumerate(colleges):
                print(f"   {i+1}. {college.get('name', 'Unknown')} - {college.get('city', 'Unknown')}")
        else:
            print("   ❌ NO COLLEGES FOUND IN DATABASE!")
    else:
        print(f"   ❌ Error: {colleges_result}")
    
    # Check courses
    print("\n2. Courses in Backend:")
    courses_result = make_request(f"{BASE_URL}/courses/")
    if courses_result['status'] == 200:
        courses = courses_result['data']
        print(f"   Total courses: {len(courses)}")
        if courses:
            for i, course in enumerate(courses[:5]):
                print(f"   {i+1}. {course.get('title', 'Unknown')}")
        else:
            print("   ❌ NO COURSES FOUND IN DATABASE!")
    else:
        print(f"   ❌ Error: {courses_result}")
    
    # Check SNS specifically
    print("\n3. Searching for SNS:")
    sns_result = make_request(f"{BASE_URL}/colleges/search?query=SNS")
    if sns_result['status'] == 200:
        sns_colleges = sns_result['data']
        if sns_colleges:
            print(f"   ✅ Found {len(sns_colleges)} SNS college(s):")
            for college in sns_colleges:
                print(f"      - {college.get('name')} in {college.get('city')}")
        else:
            print("   ❌ NO SNS COLLEGES FOUND!")
    else:
        print(f"   ❌ Search error: {sns_result}")

def check_database_connection():
    """Check if backend can connect to database"""
    print("\n🗄️ Checking Database Connection")
    print("=" * 50)
    
    health_result = make_request(f"{BASE_URL}/health")
    if health_result['status'] == 200:
        health_data = health_result['data']
        print(f"✅ Backend health: {health_data.get('status', 'unknown')}")
        print(f"✅ Database status: {health_data.get('db', 'unknown')}")
    else:
        print(f"❌ Backend health check failed: {health_result}")

def provide_solutions():
    """Provide solutions based on findings"""
    print("\n🔧 TROUBLESHOOTING STEPS")
    print("=" * 50)
    
    print("\n1. If NO DATA found in backend:")
    print("   → Your database tables are empty")
    print("   → You need to add data to PostgreSQL database first")
    print("   → Use pgAdmin, DBeaver, or SQL commands")
    
    print("\n2. If DATA exists in backend but not in frontend:")
    print("   → Clear browser cache (Ctrl+Shift+Delete)")
    print("   → Hard refresh frontend (Ctrl+F5)")
    print("   → Check browser console for errors")
    
    print("\n3. If DATABASE connection failed:")
    print("   → Check if PostgreSQL is running")
    print("   → Verify database credentials")
    print("   → Check backend logs for errors")
    
    print("\n📋 Quick Actions:")
    print("   • Frontend URL: http://localhost:3001")
    print("   • Backend API: http://localhost:8000/docs")
    print("   • Clear cache: http://localhost:3001/clear-cache-test.html")

def main():
    """Run diagnostic"""
    print("🚨 DEBUGGING: Why Updated Data Not Showing")
    print("=" * 60)
    
    check_database_connection()
    check_backend_data()
    provide_solutions()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("1. Check the results above")
    print("2. If no data in backend → Add data to database")
    print("3. If data exists → Clear browser cache")
    print("4. If still issues → Check browser console errors")

if __name__ == "__main__":
    main()
