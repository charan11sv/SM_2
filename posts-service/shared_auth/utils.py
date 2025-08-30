"""
Utility Functions for Microservice Authentication

This module provides helper functions for authentication and service communication.
"""

import requests
import logging
from django.conf import settings
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Get user information from a JWT token by calling the login service.
    
    Args:
        token (str): JWT token
        
    Returns:
        dict: User data if token is valid, None otherwise
    """
    try:
        login_service_url = getattr(settings, 'LOGIN_SERVICE_URL', 'http://localhost:8000')
        
        response = requests.post(
            f"{login_service_url}/api/users/validate-token/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Token validation failed: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Error validating token: {str(e)}")
        return None


def call_service_api(
    service_name: str, 
    endpoint: str, 
    method: str = 'GET',
    data: Optional[Dict] = None,
    token: Optional[str] = None,
    service_token: Optional[str] = None
) -> Optional[requests.Response]:
    """
    Make a service-to-service API call.
    
    Args:
        service_name (str): Name of the service to call
        endpoint (str): API endpoint path
        method (str): HTTP method (GET, POST, PUT, DELETE)
        data (dict): Request data for POST/PUT requests
        token (str): JWT token for user authentication
        service_token (str): Service token for service-to-service auth
        
    Returns:
        requests.Response: Response object if successful, None otherwise
    """
    try:
        # Get service URL from settings
        service_url = getattr(settings, 'SERVICES', {}).get(service_name)
        if not service_url:
            logger.error(f"Service URL not found for {service_name}")
            return None
        
        # Prepare headers
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        if service_token:
            headers['X-Service-Token'] = service_token
        
        # Make the request
        if method.upper() == 'GET':
            response = requests.get(f"{service_url}{endpoint}", headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(f"{service_url}{endpoint}", json=data, headers=headers, timeout=10)
        elif method.upper() == 'PUT':
            response = requests.put(f"{service_url}{endpoint}", json=data, headers=headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(f"{service_url}{endpoint}", headers=headers, timeout=10)
        else:
            logger.error(f"Unsupported HTTP method: {method}")
            return None
        
        return response
        
    except Exception as e:
        logger.error(f"Error calling service {service_name}: {str(e)}")
        return None


def validate_post_exists(post_id: str, token: Optional[str] = None) -> bool:
    """
    Validate that a post exists by calling the posts service.
    
    Args:
        post_id (str): Post ID to validate
        token (str): JWT token for authentication
        
    Returns:
        bool: True if post exists, False otherwise
    """
    response = call_service_api('posts', f'/api/posts/{post_id}/', token=token)
    return response is not None and response.status_code == 200


def validate_user_exists(user_id: str, token: Optional[str] = None) -> bool:
    """
    Validate that a user exists by calling the profile service.
    
    Args:
        user_id (str): User ID to validate
        token (str): JWT token for authentication
        
    Returns:
        bool: True if user exists, False otherwise
    """
    response = call_service_api('profile', f'/api/profiles/{user_id}/', token=token)
    return response is not None and response.status_code == 200


def get_service_token() -> Optional[str]:
    """
    Get a service token for service-to-service communication.
    
    Returns:
        str: Service token if available, None otherwise
    """
    service_tokens = getattr(settings, 'SERVICE_TOKENS', [])
    return service_tokens[0] if service_tokens else None


def log_authentication_event(user_id: str, action: str, service: str, success: bool):
    """
    Log authentication events for monitoring and debugging.
    
    Args:
        user_id (str): ID of the user
        action (str): Action being performed
        service (str): Name of the service
        success (bool): Whether the action was successful
    """
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"AUTH_{status}: User {user_id} performed {action} on {service}")


def is_development_mode() -> bool:
    """
    Check if the application is running in development mode.
    
    Returns:
        bool: True if in development mode
    """
    return getattr(settings, 'DEBUG', False)
