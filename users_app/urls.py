from django.urls import path
from .views import UserRegistrationView, UserLoginView

app_name = 'users_app'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration_url'),
    path('login/', UserLoginView.as_view(), name='login_url'),
]