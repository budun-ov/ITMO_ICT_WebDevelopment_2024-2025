from django import forms
from django.contrib.auth.models import User
from .models import Racer


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }


class RacerProfileForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['full_name', 'team_name', 'description', 'car_description', 'experience', 'class_type', 'birth_date',
                  'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'team_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Team Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            }),
            'car_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Car Description'
            }),
            'experience': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'class_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }
