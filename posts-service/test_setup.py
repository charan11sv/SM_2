#!/usr/bin/env python
"""
Simple test script to verify the posts service setup
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posts_service.settings')

# Setup Django
django.setup()

from posts.models import Post, PostMedia

def test_models():
    """Test if models can be imported and created"""
    try:
        print("✓ Django setup successful")
        print("✓ Models imported successfully")
        
        # Test model creation (without saving)
        post = Post(
            user_id="test_user",
            description="Test post description"
        )
        print("✓ Post model can be instantiated")
        
        media = PostMedia(
            post=post,
            media_type='image',
            file=None  # We won't save this
        )
        print("✓ PostMedia model can be instantiated")
        
        print("\n✅ All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_database():
    """Test database connection"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Posts Service Setup")
    print("=" * 40)
    
    success = True
    
    # Test Django setup
    if not test_models():
        success = False
    
    # Test database
    if not test_database():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Setup verification completed successfully!")
        print("Ready to run migrations and start the service.")
    else:
        print("❌ Setup verification failed. Please check the errors above.")
        sys.exit(1)
