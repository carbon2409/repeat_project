from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserLogoutView
from django.contrib.auth.decorators import login_required
app_name = 'users_app'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration_url'),
    path('login/', UserLoginView.as_view(), name='login_url'),
    path('logout/', login_required(UserLogoutView.as_view()), name='logout_url'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile_url'),
]