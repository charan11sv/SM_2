#!/usr/bin/env python
"""
Comprehensive Comments Service Testing Script
This script demonstrates the complete workflow:
1. Create sample posts and users
2. Create comments with nested replies
3. Add interactions (likes) by strangers
4. Display all comments and interactions
5. Add a reply
6. Add a like
7. Delete a like
8. Delete a comment
9. Display results after each change
"""

import os
import sys
import django
import time
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comments_service.settings')
django.setup()

from comments.models import SampleUser, SamplePost, Comment, CommentLike
from comments.serializers import CommentDetailSerializer, PostCommentsSerializer

def wait_for_database():
    """Wait for database to be ready"""
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            SampleUser.objects.count()
            print("✅ Database is ready!")
            return True
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"⏳ Waiting for database... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(2)
            else:
                print(f"❌ Database connection failed: {e}")
                return False
    return False

def create_sample_data():
    """Create sample users and posts"""
    print("\n" + "="*60)
    print("🚀 CREATING SAMPLE DATA")
    print("="*60)
    
    # Create sample users
    users_data = [
        {'user_id': 'user001', 'username': 'john_doe', 'email': 'john@example.com'},
        {'user_id': 'user002', 'username': 'jane_smith', 'email': 'jane@example.com'},
        {'user_id': 'user003', 'username': 'bob_wilson', 'email': 'bob@example.com'},
        {'user_id': 'user004', 'username': 'alice_brown', 'email': 'alice@example.com'},
        {'user_id': 'user005', 'username': 'charlie_davis', 'email': 'charlie@example.com'},
    ]
    
    users = {}
    for user_data in users_data:
        user, created = SampleUser.objects.get_or_create(
            user_id=user_data['user_id'],
            defaults=user_data
        )
        users[user_data['user_id']] = user
        if created:
            print(f"✅ Created user: {user.username} ({user.user_id})")
        else:
            print(f"ℹ️  User exists: {user.username} ({user.user_id})")
    
    # Create sample posts
    posts_data = [
        {'user_id': 'user001', 'description': 'Hello world! This is my first post about technology and innovation.'},
        {'user_id': 'user002', 'description': 'Excited to share my thoughts here! What do you think about AI?'},
        {'user_id': 'user003', 'description': 'Technology is amazing, isn\'t it? The future looks bright!'},
        {'user_id': 'user001', 'description': 'Another post from me about life, coding, and everything in between.'},
        {'user_id': 'user004', 'description': 'Food and travel are my passions! Anyone want to join me on an adventure?'},
    ]
    
    posts = {}
    for i, post_data in enumerate(posts_data, 1):
        post, created = SamplePost.objects.get_or_create(
            post_number=i,
            defaults={
                'user_id': post_data['user_id'],
                'description': post_data['description']
            }
        )
        posts[i] = post
        if created:
            print(f"✅ Created post #{i}: {post.description[:50]}...")
        else:
            print(f"ℹ️  Post exists: #{i}: {post.description[:50]}...")
    
    return users, posts

def create_initial_comments(users, posts):
    """Create initial comments with nested replies"""
    print("\n" + "="*60)
    print("💬 CREATING INITIAL COMMENTS WITH NESTED REPLIES")
    print("="*60)
    
    # Create first comment on post 1
    comment1 = Comment.objects.create(
        post=posts[1],
        user=users['user002'],
        content="Great post! Technology is indeed fascinating."
    )
    print(f"✅ Created comment 1: {comment1.content}")
    
    # Create reply to comment 1
    reply1 = Comment.objects.create(
        post=posts[1],
        user=users['user003'],
        parent_comment=comment1,
        content="I completely agree! The pace of innovation is incredible."
    )
    print(f"✅ Created reply 1: {reply1.content}")
    
    # Create second comment on post 2
    comment2 = Comment.objects.create(
        post=posts[2],
        user=users['user001'],
        content="AI is definitely the future! What specific areas interest you?"
    )
    print(f"✅ Created comment 2: {comment2.content}")
    
    # Create reply to comment 2
    reply2 = Comment.objects.create(
        post=posts[2],
        user=users['user004'],
        parent_comment=comment2,
        content="Machine learning and natural language processing are my favorites!"
    )
    print(f"✅ Created reply 2: {reply2.content}")
    
    return comment1, reply1, comment2, reply2

def add_interactions(users, comments):
    """Add likes to comments by different users"""
    print("\n" + "="*60)
    print("👍 ADDING INTERACTIONS (LIKES) BY STRANGERS")
    print("="*60)
    
    comment1, reply1, comment2, reply2 = comments
    
    # Add likes to comment 1
    CommentLike.objects.create(comment=comment1, user=users['user004'])
    CommentLike.objects.create(comment=comment1, user=users['user005'])
    print(f"✅ Added 2 likes to comment 1 by {users['user004'].username} and {users['user005'].username}")
    
    # Add likes to reply 1
    CommentLike.objects.create(comment=reply1, user=users['user001'])
    print(f"✅ Added 1 like to reply 1 by {users['user001'].username}")
    
    # Add likes to comment 2
    CommentLike.objects.create(comment=comment2, user=users['user003'])
    CommentLike.objects.create(comment=comment2, user=users['user005'])
    print(f"✅ Added 2 likes to comment 2 by {users['user003'].username} and {users['user005'].username}")
    
    # Add likes to reply 2
    CommentLike.objects.create(comment=reply2, user=users['user001'])
    CommentLike.objects.create(comment=reply2, user=users['user002'])
    print(f"✅ Added 2 likes to reply 2 by {users['user001'].username} and {users['user002'].username}")

