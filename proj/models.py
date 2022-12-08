from django.db import models

from account.models import Account


# Create your models here.
class Category(models.Model):
    category_id             = models.AutoField
    category_name           = models.CharField(max_length=100)
    # sub                     = models.ManyToManyField(SubCategory)
    offer_name              = models.CharField(max_length=100,null=True,blank=True)
    category_offer          = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.category_name
    @property    
    def filtered(self):
        sub = self.subcategory_set.all()
        return sub
    @property
    def products(self):
        product = self.product_set.all()
        return product


class SubCategory(models.Model):
    sub_name                = models.CharField(max_length=50)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_name
    @property
    def Products(self):
        product = self.product_set.all()
        return product

        


class Product(models.Model):
    product_id              = models.AutoField
    product_name            = models.CharField(max_length=50)
    price                   = models.BigIntegerField()
    desc                    = models.CharField(max_length=600)
    quantity                = models.IntegerField(default=0)
    image1                  = models.ImageField(upload_to="media/images")
    image2                  = models.ImageField(upload_to="media/images",null=True,blank=True)
    image3                  = models.ImageField(upload_to="media/images",null=True,blank=True)
    image4                  = models.ImageField(upload_to="media/images",null=True,blank=True)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub                     = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    offer_name              = models.CharField(max_length=100,null = True,blank=True)
    product_offer           = models.IntegerField(null = True,blank=True,default=0)
    


    def __str__(self):
        return self.product_name



    @property
    def get_product_price(self):
        if self.product_offer == 0 and self.category.category_offer==0:
            product_price = self.price
            
        elif self.product_offer < self.category.category_offer:
            product_price = self.price - float((self.price * self.category.category_offer)/100)
            offer = self.category.category_offer
        else:
            product_price = self.price - float((self.price * self.product_offer)/100)
            offer = self.product_offer
        product_price = float(product_price)
        return product_price
    
    @property
    def offer(self):
        if self.product_offer == 0 and self.category.category_offer==0:
            offer = self.product_offer
        elif self.product_offer < self.category.category_offer: 
            offer = self.category.category_offer
        else:
            offer = self.product_offer
        return offer









class Order(models.Model):

    account                 = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    date_order              = models.DateTimeField(auto_now_add=True)
    complete                = models.BooleanField(default=False, null=True, blank=False)
    transaction_id          = models.CharField(max_length=200, null=True,blank=False)
    tracking_no             = models.CharField(max_length=150, null=True,blank=False)
    session_id              = models.CharField(max_length=500,null=True, blank=True)

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
    order                   = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity                = models.IntegerField(default=0, null=True, blank=True)
    discound                = models.IntegerField(default=0,null=True, blank=True)
    session_id              = models.CharField(max_length=500,null=True, blank=True)

    def __str__(self):
        return str(self.product.id)

    @property
    def get_total(self):
        total = self.product.get_product_price * self.quantity
        return total
    @property
    def get_cart_items(self):

        total =0
        total = total + self.quantity
        return total
    @property
    def get_cart_total(self):
        total = 0
        total = total + self.get_total
        return total


class ShippingAddress(models.Model):
    account                 = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    order                   = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    address                 = models.CharField(max_length=200, null=True)
    city                    = models.CharField(max_length=200, null=True)
    state                   = models.CharField(max_length=200, null=True)
    pincode                 = models.CharField(max_length=10, null=True)
    phone                   = models.CharField(max_length=30)
    email                   = models.CharField(max_length=100,null=True,blank=True)
    name                    = models.CharField(max_length=100,null=True,blank=True)
    


class BannerManagement(models.Model):
    image              = models.ImageField(upload_to="media/images")
    name               = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.name


        




