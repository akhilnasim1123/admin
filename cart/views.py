from django.shortcuts import render

# Create your views here.
import json

from django.http import JsonResponse

from account.models import Account
from proj.models import Product, Order, OrderItems


def cart(request):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        print('in else')

    context = {'items': items, 'order': order}
    return render(request, 'cart/cart.html', context)


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
