from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, AuthenticationForm

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users_app:login_url')
    template_name = 'users_app/register.html'
    context_object_name = 'form'


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('main_page_url')
    template_name = 'users_app/login.html'
