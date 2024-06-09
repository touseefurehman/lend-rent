from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.helpers import send_forget_password_mail
from accounts.models import MyUser
from qrcode import *
from django.contrib.auth.hashers import make_password, check_password
# below library for generating random strings
import uuid
from accounts.helpers import EmailThread
# Register

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import MyUser

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        mail = request.POST.get('email')
        pass1 = request.POST.get('password')
        ph_code = request.POST.get('phonecode')
        ph = request.POST.get('Pnumber')
        agree = request.POST.get('agree')
        phone = ph_code + ph

        agreeTerms = False
        if agree:
            agreeTerms = True
        
        eunmae = MyUser.objects.filter(email=mail)
        phx = MyUser.objects.filter(mobile_number=phone)
        
        if eunmae:
            messages.warning(request, 'Email already exists')
        elif phx:
            messages.warning(request, 'Phone Number already exists')
        elif len(pass1) < 8:
            messages.warning(request, 'Password Length should be 8 characters')
        else:
            user = MyUser.objects.create_user(
                email=mail,
                name=uname, 
                password=pass1,
                mobile_number=phone,
                agree=agreeTerms
            )
            
            user = authenticate(email=mail, password=pass1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Your account has been created and you are now logged in')
                return redirect('rent')
            else:
                messages.error(request, 'There was an error logging you in')
                
    return render(request, 'signup.html')



# Create your views here.
# Login

def loginuser(request):
    error_message = None  # Initialize error_message

    if request.method == 'POST':
        mail = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        # print(mail, pass1)
        a = MyUser.objects.filter(email=mail, password=pass1).last()
        print(a)
        user1 = authenticate(request, email=mail, password=pass1)
        print(user1)
        if user1 is not None:
            login(request, user1, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/rent/')
        else:
             error_message = "User does not exist or invalid credentials."
    return render(request, 'login.html',{'error_message': error_message})


# Logout

def logoutuser(request):
    logout(request)
    return redirect('login_user')

# Forgot Password


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not MyUser.objects.filter(email=email).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forgotPassword')

            user_obj = MyUser.objects.get(email=email)

            mail = user_obj.username
            print(mail)
            token = str(uuid.uuid4())
            user_obj.forget_password_token = token
            user_obj.save()
            EmailThread(request, user_obj.email, token).start()
            messages.success(
                request, f'An email is sent to your email address {mail}.')
            return redirect('forgotPassword')

    except Exception as e:
        print(e)
    return render(request, 'forget.html')


# Change Password
def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = MyUser.objects.get(forget_password_token=token)
        print(profile_obj)
        context = {'user_id': profile_obj.id}
        print(context)
        if request.method == 'POST':
            id = request.POST.get('u_id')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            print(id, pass1, pass2)
            if id is None:
                messages.warning(request, 'no user found')
                return redirect(f'resest_password/{token}')
            if pass1 != pass2:
                messages.warning(request, 'both passwords should be same ')
                return redirect(f'{token}')
            userobj = MyUser.objects.get(id=id)
            userobj.set_password(pass1)
            userobj.save()
            messages.success(
                request, 'your password has been updated successfully now you can login')
            return redirect('login_user')

    except Exception as e:
        print(e)
    return render(request, 'reset.html', context=context)

def setup_profile(request):


    if request.method == "POST":
        location= request.POST.get('location')
        number= request.POST.get('number')
        about= request.POST.get('about')
        profile_img= request.FILES.get('image')


        user.location=location
        user.mobile_number=number
        user.about_me=about
        user.save()






    return render(request, 'profile/setup_profile.html')










def profile(request):
    user=request.user
    print(user.about_me)
    

    
    return render(request, "profile/profile.html", {'user': user})



def edit_profile(request):
    user=request.user
    if request.method == 'POST':    
        name= request.POST.get('name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        location= request.POST.get('location')
        about= request.POST.get('about')
        number= request.POST.get('number')
        image=request.FILES.get('image')
        
        print(image)

        if image:
            user.profile_img = image
        user.name=name
        user.email=email
        user.location=location
        user.about_me=about
        user.mobile_number=number
        user.last_name=last_name
        user.save()
        return redirect('profile')

    return render(request, "profile/edit_profile.html",{'user': user})




