from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# Create your views here.

from account.forms import RegistrationForm


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
    return render(request, 'page.html')

def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user= authenticate(email=email,password=password,is_superuser=False)
        if user is not None:
            print('success')
            return redirect('home')
        else:
            return redirect('loginpage')
    return redirect('loginpage')






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
