from django.urls import path
from django.conf.urls import include
from .views import CreateOrderView, SuccessOrderView, CancelOrderView, OrderListView, OrderDetailView

app_name = 'orders_app'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order_url'),
    path('success/', SuccessOrderView.as_view(), name='success_order_url'),
    path('cancel/', CancelOrderView.as_view(), name='cancel_order_url'),
    path('list/', OrderListView.as_view(), name='orders_list_url'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail_url'),
]