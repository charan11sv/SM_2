#!/usr/bin/env python
"""
Quick script to check post ownership details
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likes_service.settings')
django.setup()

from likes.models import SamplePost, SampleUser

print("=== POSTS AND THEIR OWNERS ===")
print("=" * 50)

posts = SamplePost.objects.all().order_by('post_number')
for post in posts:
    print(f"Post #{post.post_number}: \"{post.description[:50]}...\"")
    print(f"   Owner: {post.user_id}")
    print(f"   Created: {post.created_at}")
    print()

print("=== USERS ===")
print("=" * 50)

users = SampleUser.objects.all().order_by('username')
for user in users:
    print(f"User: {user.username} (ID: {user.user_id})")
    print(f"   Email: {user.email}")
    print(f"   Created: {user.created_at}")
    print()
