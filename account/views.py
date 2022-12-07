import random
from random import randint
import uuid
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from twilio.rest import Client
from account.forms import AccountAuthenticationForm, RegistrationForm, UserEditForm
from account.models import Account, Profile

from cart.models import OrderedItems
from invoice.views import guest

from proj.models import BannerManagement, Category, Order, OrderItems, Product,  ShippingAddress, SubCategory
from wishlist.models import Wishlist
from account.helpers import *
from .helpers import send_forget_password_mail


# Create your views here.


def landing_page(request):
    if not request.session.session_key:
        request.session.save()
        print(request.session.session_key)
    if 'user_exist' in request.session:
        banner = BannerManagement.objects.all()

        context = {
            'banner': banner
        }
        return render(request, 'landing/index.html', context)
    banner = BannerManagement.objects.all()

    context = {
        'banner': banner
    }
    return render(request, 'landing/index.html', context)


def user_loginpage(request):
    return render(request, 'login.html')


def registration_view(request):
    referal_code ='Torque.in'+str(random.randint(1111111, 9999999))
    print(referal_code)
    context = {}
    re = 'asdfk'

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            form.save()

            # email = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password1')
            # account = (email=email, password=raw_password)
            # account = authenticate(email=email, password=raw_password)
            # login(request, account)

            return redirect('loginpage')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'signup.html', context)


def home(request):
    print(request.session.session_key)
    # if request.user.is_authenticated:

    if 'user_exist' in request.session:
        print('authenticated')
        customer = request.user
        print('customer')
        cartItems=0
        # try:
        order= Order.objects.filter(account=customer,complete=False)
        cart = OrderItems.objects.filter(
            account=customer)
        items = cart

        for i in cart:
            cartItems = i.get_cart_items
        print(cartItems)
        products = Product.objects.all().order_by('id')
        filterProduct= Product.objects.filter(product_offer__gte=1)
        filterCategory= Category.objects.filter(category_offer__gte=1)
        print(filterProduct)
        category = Category.objects.all().order_by('id')
        sub = SubCategory.objects.all().order_by('id')
        for i in category:
            sub = i.filtered
            print(sub)
        data = {'products': products, 'items': items,'category':category,'sub':sub,'filterProduct':filterProduct,
                'filterCategory':filterCategory,'order': order, 'cartItems': cartItems}
        return render(request, 'page.html', data)
        # except:
        #         # order = []
        #         # items = []
        #         # cartItems = []
        #         print("An exception occurred")
        #         # products = Product.objects.all()
        #         # category = Category.objects.all().order_by('id')
        #         # sub = SubCategory.objects.all().order_by('id')
        #         # data = {
        #         #     'products': products,
        #         #     'sub':sub,
        #         #     'category':category,
        #         #     'cartItems': cartItems,
        #         #     'items': items,
        #         #     'order': order,
        #         # }
        #         # return render(request, 'page.html', data)
    guestUser = request.session.session_key
    order, created = Order.objects.get_or_create(session_id = guestUser)
    items = OrderItems.objects.filter(session_id=guestUser)
    cartItems=0
    for i in items:
        cartItems=i.get_cart_items
    products = Product.objects.all()
    category = Category.objects.all().order_by('id')
    sub = SubCategory.objects.all().order_by('id')
    data = {
        'products': products,
        'sub':sub,
        'category':category,
        'cartItems': cartItems,
        'items': items,
        'order': order,
    }
    return render(request, 'page.html', data)

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            dat = Account.objects.filter(
                email=email, is_superuser=False).exists()
            if dat:

                print('success')
                request.session['user_exist'] = email
                guestUser = request.session.session_key
                print('guest user id', guestUser)
                if guestUser:
                    guestItem = OrderItems.objects.filter(session_id=guestUser)
                    order = Order.objects.filter(session_id=guestUser).exists()
                    if order:
                        ord = Order.objects.filter(session_id=guestUser)
                        for i in ord:
                            i.account=user
                            i.save()
                    print("Guest cart is", guestItem)
                    add = OrderItems() 
                    if guestItem:
                        items = guestItem
                        print('guestUser')
                        for item in items:
                            print(item.product)

                            check = None
                            check = OrderItems.objects.filter(account=user,product=item.product).exists() 
                            if check:
                                check = OrderItems.objects.filter(account=user,product=item.product)
                                for ch in check:
                                    ch.quantity = ch.quantity + item.quantity
                                    ch.save()
                            else:
                                OrderItems.objects.create(account=user,product=item.product,quantity=item.quantity,order=item.order)
                                # add.account = user 
                                # add.product = item.product
                                # add.quantity = item.quantity
                                # add.order = item.order
                                # add.save()  
                                item.delete()        

                guestItem.delete()
                    
                login(request, user)   
                return redirect('home')
            else:
                messages.error(request, 'Invalid Details')
                return redirect('loginpage')

        elif email == '' and password == '':
            messages.error(request, 'Invalid Details')
            return redirect('loginpage')
        elif email == '':
            messages.error(request, 'email is Required')
        elif password == '':
            messages.error(request, 'Password is Required')
        else:
            messages.error(request, 'Invalid Details')
            return redirect('loginpage')

    return redirect('loginpage')

