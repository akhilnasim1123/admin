from django.urls import path
from . import views

urlpatterns =[
    path('',views.coupenAdimin,name='coupen'),
    path('createCoupen',views.createCoupen,name='createCoupen'),
    path('trash/<int:id>',views.trashCoupen,name='trashCoupen'),
]