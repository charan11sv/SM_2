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
SERVICE_NAME = 'comments-service'
SERVICE_PORT = 8004
SERVICE_VERSION = '1.0.0'

# Database configuration
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'comments_db'),
        'USER': os.environ.get('POSTGRES_USER', 'comments_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'comments_pass'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Comment configuration
COMMENT_CONFIG = {
    'MAX_CONTENT_LENGTH': 1000,
    'MAX_REPLY_DEPTH': 5,
    'MAX_COMMENTS_PER_POST': 1000,
}
