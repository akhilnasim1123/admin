from django.urls import path
from . import views

urlpatterns =[
    path('',views.updateItem,name='updateitem'),
    path('cart', views.cart, name='cart'),
    path('shipping',views.shoppingaddress,name='shipping'),
    path('payment',views.pay_page,name='pay_page'),
    path('delete/<int:id>/<int:value>',views.deletecart,name='deletecart')

]