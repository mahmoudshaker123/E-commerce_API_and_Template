from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import Account
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            country = form.cleaned_data['country']
            password = form.cleaned_data['password']   
            email = form.cleaned_data['email'] 
            username = email.split('@')[0]
            phone_number = form.cleaned_data['phone_number']

            user = Account.objects.create_user(first_name=first_name , last_name=last_name , username=username , country=country , email=email , password=password)
            user.phone_number = phone_number
            user.save()