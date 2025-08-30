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
SERVICE_NAME = 'profile-service'
SERVICE_PORT = 8001
SERVICE_VERSION = '1.0.0'

# Database configuration
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'profile_db'),
        'USER': os.environ.get('POSTGRES_USER', 'profile_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'profile_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Profile configuration
PROFILE_CONFIG = {
    'MAX_BIO_LENGTH': 200,
    'MAX_USERNAME_LENGTH': 50,
    'MIN_USERNAME_LENGTH': 3,
    'MAX_INTERESTS': 5,
    'MAX_PROFILE_PICTURE_SIZE': 5 * 1024 * 1024,  # 5MB
}
