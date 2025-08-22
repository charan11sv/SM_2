from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterestViewSet

router = DefaultRouter()
router.register(r'interests', InterestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
