from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse




# # Create your views here.
#
# def register_view(request):
#     form = CustomUserCreationForm()
#     if request.method == 'POST':
#         print('success')
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print('successfully registered')
#             return redirect(reverse('register'))
#     return render(request, 'user_register.html', {'form': form})
#
#
