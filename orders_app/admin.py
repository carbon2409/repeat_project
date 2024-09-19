from django.contrib import admin
from .models import OrderModel

admin.site.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = '__all__'

    class Meta:
        model = OrderModel
        fields = '__all__'



