import os

# Service Discovery Configuration
SERVICES = {
    'login': os.environ.get('LOGIN_SERVICE_URL', 'http://localhost:8000'),
    'profile': os.environ.get('PROFILE_SERVICE_URL', 'http://localhost:8001'),
    'posts': os.environ.get('POSTS_SERVICE_URL', 'http://localhost:8002'),
    'likes': os.environ.get('LIKES_SERVICE_URL', 'http://localhost:8003'),
    'comments': os.environ.get('COMMENTS_SERVICE_URL', 'http://localhost:8004'),
}

# Current service configuration
SERVICE_NAME = 'posts-service'
SERVICE_PORT = 8002
SERVICE_VERSION = '1.0.0'

# Database configuration
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Media configuration
MEDIA_CONFIG = {
    'MAX_FILE_SIZE': 50 * 1024 * 1024,  # 50MB
    'ALLOWED_IMAGE_TYPES': ['image/jpeg', 'image/png', 'image/gif'],
    'ALLOWED_VIDEO_TYPES': ['video/mp4', 'video/avi', 'video/mov'],
}
