from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from account.forms import CoupenForm
from account.models import Account
from django.contrib import messages
from coupen.models import Coupen
from proj.models import Order, OrderItems

# Create your views here.


def coupenAdimin(request):
    form = CoupenForm()
    coupen = Coupen.objects.all().order_by('id')
    context = {
        'coupen':coupen,
        'coupen_form':form
    }

    return render(request,'admin/coupen.html',context)


def createCoupen(request):
    some_value = Coupen.objects.all()
    if request.method == 'POST':
        form = CoupenForm(request.POST)
        print(form.instance)
        if form.is_valid():
                form.save()
                return redirect(coupenAdimin)

    return redirect(coupenAdimin)
def trashCoupen(request,id):
    coupen = Coupen.objects.get(id=id)
    coupen.delete()
    return redirect(coupenAdimin)


    



