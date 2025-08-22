# Email Verification System

This Django application implements a complete email verification system that sends verification codes to users' email addresses instead of just returning them in the API response.

## Features

- ✅ **Real Email Sending**: Verification codes are actually sent via SMTP
- ✅ **HTML Email Templates**: Beautiful, responsive email templates
- ✅ **Code Expiration**: Verification codes expire after 10 minutes
- ✅ **RESTful API**: Clean API endpoints for verification flow
- ✅ **Error Handling**: Proper error handling for email failures
- ✅ **Database Storage**: Verification codes are stored and validated

## API Endpoints

### 1. Request Verification Code
```
POST /api/users/request-verification/
Content-Type: application/json

{
    "email": "user@example.com"
}
```

**Response:**
```json
{
    "message": "Verification code sent successfully to your email",
    "email": "user@example.com"
}
```

### 2. Verify Email
```
POST /api/users/verify-email/
Content-Type: application/json

{
    "email": "user@example.com",
    "code": "123456"
}
```

**Response:**
```json
{
    "message": "Email verified successfully"
}
```

### 3. User Onboarding
```
POST /api/users/onboard/
Content-Type: application/json

{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123"
}
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings
Edit `onboarding/settings.py` and update the email configuration:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-actual-email@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Your app password
DEFAULT_FROM_EMAIL = 'your-actual-email@gmail.com'  # Your email address
```

### 3. Gmail Setup (Recommended)
1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use this app password in `EMAIL_HOST_PASSWORD`

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```

## Testing the System

### Option 1: Use the Test Script
```bash
python test_email.py
```

### Option 2: Use curl
```bash
# Request verification code
curl -X POST http://localhost:8000/api/users/request-verification/ \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@example.com"}'

# Verify email (after you receive the code)
curl -X POST http://localhost:8000/api/users/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@example.com", "code": "123456"}'
```

### Option 3: Use Postman or similar API testing tool
- Import the endpoints from the API documentation above
- Test with your actual email address

## Email Template Customization

The email template is located at `users/templates/users/verification_email.html`. You can customize:

- Colors and styling
- Company branding
- Message content
- Layout and design

## Troubleshooting

### Common Issues

1. **"Failed to send verification code"**
   - Check your email credentials in settings.py
   - Verify your app password is correct
   - Check if your email provider allows SMTP access

2. **"Connection refused"**
   - Make sure your Django server is running
   - Check if the port is correct (default: 8000)

3. **"Invalid verification code"**
   - Codes expire after 10 minutes
   - Request a new code if needed

### Email Provider Alternatives

- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Use your provider's settings

## Security Features

- ✅ Verification codes expire after 10 minutes
- ✅ Codes are deleted after successful verification
- ✅ No sensitive information in API responses
- ✅ Proper error handling without information leakage

## Production Considerations

- Use environment variables for sensitive credentials
- Implement rate limiting for verification requests
- Add logging for email sending operations
- Consider using email service providers (SendGrid, Mailgun, etc.)
- Implement proper SSL/TLS for production

## File Structure

```
├── onboarding/          # Main Django project
│   ├── settings.py      # Email configuration
│   └── urls.py         # URL routing
├── users/              # Users app
│   ├── models.py       # User and EmailVerification models
│   ├── views.py        # API views with email sending
│   ├── urls.py         # App-specific URLs
│   └── templates/      # Email templates
├── requirements.txt     # Python dependencies
├── test_email.py       # Testing script
└── README.md           # This file
```

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your email configuration
3. Test with the provided test script
4. Check Django server logs for detailed error messages

---

**Note**: This system is designed for development and testing. For production use, consider implementing additional security measures and using professional email service providers.
