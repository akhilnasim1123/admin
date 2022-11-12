from django.db import models

from account.models import *
from proj.models import *

# Create your models here.


class OrderedItems(models.Model):
    status_choices ={
        ('accepted','accepted'),
        ('pending','pending')
    }
    account                     = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    order                       = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    orderitems                  = models.ForeignKey(OrderItems,on_delete=models.SET_NULL,blank=True,null=True)
    status                      = models.CharField(max_length=20,choices=status_choices, default='pending')
    shippingaddress             = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE,blank=True,null=True)
    payment                     = models.CharField(max_length=20,blank=True, null=True)
    quantity                    = models.CharField(max_length=40,blank=True, null=True)
    active                      = models.CharField(max_length=20,default='ordered')
    price                       = models.CharField(max_length=40,blank=True, null=True)


    def __str__(self):
        return str(self.account)


