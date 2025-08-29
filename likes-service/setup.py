#!/usr/bin/env python
"""
Setup script for the likes microservice.
This script will initialize the database and create sample data.
"""

import os
import sys
import django

def setup_service():
    """Setup the likes microservice"""
    print("🚀 Setting up Likes Microservice...")
    print("=" * 50)
    
    try:
        # Setup Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likes_service.settings')
        django.setup()
        
        print("✅ Django environment setup complete")
        
        # Import models after Django setup
        from likes.models import SamplePost, SampleUser, PostLike
        
        print("✅ Models imported successfully")
        
        # Check if data already exists
        user_count = SampleUser.objects.count()
        post_count = SamplePost.objects.count()
        like_count = PostLike.objects.count()
        
        print(f"\n📊 Current database state:")
        print(f"   Users: {user_count}")
        print(f"   Posts: {post_count}")
        print(f"   Likes: {like_count}")
        
        if user_count == 0 and post_count == 0:
            print("\n🔄 No sample data found. Run the test workflow to create data:")
            print("   python test_likes_workflow.py")
        else:
            print("\n✅ Sample data already exists!")
            print("   Run 'python test_likes_workflow.py' to test the complete workflow")
            print("   Run 'python test_api.py' to test the API endpoints")
        
        print("\n🎯 Next steps:")
        print("   1. Start the service: python manage.py runserver 0.0.0.0:8001")
        print("   2. Test the API: python test_api.py")
        print("   3. Run complete workflow: python test_likes_workflow.py")
        print("   4. Access admin panel: http://localhost:8001/admin/")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you're in the likes-service directory")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Run migrations: python manage.py makemigrations && python manage.py migrate")
        return False
    
    print("\n🎉 Setup completed successfully!")
    return True

if __name__ == "__main__":
    setup_service()
