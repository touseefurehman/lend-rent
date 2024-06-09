from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect


from django.shortcuts import render
from django.conf import settings
import stripe
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
#from log.models import bio

User = get_user_model()












def forget(request):
    if request.method=="POST":
        email = request.POST.get("email")
        if not User.objects.filter(email=email).exists():
            messages.warning(request, "User Not exist in the databasse")
            
        
    return render(request,'forget.html')
def pass_reset(request):
    return render(request,'authentication/pass_reset.html')
def home(request):
    return render(request,'home.html')


def rent(request):
    return render(request,'rent.html')

def lend (request):
    return render(request,'lend.html')









def profile(request):
    return render(request,'profile.html')


def checkout(request):
    return render(request, 'checkout.html')





def search(request):
    return render(request,'search.html')


def rental(request):
    return render(request,'rental.html')
def rental_list(request):
    
    return render(request,'rental_list.html')








 
 
 
def search(request):
    return render(request,'search_pages/search.html')
 
 
def confirm(request):
    return render(request,'conformation_message/conformation_message.html')