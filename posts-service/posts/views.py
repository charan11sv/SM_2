from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import FileResponse
from django.utils import timezone
import os

from .models import Post, PostMedia
from .serializers import (
    PostSerializer, PostCreateSerializer, PostListSerializer
)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for the posts service"""
    return Response({
        'service': 'posts-service',
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'port': 8002
    })


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model"""
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]  # Temporarily allow all for development
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_queryset(self):
        """Filter queryset based on request parameters"""
        queryset = Post.objects.all()
        
        # Filter by user_id if provided
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset.select_related().prefetch_related('media_files')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """Create post with user_id"""
        user_id = self.request.data.get('user_id', 'default_user')
        serializer.save(user_id=user_id)
    
    @action(detail=False, methods=['delete'])
    def delete_user_posts(self, request):
        """Delete all posts by a specific user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete all posts by the user (this will cascade delete media files)
        deleted_count, _ = Post.objects.filter(user_id=user_id).delete()
        
        return Response({
            'message': f'Deleted {deleted_count} posts for user {user_id}',
            'deleted_count': deleted_count
        }, status=status.HTTP_200_OK)


class MediaViewSet(viewsets.ViewSet):
    """ViewSet for serving media files"""
    
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, pk=None):
        """Serve media file"""
        try:
            media = PostMedia.objects.get(pk=pk)
            if media.file and os.path.exists(media.file.path):
                return FileResponse(media.file, content_type='application/octet-stream')
            else:
                return Response(
                    {'error': 'File not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except PostMedia.DoesNotExist:
            return Response(
                {'error': 'Media not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
