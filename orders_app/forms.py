from django import forms
from .models import OrderModel
from users_app.models import CustomUser

class CreateOrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Введите фамилию'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Введите email'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Россия, Москва, ул. Мира, дом 6'}))

    class Meta:
        model = OrderModel
        fields = ('first_name', 'last_name', 'email', 'address')
