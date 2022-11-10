import random

from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
import json

from django.http import JsonResponse
from django.urls import reverse

from account.models import Account
from proj.models import Product, Order, OrderItems, ShippingAddress


def cart(request):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer')
        order = Order.objects.get(account=customer, complete=False)

        items = order.orderitems_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        print('in else')

    context = {'items': items, 'order': order}
    return render(request, 'cart/cart.html', context)


def shoppingaddress(request):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']

        print('in else')

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shipping/shipping.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)
    account = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(account=account, complete=False)

    orderItem, created = OrderItems.objects.get_or_create(order=order, product=product)
    print('hr')
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was Added', safe=False)


def pay_page(request, id):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']
        print('in else')

    if request.method == "POST":
        add = ShippingAddress()
        add.address = request.POST.get('address')
        add.city = request.POST.get('city')
        add.state = request.POST.get('state')
        add.pincode = request.POST.get('pincode')
        add.account = customer
        track_no = order.account.name+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=track_no)is None:
            track_no = order.account.name + str(random.randint(1111111, 9999999))
        add.tracking_no = track_no

        print('pay like a dog')
        if add.address == '' or add.city == '' or add.state == '' or add.pincode == '':
            messages.error(request,'These Fields are Required')
            return redirect('shipping')
        trackno = customer+str
        add.save()
        neworder= Order.objects
        context = {'cartItems': cartItems}
        return render(request, 'Payment/payment.html')
