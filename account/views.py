from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from random import randint
from django.core.mail import send_mail

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        if not User.objects.filter(email=request.POST['emailid']).exists():
            user=User()
            user.first_name= request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['emailid']
            user.username = request.POST['emailid']
            user.password = make_password(request.POST['password'])
            user.save()
            profile = Profile()
            profile.phone_number = request.POST['phonenumber']
            profile.address = request.POST['address']
            profile.user = user
            profile.save()
            messages.success(request, 'User is registered successfully')
            return render(request, 'register.html')
        else:
            messages.error(request, 'User is already registered')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method=='POST':
        user = authenticate(username= request.POST['emailid'], password = request.POST['password'])
        if user is not None:
            login(request , user)
            return redirect ('home')
        else:
            messages.error(request, 'Incorrect email id or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


def reset_password_view(request):
    if request.method == 'POST':
        if 'emailid' in request.POST:
            if User.objects.filter(email= request.POST['emailid']).exists():
                user= User.objects.get(email= request.POST['emailid'])
                otp = str(randint(100000,999999))
                profile = Profile.objects.get(user_id = user.id)
                profile.password_reset_code = otp
                profile.save()
                subject = "One Time Password(OTP) to reset your password"
                message = "Your OTP to reset your IceCreamsCorner account is: " + otp
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['emailid']]
                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                except Exception:
                    messages.error(request, "Something went wrong! Please try again.")
                    return render(request, 'resetpassword.html')
                else:
                    messages.success(request, "OTP is mailed successfully to your registered email id")
                    return render(request, 'resetpassword.html', {"OTP_Status": 'generated', 'user_id': request.POST['userid']})
            else:
                messages.error(request, 'Email id is not registered')
                return render(request, 'resetpassword.html')
        elif 'otp' in request.POST:
            otp = request.POST['otp']
            profile = Profile.objects.get(user_id = request.POST['userid'])
            if profile.password_reset_code == otp:
                messages.success(request, 'OTP is verified')
                return render(request, 'resetpassword.html', {"OTP_Status": 'verified', 'user_id':request.POST['userid']})
            else:
                messages.error(request, 'Incorrect OTP')
                return render(request, 'resetpassword.html' ,{"OTP_Status": 'generated', 'user_id': request.POST['userid']})
        else:
            newpassword= request.POST['newpassword']
            confirmpassword = request.POST['confirmpassword']
            if newpassword == confirmpassword:
                user = User.objects.get(id= request.POST['userid'])
                user.set_password(newpassword)
                user.save()
                messages.success(request, 'Password is reset succesfully')
                return render(request, 'resetpassword.html')
            else:
                messages.error(request, 'New and Confirm password mismatched')
                return render(request, 'resetpassword.html', {"OTP_Status": 'verified', "user_id":request.POST['userid']})
    else:
        return render(request, 'resetpassword.html')

