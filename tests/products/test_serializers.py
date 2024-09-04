# products/test_serializers.py
from django.test import TestCase
import uuid
from rest_framework.exceptions import ValidationError
from products.models import Product
from products.serializers import ProductSerializer
from stores.models import Store
from categories.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.store = Store.objects.create(owner=self.user, name="Test Store")
        self.category = Category.objects.create(name="Electronics")
        self.product_data = {
            'name': 'Test Product',
            'description': 'A test product description',
            'price': '19.99',
            'stock': 10,
            'store': self.store.id,
            'categories': [self.category.id],
        }

    def test_product_serializer_valid_data(self):
        serializer = ProductSerializer(data=self.product_data, context={'request': self.user})
        self.assertTrue(serializer.is_valid())
        product = serializer.save(owner=self.user)
        
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'A test product description')
        self.assertEqual(str(product.price), '19.99')
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.store, self.store)
        self.assertIn(self.category, product.categories.all())
        self.assertEqual(product.owner, self.user)
        self.assertIsNotNone(product.slug)
        self.assertIsInstance(product.product_id, uuid.UUID)

    def test_product_serializer_invalid_data(self):
        invalid_data = self.product_data.copy()
        invalid_data['price'] = 'invalid_price'  # Invalid price
        serializer = ProductSerializer(data=invalid_data, context={'request': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_product_serializer_read_only_fields(self):
        serializer = ProductSerializer(data=self.product_data, context={'request': self.user})
        serializer.is_valid()
        product = serializer.save(owner=self.user)
        
        # Attempt to change read-only fields
        read_only_data = {
            'owner': '2',
            'slug': 'new-slug',
            'product_id': '12345'
        }
        serializer = ProductSerializer(product, data=read_only_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_product = serializer.save()
        
        self.assertEqual(updated_product.owner, self.user)  # Owner should not change
        self.assertNotEqual(updated_product.slug, 'new-slug')  # Slug should not change
        self.assertEqual(updated_product.slug, product.slug)  # Slug remains the same

    def test_product_serializer_output(self):
        product = Product.objects.create(
            owner=self.user,
            name="Test Product",
            description="A test product.",
            price=19.99,
            stock=10,
            store=self.store,
        )
        product.categories.add(self.category)
        serializer = ProductSerializer(product)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(data['owner'], self.user.id)
        self.assertEqual(data['slug'], product.slug)
        self.assertEqual(data['price'], '19.99')
        self.assertEqual(data['stock'], 10)
        self.assertEqual(data['store'], self.store.id)
        self.assertIn(self.category.id, data['categories'])
