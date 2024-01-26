from django.urls import path
from django.conf.urls import include
from .views import CreateOrderView, SuccessOrderView

app_name = 'orders_app'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order_url'),
    path('success/', SuccessOrderView.as_view(), name='success_order_url'),
]