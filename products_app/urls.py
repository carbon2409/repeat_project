from django.urls import path

from products_app import views
from django.views.decorators.cache import cache_page

app_name = 'products_app'

urlpatterns = [
    path('page/<int:page_number>/', views.ProductListView.as_view(), name='product_list_url'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='category_list_url'),
]
