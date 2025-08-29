from django.contrib import admin
from .models import SamplePost, SampleUser, PostLike


@admin.register(SamplePost)
class SamplePostAdmin(admin.ModelAdmin):
    list_display = ['post_number', 'user_id', 'description', 'created_at']
    list_filter = ['created_at', 'user_id']
    search_fields = ['description', 'user_id']
    ordering = ['-post_number']


@admin.register(SampleUser)
class SampleUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_id', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['username', 'user_id', 'email']
    ordering = ['username']


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__post_number', 'user__username']
    ordering = ['-created_at']
