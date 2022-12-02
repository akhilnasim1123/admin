# Create your views here.
import json
import random
from random import randint
import uuid

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from account.models import Account
from account.views import login_page


from cart.models import OrderedItems
from coupen.models import Coupen
from invoice.views import guest
from proj.models import  Order, OrderItems, Product,  ShippingAddress

#guest user func


def cart(request):

 

    if cart:
        print("Guest cart items are")

    else:
        print("Nop!")
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer') 
        order = Order.objects.filter(
            account=customer, complete=False)
        items = OrderItems.objects.filter(account=customer)
        print(items)     
        # for i in items:
        #     print(i.get_total)
        for i in order:
            cartItems = i.get_cart_items
        # items = OrderItems.objects.filter(account=customer)
        product_id =0
        # count = itm.product.quantity
        # price= itm.product.price
        # print(count)
        
            
       
        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'cart/cart.html', context)
    else:
        user = guest(request)
        order = Order.objects.filter(
            session_id=user, complete=False)
        items = OrderItems.objects.filter(session_id=user) 

        print("The items in cart are",items)

        cartItems=0
        for  i  in order:
            cartItems = i.get_cart_items
        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'cart/cart.html', context)

@login_required(login_url='login_page')
def shippingaddress(request):
    if request.user.is_authenticated:
        discound = 0
        print('authenticated')
        customer = request.user
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
        address = ShippingAddress.objects.filter(
            account=customer).order_by('id')
        coupen = None
        if request.method == 'POST':
            print('coupen')
            coupen = request.POST.get('coupen')
            print(coupen)
            coupen_check = Coupen.objects.filter(coupen=coupen).exists()
            if coupen_check: 
                coupen_discound = Coupen.objects.get(coupen=coupen)
                user = Account.objects.get(id=customer.id)
                cart = Order.objects.get(account=user)
                print(cart.get_cart_total)
                # items = OrderItems.objects.filter(cart=cart)
                if int(coupen_discound.minimum_price) <= int(cart.get_cart_total) and int(coupen_discound.maximum_price) >= int(cart.get_cart_total):
                    print('entered')
                    discound =  cart.get_cart_total - int(coupen_discound.price) 
                    print(discound)
                    messages.success(request,'coupen applied')
                else:
                    messages.error(request,'you are not eligible for this coupen..!')


    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']
        address = []

        print('in else')
    # itm = OrderItems.objects.filter(account=customer)
    # count =itm.product.quantity

    if discound is not None:
            context = {'items': items, 'order': order,'coupen':coupen,
               'cartItems': cartItems,'discound':discound, 'address': address}
    else:
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
    
    if request.user.is_authenticated:
        print('asdjfaidfhaousdgiviufah')
        order, created = Order.objects.get_or_create(
            account=account, complete=False)
        orderItem, created = OrderItems.objects.get_or_create(
        order=order, product=product,account=account)
        print(orderItem)
    else:
        print('sjkdfajhkjhbkhjhggjgg')
        guestUser = guest(request) 
        order, created = Order.objects.get_or_create(
           session_id=guestUser, complete=False)

        orderItem, created = OrderItems.objects.get_or_create(
        product=product,order=order,session_id=guestUser)

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
    # data = request.POST['city']

    # data = request.POST['city']

    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        idid = Account.objects.get(id=customer.id)
        print(idid,'thisn is user id')
        
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
    else:
        return redirect(login_page)

    if request.method == "POST":
        value = request.POST.get('butt')
        discound_or_not = request.POST.get('check')
        coupen = request.POST.get('coupens')
        if coupen is not None:
            coupen = Coupen.objects.get(coupen=coupen)
        else:
            coupen = None
        if discound_or_not == '1':
            discounded = 'Yes'
        else:
            discounded = 'No'
        address = request.POST.get('addresses')
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
            user_order = OrderedItems()
            orItemss = item
            prod_qunt = Product.objects.get(id=orItemss.product.id)
            user_order.account = customer
            user_order.order = order
            user_order.shippingaddress = saddress
            user_order.tracking_no = track_no
            user_order.quantity = orItemss.quantity
            prod_qunt.quantity -= user_order.quantity
            user_order.coupen_applied = discounded
            user_order.total_price = user_order.quantity * prod_qunt.price
            user_order.price = item.get_total
            user_order.coupen = coupen
            user_order.product = prod_qunt
            user_order.discound = user_order.product.price-user_order.product.get_product_price
            user_order.payment_id = request.POST.get('payment_id')
            user_order.payment = request.POST.get('payment_mode')

            user_order.save()

            prod_qunt.save()

        product = OrderItems.objects.filter(order=order)
        product.delete()

        payMode = request.POST.get('payment_mode')
        if (payMode == 'Paid by Razorpay' or payMode == 'Paid by Paypal' or payMode == 'COD'):
            return JsonResponse({"status": "success"})
        context = {'cartItems': cartItems}
        return render(request, 'shipping/success.html', context)
    order = Order.objects.get(account=customer, complete=False)
    items = order.orderitems_set.all()
    cartItems = order.get_cart_items
    context = {'cartItems': cartItems}
    return render(request, 'shipping/success.html', context)




def deletecart(request, id):
    print('asdhfnkjahsdfkahsfdkhashhafdskhaksfhakshdfkashhasfdhkash')
    delete = OrderItems.objects.get(id=id)

    delete.delete()
    total = delete.order.get_cart_total
    count = delete.order.get_cart_items
    values = {
        'total':total,
        'count':count,
    }
    

    return JsonResponse(values,safe=False)

    # if value == 1:
    #     return redirect(cart)
    # else:
    #     return redirect(shoppingaddress)


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


def addressSelect(request,id):
    print('asdfhakfhaskfhasff')

    print(id)
   
    address = ShippingAddress.objects.get(id=id)
    
    return JsonResponse({
        'name':address.account.first_name,
        'email': address.account.email,
        'phone': address.account.phone,
        'address':address.address,
        'city':address.city,
        'state':address.state,
        'pincode':address.pincode
    })
    