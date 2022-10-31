from django.contrib import admin
from django.urls import path, include

from proj import views

urlpatterns = [
    path('', views.admin_log, name='admin_log'),
    path('admin-auth', views.admin_auth, name='admin_auth'),
    path('admin-page', views.admin_page, name='admin_page'),
    path('admin-user', views.admin_user, name='admin_user'),
    path('block/<int:user_id>',views.block,name='block'),
    path('unblock/<int:user_id>',views.unblock,name='unblock'),
    path('product',views.product,name='product')

]
