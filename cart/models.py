from django.db import models

from account.models import *
from coupen.models import Coupen
from proj.models import *

# Create your models here.

class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat()
        return ''


class OrderedItems(models.Model):
    status_choices ={
        ('pending','pending'),
        ('out for shipping','out for shipping'),
        ('completed','completed'),

    }
    product                     = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    account                     = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    order                       = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    status                      = models.CharField(max_length=20,choices=status_choices, default='pending')
    shippingaddress             = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE,blank=True,null=True)
    payment                     = models.CharField(max_length=120,null=True)
    quantity                    = models.IntegerField(blank=True, null=True)
    total_price                 = models.CharField(max_length=200,blank=True,null=True)
    price                       = models.CharField(max_length=40,blank=True, null=True)
    coupen_applied              = models.CharField(max_length=100)
    payment_id                  = models.CharField(max_length=100,blank=True,null=True)
    message                     = models.TextField(null=True,blank=True)
    tracking_no                 = models.CharField(max_length=150,null=True)
    ordered                     = models.DateTimeField(auto_now_add=True)
    coupen                      = models.ForeignKey(Coupen,on_delete=models.SET_NULL,blank=True,null=True)




   

   
    def __str__(self):
        return str(self.account)



    def get_total(self):
        total = self.product.price * self.quantity
        return total



    

