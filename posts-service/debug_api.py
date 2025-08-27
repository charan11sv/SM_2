#!/usr/bin/env python
"""
Debug script to see what the API response looks like
"""

import requests
import json

BASE_URL = "http://localhost:8002"

def debug_post_creation():
    """Debug post creation to see the actual response"""
    
    print("🧪 Debugging Post Creation")
    print("=" * 40)
    
    # Test data
    test_data = {
        'user_id': 'debug_user_123',
        'description': 'Debug test post'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/posts/", data=test_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            try:
                post_data = response.json()
                print(f"JSON Response: {json.dumps(post_data, indent=2)}")
                print(f"Response Keys: {list(post_data.keys())}")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
        else:
            print(f"Failed to create post: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

def debug_get_posts():
    """Debug getting posts to see the actual response"""
    
    print("\n🧪 Debugging Get Posts")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/posts/")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response: {json.dumps(data, indent=2)}")
                if 'results' in data and data['results']:
                    first_post = data['results'][0]
                    print(f"First Post Keys: {list(first_post.keys())}")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
        else:
            print(f"Failed to get posts: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    debug_post_creation()
    debug_get_posts()
