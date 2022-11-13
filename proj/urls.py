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
    path('product',views.product,name='product'),
    path('logout', views.logout, name='logout'),
    path('product-list',views.product_list,name='product_list'),

    path('category', views.category_view, name='category_view'),
    path('add-category', views.category, name='category'),
    path('editpage/<int:id>/',views.editpage,name='editpage'),
    path('editdata/<int:id>/',views.editData,name='editData'),
    path('deletedata/<int:id>/',views.deleteData,name='deleteData'),
    path('search', views.searchdata, name='searchdata'),
    path('editcatpage/<int:cat_id>/',views.editcatpage,name='editcatpage'),
    path('editCat/<int:cat_id>/',views.editCat,name='editCat'),
    path('deleteCat/<int:id>/',views.deleteCat,name='deleteCat'),
    path('search', views.searchCat, name='searchCat'),
    path('test', views.test, name='test'),



    path('subcategory',views.sub_category,name='sub_category'),
    path('add-sub',views.sub_cat,name='sub_cat'),
    path('delete-sub/<int:id>',views.deleteSub,name='deleteSub'),
    path('editSub/<int:id>',views.editSubpage,name='editSubpage'),
    path('orders',views.order_list,name='order_list'),
    path('cancel/<int:id><int:val>',views.cancel,name='cancel'),
    path('orders-details/<int:id>',views.order_view,name='order_view'),
    path('banner',views.banner,name='banner')


]
