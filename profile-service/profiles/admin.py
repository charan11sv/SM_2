from django.contrib import admin
from .models import Profile, UserInterest, ProfilePicture


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_id', 'is_complete', 'is_public', 'interests_count', 'created_at']
    list_filter = ['is_complete', 'is_public', 'created_at', 'updated_at']
    search_fields = ['username', 'user_id', 'bio']
    list_editable = ['is_public']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user_id', 'username', 'bio')
        }),
        ('Media', {
            'fields': ('profile_picture',)
        }),
        ('Settings', {
            'fields': ('is_complete', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'interests_count']
    
    def interests_count(self, obj):
        return obj.interests_count
    interests_count.short_description = 'Interests'


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['profile', 'interest', 'created_at']
    list_filter = ['interest__category', 'created_at']
    search_fields = ['profile__username', 'interest__name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Relationship', {
            'fields': ('profile', 'interest')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']


@admin.register(ProfilePicture)
class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = ['profile', 'image', 'is_current', 'uploaded_at']
    list_filter = ['is_current', 'uploaded_at']
    search_fields = ['profile__username']
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('Picture Information', {
            'fields': ('profile', 'image', 'is_current')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['uploaded_at']
