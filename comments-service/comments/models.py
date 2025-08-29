import uuid
from django.db import models
from django.core.validators import MinLengthValidator


class SamplePost(models.Model):
    """Sample post model for testing comments"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50, unique=False)
    description = models.TextField()
    post_number = models.PositiveIntegerField(unique=True, auto_created=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sample_posts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Post #{self.post_number}: {self.description[:50]}..."


class SampleUser(models.Model):
    """Sample user model for testing comments"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sample_users'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.user_id})"


class Comment(models.Model):
    """Comment model with support for nested replies"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(SamplePost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(SampleUser, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['parent_comment', 'created_at']),
        ]

    def __str__(self):
        if self.parent_comment:
            return f"Reply by {self.user.username} on {self.post.post_number}"
        return f"Comment by {self.user.username} on {self.post.post_number}"

    @property
    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent_comment is not None

    @property
    def reply_count(self):
        """Get the number of replies to this comment"""
        return self.replies.filter(is_deleted=False).count()

    @property
    def like_count(self):
        """Get the number of likes on this comment"""
        return self.likes.count()


class CommentLike(models.Model):
    """Model for liking comments"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(SampleUser, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_likes'
        unique_together = ['comment', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.comment.id}"
