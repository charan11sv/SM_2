from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Profile, UserInterest, ProfilePicture
from interests.serializers import InterestSerializer


class ProfilePictureSerializer(serializers.ModelSerializer):
    """Serializer for profile picture uploads"""
    
    class Meta:
        model = ProfilePicture
        fields = ['id', 'image', 'uploaded_at', 'is_current']
        read_only_fields = ['id', 'uploaded_at', 'is_current']


class UserInterestSerializer(serializers.ModelSerializer):
    """Serializer for user interests"""
    
    interest = InterestSerializer(read_only=True)
    interest_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserInterest
        fields = ['id', 'interest', 'interest_id', 'created_at']
        read_only_fields = ['id', 'interest', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    """Main profile serializer"""
    
    profile_picture_url = serializers.CharField(read_only=True)
    interests_count = serializers.IntegerField(read_only=True)
    user_interests = UserInterestSerializer(many=True, read_only=True)
    interests = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of interest IDs (max 5)"
    )
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user_id', 'username', 'bio', 'profile_picture', 
            'profile_picture_url', 'is_complete', 'is_public', 
            'interests_count', 'user_interests', 'interests',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_id', 'is_complete', 'created_at', 'updated_at']
    
    def validate_username(self, value):
        """Validate username"""
        if value:
            # Check for valid characters
            if not value.replace('_', '').replace('-', '').isalnum():
                raise serializers.ValidationError(
                    "Username can only contain letters, numbers, underscores, and hyphens"
                )
            
            # Check for reserved names
            reserved_names = ['admin', 'root', 'system', 'user', 'test', 'demo']
            if value.lower() in reserved_names:
                raise serializers.ValidationError(
                    "This username is reserved and cannot be used"
                )
        
        return value
    
    def validate_interests(self, value):
        """Validate interests list"""
        if value and len(value) > 5:
            raise serializers.ValidationError(
                "Maximum 5 interests allowed"
            )
        return value
    
    def create(self, validated_data):
        """Create profile with interests"""
        interests_data = validated_data.pop('interests', [])
        profile = Profile.objects.create(**validated_data)
        
        # Add interests
        for interest_id in interests_data:
            UserInterest.objects.create(
                profile=profile,
                interest_id=interest_id
            )
        
        return profile
    
    def update(self, instance, validated_data):
        """Update profile with interests"""
        interests_data = validated_data.pop('interests', None)
        
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Update interests if provided
        if interests_data is not None:
            # Clear existing interests
            instance.user_interests.all().delete()
            
            # Add new interests
            for interest_id in interests_data:
                UserInterest.objects.create(
                    profile=instance,
                    interest_id=interest_id
                )
        
        return instance


class ProfileSetupSerializer(serializers.ModelSerializer):
    """Serializer for initial profile setup"""
    
    interests = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        help_text="List of interest IDs (max 5)"
    )
    
    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_picture', 'interests']
    
    def validate_interests(self, value):
        """Validate interests list"""
        if not value:
            raise serializers.ValidationError("At least one interest is required")
        
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 interests allowed")
        
        return value
    
    def create(self, validated_data):
        """Create profile with interests"""
        # Extract interests data before creating profile
        interests_data = validated_data.pop('interests', [])
        
        # Create the profile
        profile = Profile.objects.create(**validated_data)
        
        # Add interests through UserInterest model
        for interest_id in interests_data:
            UserInterest.objects.create(
                profile=profile,
                interest_id=interest_id
            )
        
        return profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for profile updates"""
    
    interests = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of interest IDs (max 5)"
    )
    
    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_picture', 'interests', 'is_public']
        extra_kwargs = {
            'username': {'required': False},
            'profile_picture': {'required': False}
        }
    
    def update(self, instance, validated_data):
        """Update profile with interests"""
        # Extract interests data before updating profile
        interests_data = validated_data.pop('interests', None)
        
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Update interests if provided
        if interests_data is not None:
            # Clear existing interests
            instance.user_interests.all().delete()
            
            # Add new interests
            for interest_id in interests_data:
                UserInterest.objects.create(
                    profile=instance,
                    interest_id=interest_id
                )
        
        return instance
