from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate , login as login_auth , logout

# Activation Email  عشان اعمل اكتيف لليوزر بعد التسجيل
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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

            #User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('accounts/account_verification_email.html' ,{
                'user': user ,
                'domain': current_site ,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject , message , to=[to_email])
            send_mail.send()
            return redirect('login'+f'?command=verification&email={email}')
        
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }

    return render(request , 'accounts/register.html' , context)  


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request , email=email , password=password)
        if user is not None:
            login_auth(request , user)
            return redirect('home')
        else:
            return redirect('accounts:login')
        
    return render(request , 'accounts/login.html')
        
def activate(request , uidb64 , token):
    pass