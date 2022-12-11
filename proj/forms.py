from django import forms
from django.forms import FileInput, ImageField, NumberInput, Select, TextInput, ValidationError
from .models import *


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'desc','quantity', 'image1', 'image2', 'image3', 'image4', 'category', 'sub']


class SubForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['sub_name', 'category']

class BannerForm(forms.ModelForm):
    class Meta:
        model = BannerManagement
        fields = ['name','image']
        
class ProductEditForm(forms.ModelForm):
    class Meta:
        model= Product
        fields= '__all__'
        widgets = {
                    'product_name': TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'price':NumberInput(attrs={
                    'class':'form-control',
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'desc': TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'quantity':NumberInput(attrs={
                    'class':'form-control',
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                     'image1': FileInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'image2': FileInput(attrs={
                    'class':'form-control',
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'image3': FileInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'image4': FileInput(attrs={
                    'class':'form-control',
                    'style': 'max-width: 300px;margin-left:15%;',
                    }), 
                    'category': Select(attrs={
                    'class':'form-control',
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'sub':  Select(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),
                    'offer_name': TextInput(attrs={
                    'class':'form-control',
                    'style': 'max-width: 300px;margin-left:15%;',
                    }),    
                    'product_offer': NumberInput(attrs={
                    'class':'form-control',
                    'style': 'max-width: 300px;margin-left:15%;',
                    })                                                                    
                }




        





