# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from django.core.mail import send_mail
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError



# users/views.py
from rest_framework_simplejwt.tokens import UntypedToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        if user.role == 'seller':
            self.send_verification_email(user)

    def send_verification_email(self, user):
        token = RefreshToken.for_user(user).access_token
        verification_url = f"http://127.0.0.1:8000/api/users/verify/{token}/"
        send_mail(
            'Verify your email',
            f'Click the following link to verify your email: {verification_url}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            # Decode the token to extract the user information
            decoded_token = UntypedToken(token)
            user_id = decoded_token['user_id']

            # Fetch the user from the database
            user = User.objects.get(id=user_id)

            # Optionally, you can activate the user or perform other actions here
            user.email_verified = True
            user.save()

            return Response({
                "detail": "Email verified successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "email_verified":user.email_verified,
                }
            }, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError, User.DoesNotExist) as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
