from django.db import models


class Interest(models.Model):
    """Predefined interests that users can select from"""
    
    INTEREST_CATEGORIES = [
        ('technology', 'Technology'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('travel', 'Travel'),
        ('food', 'Food & Cooking'),
        ('art', 'Art & Design'),
        ('fashion', 'Fashion'),
        ('gaming', 'Gaming'),
        ('fitness', 'Fitness & Health'),
        ('books', 'Books & Reading'),
        ('movies', 'Movies & TV'),
        ('photography', 'Photography'),
        ('nature', 'Nature & Outdoors'),
        ('business', 'Business & Finance'),
        ('education', 'Education'),
        ('politics', 'Politics'),
        ('science', 'Science'),
        ('history', 'History'),
        ('languages', 'Languages'),
        ('crafts', 'Crafts & DIY'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=INTEREST_CATEGORIES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For future icon support
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
