from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .models import User, University
from .serializers import UserProfileSerializer, UniversitySerializer
from .permissions import IsAdminOrReadOnly

class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"{settings.FRONTEND_URL}/password-reset/{uid}/{token}/"

        try:
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({'detail': f'Email sending failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Password reset email sent'})


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({'detail': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successfully'})
        return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class SocialLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({'detail': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class EmailVerificationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'detail': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    http_method_names = ['get', 'patch', 'post', 'head', 'options']

    def get_object(self):
        if self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()

    @action(detail=False, methods=['post'])
    def switch_to_seller(self, request):
        user = request.user
        if user.user_type == 'buyer':
            user.user_type = 'seller'
            user.save()
            return Response({'status': 'Role switched to seller'})
        return Response(
            {'error': 'Only buyers can switch to seller role'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = University.objects.filter(is_verified=True)
    serializer_class = UniversitySerializer
    pagination_class = None
    permission_classes = [AllowAny]
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_token(request):
    """
    Check if the user's token is still valid.
    If valid, returns user info.
    """
    user = request.user
    return Response({
        "valid": True,
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }, status=status.HTTP_200_OK)