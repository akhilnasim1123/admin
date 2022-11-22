from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from account.forms import RegistrationForm
from account.models import Account
from account.views import order_userside
from cart.models import OrderedItems
from proj.forms import BannerForm, ItemsForm, SubForm
from proj.models import BannerManagement, Product, Category, ShippingAddress, SubCategory


# admin login page -------------------------------->
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_log(request):
    if 'email' in request.session:
        return redirect('admin_page')
    return render(request, 'admin_log.html')


# admin homepage html ------------------------------->
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_page(request):
    if 'email' in request.session:
        return render(request, 'admin.html')


# admin authentication ---------------------------->

def admin_auth(request):
    if 'email' in request.session:
        return redirect('admin_page')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = authenticate(email=email, password=password)
        if admin is not None:
            if admin.is_superuser:
                print('yes')

                request.session['email'] = email
                login(request, admin)
                return redirect('admin_page')
            else:
                print('nope')
                messages.error(request, 'Your Not a Admin')
                return redirect('admin_log')

        else:
            print('not yet')
            messages.error(request, 'Your Not a Admin')
            return redirect('admin_log')
    return redirect('admin_log')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_log)
def admin_user(request):
    if 'email' in request.session:
        user_data = Account.objects.filter(is_superuser=False)
        data = {
            'key1': user_data
        }
        return render(request, 'users.html', {'key1': user_data})
    return redirect('admin_log')


def block(request, user_id):
    Account.objects.filter(id=user_id).update(is_active=False)
    return redirect('admin_user')


def unblock(request, user_id):
    Account.objects.filter(id=user_id).update(is_active=True)
    return redirect('admin_user')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=admin_log)
def product(request):
    if 'email' in request.session:
        # data = Category.objects.all()
        context = {}
        if request.method == 'POST':
            form = ItemsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                print('saved')
                return redirect('product_list')

        else:
            print('not')
            form = ItemsForm()
            context['product_form'] = form
        return render(request, 'product.html', context)
    return redirect('admin_log')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if 'email' in request.session:
        del request.session['email']
        print('hey')
        return redirect('admin_log')
    return redirect('admin_log')


@login_required(login_url=admin_log)
def category_view(request):
    if 'email' in request.session:
        cat_data = Category.objects.all()
        return render(request, 'category_list.html', {'key1': cat_data})
    return redirect('admin_log')


@login_required(login_url=admin_log)
def category(request):
    if 'email' in request.session:
        if request.method == 'POST':
            category_name = request.POST.get('category_name')
            Category.objects.create(category_name=category_name)
            return redirect('category')
        return render(request, 'category.html')
    return redirect('admin_log')


@login_required(login_url=admin_log)
def sub_category(request):
    if 'email' in request.session:
        sub = SubCategory.objects.all()
        return render(request, 'SubCategory/sub_view.html', {'sub': sub})
    return redirect('admin_log')


def sub_cat(request):
    context = {}
    if request.method == 'POST':
        form = SubForm(request.POST)
        if form.is_valid():
            print('post')
            form.save()
            return redirect('sub_category')
    else:
        print('get')
        form = SubForm
        context['sub_form'] = form
    return render(request, 'SubCategory/sub.html', context)


def deleteSub(request, id):
    delete = SubCategory.objects.get(id=id)
    delete.delete()
    return redirect('sub_category')


def editSubpage(request, id):
    pass


def product_list(request):
    user_data = Product.objects.all()
    return render(request, 'product_edit.html', {'key2': user_data})


def editpage(request, id):
    val = Product.objects.get(id=id)
    return render(request, 'proEdit.html', {'key3': val})


def editData(request, id):
    if request.method == 'POST':
        edit = Product.objects.get(id=id)
        edit.product_name = request.POST.get('product_name')
        edit.desc = request.POST.get('description')
        edit.price = request.POST.get('price')
        edit.save()
        return redirect('product_list')


def deleteData(request, id):
    delete = Product.objects.get(id=id)
    delete.delete()
    return redirect('product_list')


def searchdata(request):
    pass


def editCat(request, cat_id):
    if request.method == 'POST':
        editdat = Category.objects.get(id=cat_id)
        editdat.category_name = request.POST.get('category_name')
        editdat.save()
        return redirect('category_view')


def editcatpage(request, cat_id):
    value = Category.objects.get(id=cat_id)
    return render(request, 'editcat.html', {'key4': value})


def deleteCat(request, id):
    delete = Category.objects.get(id=id)
    delete.delete()
    return redirect('category_view')


def searchCat(request):
    pass


def test(request):
    form = ItemsForm()
    return render(request, 'test.html', {'form': form})


def order_list(request):
    order = OrderedItems.objects.all()
    return render(request, 'admin/orders.html', {'order': order})


def cancel(request, id, val):
    pro = OrderedItems.objects.get(id=id)
    product = Product.objects.get(id=pro.product.id)
    pro.status = 'Cancelled'
    # for qnty in product:
    #     qnty.quantity = qnty.quantity + pro.quantity
    #     print(qnty.quantity)
    #     qnty.save()
    product.quantity = product.quantity + pro.quantity
    
    product.save()
    user_id = pro.account.id
    pro.save()
    if val == '1':
        return redirect('order_list')
    else:
        return redirect(order_userside, user_id)


def order_view(request, id):
    order = OrderedItems.objects.get_or_create(id=id)
    print(order)

    print(id)
    return render(request, 'admin/order_view.html', {'order': order})


def banner(request):
    context = {}
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        old_banner = BannerManagement.objects.all()

        if form.is_valid():
            old_banner.delete()
            form.save()
            print('saved')
            return redirect('banner')

    print('get')
    form = BannerForm()
    context['banner_form'] = form
    return render(request, 'admin/bannermanage.html', context)


def dashboard(request):
    cancel_data = OrderedItems.objects.filter(status='Cancelled').count()
    order_data = OrderedItems.objects.all().count()
    order = OrderedItems.objects.all()
    total_revenue = 0
    for item in order:
        total_revenue = total_revenue + int(item.price)
    razorpay = OrderedItems.objects.filter(payment='Paid by Razorpay').count()
    paypal = OrderedItems.objects.filter(payment='Paid by Paypal').count()
    cash_on_delivery = OrderedItems.objects.filter(payment='COD').count()
    print(razorpay)
    cancel = OrderedItems.objects.filter(status='Cancelled')
    refund = 0
    for money in cancel:
        refund = refund + int(money.price)

    refund = total_revenue - refund

    cod = OrderedItems.objects.filter(payment='COD')
    cod_total = 0
    for price in cod:
        cod_total = cod_total + int(price.price)

    payp = OrderedItems.objects.filter(payment='Paid by Paypal')
    paypal_total = 0
    for pp in payp:
        paypal_total = paypal_total+int(pp.price)

    razor = OrderedItems.objects.filter(payment='Paid by Razorpay')
    razorpay_total = 0
    for rp in razor:
        razorpay_total = razorpay_total + int(rp.price)

    print(total_revenue)

    print(cancel_data)
    print(order_data)
    context = {
        'cancel_data': cancel_data,
        'order_data': order_data,
        'total_revenue': total_revenue,
        'razorpay': razorpay,
        'paypal': paypal,
        'cash_on_delivery': cash_on_delivery,
        'refund': refund,
        'cod_total': cod_total,
        'paypal_total': paypal_total,
        'razorpay_total': razorpay_total,

    }
    print(razorpay)
    return render(request, 'dashboard/maindash.html', context)
