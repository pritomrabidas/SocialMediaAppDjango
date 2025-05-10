import django.conf
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from social.settings import EMAIL_HOST_USER
from .models import User
from django.contrib import messages
import random
from django.conf import settings

def register(request):
    if request.method == 'POST':
        fullName = request.POST.get('fullName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        if password == confirmPassword:
            otp = random.randint(100000, 999999)
            user = User.objects.create_user(
                fullName=fullName,
                username=username,
                email=email,
                password=password,
            )
            user.otp = str(otp)
            user.save()
            send_email(email, otp)
            return redirect('varification')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/registration.html')
    return render(request, 'auth/registration.html')

def send_email(email, otp):
    try:
        subject = 'welcome to our site'
        message = f'Your OTP is {otp}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
def varification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp:
            user  = User.objects.filter(otp=otp).first()
            if user:
                user.is_verified = True
                user.save()
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP.')
                return render(request, 'auth/varification.html')
        
    return render(request, 'auth/varification.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_verified:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Please verify your email first.')
                return redirect('varification')
    return render(request, 'auth/login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def profile(request):
    return render(request, 'auth/profile.html')