def logout_page(request):
    print('prrr')
    if 'user_exist' in request.session:
        del request.session['user_exist']
        print('hey')
        guestUser = request.session.session_key
        logout(request)
        items = OrderItems.objects.filter(session_id=guestUser)
        items.delete()
        return redirect('home')
    logout(request)
    return redirect('home')




def product_view(request, id):
    digit = str(uuid.uuid4())
    print(digit)
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer')
        try:
            order = Order.objects.filter(account=customer, complete=False)
            items = OrderItems.objects.filter(account=customer)
            cartItems=0
            for item in items:
                cartItems = item.get_cart_items
            val = Product.objects.get(id=id)
            related_products = Product.objects.filter(sub=val.sub)
            print(related_products)
            offer = 0
            price = 0
            pro = Product.objects.get(id=id)
            wishlist = Wishlist.objects.get(product=val, account=customer)
            print(wishlist)

            if val.quantity < 0:
                messages.error(request, 'Out Of Stock')

            if val.quantity < 0:
                messages.error(request, 'Out Of Stock')

                context = {'key5': val, 'items': items, 'wishlist': wishlist, 'offer': offer,'related_products':related_products,
                           'order': order, 'cartItems': cartItems}
                return render(request, 'product_view.html', context)
            else:
                context = {'key5': val, 'items': items, 'wishlist': wishlist, 'offer': offer,'related_products':related_products,
                           'order': order, 'cartItems': cartItems}
                return render(request, 'product_view.html', context)
        except:
            order = Order.objects.filter(account=customer, complete=False)
            items = OrderItems.objects.filter(account=customer)
            cartItems=0
            for item in items:
                cartItems = item.get_cart_items
            val = Product.objects.get(id=id)
            related_products = Product.objects.filter(sub=val.sub)
            if val.quantity < 0:
                messages.error(request, 'Out Of Stock')
            wishlist = Wishlist.objects.filter(product=val, account=customer).exists()
            if wishlist:
                wishlist = wishlist

            print(wishlist)
            print(offer)
            print(val.quantity)
            
            context = {'key5': val, 'cartItems': cartItems,'wishlist':wishlist,'related_products':related_products,
                       'offer': offer, 'price': price}
            print("An exception occurred")

            return render(request, 'product_view.html', context)


    order, created = Order.objects.get_or_create(session_id = request.session.session_key)
    items  = OrderItems.objects.filter(session_id=request.session.session_key)
    cartItems = order.get_cart_items

    val = Product.objects.get(id=id)
    if val.quantity < 0:
        messages.error(request, 'Out Of Stock')
    print(val.quantity)
    related_products = Product.objects.filter(sub=val.sub)
    print(related_products)
    context = {'key5': val, 'items': items,'related_products':related_products,
            'order': order, 'cartItems': cartItems}
    return render(request, 'product_view.html', context)


@never_cache
def otp_login_page(request):
    return render(request, 'phone.html')


@never_cache
def otp_login(request):
    print("hello")
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        print(phone_number)
        user = Account.objects.filter(phone=phone_number)
        if not user.exists():
            messages.error(request, "please enter A valid mobile number")
            return redirect(otp_login_page)
        else:
            OtpGenerate.send_otp(phone_number)
            return render(request, 'otp.html')


def enter_otp(request):
    return render(request, 'otp.html')


@never_cache
def verify_otp(request):
    obj = OtpGenerate()
    if request.method == 'POST':
        re_otp = request.POST.get('otp')
        ge_otp = obj.Otp
        if re_otp == ge_otp:
            user = Account.objects.filter(phone=obj.phone).first()

            if request.user.is_superuser is False:
                login(request, user)
            # login(request,request.user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Otp")
            return redirect('enter_otp')
    else:
        messages.error(request, "Invalid Credentials")
        return redirect('otp_login_page')


