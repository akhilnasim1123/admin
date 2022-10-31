from django.contrib import admin

from django.contrib import admin
from django.contrib.auth import get_user_model

from proj.models import Product

admin.site.register(Product)