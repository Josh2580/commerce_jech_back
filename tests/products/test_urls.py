# products/tests/test_urls.py
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from products.views import ProductListCreateView, ProductDetailView

class ProductURLsTest(SimpleTestCase):

    def test_product_list_url_resolves(self):
        url = reverse('product-list-create')
        self.assertEqual(resolve(url).func.view_class, ProductListCreateView)

    def test_product_detail_url_resolves(self):
        url = reverse('product-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)
