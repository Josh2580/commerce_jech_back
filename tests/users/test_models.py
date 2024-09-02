# users/tests/test_models.py
from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword123'))

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
