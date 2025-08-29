from rest_framework import serializers
from .models import SampleUser, SamplePost, Comment, CommentLike


class SampleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleUser
        fields = ['id', 'user_id', 'username', 'email', 'created_at']


class SamplePostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SamplePost
        fields = ['id', 'user_id', 'description', 'post_number', 'created_at', 'updated_at', 'comment_count']
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_deleted=False).count()


class CommentLikeSerializer(serializers.ModelSerializer):
    user = SampleUserSerializer(read_only=True)
    
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = SampleUserSerializer(read_only=True)
    likes = CommentLikeSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    is_reply = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'parent_comment', 'content', 'created_at', 
                 'updated_at', 'is_edited', 'is_deleted', 'likes', 'like_count', 
                 'reply_count', 'is_reply']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'parent_comment', 'content']


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


class CommentDetailSerializer(serializers.ModelSerializer):
    user = SampleUserSerializer(read_only=True)
    post = SamplePostSerializer(read_only=True)
    parent_comment = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    likes = CommentLikeSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'parent_comment', 'content', 'created_at', 
                 'updated_at', 'is_edited', 'is_deleted', 'replies', 'likes', 
                 'like_count', 'reply_count']
    
    def get_parent_comment(self, obj):
        if obj.parent_comment:
            return {
                'id': obj.parent_comment.id,
                'content': obj.parent_comment.content,
                'user': SampleUserSerializer(obj.parent_comment.user).data
            }
        return None
    
    def get_replies(self, obj):
        replies = obj.replies.filter(is_deleted=False).order_by('created_at')
        return CommentSerializer(replies, many=True).data


class CommentListSerializer(serializers.ModelSerializer):
    user = SampleUserSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    is_reply = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 
                 'is_edited', 'is_deleted', 'like_count', 'reply_count', 'is_reply']


class CommentLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['comment', 'user']


class UserCommentsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = SampleUser
        fields = ['id', 'user_id', 'username', 'email', 'comments']
    
    def get_comments(self, obj):
        comments = obj.comments.filter(is_deleted=False).order_by('-created_at')
        return CommentListSerializer(comments, many=True).data


class PostCommentsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = SamplePost
        fields = ['id', 'user_id', 'description', 'post_number', 'comments']
    
    def get_comments(self, obj):
        # Get top-level comments (not replies) ordered by creation time
        comments = obj.comments.filter(parent_comment__isnull=True, is_deleted=False).order_by('created_at')
        return CommentDetailSerializer(comments, many=True).data
