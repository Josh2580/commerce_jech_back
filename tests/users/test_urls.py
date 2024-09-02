# users/tests/test_urls.py
from django.urls import resolve, reverse
from django.test import SimpleTestCase
from users.views import RegisterView,  ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class UserURLsTest(SimpleTestCase):
    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_login_url(self):
        url = reverse('token_obtain_pair_login')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)
