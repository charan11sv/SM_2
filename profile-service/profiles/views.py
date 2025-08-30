import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from .models import Profile, UserInterest, ProfilePicture
from .serializers import (
    ProfileSerializer, ProfileSetupSerializer, ProfileUpdateSerializer,
    ProfilePictureSerializer
)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for the profile service"""
    return Response({
        'service': 'profile-service',
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'port': 8001
    })


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Profile model"""
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_queryset(self):
        """Filter queryset based on user"""
        return Profile.objects.filter(user_id=self.request.user.id)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return ProfileSetupSerializer
        elif self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        return ProfileSerializer
    
    def perform_create(self, serializer):
        """Create profile with user_id from JWT token"""
        # Extract user_id from JWT token
        user_id = self.request.user.id
        serializer.save(user_id=str(user_id))
    
    def perform_update(self, serializer):
        """Update profile and check completion status"""
        profile = serializer.save()
        
        # Check if profile is now complete
        if profile.is_setup_complete() and not profile.is_complete:
            profile.is_complete = True
            profile.save()
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile"""
        try:
            profile = Profile.objects.get(user_id=request.user.id)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found. Please complete profile setup.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def setup(self, request):
        """Initial profile setup for first-time users"""
        try:
            # Debug logging
            print(f"DEBUG: Request method: {request.method}")
            print(f"DEBUG: Request content type: {request.content_type}")
            print(f"DEBUG: Request data: {request.data}")
            print(f"DEBUG: Request FILES: {request.FILES}")
            print(f"DEBUG: Request user: {request.user}")
            print(f"DEBUG: Request user ID: {getattr(request.user, 'id', 'NO_ID')}")
            
            # Check if profile already exists
            if Profile.objects.filter(user_id=request.user.id).exists():
                return Response(
                    {'detail': 'Profile already exists. Use update endpoint instead.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = ProfileSetupSerializer(data=request.data)
            if serializer.is_valid():
                # Create profile with user_id
                profile = serializer.save(user_id=str(request.user.id))
                
                # Check completion status
                if profile.is_setup_complete():
                    profile.is_complete = True
                    profile.save()
                
                # Return full profile data
                full_serializer = ProfileSerializer(profile)
                return Response(full_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(f"DEBUG: Exception in setup: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'detail': f'Profile setup failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def upload_picture(self, request):
        """Upload profile picture"""
        try:
            if 'image' not in request.FILES:
                return Response(
                    {'detail': 'No image file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            image_file = request.FILES['image']
            
            # Validate file type
            if not image_file.content_type in settings.ALLOWED_IMAGE_TYPES:
                return Response(
                    {'detail': 'Invalid file type. Only JPEG, PNG, and GIF are allowed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate file size
            if image_file.size > settings.MAX_UPLOAD_SIZE:
                return Response(
                    {'detail': f'File size too large. Maximum size is {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get or create profile
            profile, created = Profile.objects.get_or_create(
                user_id=request.user.id,
                defaults={'username': f'user_{request.user.id}'}
            )
            
            # Update profile picture
            profile.profile_picture = image_file
            profile.save()
            
            # Create profile picture record
            ProfilePicture.objects.create(
                profile=profile,
                image=image_file,
                is_current=True
            )
            
            # Check completion status
            if profile.is_setup_complete() and not profile.is_complete:
                profile.is_complete = True
                profile.save()
            
            return Response({
                'detail': 'Profile picture uploaded successfully',
                'profile_picture_url': profile.profile_picture_url
            })
        
        except Exception as e:
            return Response(
                {'detail': f'Picture upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        """Get profile completion status"""
        try:
            profile = Profile.objects.get(user_id=request.user.id)
            return Response({
                'is_complete': profile.is_complete,
                'has_username': bool(profile.username),
                'has_picture': bool(profile.profile_picture),
                'interests_count': profile.interests_count,
                'missing_fields': []
            })
        except Profile.DoesNotExist:
            return Response({
                'is_complete': False,
                'has_username': False,
                'has_picture': False,
                'interests_count': 0,
                'missing_fields': ['username', 'profile_picture', 'interests']
            })
    
    @action(detail=False, methods=['post'])
    def check_username(self, request):
        """Check if username is available"""
        username = request.data.get('username', '').strip()
        
        if not username:
            return Response(
                {'detail': 'Username is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if username exists
        if Profile.objects.filter(username=username).exists():
            return Response({
                'available': False,
                'detail': 'Username already taken'
            })
        
        # Check if username is valid
        try:
            Profile(username=username).clean()
            return Response({
                'available': True,
                'detail': 'Username is available'
            })
        except ValidationError as e:
            return Response({
                'available': False,
                'detail': str(e)
            })


class ProfilePictureViewSet(viewsets.ModelViewSet):
    """ViewSet for ProfilePicture model"""
    
    queryset = ProfilePicture.objects.all()
    serializer_class = ProfilePictureSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user's profile"""
        return ProfilePicture.objects.filter(profile__user_id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get profile picture history for current user"""
        pictures = self.get_queryset().order_by('-uploaded_at')
        serializer = self.get_serializer(pictures, many=True)
        return Response(serializer.data)
