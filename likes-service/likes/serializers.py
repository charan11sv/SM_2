from rest_framework import serializers
from .models import SamplePost, SampleUser, PostLike


class SampleUserSerializer(serializers.ModelSerializer):
    """Serializer for sample users"""
    
    class Meta:
        model = SampleUser
        fields = ['id', 'user_id', 'username', 'email', 'created_at']


class SamplePostSerializer(serializers.ModelSerializer):
    """Serializer for sample posts"""
    
    user = SampleUserSerializer(read_only=True)
    
    class Meta:
        model = SamplePost
        fields = ['id', 'user_id', 'description', 'post_number', 'created_at', 'updated_at', 'user']


class PostLikeSerializer(serializers.ModelSerializer):
    """Serializer for post likes"""
    
    post = SamplePostSerializer(read_only=True)
    user = SampleUserSerializer(read_only=True)
    
    class Meta:
        model = PostLike
        fields = ['id', 'post', 'user', 'created_at']


class PostLikeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating likes"""
    
    class Meta:
        model = PostLike
        fields = ['post', 'user']


class PostLikeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for likes with post and user info"""
    
    post_id = serializers.UUIDField(source='post.id', read_only=True)
    post_number = serializers.IntegerField(source='post.post_number', read_only=True)
    post_description = serializers.CharField(source='post.description', read_only=True)
    post_user_id = serializers.CharField(source='post.user_id', read_only=True)
    
    user_id = serializers.CharField(source='user.user_id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = PostLike
        fields = [
            'id', 'created_at',
            'post_id', 'post_number', 'post_description', 'post_user_id',
            'user_id', 'username', 'email'
        ]


class PostLikeCountSerializer(serializers.Serializer):
    """Serializer for like count responses"""
    
    post_id = serializers.UUIDField()
    post_number = serializers.IntegerField()
    like_count = serializers.IntegerField()
    liked_by_users = serializers.ListField(child=serializers.CharField())


class UserLikesSerializer(serializers.Serializer):
    """Serializer for user's liked posts"""
    
    user_id = serializers.CharField()
    username = serializers.CharField()
    total_likes = serializers.IntegerField()
    liked_posts = serializers.ListField(child=serializers.DictField())
