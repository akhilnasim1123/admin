from django.contrib import admin
from django.urls import path, include

from account import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registration_view, name='register'),
    path('log/',views.user_loginpage, name='loginpage'),
    path('logi',views.login,name='login'),

]
