from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, BasketModel, EmailVerificationModel
from http import HTTPStatus

class RegistrationTests(TestCase):
    fixtures = ['users.json', 'basket.json', 'email_verifications.json', 'products.json', 'categories.json']

    def setUp(self):
        self.user_data ={
            'username': 'carboneum2409',
            'first_name': 'Insaf',
            'last_name': 'Nizamov',
            'email': 'carbon2409@mail.ru',
            'password1': '123456789pP',
            'password2': '123456789pP',

        }
        self.username = self.user_data['username']


    def _common_tests(self, response):
        self.assertTemplateUsed(response, template_name='users_app/register.html')
    def test_registration(self):
        path = reverse('users_app:registration_url')
        get_response = self.client.get(path)
        users = CustomUser.objects.all()
        self._common_tests(get_response)
        self.assertFalse(users.filter(username=self.username).exists())
        post_response = self.client.post(path, data=self.user_data)
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertContains(self.client.get(reverse('users_app:login_url')), text='Вы успешно зарегистрировались')
        self.assertTrue(users.filter(username=self.username).exists())

        email_verification_object = EmailVerificationModel.objects.filter(user__email=self.user_data['email'])
        self.assertTrue(email_verification_object.exists())

    def test_login_user(self):
        register_path = reverse('users_app:registration_url')
        login_path = reverse('users_app:login_url')
        get_response = self.client.get(login_path)
        self.assertEqual(get_response.status_code, HTTPStatus.OK)

        _register_test_user = self.client.post(register_path, data=self.user_data)
        post_response = self.client.post(login_path, data={'username': self.username,
                                                          'password': self.user_data['password1']})
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertTrue(post_response.wsgi_request.user.is_authenticated)






