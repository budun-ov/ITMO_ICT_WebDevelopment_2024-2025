from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Car
from .models import Owner
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'passport_number', 'address', 'nationality')

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['last_name', 'first_name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})  # Виджет для ввода даты
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'brand', 'model', 'color']
