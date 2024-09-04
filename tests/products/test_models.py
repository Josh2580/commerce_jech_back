# products/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from products.models import Product
from stores.models import Store
from categories.models import Category
import uuid

User = get_user_model()

class ProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.store = Store.objects.create(owner=self.user, name="Test Store")
        self.category = Category.objects.create(name="Electronics")
        
    def test_create_product(self):
        product = Product.objects.create(
            owner=self.user,
            name="Test Product",
            description="A test product.",
            price=19.99,
            stock=10,
            store=self.store,
        )
        product.categories.add(self.category)

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.slug, slugify("Test Product"))
        self.assertEqual(product.price, 19.99)
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.store, self.store)
        self.assertIn(self.category, product.categories.all())
        self.assertIsInstance(product.product_id, uuid.UUID)

    def test_slug_is_unique_per_owner(self):
        product1 = Product.objects.create(
            owner=self.user,
            name="Test Product",
            description="A test product.",
            price=19.99,
            stock=10,
            store=self.store,
        )
        product2 = Product.objects.create(
            owner=self.user,
            name="Test Product",
            description="Another test product with the same name.",
            price=29.99,
            stock=5,
            store=self.store,
        )
        self.assertNotEqual(product1.slug, product2.slug)
        self.assertTrue(product2.slug.startswith(f"{slugify('Test Product')}-"))

    def test_slug_is_owner_specific(self):
        user2 = User.objects.create_user(email='anotheruser@example.com', password='anotherpassword')
        product1 = Product.objects.create(
            owner=self.user,
            name="Test Product",
            description="A test product.",
            price=19.99,
            stock=10,
            store=self.store,
        )
        product2 = Product.objects.create(
            owner=user2,
            name="Test Product",
            description="A test product with a different owner.",
            price=29.99,
            stock=5,
        )
        self.assertEqual(product1.slug, product2.slug)

    def test_product_str(self):
        product = Product.objects.create(
            owner=self.user,
            name="Test Product",
            description="A test product.",
            price=19.99,
            stock=10,
            store=self.store,
        )
        self.assertEqual(str(product), "Test Product")
