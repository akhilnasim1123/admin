import random
from turtle import numinput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import EmailInput, NumberInput, PasswordInput, TextInput
from phonenumber_field.formfields import PhoneNumberField
import account
from account.models import Account
from coupen.models import Coupen


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')


    class Meta:
        model = Account
        fields = ('first_name','last_name','phone','email', 'password1', 'password2')
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;margin-left:15%;color:white',
                'placeholder': 'First Name'
                }),
            'last_name':TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;margin-left:15%;color:white',
                'placeholder': 'Last Name'
            }),
            'phone': TextInput(attrs={
            'class': "form-control", 
            'style': 'max-width: 300px;margin-left:15%;color:white',
            'placeholder': 'Phone'
            }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;margin-left:15%;color:white',
                'placeholder': 'Email'
            }),
            'password1': PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;margin-left:15%;color:white',
                'placeholder': 'Password'
            }),
            'password2': PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;margin-left:15%;color:white',
                'placeholder': 'Confirm Password'
            }),



        }



class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')


    class Meta:
        email = Account
        fields = ('email', 'password')

class UserEditForm(forms.ModelForm):
     class Meta:
        model=Account
        fields = ('first_name','last_name','email','phone')
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;margin-left:15%;',
                'placeholder': 'First Name'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;margin-left:15%;',
                'placeholder': 'Email'
                }),
            'last_name': TextInput(attrs={
            'class': "form-control", 
            'style': 'max-width: 300px;margin-left:15%;',
            'placeholder': 'Last Name'
            }),
            'phone': TextInput(attrs={
            'class': "form-control", 
            'style': 'max-width: 300px;margin-left:15%;',
            'placeholder': 'Last Name'
            })


        }


class CoupenForm(forms.ModelForm):
     class Meta:
        model=Coupen
        fields = ('coupen','price','minimum_price','maximum_price')
        widgets = {
            'coupen': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;margin-left:15%;',
                'placeholder': 'Coupen'
                }),
            'price': NumberInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;margin-left:15%;',
                'placeholder': 'Price'
                }),
            'minimum_price': NumberInput(attrs={
            'class': "form-control", 
            'style': 'max-width: 300px;margin-left:15%;',
            'placeholder': 'Minimum Price'
            }),
            'maximum_price': NumberInput(attrs={
            'class': "form-control", 
            'style': 'max-width: 300px;margin-left:15%;',
            'placeholder': 'Maximum Price'
            })


        }


