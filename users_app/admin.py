from django.contrib import admin
from django.contrib.auth.models import User
from .models import BasketModel, BasketItemModel
admin.site.register(BasketModel)
admin.site.register(BasketItemModel)


