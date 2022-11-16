import random
from random import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from twilio.rest import Client

from account.forms import AccountAuthenticationForm, RegistrationForm
from account.models import Account
from cart.models import OrderedItems
from proj.models import BannerManagement, Category, Order, Product, ShippingAddress
from wishlist.models import Wishlist

# Create your views here.



def landing_page(request):
    banner          = BannerManagement.objects.all()

    context         = {
        'banner':banner
    }
    return render(request, 'landing/index.html',context)


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
            order,create = Order.objects.get_or_create(account=customer, complete=False)
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
            dat = Account.objects.get(email=email, is_superuser=False)
            print('success')
            request.session['user_exist'] = dat.email
            login(request, user)
            return redirect('home')
        elif email == '' and password == '':
            messages.error(request, 'Invalid Details')
            return redirect('loginpage')
        elif email == '':
            messages.error(request,'email is Required')
        elif password == '':
            messages.error(request,'Password is Required')
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
            wishlist=Wishlist.objects.get(Product=val,account=customer)
            
            context = {'key5': val, 'items': items,'wishlist':wishlist,
               'order': order, 'cartItems': cartItems}
            return render(request, 'product_view.html', context)
        except:
            order = Order.objects.get(account=customer, complete=False)
            items = order.orderitems_set.all()
            val = Product.objects.get(id=id)
            cartItems = order.get_cart_items
            context = {'key5': val,'cartItems': cartItems}
            print("An exception occurred")
            return render(request, 'product_view.html', context)

    elif request.user is None:
        order = []
        items = []
        cartItems = []
    order = []
    items = []
    cartItems = []
    val = Product.objects.get(id=id)
    context = {'key5': val, 'items': items,
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
            # user = Account.objects.get(phone=obj.phone)
            # if request.user.is_superuser is False:
            #     login(request, user)
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
        account_sid = 'ACe7b9b69f043dc2db7caf7eede2ec925e'
        auth_token = '24b116899b1df7deba1f553db2f05217'
        target_number = '+91' + phone_number
        twilio_number = '+12183192744'
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
def user_profile(request,id):
   
   
    if request.user.is_authenticated:
        
        print('authenticated')
        customer = request.user
        print('customer')
        try:
            order = Order.objects.get(account=customer, complete=False)
            items = order.orderitems_set.all()
            cartItems = order.get_cart_items
            datas = {
                'data':data,
                 'cartItems': cartItems}
            return render(request, 'userprofile/profile.html', datas)
        except:
            print("An exception occurred")

    elif request.user is None:

        cartItems = []
    else:
        return redirect(login_page)


    data                    = ShippingAddress.objects.filter(account=id).first()
    cartItems = []
    datas ={
        'data':data,
        'cartItems': cartItems,

    }
    return render(request,'userprofile/profile.html',datas)

def address_view(request,id):
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

    account                             = Account.objects.get(id=id)
    datas                               = ShippingAddress.objects.filter(account=id)
    context ={
        'datas':datas,
        'cartItems': cartItems,
        'items': items,
        'order': order, 
    }
    return render(request,'userprofile/address_view.html',context)


def delete_address(request,id,user_id):
    delete                              = ShippingAddress.objects.filter(id=id)
    delete.delete()
    return redirect(address_view,user_id)
def address_edit(request,id):
    details = ShippingAddress.objects.get(id=id)
    details.address = request.POST.get('address')
    details.city = request.POST.get('city')
    details.state = request.POST.get('state')
    details.phone= request.POST.get('phone') 
    details.save()
    return redirect(address_view)

def order_userside(request,id):
    account              = Account.objects.get(id=id)
    orders               = OrderedItems.objects.filter(account=account).order_by('id')
    order = Order.objects.get(account=account, complete=False)
    items = order.orderitems_set.all()
    cartItems = order.get_cart_items   
    context={
        'orders':orders,'cartItems':cartItems,
    }
    return render(request,'userprofile/user_orders.html',context)

def add_wishlist(request,product_id,user_id,id):
    product                         = Product.objects.get(id=product_id)
    user                            = Account.objects.get(id=user_id)
    if Wishlist.objects.filter(product=product, account =user).exists():   
        wishlist                    = Wishlist.objects.filter(product=product,account=user)
        if wishlist:
            wishlist.delete()
            if id == '1':
                return redirect('product_view',product_id)
            else:
                return redirect('wishlists',user_id)
        else:
            return redirect('wishlists',product_id)
    else:
        product                     = Product.objects.get(id=product_id)
        user                        = Account.objects.get(id=user_id)
        wishlist                    = Wishlist.objects.create(product=product,account=user)     
        return redirect('product_view',product_id)

def wishlist_userside(request,id):
    # try:
    account = Account.objects.get(id=id)
    wishlst = Wishlist.objects.filter(account=account)
    try:
        order = Order.objects.get(account=account, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items   
        context = {'cartItems': cartItems,'wishlst':wishlst}
        return render(request,'userprofile/wishlist.html',context)
    except:
        print("An exception occurred")


    
    print(wishlst)
    context ={
        'wishlst':wishlst
    }
    return render(request,'userprofile/wishlist.html',context)
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
