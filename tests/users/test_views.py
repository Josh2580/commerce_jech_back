# users/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User



class UserViewTests(APITestCase):
    def test_register_user(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'role': 'buyer'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')
