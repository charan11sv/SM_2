# Profile Setup Microservice

A Django-based microservice for user profile setup and management, designed to work with the login microservice.

## Features

- **Profile Setup**: Complete profile creation for first-time users
- **Profile Picture Upload**: Image upload with validation (JPEG, PNG, GIF)
- **Bio Management**: User bio with 200 character limit
- **Username Selection**: Unique username validation and reservation
- **Interest Selection**: Choose up to 5 interests from predefined categories
- **Profile Completion Tracking**: Monitor setup progress
- **JWT Authentication**: Integration with login service

## Architecture

- **Django 5.2.5** with Django REST Framework
- **PostgreSQL** database
- **Docker** containerization
- **JWT** token authentication
- **File upload** handling for profile pictures

## API Endpoints

### Profiles
- `POST /api/profiles/setup/` - Initial profile setup
- `GET /api/profiles/my_profile/` - Get current user's profile
- `PUT /api/profiles/{id}/` - Update profile
- `POST /api/profiles/upload_picture/` - Upload profile picture
- `GET /api/profiles/status/` - Get profile completion status
- `POST /api/profiles/check_username/` - Check username availability

### Interests
- `GET /api/interests/` - List all interests
- `GET /api/interests/{id}/` - Get specific interest details
- `GET /api/interests/categories/` - Get interest categories
- `GET /api/interests/search/` - Search interests

### Profile Pictures
- `GET /api/profile-pictures/history/` - Get picture upload history

## Setup Instructions

### 1. Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### 2. Clone and Setup
```bash
cd profile-service
docker-compose up --build
```

### 3. Database Migrations
```bash
# In a new terminal
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 4. Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Populate Interests
```bash
docker-compose exec web python manage.py populate_interests
```

### 6. Access Services
- **Profile Service**: http://localhost:8001
- **Admin Panel**: http://localhost:8001/admin/
- **API Documentation**: http://localhost:8001/api/

## Environment Variables

```env
POSTGRES_DB=profile_db
POSTGRES_USER=profile_user
POSTGRES_PASSWORD=profile_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
LOGIN_SERVICE_URL=http://host.docker.internal:8000
```

## Database Models

### Profile
- `user_id`: Reference to login service user
- `username`: Unique username (3-50 characters)
- `bio`: User bio (max 200 characters)
- `profile_picture`: Profile image
- `is_complete`: Profile completion status
- `is_public`: Profile visibility setting

### Interest
- `name`: Interest name
- `category`: Interest category (technology, sports, music, etc.)
- `description`: Interest description
- `is_active`: Whether interest is available

### UserInterest
- `profile`: Reference to user profile
- `interest`: Reference to interest
- `created_at`: When interest was selected

### ProfilePicture
- `profile`: Reference to user profile
- `image`: Uploaded image file
- `is_current`: Whether this is the current picture
- `uploaded_at`: Upload timestamp

## Authentication

The service uses a custom authentication class that:
1. First attempts local JWT validation
2. Falls back to login service validation
3. Creates a simple user object with user_id from token

## File Upload

- **Supported formats**: JPEG, PNG, GIF
- **Maximum size**: 5MB
- **Storage**: Local media directory
- **Path**: `/media/profile_pictures/`

## Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver 8001
```

### Testing
```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test profiles
python manage.py test interests
```

## Integration with Login Service

The profile service integrates with the login service by:
1. Validating JWT tokens
2. Extracting user_id from tokens
3. Maintaining user session consistency

## API Usage Examples

### Profile Setup
```bash
curl -X POST http://localhost:8001/api/profiles/setup/ \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "bio": "Software developer passionate about AI",
    "interests": [1, 3, 5]
  }'
```

### Upload Profile Picture
```bash
curl -X POST http://localhost:8001/api/profiles/upload_picture/ \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -F "image=@profile.jpg"
```

### Get Profile Status
```bash
curl -X GET http://localhost:8001/api/profiles/status/ \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## Error Handling

The service provides comprehensive error handling for:
- Invalid file types and sizes
- Username conflicts
- Interest validation
- Authentication failures
- Database constraints

## Security Features

- JWT token validation
- File type validation
- Username sanitization
- Rate limiting (configurable)
- CORS configuration

## Monitoring and Logging

- Django admin interface for data management
- Profile completion tracking
- Upload history tracking
- Error logging and monitoring

## Future Enhancements

- Profile verification system
- Social media integration
- Advanced search and filtering
- Profile analytics
- Bulk operations
- API rate limiting
- Caching layer
- WebSocket support for real-time updates
