from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
import uuid


class Post(models.Model):
    """Main post model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, help_text="User ID from external service")
    description = models.TextField(
        validators=[MinLengthValidator(1), MaxLengthValidator(2000)],
        help_text="Post description (max 2000 characters)"
    )
    post_number = models.PositiveIntegerField(unique=True, help_text="Auto-incrementing post number for uniqueness")
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
            last_post = Post.objects.order_by('-post_number').first()
            self.post_number = (last_post.post_number + 1) if last_post else 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Post #{self.post_number} by {self.user_id} - {self.description[:50]}"


class PostMedia(models.Model):
    """Media files associated with posts"""
    
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_files')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='posts/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'media_type']),
        ]
    
    def __str__(self):
        return f"{self.media_type} for {self.post}"
    
    @property
    def file_url(self):
        """Get file URL"""
        if self.file:
            return self.file.url
        return None
