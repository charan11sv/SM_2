from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProfilePictureViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'profile-pictures', ProfilePictureViewSet, basename='profile-picture')

urlpatterns = [
    path('', include(router.urls)),
]
