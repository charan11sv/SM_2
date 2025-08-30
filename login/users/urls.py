from django.urls import path
from .views import RequestVerificationCode, VerifyEmail, OnboardUser, LoginView, LogoutView, UserProfileView, CustomTokenRefreshView, health_check

urlpatterns = [
    path('request-verification/', RequestVerificationCode.as_view(), name='request-verification'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('onboard/', OnboardUser.as_view(), name='onboard-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('health/', health_check, name='health_check'),
]
