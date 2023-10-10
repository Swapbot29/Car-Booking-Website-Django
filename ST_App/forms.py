from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Car, User_booking

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = User_booking
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')