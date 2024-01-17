from django.test import TestCase
from django.urls import reverse
class MainPageTest(TestCase):

    def test_home_page_status_code(self):
        path = reverse('main_page_url')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