def display_all_comments_and_interactions():
    """Display all comments and their interactions"""
    print("\n" + "="*60)
    print("📋 DISPLAYING ALL COMMENTS AND INTERACTIONS")
    print("="*60)
    
    posts = SamplePost.objects.all().order_by('post_number')
    
    for post in posts:
        print(f"\n📝 POST #{post.post_number}: {post.description[:60]}...")
        print(f"   Owner: {post.user_id}")
        print("-" * 50)
        
        # Get top-level comments for this post
        top_comments = post.comments.filter(parent_comment__isnull=True, is_deleted=False).order_by('created_at')
        
        for comment in top_comments:
            display_comment_with_replies(comment, level=0)

def display_comment_with_replies(comment, level=0):
    """Recursively display a comment and its replies"""
    indent = "  " * level
    prefix = "↳ " if level > 0 else "💬 "
    
    print(f"{indent}{prefix}{comment.user.username}: {comment.content}")
    print(f"{indent}   ID: {comment.id}")
    print(f"{indent}   Created: {comment.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{indent}   Likes: {comment.like_count} | Replies: {comment.reply_count}")
    
    # Display likes
    if comment.likes.exists():
        like_users = [like.user.username for like in comment.likes.all()]
        print(f"{indent}   ❤️  Liked by: {', '.join(like_users)}")
    
    # Display replies
    replies = comment.replies.filter(is_deleted=False).order_by('created_at')
    for reply in replies:
        display_comment_with_replies(reply, level + 1)
    
    print()

def add_new_reply(users, comments):
    """Add a new reply to an existing comment"""
    print("\n" + "="*60)
    print("💬 ADDING A NEW REPLY")
    print("="*60)
    
    comment1 = comments[0]  # First comment
    
    new_reply = Comment.objects.create(
        post=comment1.post,
        user=users['user005'],
        parent_comment=comment1,
        content="This is a new reply added during testing! Very interesting discussion."
    )
    print(f"✅ Added new reply: {new_reply.content}")
    print(f"   By: {new_reply.user.username}")
    print(f"   To comment: {comment1.content[:50]}...")
    
    return new_reply

def add_new_like(users, comments):
    """Add a new like to a comment"""
    print("\n" + "="*60)
    print("👍 ADDING A NEW LIKE")
    print("="*60)
    
    comment2 = comments[2]  # Second comment
    user = users['user004']
    
    # Check if like already exists
    if CommentLike.objects.filter(comment=comment2, user=user).exists():
        print(f"ℹ️  User {user.username} already liked this comment")
        return None
    
    new_like = CommentLike.objects.create(comment=comment2, user=user)
    print(f"✅ Added new like to comment: {comment2.content[:50]}...")
    print(f"   By: {user.username}")
    print(f"   Comment now has {comment2.like_count} likes")
    
    return new_like

def delete_like(users, comments):
    """Delete a like from a comment"""
    print("\n" + "="*60)
    print("❌ DELETING A LIKE")
    print("="*60)
    
    comment1 = comments[0]  # First comment
    user = users['user004']
    
    try:
        like = CommentLike.objects.get(comment=comment1, user=user)
        like.delete()
        print(f"✅ Deleted like by {user.username} from comment: {comment1.content[:50]}...")
        print(f"   Comment now has {comment1.like_count} likes")
        return True
    except CommentLike.DoesNotExist:
        print(f"ℹ️  No like found by {user.username} on this comment")
        return False

def delete_comment(comments):
    """Soft delete a comment"""
    print("\n" + "="*60)
    print("🗑️  DELETING A COMMENT (SOFT DELETE)")
    print("="*60)
    
    reply1 = comments[1]  # First reply
    
    reply1.is_deleted = True
    reply1.save()
    print(f"✅ Soft deleted reply: {reply1.content[:50]}...")
    print(f"   By: {reply1.user.username}")
    print(f"   Comment is now marked as deleted")

def main():
    """Main testing workflow"""
    print("🚀 COMMENTS MICROSERVICE - COMPREHENSIVE TESTING WORKFLOW")
    print("="*80)
    
    # Wait for database
    if not wait_for_database():
        print("❌ Cannot proceed without database connection")
        return
    
    # Step 1: Create sample data
    users, posts = create_sample_data()
    
    # Step 2: Create initial comments with nested replies
    comments = create_initial_comments(users, posts)
    
    # Step 3: Add interactions (likes) by strangers
    add_interactions(users, comments)
    
    # Step 4: Display all comments and interactions
    display_all_comments_and_interactions()
    
    # Step 5: Add a new reply
    new_reply = add_new_reply(users, comments)
    
    # Display results after adding reply
    print("\n" + "="*60)
    print("📋 RESULTS AFTER ADDING REPLY")
    print("="*60)
    display_all_comments_and_interactions()
    
    # Step 6: Add a new like
    new_like = add_new_like(users, comments)
    
    # Display results after adding like
    print("\n" + "="*60)
    print("📋 RESULTS AFTER ADDING LIKE")
    print("="*60)
    display_all_comments_and_interactions()
    
    # Step 7: Delete a like
    delete_like(users, comments)
    
    # Display results after deleting like
    print("\n" + "="*60)
    print("📋 RESULTS AFTER DELETING LIKE")
    print("="*60)
    display_all_comments_and_interactions()
    
    # Step 8: Delete a comment (soft delete)
    delete_comment(comments)
    
    # Display final results
    print("\n" + "="*60)
    print("📋 FINAL RESULTS AFTER ALL OPERATIONS")
    print("="*60)
    display_all_comments_and_interactions()
    
    print("\n" + "="*80)
    print("🎉 TESTING WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*80)

if __name__ == '__main__':
    main()
