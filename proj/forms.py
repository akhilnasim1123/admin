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

# class CategoryOfferForm(forms.ModelForm):
#     class Meta:
#         model= CategoryOffer
#         fields = ['category','categoryOffer']
#         widgets = {
#             'category': Select(attrs={
#             'class': "form-control",
#             'style': 'max-width: 300px;margin-left:15%;',
#             }),
#             'categoryOffer':NumberInput(attrs={
#             'class':'form-control',
#             'style': 'max-width: 300px;margin-left:15%;',
#             })
#         }
#     def clean(self):
#         categoyOffer = self.cleaned_data.get("categoryOffer")
#         if categoyOffer > 100:
#             raise ValidationError('Entered Number Greater than 100%')


# class ProductOfferForm(forms.ModelForm):
#     class Meta:
#         model= ProductOffer
#         fields = ['product','productOffer']
#         widgets = {
#             'product': Select(attrs={
#             'class': "form-control",
#             'style': 'max-width: 300px;margin-left:15%;',
#             }),
#             'productOffer':NumberInput(attrs={
#             'class':'form-control',
#             'style': 'max-width: 300px;margin-left:15%;',
#             })
#         }
        
#     def clean(self):
#         productOffer = self.cleaned_data.get("productOffer")
#         if productOffer > 100:
#             raise ValidationError('Entered Number Greater than 100%')

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




        





