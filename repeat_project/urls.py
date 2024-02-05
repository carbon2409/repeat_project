"""
URL configuration for repeat_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from orders_app.views import stripe_webhook_view
from products_app.views import main_page

urlpatterns = [
    path('', main_page, name='main_page_url'),
    path('admin/', admin.site.urls),
    path('products/', include('products_app.urls', namespace='products_app')),
    path('users/', include('users_app.urls', namespace='users_app')),
    path('orders/', include('orders_app.urls', namespace='orders_app')),
    path('accounts/', include('allauth.urls')),
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook_url'),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

