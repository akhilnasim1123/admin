# Create your views here.
import json
import random

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from account.models import Account
from account.views import login_page
from cart.models import OrderedItems
from proj.models import Order, OrderItems, Product, ShippingAddress


def cart(request):
    
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer')
        order                   = Order.objects.get(account=customer, complete=False)
        items                   = order.orderitems_set.all()
        cartItems               = order.get_cart_items
    elif request.user is None:
        order                   = []
        items                   = []
        cartItems               = []

    
    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'cart/cart.html', context)

@login_required(login_url=login_page)
def shoppingaddress(request):
    if request.user.is_authenticated:
        print('authenticated')
        customer                    = request.user
        order                       = Order.objects.get(account=customer, complete=False)
        items                       = order.orderitems_set.all()
        cartItems                   = order.get_cart_items
        address                     = ShippingAddress.objects.filter(account=customer)

    else:
        items                       = []
        order                       = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems                   = order['get_cart_items']
        address                     = []

        print('in else')

    context = {'items': items, 'order': order, 'cartItems': cartItems,'address':address}
    return render(request, 'shipping/shipping.html', context)


def updateItem(request):
    data                                = json.loads(request.body)
    productId                           = data['productId']
    action                              = data['action']
    print('Action:', action)
    print('productId:', productId)
    account                             = request.user
    product                             = Product.objects.get(id=productId)
    order, created                      = Order.objects.get_or_create(account=account, complete=False)

    orderItem, created                  = OrderItems.objects.get_or_create(order=order, product=product)
    print('hr')
    if action == 'add':
        orderItem.quantity              = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity              = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was Added', safe=False)

@login_required(login_url=login_page)
def pay_page(request):
    if request.user.is_authenticated:
        print('authenticated')
        customer                        = request.user
        order                           = Order.objects.get(account=customer, complete=False)
        items                           = order.orderitems_set.all()
        cartItems                       = order.get_cart_items
    else:
        return redirect(login_page)

    if request.method == "POST":

        user_order                      = OrderedItems()
        add                             = ShippingAddress()
        orItems                         = OrderItems.objects.get(order=order)
        add.address                     = request.POST.get('address')
        add.city                        = request.POST.get('city')
        add.state                       = request.POST.get('state')
        add.pincode                     = request.POST.get('pincode')
        add.account                     = customer
        add.order                       = order
        order.payment_choices           = request.POST.get('cash_on_delivery')

        track_no = order.account.first_name + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=track_no) is None:
            track_no = 'akhil' + str(random.randint(1111111, 9999999))

        add.tracking_no                 = track_no

        if add.address == '' or add.city == '' or add.state == '' or add.pincode == '':
            messages.error(request, 'These Fields are Required')
            return redirect('shipping')

        user_order.account              = customer
        user_order.order                = order
        user_order.orderitems           = orItems
        user_order.shippingaddress      = add
        user_order.payment              = order.payment_choices
        user_order.quantity             = orItems.quantity
        user_order.price                = order.get_cart_total
       
        add.save()
        user_order.save()

        prod_qunt                       = Product.objects.get(id=orItems.product.id)
        prod_qunt.quantity              = user_order.quantity - prod_qunt.quantity
        prod_qunt.save()


        context = {'cartItems': cartItems}
        return render(request, 'shipping/success.html',context)


def deletecart(request,id,value):

    delete                              = OrderItems.objects.get(id=id)

    delete.delete()

    if value == 1:
        return redirect(cart)
    else:
        return redirect(shoppingaddress)

    

