from django.db import models

# Create your models here.


class Coupen(models.Model):
    coupen = models.CharField(max_length=10)
    price =  models.CharField(max_length=200,default='200')
    minimum_price = models.CharField(max_length=100,default='500')
    maximum_price = models.CharField(max_length=100,default='5000')

    def __str__(self):
        return self.coupen
