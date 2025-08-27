from rest_framework import serializers
from .models import Post, PostMedia


class PostMediaSerializer(serializers.ModelSerializer):
    """Serializer for PostMedia model"""
    
    class Meta:
        model = PostMedia
        fields = ['id', 'media_type', 'file', 'file_url', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    
    media_files = PostMediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user_id', 'description', 'post_number', 'created_at', 'updated_at', 'media_files']


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts"""
    
    media = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['description', 'media']
    
    def create(self, validated_data):
        media_files = validated_data.pop('media', [])
        
        # Create the post (user_id will be set by the view)
        post = Post.objects.create(**validated_data)
        
        # Handle media files
        for media_file in media_files:
            # Determine media type based on file extension
            filename = media_file.name.lower()
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                media_type = 'image'
            elif filename.endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv')):
                media_type = 'video'
            else:
                # Try to determine from content type if available
                try:
                    if hasattr(media_file, 'content_type'):
                        if media_file.content_type.startswith('image/'):
                            media_type = 'image'
                        elif media_file.content_type.startswith('video/'):
                            media_type = 'video'
                        else:
                            continue  # Skip unsupported file types
                    else:
                        continue  # Skip if no content type
                except:
                    continue  # Skip if error determining type
            
            # Create PostMedia
            PostMedia.objects.create(
                post=post,
                media_type=media_type,
                file=media_file
            )
        
        return post
    
    def to_representation(self, instance):
        """Return full post data after creation"""
        return PostSerializer(instance).data


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for listing posts"""
    
    media_files = PostMediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user_id', 'description', 'post_number', 'created_at', 'media_files']
