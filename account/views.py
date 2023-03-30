from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.models import User
from .models import customeruser
from django.contrib import messages
import re
import uuid
from .models import Profile
from cart.models import Cart
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

# register

def register(request):
    if request.method == "GET":
        return render(request, 'account/register.html')
    if request.method  == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        regex = r'[!@#$%^&*(),.?":{}|<>0-9]'
        try:
            if User.objects.filter(username=username).first():
                messages.info(request, 'Tài khoảng đã tồn tại')
                return redirect('account:register')
            if User.objects.filter(email=email).first():
                messages.info(request, 'Email đã tồn tại')
                return redirect('account:register')
            # if password != password1:
            #     messages.info(request, 'Mật khẩu không trùng khớp')
            #     return redirect('account:register')
        
            obj_user = User.objects.create(username=username, email =email)
            obj_user.set_password(password)
            obj_user.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = obj_user, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email=email, token=auth_token)
            messages.success(request, "tạo tài khoảng thành công vui lòng kiểm tra email để xác thực")
            return redirect('account:register')
        except Exception as e:
            return redirect('account:register')
        


def verify(request,auth_token):
    if request.method == "GET":
        try: 
            profile_obj = Profile.objects.get(auth_token=auth_token)
            if profile_obj:
                if profile_obj.is_verified:
                    messages.success(request, "xac thuc thanh cong")
                    return redirect('account:login') 
                profile_obj.is_verified = True
                profile_obj.save()
                Cart.objects.create(user = profile_obj.user)
                customeruser.objects.create(user = profile_obj.user, name =profile_obj.user.username)
                messages.success(request, "xac thuc thanh cong")
                return redirect('account:login')  
        except Exception as e:
            return redirect('account:register')



# send email register

def send_mail_after_registration(email , token):
    subject = "Your acccuss  need to be verified"
    message = f"Vui long truy cap vao lien ket de xac thuc tai khoan http://127.0.0.1:8000/account/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from , recipient_list)



# login
def login_(request):
    if request.method == "GET":
        return render(request, 'account/login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('core:index')
        else:
            messages.info(request, "Tài khoảng hoặc mật khẩu không đúng")
            return redirect('account:login')
        

def out(request):
    logout(request)
    return redirect('core:index')



# forgetpassword

def forgetpassword(request):
    if request.method == "GET":
        return render(request, 'account/forgetpassword.html')
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).first():
            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token= token
            profile_obj.save()
            sen_forget_password_mail(email=email, token=token)
            messages.success(request, 'Vui lòng kiểm tra email để forgetpassword')
            return redirect('account:forgetpassword')

# changepassword
def change(request, token):
    if request.method == "GET":
        try:
            profile = Profile.objects.get(forget_password_token=token)
        except Exception as e:
            print(e)
        return render(request, 'account/changepassword.html',{"profile":profile})
    
    if request.method == "POST":
        token = request.POST.get('token')
        user_id = request.POST.get('user_id')
        password2 = request.POST.get('password2')
        password3 = request.POST.get('password3')
        user = User.objects.get(id=user_id)
        if not user:
            messages.info(request, "tài khoảng không tồn tại")
            return redirect("account:change")
        if password2 !=password3:
            messages.info(request, "mật khẩu không khớp")
            return redirect("account:change")
        user.set_password(password2)
        user.save()
        return redirect('account:login')

        


# send email forgetpassword


def sen_forget_password_mail(email,token):
    subject = 'You forget password link'
    message = f'Hi, click on the link to reset your http://127.0.0.1:8000/account/change/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
                    


# đổi mật khẩu
def doimatkhau(request):
    if request.method == "GET":
        return render(request, 'account/doimatkhau.html')
    if request.method == "POST":
        currentPassword = request.POST.get('currentPassword')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')
        user = request.user
        my_user = authenticate(username = user.username, password = currentPassword)
        if my_user is not None:
            if newPassword == confirmPassword:
                user.set_password(newPassword)
                user.save()
                return redirect('core:profile')
            else:
                messages.info(request, "mật khẩu mới không khớp với confimpassword")
                return redirect("account:doimatkhau")
        else:
            messages.info(request, "mật khẩu không khớp với mật khẩu hiện tại")
            return redirect("account:doimatkhau")
        
        