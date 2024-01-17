from django.contrib.auth.decorators import login_required
from django.urls import path

import users_app.views as views

app_name = 'users_app'

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration_url'),
    path('login/', views.UserLoginView.as_view(), name='login_url'),
    path('logout/', login_required(views.UserLogoutView.as_view()), name='logout_url'),
    path('verify/<int:id>/<str:code>/', views.EmailVerifyView.as_view(), name='email_verification_url'),
    path('profile/<int:pk>/', login_required(views.UserProfileView.as_view()), name='profile_url'),
    path('products/add_to_cart/<int:id>', login_required(views.AddToCartView.as_view()), name='add_to_cart_url'),
    path('products/remove_from_cart/<int:id>', login_required(views.RemoveFromCartView.as_view()),
         name='remove_from_cart_url'),
]
