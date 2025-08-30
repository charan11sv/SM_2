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
SERVICE_NAME = 'login-service'
SERVICE_PORT = 8000
SERVICE_VERSION = '1.0.0'

# Database configuration
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'mydb'),
        'USER': os.environ.get('POSTGRES_USER', 'myuser'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'mypassword'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Authentication configuration
AUTH_CONFIG = {
    'JWT_ACCESS_TOKEN_LIFETIME': 60,  # 1 hour
    'JWT_REFRESH_TOKEN_LIFETIME': 1440,  # 24 hours
    'VERIFICATION_CODE_EXPIRY': 10,  # 10 minutes
    'MAX_LOGIN_ATTEMPTS': 5,
}
