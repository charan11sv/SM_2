from django.contrib import admin
from .models import SampleUser, SamplePost, Comment, CommentLike


@admin.register(SampleUser)
class SampleUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'email', 'created_at']
    search_fields = ['user_id', 'username', 'email']
    list_filter = ['created_at']
    ordering = ['username']


@admin.register(SamplePost)
class SamplePostAdmin(admin.ModelAdmin):
    list_display = ['post_number', 'user_id', 'description', 'created_at', 'comment_count']
    search_fields = ['user_id', 'description']
    list_filter = ['created_at']
    ordering = ['-created_at']
    
    def comment_count(self, obj):
        return obj.comments.filter(is_deleted=False).count()
    comment_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'content_preview', 'parent_comment', 'is_reply', 'is_edited', 'is_deleted', 'created_at']
    list_filter = ['is_edited', 'is_deleted', 'created_at', 'parent_comment']
    search_fields = ['content', 'user__username', 'post__description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def is_reply(self, obj):
        return obj.parent_comment is not None
    is_reply.boolean = True
    is_reply.short_description = 'Is Reply'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['comment__content', 'user__username']
    ordering = ['-created_at']
