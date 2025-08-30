from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, MediaViewSet, health_check

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'media', MediaViewSet, basename='media')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/health/', health_check, name='health_check'),
]
