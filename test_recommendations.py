#!/usr/bin/env python3
"""
Test script to debug recommendation system issues
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'career-tracking-backend'))

from app.services.recommendation_engine import recommendation_engine

async def test_recommendations():
    """Test the recommendation engine"""
    print("🔍 Testing Recommendation Engine...")
    
    # Test data loading
    print("\n1. Testing data loading...")
    success = recommendation_engine.load_data()
    print(f"   Data loaded: {success}")
    
    if not success:
        print("❌ Failed to load data. Check if data files exist.")
        return
    
    # Test basic recommendation
    print("\n2. Testing basic recommendations...")
    try:
        test_interests = ["programming", "technology", "web development"]
        recommendations = recommendation_engine.get_recommendations(
            user_interests=test_interests,
            user_id=1,
            top_k=5
        )
        
        print(f"   Generated {len(recommendations)} recommendations")
        
        if recommendations:
            print("\n   Sample recommendation:")
            rec = recommendations[0]
            print(f"   - Course: {rec['course_name']}")
            print(f"   - Match: {rec['match_percentage']}%")
            print(f"   - Description: {rec['description'][:100]}...")
        else:
            print("   ❌ No recommendations generated")
            
    except Exception as e:
        print(f"   ❌ Error generating recommendations: {e}")
        import traceback
        traceback.print_exc()
    
    # Test course by ID
    print("\n3. Testing course by ID...")
    try:
        course = recommendation_engine.get_course_by_id(1)
        if course:
            print(f"   Found course: {course['course_name']}")
        else:
            print("   ❌ Course not found")
    except Exception as e:
        print(f"   ❌ Error getting course: {e}")

if __name__ == "__main__":
    asyncio.run(test_recommendations())
