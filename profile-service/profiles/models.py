import os
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from interests.models import Interest


def profile_picture_path(instance, filename):
    """Generate file path for profile pictures"""
    ext = filename.split('.')[-1]
    filename = f"profile_pic_{instance.user_id}.{ext}"
    return os.path.join('profile_pictures', filename)


class Profile(models.Model):
    """User profile model"""
    
    user_id = models.CharField(max_length=100, unique=True, help_text="ID from login service")
    username = models.CharField(
        max_length=50, 
        unique=True,
        validators=[
            MinLengthValidator(3, "Username must be at least 3 characters long"),
            MaxLengthValidator(50, "Username cannot exceed 50 characters")
        ],
        help_text="Unique username for the user"
    )
    bio = models.TextField(
        max_length=200,
        blank=True,
        validators=[
            MaxLengthValidator(200, "Bio cannot exceed 200 characters")
        ],
        help_text="User bio (max 200 characters)"
    )
    profile_picture = models.ImageField(
        upload_to=profile_picture_path,
        blank=True,
        null=True,
        help_text="User profile picture"
    )
    is_complete = models.BooleanField(
        default=False,
        help_text="Whether the profile setup is complete"
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Whether the profile is publicly visible"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return f"{self.username} ({self.user_id})"
    
    def clean(self):
        """Custom validation"""
        if self.username:
            # Check for valid username characters
            if not self.username.replace('_', '').replace('-', '').isalnum():
                raise ValidationError("Username can only contain letters, numbers, underscores, and hyphens")
            
            # Check for reserved usernames
            reserved_names = ['admin', 'root', 'system', 'user', 'test', 'demo']
            if self.username.lower() in reserved_names:
                raise ValidationError("This username is reserved and cannot be used")
    
    def save(self, *args, **kwargs):
        """Custom save method"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def profile_picture_url(self):
        """Get profile picture URL"""
        if self.profile_picture:
            return self.profile_picture.url
        return None
    
    @property
    def interests_count(self):
        """Get count of user interests"""
        return self.user_interests.count()
    
    def is_setup_complete(self):
        """Check if profile setup is complete"""
        return bool(
            self.username and 
            self.profile_picture and 
            self.user_interests.count() > 0
        )


class UserInterest(models.Model):
    """Many-to-many relationship between users and interests"""
    
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='user_interests'
    )
    interest = models.ForeignKey(
        Interest, 
        on_delete=models.CASCADE, 
        related_name='user_profiles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['profile', 'interest']
        ordering = ['-created_at']
        verbose_name = 'User Interest'
        verbose_name_plural = 'User Interests'
    
    def __str__(self):
        return f"{self.profile.username} - {self.interest.name}"
    
    def clean(self):
        """Custom validation"""
        if self.profile and self.profile.user_interests.count() >= 5:
            raise ValidationError("Users can select maximum 5 interests")
    
    def save(self, *args, **kwargs):
        """Custom save method"""
        self.full_clean()
        super().save(*args, **kwargs)


class ProfilePicture(models.Model):
    """Model to track profile picture uploads and changes"""
    
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='picture_history'
    )
    image = models.ImageField(upload_to=profile_picture_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Profile Picture'
        verbose_name_plural = 'Profile Pictures'
    
    def __str__(self):
        return f"{self.profile.username} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        """Ensure only one current picture per profile"""
        if self.is_current:
            # Set all other pictures for this profile as not current
            ProfilePicture.objects.filter(
                profile=self.profile, 
                is_current=True
            ).update(is_current=False)
        super().save(*args, **kwargs)
