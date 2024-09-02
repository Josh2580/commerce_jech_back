# users/tests/test_serializers.py
from django.test import TestCase
from users.serializers import RegisterSerializer
from users.models import User

class RegisterSerializerTest(TestCase):
    def test_serializer_with_valid_data(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'buyer'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword123'))

    def test_serializer_with_invalid_data(self):
        data = {
            'email': '',
            'password': 'testpassword123',
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
