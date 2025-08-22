from rest_framework import serializers
from .models import User, EmailVerification
from django.contrib.auth import authenticate

class OnboardingSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data["email"]
        code = data["verification_code"]

        try:
            verification = EmailVerification.objects.filter(email=email, code=code).latest("created_at")
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid verification code.")

        if not verification.is_valid():
            raise serializers.ValidationError("Verification code expired.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User already exists.")

        return data

    def create(self, validated_data):
        # Remove verification_code from validated_data before creating user
        validated_data.pop('verification_code', None)
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=password,
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Must include email and password.")
