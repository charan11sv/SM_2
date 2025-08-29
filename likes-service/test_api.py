#!/usr/bin/env python
"""
Simple API test script for the likes microservice.
Run this after starting the service to test the endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_endpoints():
    """Test all the main endpoints"""
    print("🧪 Testing Likes Microservice API Endpoints")
    print("=" * 60)
    
    # Test 1: Get all posts
    print("\n1. Testing GET /api/posts/")
    try:
        response = requests.get(f"{BASE_URL}/posts/")
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Success! Found {len(posts['results'])} posts")
            for post in posts['results'][:3]:  # Show first 3
                print(f"   - Post #{post['post_number']}: {post['description'][:50]}...")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get all users
    print("\n2. Testing GET /api/users/")
    try:
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Success! Found {len(users['results'])} users")
            for user in users['results'][:3]:  # Show first 3
                print(f"   - {user['username']} ({user['user_id']})")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get all likes
    print("\n3. Testing GET /api/likes/")
    try:
        response = requests.get(f"{BASE_URL}/likes/")
        if response.status_code == 200:
            likes = response.json()
            print(f"✅ Success! Found {len(likes['results'])} likes")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Get analytics
    print("\n4. Testing GET /api/likes/analytics/")
    try:
        response = requests.get(f"{BASE_URL}/likes/analytics/")
        if response.status_code == 200:
            analytics = response.json()
            print(f"✅ Success! Analytics data:")
            print(f"   - Total likes: {analytics['total_likes']}")
            print(f"   - Total posts: {analytics['total_posts']}")
            print(f"   - Total users: {analytics['total_users']}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Test post likes endpoint (if posts exist)
    print("\n5. Testing GET /api/likes/post_likes/")
    try:
        # First get a post ID
        posts_response = requests.get(f"{BASE_URL}/posts/")
        if posts_response.status_code == 200:
            posts = posts_response.json()
            if posts['results']:
                post_id = posts['results'][0]['id']
                response = requests.get(f"{BASE_URL}/likes/post_likes/?post_id={post_id}")
                if response.status_code == 200:
                    post_likes = response.json()
                    print(f"✅ Success! Post has {post_likes['total_likes']} likes")
                else:
                    print(f"❌ Failed with status {response.status_code}")
            else:
                print("ℹ️  No posts found to test with")
        else:
            print(f"❌ Could not get posts for testing")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API testing completed!")
    print("\nTo run the complete workflow test:")
    print("python test_likes_workflow.py")

if __name__ == "__main__":
    test_endpoints()
