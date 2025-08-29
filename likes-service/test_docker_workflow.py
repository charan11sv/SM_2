#!/usr/bin/env python
"""
Docker-compatible test script for the likes microservice workflow.
This script will work both locally and inside the Docker container.
"""

import os
import sys
import django
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likes_service.settings')
django.setup()

from likes.models import SamplePost, SampleUser, PostLike


def wait_for_database():
    """Wait for database to be ready (useful in Docker)"""
    print("🔄 Waiting for database to be ready...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Try to count users (simple query)
            SampleUser.objects.count()
            print("✅ Database is ready!")
            return True
        except Exception as e:
            attempt += 1
            print(f"⏳ Database not ready yet (attempt {attempt}/{max_attempts}): {e}")
            time.sleep(2)
    
    print("❌ Database connection failed after maximum attempts")
    return False


def create_sample_data():
    """Create sample users and posts for testing"""
    print("🔄 Creating sample data...")
    
    # Create sample users
    users_data = [
        {'user_id': 'user001', 'username': 'john_doe', 'email': 'john@example.com'},
        {'user_id': 'user002', 'username': 'jane_smith', 'email': 'jane@example.com'},
        {'user_id': 'user003', 'username': 'bob_wilson', 'email': 'bob@example.com'},
        {'user_id': 'user004', 'username': 'alice_brown', 'email': 'alice@example.com'},
        {'user_id': 'user005', 'username': 'charlie_davis', 'email': 'charlie@example.com'},
    ]
    
    users = []
    for user_data in users_data:
        user, created = SampleUser.objects.get_or_create(
            user_id=user_data['user_id'],
            defaults=user_data
        )
        users.append(user)
        if created:
            print(f"✅ Created user: {user.username}")
        else:
            print(f"ℹ️  User already exists: {user.username}")
    
    # Create sample posts
    posts_data = [
        {'user_id': 'user001', 'description': 'Hello world! This is my first post.'},
        {'user_id': 'user002', 'description': 'Excited to share my thoughts here!'},
        {'user_id': 'user003', 'description': 'Technology is amazing, isn\'t it?'},
        {'user_id': 'user001', 'description': 'Another post from me about life.'},
        {'user_id': 'user004', 'description': 'Food and travel are my passions!'},
    ]
    
    posts = []
    for post_data in posts_data:
        post, created = SamplePost.objects.get_or_create(
            user_id=post_data['user_id'],
            description=post_data['description'],
            defaults={'user_id': post_data['user_id'], 'description': post_data['description']}
        )
        posts.append(post)
        if created:
            print(f"✅ Created post: #{post.post_number} - {post.description[:50]}...")
        else:
            print(f"ℹ️  Post already exists: #{post.post_number}")
    
    return users, posts


def register_likes(users, posts):
    """Register likes from multiple users on different posts"""
    print("\n🔄 Registering likes...")
    
    # Like distribution: each user likes multiple posts
    like_combinations = [
        # User 1 likes posts 2, 3, 5
        (users[0], posts[1]),  # john likes jane's post
        (users[0], posts[2]),  # john likes bob's post
        (users[0], posts[4]),  # john likes alice's post
        
        # User 2 likes posts 1, 3, 4
        (users[1], posts[0]),  # jane likes john's first post
        (users[1], posts[2]),  # jane likes bob's post
        (users[1], posts[3]),  # jane likes john's second post
        
        # User 3 likes posts 1, 2, 5
        (users[2], posts[0]),  # bob likes john's first post
        (users[2], posts[1]),  # bob likes jane's post
        (users[2], posts[4]),  # bob likes alice's post
        
        # User 4 likes posts 1, 2, 3
        (users[3], posts[0]),  # alice likes john's first post
        (users[3], posts[1]),  # alice likes jane's post
        (users[3], posts[2]),  # alice likes bob's post
        
        # User 5 likes posts 1, 3, 4
        (users[4], posts[0]),  # charlie likes john's first post
        (users[4], posts[2]),  # charlie likes bob's post
        (users[4], posts[3]),  # charlie likes john's second post
    ]
    
    likes_created = []
    for user, post in like_combinations:
        like, created = PostLike.objects.get_or_create(
            post=post,
            user=user,
            defaults={'post': post, 'user': user}
        )
        if created:
            print(f"✅ {user.username} liked Post #{post.post_number}")
            likes_created.append(like)
        else:
            print(f"ℹ️  {user.username} already liked Post #{post.post_number}")
    
    return likes_created


def display_analytics():
    """Display analytics about likes"""
    print("\n📈 Likes Analytics:")
    print("=" * 60)
    
    total_likes = PostLike.objects.count()
    total_posts = SamplePost.objects.count()
    total_users = SampleUser.objects.count()
    
    print(f"Total likes: {total_likes}")
    print(f"Total posts: {total_posts}")
    print(f"Total users: {total_users}")
    
    # Most liked posts
    print("\n🏆 Most liked posts:")
    from django.db.models import Count
    most_liked = PostLike.objects.values('post__post_number', 'post__description')\
        .annotate(like_count=Count('id'))\
        .order_by('-like_count')[:3]
    
    for post in most_liked:
        print(f"   Post #{post['post__post_number']}: {post['like_count']} likes")
    
    # Most active likers
    print("\n👑 Most active likers:")
    most_active = PostLike.objects.values('user__username')\
        .annotate(like_count=Count('id'))\
        .order_by('-like_count')[:3]
    
    for user in most_active:
        print(f"   {user['user__username']}: {user['like_count']} likes given")


def main():
    """Main test workflow"""
    print("🚀 Starting Likes Microservice Docker Test Workflow")
    print("=" * 60)
    
    try:
        # Step 1: Wait for database
        if not wait_for_database():
            return
        
        # Step 2: Create sample data
        users, posts = create_sample_data()
        
        # Step 3: Register likes
        likes = register_likes(users, posts)
        
        # Step 4: Display analytics
        display_analytics()
        
        print("\n🎉 Docker test workflow completed successfully!")
        print("\n📍 Service is running at: http://localhost:8001")
        print("   API endpoints available at: http://localhost:8001/api/")
        
    except Exception as e:
        print(f"\n❌ Error during test workflow: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
