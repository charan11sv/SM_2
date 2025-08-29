from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from .models import SampleUser, SamplePost, Comment, CommentLike
from .serializers import (
    SampleUserSerializer, SamplePostSerializer, CommentSerializer,
    CommentCreateSerializer, CommentUpdateSerializer, CommentDetailSerializer,
    CommentListSerializer, CommentLikeCreateSerializer, UserCommentsSerializer,
    PostCommentsSerializer
)


class SampleUserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing sample users"""
    queryset = SampleUser.objects.all()
    serializer_class = SampleUserSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments by a specific user"""
        user = self.get_object()
        serializer = UserCommentsSerializer(user)
        return Response(serializer.data)


class SamplePostViewSet(viewsets.ModelViewSet):
    """ViewSet for managing sample posts"""
    queryset = SamplePost.objects.all()
    serializer_class = SamplePostSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post with nested structure"""
        post = self.get_object()
        serializer = PostCommentsSerializer(post)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments with nested replies"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        elif self.action in ['retrieve', 'post_comments', 'user_comments']:
            return CommentDetailSerializer
        return CommentSerializer

    @action(detail=False, methods=['get'])
    def post_comments(self, request):
        """Get all comments for a specific post"""
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response({'error': 'post_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = SamplePost.objects.get(id=post_id)
            serializer = PostCommentsSerializer(post)
            return Response(serializer.data)
        except SamplePost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def user_comments(self, request):
        """Get all comments by a specific user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = SampleUser.objects.get(id=user_id)
            serializer = UserCommentsSerializer(user)
            return Response(serializer.data)
        except SampleUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Add a reply to a comment"""
        parent_comment = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(parent_comment=parent_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get all replies to a comment"""
        comment = self.get_object()
        replies = comment.replies.filter(is_deleted=False).order_by('created_at')
        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def soft_delete(self, request, pk=None):
        """Soft delete a comment (mark as deleted)"""
        comment = self.get_object()
        comment.is_deleted = True
        comment.save()
        return Response({'message': 'Comment soft deleted successfully'})

    @action(detail=True, methods=['put'])
    def edit(self, request, pk=None):
        """Edit a comment"""
        comment = self.get_object()
        serializer = CommentUpdateSerializer(comment, data=request.data, partial=True)
        
        if serializer.is_valid():
            comment.is_edited = True
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get comment analytics"""
        total_comments = Comment.objects.filter(is_deleted=False).count()
        total_replies = Comment.objects.filter(is_deleted=False, parent_comment__isnull=False).count()
        total_top_level = Comment.objects.filter(is_deleted=False, parent_comment__isnull=True).count()
        
        # Most commented posts
        top_posts = SamplePost.objects.annotate(
            comment_count=Count('comments', filter=Q(comments__is_deleted=False))
        ).order_by('-comment_count')[:5]
        
        # Most active commenters
        top_users = SampleUser.objects.annotate(
            comment_count=Count('comments', filter=Q(comments__is_deleted=False))
        ).order_by('-comment_count')[:5]
        
        return Response({
            'total_comments': total_comments,
            'total_replies': total_replies,
            'total_top_level': total_top_level,
            'top_posts': SamplePostSerializer(top_posts, many=True).data,
            'top_users': SampleUserSerializer(top_users, many=True).data
        })


class CommentLikeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comment likes"""
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeCreateSerializer

    def create(self, request, *args, **kwargs):
        """Create a like on a comment"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.validated_data['comment']
            user = serializer.validated_data['user']
            
            # Check if like already exists
            if CommentLike.objects.filter(comment=comment, user=user).exists():
                return Response({'error': 'User already liked this comment'}, 
                             status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def remove_like(self, request):
        """Remove a like from a comment"""
        comment_id = request.query_params.get('comment_id')
        user_id = request.query_params.get('user_id')
        
        if not comment_id or not user_id:
            return Response({'error': 'Both comment_id and user_id parameters required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            like = CommentLike.objects.get(comment_id=comment_id, user_id=user_id)
            like.delete()
            return Response({'message': 'Like removed successfully'})
        except CommentLike.DoesNotExist:
            return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def comment_likes(self, request):
        """Get all likes for a specific comment"""
        comment_id = request.query_params.get('comment_id')
        if not comment_id:
            return Response({'error': 'comment_id parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comment = Comment.objects.get(id=comment_id)
            likes = comment.likes.all()
            serializer = CommentLikeSerializer(likes, many=True)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
