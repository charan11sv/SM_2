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
SERVICE_NAME = 'likes-service'
SERVICE_PORT = 8003
SERVICE_VERSION = '1.0.0'

# Database configuration
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'likes_db'),
        'USER': os.environ.get('POSTGRES_USER', 'likes_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'likes_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Like configuration
LIKE_CONFIG = {
    'MAX_LIKES_PER_POST': 10000,
    'MAX_LIKES_PER_USER': 1000,
    'LIKE_CACHE_TTL': 300,  # 5 minutes
}
