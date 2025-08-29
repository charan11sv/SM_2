# Likes Microservice

A Django-based microservice for managing post likes in a social media application.

## Features

- **Like Management**: Register and remove likes on posts
- **Sample Data**: Built-in sample users and posts for testing
- **Analytics**: Like counts, user activity, and post popularity
- **RESTful API**: Complete CRUD operations for likes
- **Duplicate Prevention**: Users can't like the same post twice
- **Efficient Queries**: Optimized database queries with proper indexing
- **Docker Support**: Full containerization with PostgreSQL database

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Start with Docker
docker-start.bat          # Windows
./docker-start.sh         # Linux/Mac

# Or manually
docker-compose up --build
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start service
python manage.py runserver 0.0.0.0:8001
```

## API Endpoints

### Likes
- `GET /api/likes/` - List all likes
- `POST /api/likes/` - Create a new like
- `GET /api/likes/{id}/` - Get specific like details
- `PUT /api/likes/{id}/` - Update a like
- `DELETE /api/likes/{id}/` - Delete a like

### Custom Actions
- `GET /api/likes/post_likes/?post_id={id}` - Get all likes for a specific post
- `GET /api/likes/user_likes/?user_id={id}` - Get all posts liked by a user
- `GET /api/likes/like_count/?post_id={id}` - Get like count for a post
- `DELETE /api/likes/remove_like/?post_id={id}&user_id={id}` - Remove a like
- `GET /api/likes/analytics/` - Get likes analytics

### Sample Data (Testing)
- `GET /api/posts/` - List sample posts
- `POST /api/posts/` - Create sample post
- `GET /api/users/` - List sample users
- `POST /api/users/` - Create sample user

## Database Schema

### PostLike Model
- `id`: UUID primary key
- `post`: ForeignKey to SamplePost
- `user`: ForeignKey to SampleUser
- `created_at`: Timestamp when like was created

### SamplePost Model
- `id`: UUID primary key
- `user_id`: String identifier for post owner
- `description`: Post content (max 2000 chars)
- `post_number`: Auto-incrementing unique number
- `created_at`, `updated_at`: Timestamps

### SampleUser Model
- `id`: UUID primary key
- `user_id`: String identifier for user
- `username`: Unique username
- `email`: Unique email address
- `created_at`: Timestamp when user was created

## Setup Instructions

### Docker Deployment (Recommended)

1. **Prerequisites**: Docker and Docker Compose installed
2. **Start Services**: 
   ```bash
   # Windows
   docker-start.bat
   
   # Linux/Mac
   chmod +x docker-start.sh
   ./docker-start.sh
   ```
3. **Access Service**: http://localhost:8001
4. **Database**: PostgreSQL on localhost:5433

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the Service**
   ```bash
   python manage.py runserver 0.0.0.0:8001
   ```

## Testing Workflow

### Docker Testing
```bash
# Run Docker-compatible test
docker exec -it likes-service_likes-service_1 python test_docker_workflow.py
```

### Local Testing
```bash
# Run complete workflow test
python test_likes_workflow.py

# Test API endpoints
python test_api.py
```

The test workflow will:
1. Create 5 sample users and 5 sample posts
2. Register multiple likes from different users
3. Display all likes for each post
4. Show posts liked by each user
5. Remove 2 specific likes
6. Verify the changes in the database
7. Display analytics

### Manual Testing

#### Create Sample Data
```bash
# Create users
curl -X POST http://localhost:8001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test001", "username": "testuser", "email": "test@example.com"}'

# Create posts
curl -X POST http://localhost:8001/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test001", "description": "Test post"}'
```

#### Test Likes
```bash
# Like a post
curl -X POST http://localhost:8001/api/likes/ \
  -H "Content-Type: application/json" \
  -d '{"post": "POST_UUID", "user": "USER_UUID"}'

# Get likes for a post
curl "http://localhost:8001/api/likes/post_likes/?post_id=POST_UUID"

# Remove a like
curl -X DELETE "http://localhost:8001/api/likes/remove_like/?post_id=POST_UUID&user_id=USER_ID"
```

## Docker Configuration

### Services
- **likes-service**: Django application on port 8001
- **db**: PostgreSQL database on port 5433

### Volumes
- `postgres_data`: Persistent database storage
- `media_volume`: Media file storage

### Environment Variables
- `POSTGRES_DB`: Database name (default: likes_db)
- `POSTGRES_USER`: Database user (default: likes_user)
- `POSTGRES_PASSWORD`: Database password (default: likes_password)

## Future Integration

This service is designed to be easily integrated with:
- **Posts Service**: Replace SamplePost with actual Post model
- **Authentication Service**: Replace SampleUser with actual User model
- **Real-time Notifications**: Add WebSocket support for like notifications
- **Analytics Service**: Export like data for advanced analytics

## Development Notes

- **Docker**: Uses PostgreSQL for production-like database
- **Local**: Uses SQLite for development simplicity
- All endpoints allow any access (permissions.AllowAny) for testing
- Sample data models will be replaced with actual service models
- Database indexes are optimized for like queries
- Unique constraint prevents duplicate likes

## API Response Examples

### Post Likes Response
```json
{
  "post_id": "uuid",
  "post_number": 1,
  "post_description": "Post content...",
  "total_likes": 3,
  "likes": [
    {
      "id": "like_uuid",
      "created_at": "2024-01-01T12:00:00Z",
      "user_id": "user001",
      "username": "john_doe",
      "email": "john@example.com"
    }
  ]
}
```

### Analytics Response
```json
{
  "total_likes": 15,
  "total_posts": 5,
  "total_users": 5,
  "most_liked_posts": [
    {"post__post_number": 1, "like_count": 4}
  ],
  "most_active_likers": [
    {"user__username": "john_doe", "like_count": 3}
  ]
}
```

## Troubleshooting

### Docker Issues
- Ensure Docker Desktop is running
- Check if ports 8001 and 5433 are available
- Use `docker-compose logs` to view service logs

### Database Issues
- Wait for database to be ready (Docker startup takes time)
- Check database connection settings
- Verify PostgreSQL service is running

### API Issues
- Ensure service is running on correct port
- Check CORS settings for frontend integration
- Verify request format and parameters
