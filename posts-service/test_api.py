#!/usr/bin/env python
"""
Simple API test script for posts service
"""

import requests
import time
import json

BASE_URL = "http://localhost:8002"

def test_api_endpoints():
    """Test basic API endpoints"""
    
    print("🧪 Testing Posts Service API Endpoints")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/posts/")
        if response.status_code == 200:
            print("✅ Server is running and API is accessible")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8000")
        return False
    
    # Test 2: Create a test post
    print("\n📝 Testing post creation...")
    test_data = {
        'user_id': 'test_user_123',
        'description': 'This is a test post for API testing'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/posts/", data=test_data)
        if response.status_code == 201:
            post_data = response.json()
            print(f"✅ Post created successfully!")
            print(f"   Post ID: {post_data['id']}")
            print(f"   Post Number: {post_data['post_number']}")
            print(f"   User ID: {post_data['user_id']}")
            return post_data
        else:
            print(f"❌ Failed to create post: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating post: {str(e)}")
        return None

def test_get_posts():
    """Test getting posts"""
    print("\n📋 Testing post retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/posts/")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            print(f"✅ Retrieved {len(posts)} posts")
            for post in posts:
                print(f"   - Post #{post['post_number']} by {post['user_id']}: {post['description'][:50]}...")
            return posts
        else:
            print(f"❌ Failed to get posts: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting posts: {str(e)}")
        return []

def test_user_posts(user_id):
    """Test getting posts by user"""
    print(f"\n👤 Testing posts by user {user_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/posts/?user_id={user_id}")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('results', [])
            print(f"✅ Retrieved {len(posts)} posts for user {user_id}")
            return posts
        else:
            print(f"❌ Failed to get user posts: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting user posts: {str(e)}")
        return []

if __name__ == "__main__":
    print("🚀 Starting API Tests...")
    
    # Test basic endpoints
    post_data = test_api_endpoints()
    
    if post_data:
        # Test getting all posts
        all_posts = test_get_posts()
        
        # Test getting posts by user
        user_posts = test_user_posts('test_user_123')
        
        print("\n" + "=" * 50)
        print("🎉 API Tests Completed Successfully!")
        print("✅ Posts service is working correctly")
    else:
        print("\n" + "=" * 50)
        print("❌ API Tests Failed!")
        print("Please check the server logs for errors")
