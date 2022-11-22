# Create your views here.
import json
import random
from random import randint

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
        order, created = Order.objects.get_or_create(
            account=customer, complete=False)
        items = OrderItems.objects.all().order_by('id')
        # for i in items:
        #     print(i.get_total)
        cartItems = order.get_cart_items
        itm = OrderItems.objects.filter(account=customer)

        # count = itm.product.quantity
        # price= itm.product.price
        # print(count)
        for i in itm:
            count = i.product.quantity
            price = i.product.price
            pro_id = i.product.id
            print(count)
            print(price)
            print(pro_id)

        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'cart/cart.html', context)
    elif request.user is None:
        order = []
        items = []
        cartItems = []
    order = []
    items = []
    cartItems = []

    messages.error(request, 'Cart is Empty')
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart/cart.html', context)


@login_required(login_url=login_page)
def shoppingaddress(request):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
        address = ShippingAddress.objects.filter(
            account=customer).order_by('id')

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']
        address = []

        print('in else')
    # itm = OrderItems.objects.filter(account=customer)
    # count =itm.product.quantity
    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'address': address}
    return render(request, 'shipping/shipping.html', context)


def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)
    account = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        account=account, complete=False)

    orderItem, created = OrderItems.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        if product.quantity <= 0 and orderItem.quantity > product.quantity:
            messages.error(request, 'Out of Stock')
        else:
            orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        if orderItem.quantity <= 0:
            messages.error(request, '')
        else:
            orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    return JsonResponse('Item was Added', safe=False)


@login_required(login_url=login_page)
def pay_page(request):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
    else:
        return redirect(login_page)

    if request.method == "POST":
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        account = customer
        order = order

        track_no = str(account.first_name)+str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=track_no) is None:
            track_no = str(account.first_name)+str(random.randint(1111111, 9999999))

        order.tracking_no = track_no
        order.save()

        if address == '' or city == '' or state == '' or pincode == '':
            messages.error(request, 'These Fields are Required')
            return redirect('shipping')
        orItems = OrderItems.objects.filter(order=order)


        #     messages.error(request, 'this address already exist')
        # else:
        add = ShippingAddress() 
        add.address = address
        add.city = city
        add.state = state
        add.pincode = pincode
        add.account = customer
        add.order = order
        addrs = ShippingAddress.objects.filter(
            address=address, city=city, account=account).exists()
        if addrs:
            address_get = ShippingAddress.objects.get(address=address,city=city,account=account)
            add = address_get
        else:
            add_count = ShippingAddress.objects.filter(
                account=customer).count()
            if add_count > 4:
                dele = ShippingAddress.objects.filter(
                    account=customer).reverse()
                print(dele)
                print(add_count)
                dele.delete()
                add.save()
            else:
                add.save()

        saddress = add
        
        user_order = OrderedItems()

        for item in orItems:

            orItemss = item
            prod_qunt = Product.objects.get(id=orItemss.product.id)

            user_order.account = customer
            user_order.order = order
            user_order.shippingaddress = saddress
            user_order.tracking_no = track_no
            user_order.quantity = orItemss.quantity
            prod_qunt.quantity -= user_order.quantity
            user_order.price = order.get_cart_total
            user_order.product = prod_qunt
            user_order.payment_id = request.POST.get('payment_id')
            user_order.payment = request.POST.get('payment_mode')

            user_order.save()

            prod_qunt.save()

        product = OrderItems.objects.filter(order=order)
        product.delete()

        payMode = request.POST.get('payment_mode')
        if (payMode == 'Paid by Razorpay' or payMode == 'Paid by Paypal'):
            return JsonResponse({"status": "success"})

        context = {'cartItems': cartItems}
        return render(request, 'shipping/success.html', context)
    order = Order.objects.get(account=customer, complete=False)
    items = order.orderitems_set.all()
    cartItems = order.get_cart_items
    context = {'cartItems': cartItems}
    return render(request, 'shipping/success.html', context)


def deletecart(request, id, value):

    delete = OrderItems.objects.get(id=id)

    delete.delete()

    if value == 1:
        return redirect(cart)
    else:
        return redirect(shoppingaddress)


def razorpay(request):
    cartitems = Order.objects.get(account=request.user)
    total_price = cartitems.get_cart_total

    return JsonResponse({
        'total_price': total_price
    })


def success(request):
    return render(request, 'shipping/success.html')

    #     OrderedItems.objects.create(

    # order=order,
    # product=item.product,
    # price= order.get_cart_total,
    # quantity             = item.quantity,

    # tracking_no     = order.tracking_no,
    # shippingaddress = add,

    # )
