from django.urls import path
from . import views

urlpatterns =[
    path('',views.updateItem,name='updateitem'),
    path('cart', views.cart, name='cart'),
    path('shipping',views.shippingaddress,name='shipping'),
    path('payment',views.pay_page,name='pay_page'),
    path('deletecart/<int:id>',views.deletecart,name='deletecart'),
    path('razorpay',views.razorpay,name='razorpay'),
    path('success',views.success,name='success'),
    path('addressSelect/<int:id>',views.addressSelect,name='addressSelect'),
    path('guest',views.guest,name='guest'),

]