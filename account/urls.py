from django.contrib import admin
from django.urls import path, include

from account import views

urlpatterns = [
    path('',views.landing_page,name='landing_page'),
    path('home/', views.home, name='home'),
    path('register/', views.registration_view, name='register'),
    path('log/',views.user_loginpage, name='loginpage'),
    path('logi',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('product_view/<int:id>',views.product_view,name='product_view'),

    path('otp-login',views.otp_login,name='otp_login'),
    path('otp-login-page',views.otp_login_page,name='otp_login_page'),
    path('enter-otp',views.enter_otp,name='enter_otp'),
    path('verify-otp',views.verify_otp,name='verify_otp'),


]