class OtpGenerate():
    Otp = None
    phone = None

    def send_otp(phone_number):
        account_sid = settings.ACCOUNT_SID
        auth_token = settings.AUTH_TOKEN
        target_number = '+91' + phone_number
        twilio_number = '+17199744556'
        otp = random.randint(1000, 9999)
        OtpGenerate.Otp = str(otp)
        OtpGenerate.phone = phone_number
        msg = "your otp is " + str(otp)
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=msg,
            from_=twilio_number,
            to=target_number
        )
        print(message.body)
        return True


@login_required(login_url=login_page)
def user_profile(request, id):

    if request.user.is_authenticated:

        print('authenticated')
        customer = request.user
        print('customer')
        try:
            cartItems =0
            items = 0
            order = OrderItems.objects.filter(account=customer)
            items = order
            for i in order:
                cartItems = i.get_cart_items
            datas = {
                'data': data,
                'cartItems': cartItems}
            return render(request, 'userprofile/profile.html', datas)
        except:
            print("An exception occurred")
    else:
        return redirect(login_page)
    user = Account.objects.get(id=id)
    data = ShippingAddress.objects.filter(account=id).first()
    account = Account.objects.get(id=id)
    orders = OrderedItems.objects.filter(account=account).order_by('id')
    if orders:
            for i in orders:
                print(i.returnPolicy)
    print('heyyyyyyyyy')
    cart = OrderItems.objects.filter(account=account)
    cartItems =0
    if cart:
            for i in cart:
                cartItems = cartItems + i.get_cart_items

    account = Account.objects.get(id=id)
    wishlst = Wishlist.objects.filter(account=account)
    context = {'cartItems': cartItems, 'wishlst': wishlst}

    try:
        orders = OrderedItems.objects.filter(account=account).order_by('id')
        print('heyyyyyyyyy')
        cart = OrderItems.objects.filter(account=account)
        cartItems =0
        if cart:
                for i in cart:
                    cartItems = cartItems + i.get_cart_items
    except:
        cartItems = []
    datas = {
        'data': data,
        'cartItems': cartItems,
        'user': user,
        'orders': orders, 
        'wishlst': wishlst
    }
    return render(request, 'userprofile/profile.html', datas)


def address_view(request, id):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer')
        try:
            order = OrderItems.objects.filter(account=customer)
            items = order
            cartItems = 0
            for i in order:
                cartItems = cartItems + i.get_cart_items
            context = {'items': items,
                       'order': order, 'cartItems': cartItems}
            return render(request, 'address_view.html', context)
        except:
            print("An exception occurred")

    elif request.user is None:
        order = []
        items = []
        cartItems = []

    account = Account.objects.get(id=id)
    datas = ShippingAddress.objects.filter(account=id).order_by('id')
    order = OrderItems.objects.filter(account=customer)
    items = order
    cartItems = 0
    for i in order:
        cartItems = cartItems + i.get_cart_items
    context = {
        'datas': datas,
        'cartItems': cartItems,
        'items': items,
        'order': order,
    }
    return render(request, 'userprofile/address_view.html', context)


def delete_address(request, id, user_id):
    delete = ShippingAddress.objects.filter(id=id)
    delete.delete()
    return JsonResponse('deleted',safe=False)


def address_edit(request, id):
    details = ShippingAddress.objects.get(id=id)
    details.address = request.POST.get('address')
    details.city = request.POST.get('city')
    details.state = request.POST.get('state')
    details.phone = request.POST.get('phone')
    details.pincode = request.POST.get('pincode')
    details.save()
    id = details.account.id
    return redirect(address_view, id)


def order_userside(request, id):
    pass
#     account = Account.objects.get(id=id)
#     orders = OrderedItems.objects.filter(account=account).order_by('id')
#     order = Order.objects.get(account=account, complete=False)
#     items = order.orderitems_set.all()
#     cartItems = order.get_cart_items
#     context = {
#         'orders': orders, 'cartItems': cartItems,
#     }
#     return render(request, 'userprofile/user_orders.html', context)

