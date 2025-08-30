from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone

from .models import SamplePost, SampleUser, PostLike
from .serializers import (
    PostLikeSerializer, PostLikeCreateSerializer, PostLikeDetailSerializer,
    PostLikeCountSerializer, UserLikesSerializer, SamplePostSerializer, SampleUserSerializer
)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for the likes service"""
    return Response({
        'service': 'likes-service',
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'port': 8003
    })


class PostLikeViewSet(viewsets.ModelViewSet):
    """ViewSet for PostLike model"""
    
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.AllowAny]  # Temporarily allow all for development
    
    def get_queryset(self):
        """Filter queryset based on request parameters"""
        queryset = PostLike.objects.select_related('post', 'user').all()
        
        # Filter by post_id if provided
        post_id = self.request.query_params.get('post_id', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        # Filter by user_id if provided
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user__user_id=user_id)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return PostLikeCreateSerializer
        elif self.action in ['list', 'retrieve']:
            return PostLikeDetailSerializer
        return PostLikeSerializer
    
    def perform_create(self, serializer):
        """Create like with validation"""
        # Check if like already exists
        post = serializer.validated_data['post']
        user = serializer.validated_data['user']
        
        if PostLike.objects.filter(post=post, user=user).exists():
            raise serializers.ValidationError("User has already liked this post")
        
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def post_likes(self, request):
        """Get all likes for a specific post"""
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response(
                {'error': 'post_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            post = SamplePost.objects.get(id=post_id)
            likes = PostLike.objects.filter(post=post).select_related('user')
            serializer = PostLikeDetailSerializer(likes, many=True)
            
            return Response({
                'post_id': str(post.id),
                'post_number': post.post_number,
                'post_description': post.description,
                'total_likes': likes.count(),
                'likes': serializer.data
            })
        except SamplePost.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def user_likes(self, request):
        """Get all posts liked by a specific user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = SampleUser.objects.get(user_id=user_id)
            likes = PostLike.objects.filter(user=user).select_related('post')
            
            liked_posts = []
            for like in likes:
                liked_posts.append({
                    'post_id': str(like.post.id),
                    'post_number': like.post.post_number,
                    'post_description': like.post.description,
                    'post_user_id': like.post.user_id,
                    'liked_at': like.created_at
                })
            
            return Response({
                'user_id': user.user_id,
                'username': user.username,
                'total_likes': likes.count(),
                'liked_posts': liked_posts
            })
        except SampleUser.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def like_count(self, request):
        """Get like count for a specific post"""
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response(
                {'error': 'post_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            post = SamplePost.objects.get(id=post_id)
            likes = PostLike.objects.filter(post=post).select_related('user')
            
            liked_by_users = [like.user.username for like in likes]
            
            return Response({
                'post_id': str(post.id),
                'post_number': post.post_number,
                'like_count': likes.count(),
                'liked_by_users': liked_by_users
            })
        except SamplePost.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['delete'])
    def remove_like(self, request):
        """Remove a like by post_id and user_id"""
        post_id = request.query_params.get('post_id')
        user_id = request.query_params.get('user_id')
        
        if not post_id or not user_id:
            return Response(
                {'error': 'Both post_id and user_id parameters are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            like = PostLike.objects.get(
                post_id=post_id, 
                user__user_id=user_id
            )
            like.delete()
            
            return Response({
                'message': 'Like removed successfully',
                'post_id': post_id,
                'user_id': user_id
            })
        except PostLike.DoesNotExist:
            return Response(
                {'error': 'Like not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get analytics about likes"""
        total_likes = PostLike.objects.count()
        total_posts = SamplePost.objects.count()
        total_users = SampleUser.objects.count()
        
        # Most liked posts
        most_liked_posts = PostLike.objects.values('post__post_number', 'post__description')\
            .annotate(like_count=Count('id'))\
            .order_by('-like_count')[:5]
        
        # Most active likers
        most_active_likers = PostLike.objects.values('user__username')\
            .annotate(like_count=Count('id'))\
            .order_by('-like_count')[:5]
        
        return Response({
            'total_likes': total_likes,
            'total_posts': total_posts,
            'total_users': total_users,
            'most_liked_posts': most_liked_posts,
            'most_active_likers': most_active_likers
        })


class SamplePostViewSet(viewsets.ModelViewSet):
    """ViewSet for SamplePost model - for testing purposes"""
    
    queryset = SamplePost.objects.all()
    serializer_class = SamplePostSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        """Create post with auto-incrementing post number"""
        serializer.save()


class SampleUserViewSet(viewsets.ModelViewSet):
    """ViewSet for SampleUser model - for testing purposes"""
    
    queryset = SampleUser.objects.all()
    serializer_class = SampleUserSerializer
    permission_classes = [permissions.AllowAny]
