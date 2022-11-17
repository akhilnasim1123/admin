from django.db import models

from account.models import *
from proj.models import *

# Create your models here.


class OrderedItems(models.Model):
    status_choices ={
        ('pending','pending'),
        ('out for shipping','out for shipping'),
        ('completed','completed'),

    }
    product                     = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    account                     = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    order                       = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    orderitems                  = models.ForeignKey(OrderItems,on_delete=models.SET_NULL,blank=True,null=True)
    status                      = models.CharField(max_length=20,choices=status_choices, default='pending')
    shippingaddress             = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE,blank=True,null=True)
    payment                     = models.CharField(max_length=120,null=True)
    quantity                    = models.IntegerField(blank=True, null=True)
    active                      = models.CharField(max_length=20,default='ordered')
    price                       = models.CharField(max_length=40,blank=True, null=True)
    payment_id                  = models.CharField(max_length=100,blank=True,null=True)
    message                     = models.TextField(null=True)
    tracking_no                 = models.CharField(max_length=150,null=True)


   
   
    def __str__(self):
        return str(self.account)


