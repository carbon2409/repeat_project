from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import CustomUser, EmailVerificationModel
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from datetime import timedelta
from django.utils.timezone import now
import uuid


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                                                       'placeholder': 'Введите имя пользователя',
                                                                                       'required': True,
                                                                                       }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'class': 'form-control py-4',
        'required': True
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(label='Имя',
                           widget=forms.TextInput(attrs={'placeholder': 'Введите имя',
                                                         'class': 'form-control py-4',
                                                         'required': True,
                                                         'type': 'text'}))
    surname = forms.CharField(label='Фамилия',
                              widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию',
                                                            'class': 'form-control py-4',
                                                            'required': False,
                                                            'type': 'text'}))
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя',
                                                             'class': 'form-control py-4',
                                                             'required': True,
                                                             'type': 'text',
                                                             'aria-describedby': 'usernameHelp'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Введите email',
                                                            'class': 'form-control py-4',
                                                            'required': True,
                                                            'type': 'email',
                                                            'aria-describedby': 'emailHelp'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль',
                                                                  'class': 'form-control py-4',
                                                                  'required': True,
                                                                  'type': 'password'}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль еще раз',
                                                                  'class': 'form-control py-4',
                                                                  'required': True,
                                                                  'type': 'password'}))

    def save(self, commit=True):
        user = super().save(commit=True)
        email_verification = EmailVerificationModel.objects.create(user=user,
                                                                   code=uuid.uuid4(),
                                                                   expired_at=now()+timedelta(hours=48),
                                                                   created_at=now())
        email_verification.send_verification_email()
        return user


    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={'type': 'text',
                                                                      'class': 'form-control py-4',
                                                                      'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={'type': 'text',
                                                                             'class': 'form-control py-4',
                                                                             'placeholder': 'Введите фамилию'}))
    username = forms.CharField(label='Имя пользователя', required=True, widget=forms.TextInput(attrs={'type': 'text',
                                                                                                      'class': 'form-control py-4',
                                                                                                      'readonly': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'type': 'email',
                                                                           'class': 'form-control py-4',
                                                                           'readonly': True}))
    avatar = forms.ImageField(label='Изменить фото профиля', widget=forms.FileInput(attrs={#'class': 'custom-file-input',
                                                                              'size': 50,
                                                                              'required': False}))

    class Meta:
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']
        model = CustomUser
