from django import forms
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




