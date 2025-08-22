import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken


class LoginServiceAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class that validates JWT tokens with the login service
    """
    
    def authenticate(self, request):
        """Authenticate the request and return a two-tuple of (user, token)"""
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        
        return self.get_user(validated_token), validated_token
    
    def get_header(self, request):
        """Extract the header containing the JWT token"""
        header = request.META.get('HTTP_AUTHORIZATION')
        
        if isinstance(header, str):
            header = header.encode('iso-8859-1')
        
        return header
    
    def get_raw_token(self, header):
        """Extract the raw token from the header"""
        parts = header.split()
        
        if len(parts) == 0:
            return None
        
        if parts[0].decode() != 'Bearer':
            return None
        
        if len(parts) != 2:
            raise AuthenticationFailed('Authorization header must contain two space-delimited values')
        
        return parts[1]
    
    def get_validated_token(self, raw_token):
        """Validate the raw token and return a validated token"""
        try:
            # First try to validate locally
            return AccessToken(raw_token)
        except (InvalidToken, TokenError):
            # If local validation fails, try to validate with login service
            return self.validate_with_login_service(raw_token)
    
    def validate_with_login_service(self, raw_token):
        """Validate token with the login service"""
        try:
            # Call login service to validate token
            response = requests.post(
                f"{settings.LOGIN_SERVICE_URL}/api/validate-token/",
                headers={'Authorization': f'Bearer {raw_token.decode()}'},
                timeout=5
            )
            
            if response.status_code == 200:
                # Token is valid, create a local token object
                token = AccessToken(raw_token)
                return token
            else:
                raise AuthenticationFailed('Invalid token')
                
        except requests.RequestException:
            # If login service is unavailable, fall back to local validation
            # This allows for offline development
            try:
                return AccessToken(raw_token)
            except (InvalidToken, TokenError):
                raise AuthenticationFailed('Invalid token')
    
    def get_user(self, validated_token):
        """Get the user from the validated token"""
        # Extract user_id from token payload
        user_id = validated_token.payload.get('user_id')
        
        if not user_id:
            raise AuthenticationFailed('Token contains no recognizable user identification')
        
        # Create a simple user object with the user_id
        user = SimpleUser(user_id)
        return user


class SimpleUser:
    """
    Simple user object that contains the user_id from the JWT token
    """
    
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True
        self.is_anonymous = False
    
    def __str__(self):
        return f"User(id={self.id})"
    
    def __repr__(self):
        return self.__str__()
