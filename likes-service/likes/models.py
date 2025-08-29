from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
import uuid


class SamplePost(models.Model):
    """Sample post model for testing - will be replaced by actual posts service later"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, help_text="User ID from external service")
    description = models.TextField(
        validators=[MinLengthValidator(1), MaxLengthValidator(2000)],
        help_text="Post description (max 2000 characters)"
    )
    post_number = models.PositiveIntegerField(unique=True, help_text="Auto-incrementing post number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['post_number']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.post_number:
            # Auto-increment post number
            last_post = SamplePost.objects.order_by('-post_number').first()
            self.post_number = (last_post.post_number + 1) if last_post else 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Post #{self.post_number} by {self.user_id} - {self.description[:50]}"


class SampleUser(models.Model):
    """Sample user model for testing - will be replaced by actual auth service later"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, unique=True, help_text="User ID from external service")
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['username']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['username']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.user_id})"


class PostLike(models.Model):
    """Post like model - the main model for this service"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(SamplePost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(SampleUser, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']  # Prevent duplicate likes
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'user']),
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Like by {self.user.username} on Post #{self.post.post_number}"
    
    @property
    def post_user_id(self):
        """Get the user_id of the post owner"""
        return self.post.user_id
    
    @property
    def like_user_id(self):
        """Get the user_id of the person who liked"""
        return self.user.user_id
