#!/usr/bin/env python
"""
Complete workflow test for Posts Service
Tests: creation, retrieval, user-specific retrieval, deletion, and media download
"""

import requests
import os
import time

# Configuration
BASE_URL = "http://localhost:8002"
TEST_IMAGES_DIR = r"C:\Users\Dell\Documents\projects\social media\test_images"

# Test media files
TEST_MEDIA_FILES = {
    'container_image': r"C:\Users\Dell\Pictures\container.PNG",
    'startup_image': r"C:\Users\Dell\Pictures\startup.PNG", 
    'sample_video': r"C:\Users\Dell\Downloads\sample-mp4-file-small.mp4"
}

def check_api_status():
    """Check if the API is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/api/posts/")
        if response.status_code == 200:
            print("✓ API is running and accessible")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to API: {str(e)}")
        return False

def create_post_with_media(user_id, description, media_file_path):
    """Create a post with media file"""
    url = f"{BASE_URL}/api/posts/"
    
    # Check if media file exists
    if not os.path.exists(media_file_path):
        print(f"✗ Media file not found: {media_file_path}")
        return None
    
    # Prepare data
    data = {
        'user_id': user_id,
        'description': description
    }
    
    # Prepare files
    if media_file_path:
        filename = os.path.basename(media_file_path)
        
        try:
            with open(media_file_path, 'rb') as file_obj:
                files = {'media': (filename, file_obj, 'application/octet-stream')}
                response = requests.post(url, data=data, files=files)
            
            if response.status_code == 201:
                post_data = response.json()
                print(f"✓ Post created successfully: {post_data['id']}")
                return post_data
            else:
                print(f"✗ Failed to create post: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"✗ Error creating post: {str(e)}")
            return None
    else:
        print(f"✗ No media file provided for post")
        return None

def create_test_posts():
    """Create test posts with media files"""
    print("\n============================================================")
    print("📝 PHASE 1: Creating Test Posts with Media")
    print("============================================================")
    
    posts_created = []
    
    # Create posts for john_doe_123 (2 posts)
    print("\n👤 Creating posts for john_doe_123:")
    
    # Post 1: Container image
    post1 = create_post_with_media(
        'john_doe_123',
        'Check out this amazing container setup! 🐳',
        TEST_MEDIA_FILES['container_image']
    )
    if post1:
        posts_created.append(post1)
    
    # Post 2: Startup image  
    post2 = create_post_with_media(
        'john_doe_123',
        'Startup vibes! 🚀',
        TEST_MEDIA_FILES['startup_image']
    )
    if post2:
        posts_created.append(post2)
    
    # Create post for jane_smith_456 (1 post)
    print("\n👤 Creating post for jane_smith_456:")
    post3 = create_post_with_media(
        'jane_smith_456',
        'Sample video content 🎥',
        TEST_MEDIA_FILES['sample_video']
    )
    if post3:
        posts_created.append(post3)
    
    if len(posts_created) == 3:
        print(f"\n✅ Successfully created {len(posts_created)} posts")
        return True
    else:
        print(f"\n✗ Only created {len(posts_created)} posts out of 3 expected")
        return False

def get_all_posts():
    """Get all posts from all users"""
    print("\n============================================================")
    print("📋 PHASE 2: Getting All Posts")
    print("============================================================")
    
    url = f"{BASE_URL}/api/posts/"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()['results']
            print(f"✓ Retrieved {len(posts)} posts")
            
            # Display posts
            print(f"\n📊 Total posts in system: {len(posts)}")
            for post in posts:
                media_count = len(post.get('media_files', []))
                print(f"  - Post #{post['post_number']} by {post['user_id']}: {post['description'][:50]}...")
                print(f"    Media files: {media_count}")
            
            return posts
        else:
            print(f"✗ Failed to get posts: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Error getting posts: {str(e)}")
        return []

def get_user_posts(user_id):
    """Get posts by a specific user"""
    url = f"{BASE_URL}/api/posts/?user_id={user_id}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()['results']
            print(f"✓ Retrieved {len(posts)} posts for user {user_id}")
            return posts
        else:
            print(f"✗ Failed to get user posts: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Error getting user posts: {str(e)}")
        return []

def download_media_files(posts):
    """Download media files from posts to test directory"""
    print(f"\n📥 Downloading media files to: {TEST_IMAGES_DIR}")
    
    for post in posts:
        user_id = post['user_id']
        post_number = post['post_number']
        
        for media in post.get('media_files', []):
            media_id = media['id']
            media_type = media['media_type']
            
            # Download media file
            media_url = f"{BASE_URL}/api/media/{media_id}/"
            try:
                response = requests.get(media_url)
                if response.status_code == 200:
                    # Create filename
                    original_filename = os.path.basename(media['file'])
                    filename = f"{user_id}_post{post_number}_{original_filename}"
                    filepath = os.path.join(TEST_IMAGES_DIR, filename)
                    
                    # Save file
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"  ✓ Downloaded: {filename}")
                else:
                    print(f"  ✗ Failed to download media {media_id}: {response.status_code}")
            except Exception as e:
                print(f"  ✗ Error downloading media {media_id}: {str(e)}")

def delete_user_posts(user_id):
    """Delete all posts by a specific user"""
    url = f"{BASE_URL}/api/posts/delete_user_posts/?user_id={user_id}"
    
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Deleted {result['deleted_count']} posts for user {user_id}")
            return True
        else:
            print(f"✗ Failed to delete posts: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error deleting posts: {str(e)}")
        return False

def main():
    """Main test workflow"""
    print("🚀 Starting Posts Service Complete Workflow Test with Media")
    print("============================================================")
    
    # Check test directory
    if not os.path.exists(TEST_IMAGES_DIR):
        os.makedirs(TEST_IMAGES_DIR)
        print(f"✓ Created test directory: {TEST_IMAGES_DIR}")
    else:
        print(f"✓ Test directory ready: {TEST_IMAGES_DIR}")
    
    # Check API status
    if not check_api_status():
        print("❌ API not accessible. Stopping test.")
        return
    
    # Phase 1: Create posts with media
    if not create_test_posts():
        print("❌ Failed to create posts. Stopping test.")
        return
    
    # Phase 2: Get all posts and download media
    posts = get_all_posts()
    if posts:
        download_media_files(posts)
    
    # Phase 3: Get posts by specific users
    print("\n============================================================")
    print("👤 PHASE 3: Getting Posts by Specific Users")
    print("============================================================")
    
    print("\n👤 Posts by john_doe_123:")
    john_posts = get_user_posts('john_doe_123')
    
    print("\n👤 Posts by jane_smith_456:")
    jane_posts = get_user_posts('jane_smith_456')
    
    # Phase 4: Delete posts by one user
    print("\n============================================================")
    print("🗑️ PHASE 4: Deleting User Posts")
    print("============================================================")
    
    print("\n🗑️ Deleting posts by john_doe_123:")
    delete_user_posts('john_doe_123')
    
    # Phase 5: Verify deletion
    print("\n============================================================")
    print("✅ PHASE 5: Verification After Deletion")
    print("============================================================")
    
    # Get remaining posts
    remaining_posts = get_all_posts()
    
    # Check posts by specific users
    print("\n👤 Posts by john_doe_123 (should be empty):")
    john_posts_after = get_user_posts('john_doe_123')
    
    print("\n👤 Posts by jane_smith_456 (should still have posts):")
    jane_posts_after = get_user_posts('jane_smith_456')
    
    print("\n============================================================")
    print("🎉 Testing Complete!")
    print("============================================================")
    print(f"📁 Check downloaded media files in: {TEST_IMAGES_DIR}")
    print("\n✅ All phases completed successfully!")

if __name__ == "__main__":
    main()
