"""
Shared Authentication for Microservices

This module provides JWT token validation by communicating with the login service.
"""

import requests
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)


class MicroserviceUser:
    """Simple user object for microservices"""
    
    def __init__(self, user_id, email=None, username=None):
        self.id = user_id
        self.email = email
        self.username = username
        self.is_authenticated = True
        self.is_anonymous = False
    
    def __str__(self):
        return f"MicroserviceUser(id={self.id})"


class MicroserviceAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class that validates JWT tokens with the login service.
    
    This allows microservices to authenticate users without duplicating JWT logic.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        # Get the authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        # Check if it's a Bearer token
        if not auth_header.startswith('Bearer '):
            return None
        
        # Extract the token
        token = auth_header.split(' ')[1]
        
        try:
            # Validate token with login service
            user_data = self._validate_token_with_login_service(token)
            
            if user_data:
                # Create a user object
                user = MicroserviceUser(
                    user_id=user_data.get('user_id'),
                    email=user_data.get('email'),
                    username=user_data.get('username')
                )
                return (user, token)
            
        except AuthenticationFailed:
            # Re-raise authentication failures
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
        
        return None
    
    def _validate_token_with_login_service(self, token):
        """
        Validate JWT token by calling the login service.
        
        Args:
            token (str): JWT token to validate
            
        Returns:
            dict: User data if token is valid
            
        Raises:
            AuthenticationFailed: If token is invalid
        """
        try:
            # Get login service URL from settings
            login_service_url = getattr(settings, 'LOGIN_SERVICE_URL', 'http://localhost:8000')
            
            # Call login service to validate token
            response = requests.post(
                f"{login_service_url}/api/users/validate-token/",
                headers={'Authorization': f'Bearer {token}'},
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise AuthenticationFailed('Invalid or expired token')
            else:
                logger.error(f"Login service error: {response.status_code}")
                raise AuthenticationFailed('Authentication service error')
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to login service failed: {str(e)}")
            raise AuthenticationFailed('Authentication service unavailable')
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return 'Bearer realm="api"'


class ServiceToServiceAuthentication(authentication.BaseAuthentication):
    """
    Authentication for service-to-service communication.
    
    This allows services to authenticate with each other using service tokens.
    """
    
    def authenticate(self, request):
        """
        Authenticate service-to-service requests.
        """
        # Get the service token header
        service_token = request.META.get('HTTP_X_SERVICE_TOKEN', '')
        
        if not service_token:
            return None
        
        # Validate service token (simple check for now)
        if self._is_valid_service_token(service_token):
            # Create a service user
            user = MicroserviceUser(
                user_id='service_user',
                email='service@internal',
                username='internal_service'
            )
            return (user, service_token)
        
        return None
    
    def _is_valid_service_token(self, token):
        """
        Validate service token.
        
        In production, this should check against a secure token store.
        """
        # Simple validation for development
        valid_tokens = getattr(settings, 'SERVICE_TOKENS', [])
        return token in valid_tokens
    
    def authenticate_header(self, request):
        return 'ServiceToken realm="api"'
