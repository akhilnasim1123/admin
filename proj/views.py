from datetime import timedelta, timezone
import datetime
from time import strftime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import DateTimeField
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from account.forms import RegistrationForm
from account.models import Account
from account.views import  order_userside, user_profile
from cart.models import OrderedItems
from proj.forms import BannerForm, ItemsForm, ProductEditForm, SubForm
from proj.models import BannerManagement, Order, Product, Category,  ShippingAddress, SubCategory
import xlwt

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
                ad = admin.is_superuser
                request.session['email'] = ad
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
            category_offer = request.POST.get('category_offer')
            Category.objects.create(category_name=category_name,category_offer=category_offer)
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
    return redirect('productAdding')


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
    order = OrderedItems.objects.all().order_by('ordered')
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
        print('here')
        return redirect(order_list)
    else:
        print('user')
        return redirect(user_profile, user_id)

    

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
    returned = OrderedItems.objects.filter(status='is_returned').count()
    order_data = OrderedItems.objects.all().count()
    order = OrderedItems.objects.all()
    total_revenue = 0
    for item in order:
        total_revenue = float(total_revenue) + float(item.price)
    razorpay = OrderedItems.objects.filter(payment='Paid by Razorpay').count()
    paypal = OrderedItems.objects.filter(payment='Paid by Paypal').count()
    cash_on_delivery = OrderedItems.objects.filter(payment='COD').count()
    print(razorpay)
    cancel = OrderedItems.objects.filter(status='Cancelled')
    refund = 0
    for money in cancel:
        refund = refund + float(money.price)

    refund = total_revenue - refund

    cod = OrderedItems.objects.filter(payment='COD')
    cod_total = 0
    for price in cod:
        cod_total = cod_total + float(price.price)

    payp = OrderedItems.objects.filter(payment='Paid by Paypal')
    paypal_total = 0
    for pp in payp:
        paypal_total = paypal_total+float(pp.price)

    razor = OrderedItems.objects.filter(payment='Paid by Razorpay')
    razorpay_total = 0
    for rp in razor:
        razorpay_total = razorpay_total + float(rp.price)

    print(total_revenue)

    print(cancel_data)
    print(order_data)
    context = {
        'cancel_data': cancel_data,
        'returned':returned,
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



def productAdding(request):
    categorys = Category.objects.all()
    sub_category = SubCategory.objects.all()
    product_details = Product.objects.all().order_by('id')
    if request.method == 'POST':
        product = request.POST.get('productname')
        description = request.POST.get('description')
        categoryid = request.POST.get('categoryid')
        price = request.POST.get('price')
        subcat = request.POST.get('subcat')
        offer_name = request.POST.get('OfferName')
        offer = request.POST.get('offer')
        stock = request.POST.get('stock')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        categoryid = Category.objects.get(id=categoryid)
        subcat=SubCategory.objects.get(id=subcat)
        Product.objects.create(product_name=product,price=price,desc=description,sub=subcat,category=categoryid,
        quantity=stock,image1=image1,image2=image2,image3=image3,offer_name=offer_name,product_offer=offer)
        return redirect(productAdding)

    context = {
        'category':categorys,
        'subcategory':sub_category,
        'product':product_details,
    }
    return render(request,'admin/product_adding.html',context)
    


def productEdit(request,id):
    form = ProductEditForm()
    instance = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductEditForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            print(id)
            form.save(productAdding)
    form = ProductEditForm(instance=instance)
    return render(request,'admin/productEdit.html',{'form': form,'id':id})


def Offers(request):
    product = Product.objects.exclude(offer_name=None)
    category = Category.objects.exclude(offer_name=None)
    productoff = Product.objects.all().order_by('id')
    categoryoff = Category.objects.all().order_by('id')
    print(productoff)
    context ={
        'productoff':productoff,
        'categoryoff':categoryoff, 
        'product':product,
        'category':category,      
    }
    return render(request,'admin/offers.html',context)


def categoryOffer(request):
    if request.method == 'POST':
        offer = request.POST.get('offer_name')
        pers = request.POST.get('pers')
        category = request.POST.get('category')
        cat = Category.objects.get(id=category)
        cat.offer_name = offer
        cat.category_offer = pers
        cat.save()
        return redirect(Offers)
def productOffer(request):
    if request.method == 'POST':
       offer = request.POST.get('offer_name')
       pers = request.POST.get('pers')
       product = request.POST.get('product')
       pro = Product.objects.get(id=product)
       pro.offer_name = offer
       pro.product_offer = pers
       pro.save()
       return redirect(Offers)


def filterOrder(request):
    if request.method == 'POST':
        
        filter = request.POST.get('status')
        if filter == 'orderes':
            return redirect(order_list)
        else:
            status = OrderedItems.objects.filter(status = filter)

            return render(request,'admin/filter.html',{'status':status})
        
def statusEdit(request,id):
    order = OrderedItems.objects.get(id=id)
    if order.status == 'pending':
        order.status = 'out_of_delivery'
        order.save()
        return redirect(order_list)
    if order.status == 'out_of_delivery':
        order.status = 'Shipped'
        order.save()
        return redirect(order_list)
    elif order.status == 'Shipped':
        order.status = 'delivered'
        order.delivered_at=timezone.now()
        order.save()
        return redirect(order_list)
    else:
        return redirect(order_list)

def returnProduct(request,id):
    order = OrderedItems.objects.get(id=id)
    product = Product.objects.get(id=order.product.id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        order.reason = reason
        order.is_return = True
        order.status = 'is_returned'
        order.return_date = datetime.datetime.now()
        product.quantity = order.quantity + product.quantity
        order.save()
        product.save()
        return redirect(user_profile,order.account.id)
    return render(request,'userprofile/return.html',{'product':product,'id':id})

def deleteProOffer(request,id):
    offer = Product.objects.get(id=id)
    offer.product_offer = 0
    offer.offer_name = None
    offer.save()
    return redirect(Offers)
def deleteCatOffer(request,id):
    offer = Category.objects.get(id=id)
    offer.category_offer =0 
    offer.offer_name = None
    offer.save()
    return redirect(Offers)

from django.utils import timezone

def salesReport(request):
    orders = OrderedItems.objects.filter(status='delivered').order_by('ordered')
    if request.method == 'POST':
        date = request.POST.get('datepicker')
        dd = date
        date = date+" 23:59:59.562476+00:00"
        day = dd+" 00:00:00.000000+00:00"
        print(day)
        date =strftime(date)
        day=strftime(day)
        print(date)
        print(timezone.now())
        date = OrderedItems.objects.filter(ordered__lte=date,ordered__gte=day, status='delivered')
        # print(date)
        # if date:
        return render(request,'admin/salesReport.html',{'orders':date})  
        # else:
        #     orders = []
        #     return render(request,'admin/salesReport.html',{'orders':orders})  

                  
    return render(request,'admin/salesReport.html',{'orders':orders})

def export_as_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=SalesReport' +\
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['product','quantity','account','payment', 'ordered', 'total_price','price']
    for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    # if value != None and tovalue != None and state == 'date':
    #     print('hello')
    #     rows = Order.objects.filter(orderd=True, date_ordered__lte = tovalue, date_ordered__gte = value).values_list('user__username','payment_method',  'date_ordered', 'total_price')
    # elif value != None and tovalue == None and state == 'month':
    #     rows = Order.objects.filter(orderd=True, date_ordered__month = value[1], date_ordered__year = value[0]).values_list('user__username','payment_method',  'date_ordered', 'total_price')
    # elif value != None and tovalue == None and state == 'year':
    #     rows = Order.objects.filter(orderd=True, date_ordered__year = value).values_list('user__username','payment_method',  'date_ordered', 'total_price')
    # else:
    rows = OrderedItems.objects.filter(status='delivered').order_by('ordered').values_list('product','quantity','account','payment', 'ordered', 'total_price','price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)
    return response

def weekly(request):
    last_week = datetime.datetime.now().date() - timedelta(days=7)
    print(last_week)
    orders = OrderedItems.objects.filter(ordered__lte=datetime.datetime.now().date(),ordered__gte=last_week,status='delivered')
    print('success')
    print(orders)
    return render(request,'admin/salesReport.html',{'orders':orders})
def monthly(request):
    last_month = datetime.datetime.now().date() - timedelta(days=30)
    print(last_month)
    orders = OrderedItems.objects.filter(ordered__lte=datetime.datetime.now().date(),ordered__gte=last_month,status='delivered')
    print(orders)
    print('success')
    return render(request,'admin/salesReport.html',{'orders':orders})

def progressGraph(request):
    pass

