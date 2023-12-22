from django.urls import path
from products_app import views

app_name = 'products_app'

urlpatterns = [
     path('', views.ProductListView.as_view(), name='product_list_url'),
     path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='category_list_url'),
]