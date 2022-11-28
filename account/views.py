import random
from random import randint
import uuid
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from twilio.rest import Client

from account.forms import AccountAuthenticationForm, RegistrationForm, UserEditForm
from account.models import Account, Profile
from cart.models import OrderedItems
from proj.models import BannerManagement, Category, CategoryOffer, Order, Product, ProductOffer, ShippingAddress
from wishlist.models import Wishlist
from account.helpers import *
from .helpers import send_forget_password_mail


# Create your views here.


def landing_page(request):
    banner = BannerManagement.objects.all()

    context = {
        'banner': banner
    }
    return render(request, 'landing/index.html', context)


def user_loginpage(request):
    return render(request, 'login.html')


def registration_view(request):
    context = {}
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

    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer')
        try:
            order, create = Order.objects.get_or_create(
                account=customer, complete=False)
            items = order.orderitems_set.all()
            cartItems = order.get_cart_items
            products = Product.objects.all()
            data = {'products': products, 'items': items,
                    'order': order, 'cartItems': cartItems}
            return render(request, 'page.html', data)
        except:
            print("An exception occurred")
    elif request.user is None:
        order = []
        items = []
        cartItems = []
    order = []
    items = []
    cartItems = []
    products = Product.objects.all()
    data = {
        'products': products,
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

        return redirect('home')
    logout(request)
    return redirect('home')


def product_view(request, id):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer')
        try:
            order = Order.objects.get(account=customer, complete=False)
            items = order.orderitems_set.all()
            cartItems = order.get_cart_items
            val = Product.objects.get(id=id)
            offer = 0
            price = 0
            pro = Product.objects.get(id=id)

            if val.quantity < 0:
                messages.error(request, 'Out Of Stock')
            productoff = ProductOffer.objects.filter(product=pro).exists()
            categoryoff = CategoryOffer.objects.filter(
                category=pro.category).exists()
            if productoff and categoryoff:
                productoff = ProductOffer.objects.get(product=pro)
                categoryoff = CategoryOffer.objects.get(category=pro.category)
                if productoff.productOffer > categoryoff.categoryOffer:
                    offer = productoff.productOffer
                    print(offer, 'hgjgbjhgjh')
                elif productoff.productOffer < categoryoff.categoryOffer:
                    offer = categoryoff.categoryOffer
                    print(offer, 'jhhgftdrsrtdrdtrdtrdr')
                    print(offer)
                wishlist = Wishlist.objects.get(Product=val, account=customer)
            if val.quantity < 0:
                messages.error(request, 'Out Of Stock')

                context = {'key5': val, 'items': items, 'wishlist': wishlist, 'offer': offer,
                           'order': order, 'cartItems': cartItems}
                return render(request, 'product_view.html', context)
            else:
                context = {'key5': val, 'items': items, 'wishlist': wishlist, 'offer': offer,
                           'order': order, 'cartItems': cartItems}
                return render(request, 'product_view.html', context)
        except:
            order = Order.objects.get(account=customer, complete=False)
            items = order.orderitems_set.all()
            val = Product.objects.get(id=id)
            if val.quantity < 0:
                messages.error(request, 'Out Of Stock')
            pro = Product.objects.get(id=id)
            productoff = ProductOffer.objects.filter(product=pro).exists()
            categoryoff = CategoryOffer.objects.filter(
                category=pro.category).exists()
            print(categoryoff)
            print(productoff)
            if productoff:
                offer = 0
                price = 0
                productoff = ProductOffer.objects.get(product=pro)
                offer = productoff.productOffer
                offer = 100/offer
                price = val.price
                val.price = val.price/int(offer)
            elif categoryoff:
                offer = 0
                price = 0
                cat = pro.category
                categoryoff = CategoryOffer.objects.get(category=cat)
                offer = categoryoff.categoryOffer
                # offer = 100/offer
                print(offer)
                price = val.price
                val.price = val.price-val.price*offer/100
            elif productoff and categoryoff:
                offer = 0
                price = 0
                cat = pro.category
                productoff = ProductOffer.objects.get(product=pro)
                categoryoff = CategoryOffer.objects.get(category=cat)
                print(cat, 'uyoytytutuygu')
                print(categoryoff)
                if productoff.productOffer > categoryoff.categoryOffer:
                    offer = productoff.productOffer
                    print(offer, 'hgjgbjhgjh')
                elif productoff.productOffer < categoryoff.categoryOffer:
                    offer = categoryoff.categoryOffer
                    print(offer, 'jhhgftdrsrtdrdtrdtrdr')
                offer = 100/offer
                price = val.price
                val.price = val.price/int(offer)
                print(val.price)
            print(offer)
            cartItems = order.get_cart_items
            context = {'key5': val, 'cartItems': cartItems,
                       'offer': offer, 'price': price}
            print("An exception occurred")

            return render(request, 'product_view.html', context)

    elif request.user is None:
        order = []
        items = []
        cartItems = []
        offer

    order = []
    items = []
    cartItems = []
    val = Product.objects.get(id=id)
    context = {'key5': val, 'items': items, 'offer': offer,
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
            order = Order.objects.get(account=customer, complete=False)
            items = order.orderitems_set.all()
            cartItems = order.get_cart_items
            datas = {
                'data': data,
                'cartItems': cartItems}
            return render(request, 'userprofile/profile.html', datas)
        except:
            print("An exception occurred")

    elif request.user is None:

        cartItems = []
    else:
        return redirect(login_page)
    user = Account.objects.get(id=id)
    data = ShippingAddress.objects.filter(account=id).first()
    cartItems = []
    datas = {
        'data': data,
        'cartItems': cartItems,
        'user': user,

    }
    return render(request, 'userprofile/profile.html', datas)


def address_view(request, id):
    if request.user.is_authenticated:
        print('authenticated')
        customer = request.user
        print('customer')
        try:
            order = Order.objects.get(account=customer, complete=False)
            items = order.orderitems_set.all()
            cartItems = order.get_cart_items
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
    return redirect(address_view, user_id)


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
    account = Account.objects.get(id=id)
    orders = OrderedItems.objects.filter(account=account).order_by('id')
    order = Order.objects.get(account=account, complete=False)
    items = order.orderitems_set.all()
    cartItems = order.get_cart_items
    context = {
        'orders': orders, 'cartItems': cartItems,
    }
    return render(request, 'userprofile/user_orders.html', context)


def add_wishlist(request, product_id, user_id, id):
    product = Product.objects.get(id=product_id)
    user = Account.objects.get(id=user_id)
    if Wishlist.objects.filter(product=product, account=user).exists():
        wishlist = Wishlist.objects.filter(product=product, account=user)
        if wishlist:
            wishlist.delete()
            if id == '1':
                return redirect('product_view', product_id)
            else:
                return redirect('wishlists', user_id)
        else:
            return redirect('wishlists', product_id)
    else:
        product = Product.objects.get(id=product_id)
        user = Account.objects.get(id=user_id)
        wishlist = Wishlist.objects.create(product=product, account=user)
        return redirect('product_view', product_id)


def wishlist_userside(request, id):
    # try:
    account = Account.objects.get(id=id)
    wishlst = Wishlist.objects.filter(account=account)
    try:
        order = Order.objects.get(account=account, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items
        context = {'cartItems': cartItems, 'wishlst': wishlst}
        return render(request, 'userprofile/wishlist.html', context)
    except:
        print("An exception occurred")

    print(wishlst)
    context = {
        'wishlst': wishlst
    }
    return render(request, 'userprofile/wishlist.html', context)
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
