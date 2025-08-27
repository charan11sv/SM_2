# Posts Service

A Django REST API microservice for managing social media posts with media uploads (images and videos).

## Features

- **Post Management**: Create, read, update, delete posts
- **Media Support**: Upload and serve images and videos
- **User-based Posts**: Associate posts with specific users
- **Auto-incrementing Post Numbers**: Unique identification for each post
- **RESTful API**: Clean, testable endpoints
- **Docker Support**: Containerized deployment

## API Endpoints

### Posts
- `POST /api/posts/` - Create a new post with media
- `GET /api/posts/` - Get all posts (all users)
- `GET /api/posts/?user_id={user_id}` - Get posts by specific user
- `PUT /api/posts/{id}/` - Update a post
- `DELETE /api/posts/{id}/` - Delete a specific post
- `DELETE /api/posts/delete_user_posts/?user_id={user_id}` - Delete all posts by a user

### Media
- `GET /api/media/{id}/` - Serve media files

## Models

### Post
- `id`: UUID primary key
- `user_id`: User identifier (string)
- `description`: Post content (max 2000 chars)
- `post_number`: Auto-incrementing unique number
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### PostMedia
- `id`: UUID primary key
- `post`: Foreign key to Post
- `media_type`: 'image' or 'video'
- `file`: Uploaded media file
- `created_at`: Creation timestamp

## Quick Start

### 1. Build and Run with Docker

```bash
# Build the container
docker-compose build

# Start the service
docker-compose up

# The service will be available at http://localhost:8002
```

### 2. Run Tests

```bash
# Install test dependencies
pip install requests

# Run the complete workflow test
python test_complete_workflow.py
```

## Testing Workflow

The service includes a comprehensive testing script that:

1. **Creates 3 test posts**:
   - 2 image posts for user1 (john_doe_123)
   - 1 video post for user2 (jane_smith_456)

2. **Tests all API endpoints**:
   - Post creation
   - Post retrieval (all posts, user-specific)
   - Media file serving
   - Post deletion

3. **Downloads media files** to `C:\Users\Dell\Documents\projects\social media\test_images`

4. **Verifies deletion** by removing user1's posts and confirming

## Test Media Files

The testing script expects these files:
- `C:\Users\Dell\Pictures\container.PNG`
- `C:\Users\Dell\Pictures\startup.PNG`
- `C:\Users\Dell\Downloads\sample-mp4-file-small.mp4`

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:8002
```

### Docker Development

```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

## Configuration

- **Port**: 8002 (mapped from container port 8000)
- **Database**: SQLite (for development)
- **Media Storage**: Local file system
- **File Size Limit**: 50MB
- **Supported Formats**: Images (PNG, JPG), Videos (MP4)

## Port Allocation

- **Login Service**: Port 8000
- **Profile Service**: Port 8001
- **Posts Service**: Port 8002

## Future Enhancements

- JWT authentication integration
- Database migration to PostgreSQL
- Media processing (thumbnails, compression)
- Tag system
- User feed functionality
- Like/comment system

## API Examples

### Create a Post

```bash
curl -X POST http://localhost:8002/api/posts/ \
  -F "user_id=john_doe_123" \
  -F "description=Check out this amazing setup!" \
  -F "media=@/path/to/image.jpg"
```

### Get All Posts

```bash
curl http://localhost:8002/api/posts/
```

### Get User Posts

```bash
curl "http://localhost:8002/api/posts/?user_id=john_doe_123"
```

### Delete User Posts

```bash
curl -X DELETE "http://localhost:8002/api/posts/delete_user_posts/?user_id=john_doe_123"
```
