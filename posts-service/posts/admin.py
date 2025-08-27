from django.contrib import admin
from .models import Post, PostMedia


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['post_number', 'user_id', 'description', 'created_at']
    list_filter = ['created_at', 'user_id']
    search_fields = ['user_id', 'description']
    readonly_fields = ['id', 'post_number', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['post__user_id', 'post__description']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
