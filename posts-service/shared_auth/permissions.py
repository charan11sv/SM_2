"""
Custom Permission Classes for Microservices

This module provides permission classes that work with the MicroserviceUser.
"""

from rest_framework import permissions


class IsAuthenticatedUser(permissions.BasePermission):
    """
    Allow access only to authenticated users.
    
    This permission class works with MicroserviceUser objects.
    """
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    
    Assumes the model instance has an `user_id` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return str(obj.user_id) == str(request.user.id)


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    
    Assumes the model instance has an `user_id` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        return str(obj.user_id) == str(request.user.id)


class IsServiceUser(permissions.BasePermission):
    """
    Allow access only to internal service users.
    
    This is used for service-to-service communication.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'username', '') == 'internal_service'
        )


class AllowAny(permissions.BasePermission):
    """
    Allow any access.
    
    This is useful for public endpoints like health checks.
    """
    
    def has_permission(self, request, view):
        return True


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow read access to anyone, but require authentication for writes.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
