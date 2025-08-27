#!/usr/bin/env python
"""
Script to delete all existing posts from the database
"""

import requests

BASE_URL = "http://localhost:8002"

def delete_all_posts():
    """Delete all posts from all users"""
    
    print("🗑️ Deleting all existing posts...")
    
    # First, get all posts to see what users exist
    try:
        response = requests.get(f"{BASE_URL}/api/posts/")
        if response.status_code == 200:
            data = response.json()
            posts = data['results']
            print(f"Found {len(posts)} posts to delete")
            
            # Get unique user IDs
            user_ids = list(set(post['user_id'] for post in posts))
            print(f"Users with posts: {user_ids}")
            
            # Delete posts for each user
            for user_id in user_ids:
                try:
                    delete_url = f"{BASE_URL}/api/posts/delete_user_posts/?user_id={user_id}"
                    delete_response = requests.delete(delete_url)
                    
                    if delete_response.status_code == 200:
                        result = delete_response.json()
                        print(f"✓ Deleted {result['deleted_count']} posts for user {user_id}")
                    else:
                        print(f"✗ Failed to delete posts for user {user_id}: {delete_response.status_code}")
                        
                except Exception as e:
                    print(f"✗ Error deleting posts for user {user_id}: {str(e)}")
            
            # Verify deletion
            verify_response = requests.get(f"{BASE_URL}/api/posts/")
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                remaining_posts = verify_data['count']
                print(f"\n✅ Verification: {remaining_posts} posts remaining in database")
                
                if remaining_posts == 0:
                    print("🎉 All posts successfully deleted!")
                else:
                    print("⚠️ Some posts may still remain")
                    
        else:
            print(f"✗ Failed to get posts: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    delete_all_posts()
