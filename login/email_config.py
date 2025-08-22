# Email Configuration Guide
# 
# To use this email verification system, you need to:
#
# 1. Update the email settings in onboarding/settings.py:
#    - Replace 'your-email@gmail.com' with your actual Gmail address
#    - Replace 'your-app-password' with your Gmail app password
#
# 2. For Gmail, you need to:
#    - Enable 2-factor authentication
#    - Generate an app password (not your regular password)
#    - Use that app password in EMAIL_HOST_PASSWORD
#
# 3. Alternative email providers:
#    - Outlook/Hotmail: smtp-mail.outlook.com, port 587
#    - Yahoo: smtp.mail.yahoo.com, port 587
#    - Custom SMTP: Use your provider's SMTP settings
#
# 4. Test the setup:
#    - Run the Django server
#    - Send a POST request to /api/users/request-verification/
#    - Check if the email is received

# Example settings for different providers:

# Gmail
GMAIL_CONFIG = {
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
}

# Outlook
OUTLOOK_CONFIG = {
    'EMAIL_HOST': 'smtp-mail.outlook.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
}

# Yahoo
YAHOO_CONFIG = {
    'EMAIL_HOST': 'smtp.mail.yahoo.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
}
