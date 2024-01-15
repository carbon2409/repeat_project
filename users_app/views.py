from urllib import request
from .common.mixins import UserMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, UserAuthenticationForm, UserProfileForm
from .models import CustomUser, EmailVerificationModel, BasketModel
from products_app.models import ProductsModel
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


class UserProfileView(UserMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users_app/profile.html'
    context_object_name = 'form'
    title = 'Профиль'

    def get_success_url(self):
        return reverse_lazy('users_app:profile_url', kwargs={'pk': self.object.id})


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'users_app/login.html'
    context_object_name = 'form'


class UserLogoutView(LogoutView):
    template_name = 'index.html'


class EmailVerifyView(TemplateView):
    template_name = 'users_app/email_verification.html'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['id'])
        email_verify_obj = EmailVerificationModel.objects.filter(code=self.kwargs.get('code'),
                                                                 user=user)
        if email_verify_obj.exists() and not email_verify_obj.first().is_expired():
            user.is_verified = True
            user.save()
            return render(request, 'users_app/email_verification.html')
        else:
            return HttpResponseRedirect('<h1>Нет такого</h1>')


class AddToCartView(TemplateView):
    template_name = 'product_app/products.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        product = ProductsModel.objects.get(id=kwargs['id'])
        items_queryset = BasketModel.objects.filter(product=product)
        if items_queryset.exists():
