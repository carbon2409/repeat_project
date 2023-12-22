from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserAuthenticationForm(AuthenticationForm):
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

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
