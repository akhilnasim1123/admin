from django.urls import path
from . import views

urlpatterns =[
    path('',views.updateItem,name='updateitem'),
    path('cart', views.cart, name='cart'),
    path('shipping',views.shoppingaddress,name='shipping'),
    path('payment/<int:id>',views.pay_page,name='pay_page'),

]