from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True, verbose_name='Avatar image')
    first_name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.username}'
