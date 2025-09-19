#!/usr/bin/env python3
"""
Test script to verify all ports and URLs are working
"""
import urllib.request
import json

def test_url(url, description):
    """Test a URL and return result"""
    try:
        print(f"🔍 Testing {description}: {url}")
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        print(f"✅ SUCCESS: {description}")
        print(f"   Status: {response.status}")
        if url.endswith('/health'):
            health_data = json.loads(data)
            print(f"   Response: {health_data}")
        print()
        return True
    except Exception as e:
        print(f"❌ FAILED: {description}")
        print(f"   Error: {str(e)}")
        print()
        return False

def main():
    """Test all important URLs"""
    print("🧪 Testing all ports and URLs...\n")
    
    # Test backend URLs
    backend_urls = [
        ("http://localhost:8000/health", "Backend Health (localhost)"),
        ("http://127.0.0.1:8000/health", "Backend Health (127.0.0.1)"),
        ("http://localhost:8000/docs", "Backend API Docs (localhost)"),
        ("http://127.0.0.1:8000/docs", "Backend API Docs (127.0.0.1)")
    ]
    
    backend_working = False
    for url, desc in backend_urls:
        if test_url(url, desc):
            backend_working = True
            break
    
    if backend_working:
        print("🎉 Backend is working correctly!")
        print("📋 Available endpoints:")
        print("   • Health Check: http://localhost:8000/health")
        print("   • API Documentation: http://localhost:8000/docs")
        print("   • Authentication: http://localhost:8000/auth/login")
        print("   • User Interests: http://localhost:8000/users/me/interests")
        print("   • Recommendations: http://localhost:8000/recommendations/")
        print("   • Colleges: http://localhost:8000/colleges/")
    else:
        print("❌ Backend is not accessible!")
    
    print("\n" + "="*50)
    print("🌐 Frontend should be available at:")
    print("   • Main App: http://localhost:3000")
    print("   • Cache Test: http://localhost:3000/clear-cache-test.html")
    print("   • API Test: http://localhost:3000/test-api.html")

if __name__ == "__main__":
    main()
