from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import OnboardingSerializer, LoginSerializer
from .models import EmailVerification, User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random

class RequestVerificationCode(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        # Generate a random 6-digit code
        code = str(random.randint(100000, 999999))
        
        # Save the verification code to database
        EmailVerification.objects.create(email=email, code=code)

        # Send the verification code via email
        try:
            subject = 'Email Verification Code'
            
            # Render HTML email template
            html_message = render_to_string('users/verification_email.html', {
                'verification_code': code
            })
            
            # Create plain text version
            plain_message = strip_tags(html_message)
            
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            
            return Response({
                "message": "Verification code sent successfully to your email",
                "email": email
            }, status=200)
            
        except Exception as e:
            # If email sending fails, delete the verification code and return error
            EmailVerification.objects.filter(email=email, code=code).delete()
            return Response({
                "error": "Failed to send verification code. Please try again.",
                "details": str(e)
            }, status=500)

class VerifyEmail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        
        if not email or not code:
            return Response({
                "error": "Both email and verification code are required"
            }, status=400)
        
        try:
            # Find the verification record
            verification = EmailVerification.objects.get(email=email, code=code)
            
            # Check if code is still valid
            if not verification.is_valid():
                verification.delete()
                return Response({
                    "error": "Verification code has expired. Please request a new one."
                }, status=400)
            
            # Mark email as verified (you might want to add a field to User model for this)
            # For now, we'll just delete the verification record
            verification.delete()
            
            return Response({
                "message": "Email verified successfully"
            }, status=200)
            
        except EmailVerification.DoesNotExist:
            return Response({
                "error": "Invalid verification code"
            }, status=400)

class OnboardUser(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OnboardingSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Delete the verification code after successful user creation
            email = request.data.get('email')
            EmailVerification.objects.filter(email=email).delete()
            
            return Response({"message": "User onboarded", "user_id": user.id}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
        }, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view with better error handling"""
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return Response({
                'message': 'Token refreshed successfully',
                'tokens': response.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to refresh token',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
