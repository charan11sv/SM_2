from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SampleUserViewSet, SamplePostViewSet, CommentViewSet, CommentLikeViewSet

router = DefaultRouter()
router.register(r'users', SampleUserViewSet)
router.register(r'posts', SamplePostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'comment-likes', CommentLikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