# @login_required(login_page)
def add_wishlist(request, product_id, user_id):
    print('kjdfsdfsjjshguhuhnadsf')
    product = Product.objects.get(id=product_id)
    user = Account.objects.get(id=user_id)
    if Wishlist.objects.filter(product=product, account=user).exists():
        wishlist = Wishlist.objects.filter(product=product, account=user)
        if wishlist:
            wishlist.delete()
            return JsonResponse('deleted',safe=False)
    else:
        product = Product.objects.get(id=product_id)
        user = Account.objects.get(id=user_id)
        wishlist = Wishlist.objects.create(product=product, account=user)
        return JsonResponse('added',safe=False)


def wishlist_userside(request, id):
    pass
    # try:
    # account = Account.objects.get(id=id)
    # wishlst = Wishlist.objects.filter(account=account)
    # try:
    #     order = Order.objects.get(account=account, complete=False)
    #     items = order.orderitems_set.all()
    #     cartItems = order.get_cart_items
    #     context = {'cartItems': cartItems, 'wishlst': wishlst}
    #     return render(request, 'userprofile/wishlist.html', context)
    # except:
    #     print("An exception occurred")

    # print(wishlst)
    # context = {
    #     'wishlst': wishlst
    # }
    # return render(request, 'userprofile/wishlist.html', context)
    # except:
    #     wishlst = []
    #     context = {
    #         'wishlst':wishlst
    #     }


# def user(request):
#     # if 'username' in request.session:
#     user_data = RegistrationForm()
#     return render(request, 'users.html', {'key1': user_data})
# # return redirect('register')

# def forgotpassword(request):
#     try:
#         if request.method == 'POST':
#             email = request.POST.get('email')
#             if not Account.objects.filter(email=email).first():
#                 messages.error(request,'not user found with this email')
#                 return redirect('/forgot-password')
#             user_obj=Account.objects.get(email=email)

#             print(user_obj)
#             token=str(uuid.uuid4())
#             account, create=Profile.objects.get_or_create(user=user_obj)
#             account.forget_password_token=token
#             account.save()
#             print(account.forget_password_token)
#             print(user_obj.email)
#             send_forget_password_mail(user_obj.email, token)
#             messages.error(request,'An email is sent')
#             return redirect('/forgot-password')


#     except Exception as e:
#         print(e)


#     return render(request,'forgot/forgottpassword.html')


# def changepassword(request,token):

#     context ={}
#     try:
#         account = Account.objects.filter(forgot_password_token = token).first()
#         print(account)

#     except Exception as e:
#         print(e)


#     return render(request,'forgot/changepassword.html')


def password_change(request, id):
    if request.method == 'POST':

        currentpass = request.POST.get('currentpass')
        newpass = request.POST.get('newpass')
        repeatpass = request.POST.get('repeatpass')
        if currentpass == '' or newpass == '' or repeatpass == '':
            return redirect('password_change', id)
        else:
            print(id)
            user = Account.objects.filter(id=id, password=currentpass).exists()
            if user:
                print(user)
                if newpass == repeatpass:
                    change = Account.objects.get(id=id)
                    newpass = make_password(newpass)
                    change.password = newpass
                    print('error')
                    print(change.password)
                    change.save()
                    return redirect(user_profile, id)
                else:
                    messages.error(request, 'password does not match')
                    return redirect('password_change', id)
            else:
                messages.error(request, 'Current Password is Incorrect')

    return render(request, 'userprofile/changepassword.html')


def editProfile(request):
    form = UserEditForm()
    instance = Account.objects.get(email=request.user)

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=instance)
        if form.is_valid():
            print(request.user)

            form.save()
            id = instance.id

            return redirect('userprofile', id)

    form = UserEditForm(instance=instance)
    return render(request, 'userprofile/editprofile.html', {'form': form})


def addressAdd(request):
    if request.method == 'POST':
        address = ShippingAddress()
        address.account = request.user
        address.name = request.POST.get('names')
        address.email = request.POST.get('emails')
        address.phone = request.POST.get('phones')
        address.address = request.POST.get('addressess')
        address.city = request.POST.get('citys')
        address.state = request.POST.get('states')
        address.pincode =request.POST.get('pincodes')

        if ShippingAddress.objects.filter(address=address.address,city=address.city,state=address.state,pincode=address.pincode).exists():
            messages.error(request,'this address already exist !')
            return redirect('shipping')
        elif ShippingAddress.objects.filter(account=request.user).count() > 4: 
            messages.error(request,'minimum 4 address !')
            return redirect('shipping') 
        else:
            address.save()
            return redirect('shipping')

def contact(request):
    pass

