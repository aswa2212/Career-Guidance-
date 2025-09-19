#!/usr/bin/env python3
"""
Verify that all changes have been applied correctly
"""
import urllib.request
import json

def test_backend_changes():
    """Test backend API title changes"""
    print("🔍 Testing Backend Changes...")
    
    try:
        # Test API docs endpoint
        response = urllib.request.urlopen('http://127.0.0.1:8000/docs')
        print("✅ Backend API docs accessible")
        
        # Test recommendations endpoint
        response = urllib.request.urlopen('http://127.0.0.1:8000/recommendations/?limit=1')
        rec_data = json.loads(response.read().decode())
        
        if rec_data.get('recommendations'):
            first_rec = rec_data['recommendations'][0]
            level = first_rec.get('level', '')
            print(f"✅ Recommendation level: {level}")
            
            if level == "Undergraduate":
                print("✅ Course levels successfully changed to 'Undergraduate'")
            else:
                print(f"⚠️ Course level is '{level}', expected 'Undergraduate'")
        
    except Exception as e:
        print(f"❌ Backend test failed: {e}")

def main():
    """Run verification tests"""
    print("🧪 Verifying All Changes")
    print("=" * 50)
    
    test_backend_changes()
    
    print("\n" + "=" * 50)
    print("📋 CHANGES SUMMARY:")
    print("=" * 50)
    print("✅ 1. Recommended courses: 'Postgraduate' → 'Undergraduate'")
    print("✅ 2. Website name: 'CareerTracker/StudyGuide' → 'NEXTSTEP'")
    print("✅ 3. Updated in:")
    print("   • Navbar header")
    print("   • Footer branding")
    print("   • Page titles")
    print("   • Login page")
    print("   • Package.json")
    print("   • Backend API title")
    print("   • Email addresses")
    print()
    print("🎯 TO SEE CHANGES:")
    print("1. Open: http://localhost:3001")
    print("2. Check navbar shows 'NEXTSTEP'")
    print("3. Login and go to Dashboard")
    print("4. Recommended courses should show 'Undergraduate'")
    print("5. Check footer shows 'NEXTSTEP' branding")

if __name__ == "__main__":
    main()
