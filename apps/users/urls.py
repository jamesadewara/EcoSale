from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    UserViewSet,
    UniversityViewSet,
    PasswordResetView,
    PasswordResetConfirmView,
    SocialLoginView,
    EmailVerificationView,
    validate_token,
)

urlpatterns = [
    # Authentication
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('auth/validate-token', validate_token, name='validate-token'),

    # Profile
    path('profile/', UserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='profile'),
    path('profile/me/', UserViewSet.as_view({'get': 'retrieve'}), {'pk': 'me'}, name='profile-me'),

    # Password reset
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # Social auth
    path('social/login/', SocialLoginView.as_view(), name='social-login'),

    # Email verification
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),

    # University endpoints
    path('universities/', UniversityViewSet.as_view({'get': 'list'}), name='university-list'),

    # Role management
    path('switch-to-seller/', UserViewSet.as_view({'post': 'switch_to_seller'}), name='switch-to-seller'),
]
