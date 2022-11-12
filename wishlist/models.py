from django.db import models

from account.models import Account
from proj.models import *

# Create your models here.


class Wishlist(models.Model):
    account                    = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    product                     = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)

