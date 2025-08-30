from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'likes', views.PostLikeViewSet)
router.register(r'posts', views.SamplePostViewSet)
router.register(r'users', views.SampleUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.health_check, name='health_check'),
]
