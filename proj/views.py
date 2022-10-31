from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from account.forms import RegistrationForm
from account.models import Account
from proj.models import Product


# admin login page -------------------------------->
def admin_log(request):
    return render(request, 'admin_log.html')


# admin homepage html ------------------------------->
def admin_page(request):
    return render(request, 'admin.html')


# admin authentication ---------------------------->
def admin_auth(request):
    if 'username' in request.session:
        return redirect('admin_page')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = authenticate(email=email, password=password)
        if admin is not None:
            login(request, admin)
            return redirect('admin_page')
        else:
            return redirect('admin_log')

        # if email != 'email@gmail.com':
        #     return redirect('admin_log')
        # else:
        #     # admin = authenticate(email=email, password=password,is_superuser=True)
        #     admin = Account.objects.filter(password=password)
        #     if admin is not None:
        #         # login(request, admin)
        #         return redirect('admin_page')
        #     else:
        #         return redirect('admin_log')
    return redirect('admin_log')


def admin_user(request):
    user_data = Account.objects.all()
    return render(request, 'users.html', {'key1': user_data})


def block(request, user_id):
    Account.objects.filter(id=user_id).update(is_active=False)
    return redirect(admin_user)


def unblock(request, user_id):
    Account.objects.filter(id=user_id).update(is_active=True)
    return redirect(admin_user)


def product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_image = request.POST.get('product_image')
        data = Product.objects.filter(product_name=product_image, product_image=product_image)
        data.save()
    return render(request, 'product.html')
