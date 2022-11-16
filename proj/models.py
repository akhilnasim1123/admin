from django.db import models

from account.models import Account


# Create your models here.
class Category(models.Model):
    category_id             = models.AutoField
    category_name           = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_name                = models.CharField(max_length=50)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_name


class Product(models.Model):
    product_id              = models.AutoField
    product_name            = models.CharField(max_length=50)
    price                   = models.BigIntegerField()
    desc                    = models.CharField(max_length=600)
    quantity                = models.IntegerField(default=0)
    image1                  = models.ImageField(upload_to="media/images")
    image2                  = models.ImageField(upload_to="media/images")
    image3                  = models.ImageField(upload_to="media/images")
    image4                  = models.ImageField(upload_to="media/images")
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub                     = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    # Create your models here.


class Order(models.Model):

    account                 = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    date_order              = models.DateTimeField(auto_now_add=True)
    complete                = models.BooleanField(default=False, null=True, blank=False)

    transaction_id          = models.CharField(max_length=200, null=True)
    tracking_no             = models.CharField(max_length=150, null=True)


    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

    
    @property
    def get_cart_items(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


class OrderItems(models.Model):
    account                 = models.ForeignKey(Account,on_delete=models.CASCADE, blank=True, null=True)
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    order                   = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity                = models.IntegerField(default=0, null=True, blank=True)
    date_added              = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    account                 = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    order                   = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address                 = models.CharField(max_length=200, null=True)
    city                    = models.CharField(max_length=200, null=True)
    state                   = models.CharField(max_length=200, null=True)
    pincode                 = models.CharField(max_length=10, null=True)
    phone                   = models.CharField(max_length=30)



class BannerManagement(models.Model):
    image              = models.ImageField(upload_to="media/images")
    name               = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.name
        
        




