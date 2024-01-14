import uuid
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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


class EmailVerificationModel(models.Model):
    code = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def send_verification_email(self):
        link = f'http://127.0.0.1:8001/users/verify/{self.user.id}/{self.code}'
        send_mail(
            subject='Subject msg',
            message=f'Для подтверждения email перейдите по ссылке {link}',
            from_email='continental-kzn@yandex.ru',
            recipient_list=[self.user.email]

        )

    def is_expired(self):
        return True if self.expired_at < timezone.now() else False
