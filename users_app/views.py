from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser
from django.contrib import messages, auth


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    model = CustomUser
    success_url = reverse_lazy('users_app:login_url')
    template_name = 'users_app/register.html'
    context_object_name = 'form'

    def post(self, request, *args, **kwargs):
        messages.success(request, message='Вы успешно зарегистрировались')
        response = super().post(request)
        return response

# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users_app:login_url'))
#         return render(request, 'users_app/register.html', {'form': form})
#     else:
#         return render(request, 'users_app/register.html', context={'form': UserRegistrationForm()})


class UserProfileView(UpdateView):
    model = CustomUser
    form_class = UserChangeForm
    template_name = 'users_app/profile.html'
    success_url = reverse_lazy('users_app:profile_url')
    context_object_name = 'form'


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users_app/login.html'
    context_object_name = 'form'
