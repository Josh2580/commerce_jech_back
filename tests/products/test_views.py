# products/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Product
from stores.models import Store
from categories.models import Category
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class ProductViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.user_with_store = User.objects.create_user(email='storeowner@example.com', password='testpassword')
        self.store = Store.objects.create(owner=self.user_with_store, name="Test Store")
        self.category = Category.objects.create(name="Electronics")
        
        self.product_data = {
            'name': 'Test Product',
            'description': 'A test product description',
            'price': '19.99',
            'stock': 10,
            'categories': [self.category.id],
        }
        self.client.login(email='testuser@example.com', password='testpassword')

        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        
        
        

    def test_create_product_without_store_restricted(self):
        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        # First product should succeed
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Second product should succeed
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Third product should be restricted
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You must create a store to list more than 2 products.", response.data['non_field_errors'][0])

    def test_create_product_with_store(self):

        self.client.login(email='storeowner@example.com', password='testpassword')
        # Create third product with store, should succeed
        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.store, self.store)
        self.assertEqual(product.owner, self.user_with_store)

    def test_update_product(self):
        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Create a product
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        product_id = response.data['id']
        
        # Attempt to update the product
        update_data = {
            'name': 'Updated Product',
            'price': '29.99'
        }
        response = self.client.patch(reverse('product-detail', args=[product_id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')
        self.assertEqual(response.data['price'], '29.99')

    def test_delete_product(self):
        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Create a product
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        product_id = response.data['id']
        
        # Delete the product
        response = self.client.delete(reverse('product-detail', args=[product_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product_id).exists())

    def test_permission_denied_for_other_users(self):
        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Create a product with store owner
        self.client.login(email='storeowner@example.com', password='testpassword')
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        product_id = response.data['id']
        
        # Try to update the product with a different user
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.patch(reverse('product-detail', args=[product_id]), {'name': 'Hacked Product'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
