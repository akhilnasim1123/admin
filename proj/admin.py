from django.contrib import admin

from django.contrib import admin
from django.contrib.auth import get_user_model

from proj.models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(ShippingAddress)
admin.site.register(BannerManagement)


