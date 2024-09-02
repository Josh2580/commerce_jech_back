# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import RegisterView, ProfileView, VerifyEmailView

urlpatterns = [
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ##
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),

]
