# Login Functionality Documentation

This document describes the login system implemented in the Django application.

## Overview

The login system provides secure user authentication using JWT (JSON Web Tokens) with the following features:

- User registration with email verification
- Secure login with JWT tokens
- Protected API endpoints
- Token refresh and logout functionality
- User profile management

## API Endpoints

### 1. User Registration Flow

#### Request Verification Code
- **URL**: `POST /users/request-verification/`
- **Description**: Sends a 6-digit verification code to the user's email
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**: Success message with email confirmation

#### Verify Email
- **URL**: `POST /users/verify-email/`
- **Description**: Verifies the email using the received code
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "code": "123456"
  }
  ```
- **Response**: Email verification success message

#### Onboard User
- **URL**: `POST /users/onboard/`
- **Description**: Creates a new user account after email verification
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "password": "securepassword123",
    "verification_code": "123456"
  }
  ```
- **Response**: User creation success with user ID

### 2. Authentication Endpoints

#### Login
- **URL**: `POST /users/login/`
- **Description**: Authenticates user and returns JWT tokens
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  }
  ```

#### Token Refresh
- **URL**: `POST /users/token/refresh/`
- **Description**: Refreshes JWT access token using refresh token
- **Request Body**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Token refreshed successfully",
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  }
  ```

#### Logout
- **URL**: `POST /users/logout/`
- **Description**: Logs out user and blacklists refresh token
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Response**: Logout success message

#### Get User Profile
- **URL**: `GET /users/profile/`
- **Description**: Retrieves authenticated user's profile information
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true
  }
  ```

## JWT Token Configuration

The application uses `djangorestframework-simplejwt` with the following settings:

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 1 day
- **Token Rotation**: Enabled
- **Blacklist After Rotation**: Enabled
- **Algorithm**: HS256

## Security Features

1. **Password Requirements**: Minimum 8 characters
2. **Email Verification**: Required before account creation
3. **JWT Authentication**: Secure token-based authentication
4. **Token Blacklisting**: Secure logout with token invalidation
5. **Protected Endpoints**: Authentication required for sensitive operations
6. **Token Refresh**: Automatic token rotation for enhanced security

## Usage Examples

### Complete Registration and Login Flow

1. **Request verification code**:
   ```bash
   curl -X POST http://localhost:8000/users/request-verification/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com"}'
   ```

2. **Verify email** (check email for code):
   ```bash
   curl -X POST http://localhost:8000/users/verify-email/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "code": "123456"}'
   ```

3. **Create account**:
   ```bash
   curl -X POST http://localhost:8000/users/onboard/ \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "user@example.com",
       "password": "securepassword123",
       "verification_code": "123456"
     }'
   ```

4. **Login**:
   ```bash
   curl -X POST http://localhost:8000/users/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "securepassword123"
     }'
   ```

5. **Access protected endpoint**:
   ```bash
   curl -X GET http://localhost:8000/users/profile/ \
     -H "Authorization: Bearer <access_token>"
   ```

6. **Refresh token** (when access token expires):
   ```bash
   curl -X POST http://localhost:8000/users/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "<refresh_token>"}'
   ```

7. **Logout**:
   ```bash
   curl -X POST http://localhost:8000/users/logout/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{"refresh_token": "<refresh_token>"}'
   ```

## Testing

Use the provided `test_login.py` script to test the complete login flow:

```bash
python test_login.py
```

Make sure your Django server is running on `localhost:8000` before running the test script.

## Dependencies

The following packages are required for the login functionality:

- `djangorestframework-simplejwt` - JWT authentication
- `djangorestframework` - REST API framework
- `Django` - Web framework

## Notes

- Email verification codes expire after 10 minutes
- Passwords are securely hashed using Django's built-in password hashing
- JWT tokens are automatically rotated on refresh
- All sensitive endpoints require valid JWT access tokens
- The system supports token blacklisting for secure logout
- Access tokens expire after 60 minutes, refresh tokens after 1 day
- Token refresh automatically rotates both access and refresh tokens
