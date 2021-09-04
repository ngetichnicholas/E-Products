from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import User
from .models import *
from django.core.validators import MinLengthValidator


class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
                                widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=("full_name","username","email","password1","password2")
        help_texts = {
            "username":None,
        }

