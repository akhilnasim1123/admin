from django.urls import path
from . import views

urlpatterns =[
    path('',views.updateItem,name='updateitem'),
    path('cart', views.cart, name='cart'),

]