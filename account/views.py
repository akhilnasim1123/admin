from random import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import Account
import random
from django.views.decorators.cache import never_cache
from twilio.rest import Client

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# Create your views here.

from account.forms import RegistrationForm
from proj.models import Product, Category, Order




def landing_page(request):
    return render(request, 'landing/index.html')


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
        order = Order.objects.get(account=customer, complete=False)
        items = order.orderitems_set.all()
        cartItems = order.get_cart_items

    products = Product.objects.all()
    data = {
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, 'page.html', data)


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            dat = Account.objects.get(email=email)
            print('success')
            request.session['user_exist'] = dat.first_name
            login(request, user)
            return redirect('home')
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



    val = Product.objects.get(id=id)
    context = {'key5': val}
    return render(request, 'product_view.html',context)


# def otp_login(request):
#     return render(request, 'phone.html')

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

# def login_view(request):
#     context = {}
#     user = request.user
#     # if user.is_authenticated:
#     #     return redirect('home')
#     if request.POST:
#         form = AccountAuthenticationForm(request.POST)
#         if form.is_valid():
#             email = request.POST['email']
#             password = request.POST['password']
#             user = authenticate(email=email, password=password, is_active=False)
#
#             if user:
#                 login(request, user)
#                 return redirect('home')
#         else:
#             form = AccountAuthenticationForm()
#
#             context['login_form'] = form
#     return render(request, 'login.html', context)

# def user(request):
#     # if 'username' in request.session:
#     user_data = RegistrationForm()
#     return render(request, 'users.html', {'key1': user_data})
# # return redirect('register')
