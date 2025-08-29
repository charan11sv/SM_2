# 🗨️ Comments Microservice

A comprehensive comments microservice built with Django and Django REST Framework, featuring **nested comments (replies)**, **comment interactions (likes)**, and **Instagram-style commenting system**.

## ✨ Features

### 🎯 Core Functionality
- **Nested Comments**: Support for comment replies (like Instagram)
- **Comment Threading**: Hierarchical comment structure
- **Comment Interactions**: Like/unlike comments
- **Soft Delete**: Mark comments as deleted instead of hard delete
- **Edit Tracking**: Track if comments have been edited
- **User Attribution**: Each comment shows who wrote it
- **Post Association**: Comments linked to specific posts

### 🔧 Technical Features
- **Microservice Architecture**: Independent service with its own database
- **Docker Support**: Containerized with PostgreSQL
- **RESTful API**: Comprehensive endpoints for all operations
- **Sample Data**: Built-in sample posts and users for testing
- **Comprehensive Testing**: Full workflow demonstration script

## 🏗️ Architecture

### Database Schema
```
SamplePost (sample posts for testing)
├── id (UUID)
├── user_id (CharField)
├── description (TextField)
├── post_number (PositiveIntegerField)
└── created_at, updated_at

SampleUser (sample users for testing)
├── id (UUID)
├── user_id (CharField, unique)
├── username (CharField, unique)
├── email (EmailField, unique)
└── created_at

Comment (main comment model)
├── id (UUID)
├── post (ForeignKey to SamplePost)
├── user (ForeignKey to SampleUser)
├── parent_comment (ForeignKey to Comment, for replies)
├── content (TextField)
├── created_at, updated_at
├── is_edited (Boolean)
└── is_deleted (Boolean)

CommentLike (comment interactions)
├── id (UUID)
├── comment (ForeignKey to Comment)
├── user (ForeignKey to SampleUser)
└── created_at
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Start the service:**
   ```bash
   # Windows
   docker-start.bat
   
   # Linux/Mac
   ./docker-start.sh
   ```

2. **Run the comprehensive test:**
   ```bash
   docker exec -it comments-service-comments-service-1 python test_comments_workflow.py
   ```

3. **Access the service:**
   - **Comments Service**: http://localhost:8002
   - **API Endpoints**: http://localhost:8002/api/
   - **Admin Interface**: http://localhost:8002/admin/

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Run the service:**
   ```bash
   python manage.py runserver 8002
   ```

## 📡 API Endpoints

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/{id}/` - Get comment details
- `PUT /api/comments/{id}/` - Update a comment
- `DELETE /api/comments/{id}/` - Delete a comment
- `POST /api/comments/{id}/reply/` - Reply to a comment
- `GET /api/comments/{id}/replies/` - Get replies to a comment
- `DELETE /api/comments/{id}/soft_delete/` - Soft delete a comment
- `PUT /api/comments/{id}/edit/` - Edit a comment

### Comment Actions
- `GET /api/comments/post_comments/?post_id={id}` - Get all comments for a post
- `GET /api/comments/user_comments/?user_id={id}` - Get all comments by a user
- `GET /api/comments/analytics/` - Get comment statistics

### Comment Likes
- `POST /api/comment-likes/` - Like a comment
- `DELETE /api/comment-likes/remove_like/?comment_id={id}&user_id={id}` - Remove a like
- `GET /api/comment-likes/comment_likes/?comment_id={id}` - Get likes for a comment

### Sample Data
- `GET /api/users/` - List sample users
- `GET /api/posts/` - List sample posts
- `GET /api/users/{id}/comments/` - Get user's comments
- `GET /api/posts/{id}/comments/` - Get post's comments

## 🧪 Testing Workflow

The service includes a comprehensive testing script (`test_comments_workflow.py`) that demonstrates:

1. **Sample Data Creation**: Create users and posts
2. **Comment Creation**: Add comments with nested replies
3. **Interactions**: Add likes by different users
4. **Display Results**: Show all comments and interactions
5. **Add Reply**: Create a new reply to existing comment
6. **Add Like**: Like a comment
7. **Remove Like**: Unlike a comment
8. **Delete Comment**: Soft delete a comment
9. **Final Results**: Display final state after all operations

### Run the Test
```bash
# In Docker container
docker exec -it comments-service-comments-service-1 python test_comments_workflow.py

# Locally
python test_comments_workflow.py
```

## 🔄 Sample Data

The service creates sample data for testing:

### Users
- `john_doe` (user001) - Technology enthusiast
- `jane_smith` (user002) - AI researcher
- `bob_wilson` (user003) - Developer
- `alice_brown` (user004) - Travel blogger
- `charlie_davis` (user005) - Student

### Posts
- **Post #1**: Technology and innovation discussion
- **Post #2**: AI and machine learning
- **Post #3**: General technology thoughts
- **Post #4**: Life and coding
- **Post #5**: Food and travel

## 🐳 Docker Configuration

- **Service Port**: 8002
- **Database Port**: 5434
- **PostgreSQL Version**: 15
- **Network**: Isolated bridge network

## 🔗 Future Integration

This service is designed to be easily integrated with:
- **Posts Service**: Replace sample posts with real posts
- **User Service**: Replace sample users with real users
- **Authentication Service**: Add proper user authentication
- **Notification Service**: Notify users of comments/replies

## 📝 License

This project is part of a social media microservices architecture demonstration.
