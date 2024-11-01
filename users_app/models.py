from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.conf import settings

from products_app.models import ProductsModel


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True, verbose_name='Avatar image')
    first_name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Фамилия')
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержден email?')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.username}'


class BasketQuerySet(models.QuerySet):
    def totally(self):
        return sum([item.total_price() for item in self])

class BasketModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    objects = BasketQuerySet.as_manager()

    def total_price(self):
        return self.product.price * self.quantity

    def to_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'total_price': float(self.total_price())
        }
        return basket_item


class EmailVerificationModel(models.Model):
    code = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def send_verification_email(self):
        link = f'{settings.DOMAIN_NAME}/users/verify/{self.user.id}/{self.code}'
        send_mail(
            subject='Subject msg',
            message=f'Для подтверждения email перейдите по ссылке {link}',
            from_email='continental-kzn@yandex.ru',
            recipient_list=[self.user.email]

        )

    def is_expired(self):
        return True if self.expired_at < timezone.now() else False
