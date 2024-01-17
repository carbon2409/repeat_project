from django.test import TestCase
from django.urls import reverse
from products_app.models import ProductsModel, CategoryModel

class ProductsModelTests(TestCase):
    fixtures = ['products.json', 'categories.json']

    def setUp(self):
        self.category = CategoryModel.objects.get(id=2)
        self.products = ProductsModel.objects.all()


    def _common_tests(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products_app/products.html')
    def test_products_list(self):
        path = reverse('products_app:product_list_url')
        response = self.client.get(path)
        self._common_tests(response)
        self.assertEqual(list(response.context_data['product_objects']), list(self.products))

    def test_category_list(self):
        path = reverse('products_app:category_list_url', kwargs={'category_slug': self.category.slug})
        response = self.client.get(path)
        self._common_tests(response)

        print(list(response.context_data['product_objects']),
              list(self.products.filter(category=self.category)), sep='\n\n')

        self.assertEqual(list(response.context_data['product_objects']),
                         list(self.products.filter(category=self.category)))


