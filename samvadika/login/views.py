from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import random


User=get_user_model()
# Create your views here.
def index(request):

    print(request.user)

    if request.user.is_anonymous:
       return redirect('/login')

   

    else :
        l=[]
        u=User.objects.get(user_name=request.user)
        
        q=Question.objects.order_by('-pub_date')
        for eq in q:
            if Reply.objects.filter(threadid=eq.threadid).exists():
                rp=Reply.objects.filter(threadid=eq.threadid)
                l.append([eq,rp])
            else:
                l.append([eq,''])
        
       
        return render(request,'index.html',{"query":l , "user":u})

def signup(request):
    return render(request, 'signup.html')


def User_login(request):
        return    render(request, 'login.html')

def action_(request):
    username=request.POST.get('email')
    password=request.POST.get('password')
    
    user=authenticate(request,email=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('/')
    else:
        messages.success(request, 'Incorrect Email or Password')
        return render(request, 'login.html')
def register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        print(username)
        print(password)
        if password!=confirm_password:
            messages.warning(request, 'Mismatch in Password and Confirm Password')
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return render(request, 'signup.html')
        else:
            
            user = User.objects.create_user( email, username, first_name, password)
            user.save()
            return redirect('/')
def User_logout(request):
    logout(request)
    return render(request,'login.html')

def posted(request):
    
   
    if request.method=="POST":   
        samvad = request.POST['samvad']

        q = Question( question=samvad,user_name=request.user)
        q.save()
    
        print(samvad)


    return redirect('/')


def Find_people(request):
    return render(request, 'findpeople.html')

def Notifications(request):
    return render(request, 'notifications.html')

def Saved_items(request):
    return render(request, 'saveditems.html')

def Update_profile(request):
    return render(request, 'updateprofile.html')


def answer(request):
    if request.method=="POST":   
        r = request.POST['ans']
        thread= request.POST['threadid']
        

   
    i= Question.objects.get(threadid=thread)

    u = Reply(reply=r,threadid=i,user_name=request.user )
    u.save()
   
  
    
    return redirect( '/')
    
def update_name(request):
    print("did we reach here")
    
    if request.method=="POST":   
        name=request.POST['first_name']
        user=User.objects.get(user_name=request.user)
        user.first_name=name
        user.save()
    
        print('name changed')
    return redirect('/updateprofile')
def update_email(request):
    print("did we reach here username block")
    
    if request.method=="POST":   
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exist!')
        else:
            user = User.objects.get(user_name=request.user)
            print('get user')
            user.email=email
            print('do view change')

            user.save()
            print('set username')
    return redirect('/updateprofile')

def update_pwd(request):
    print("did we reach here pwd block")
    
    if request.method=="POST":
        pwd=request.POST.get('password')
        user=User.objects.get(user_name=request.user)
        user.set_password(pwd)
        user.save()
        print('password changed')
    return redirect('/updateprofile')
def update_img(request):
    print("did we reach here img block")
    
    if request.method=="POST":
        user=User.objects.get(user_name=request.user)
        if user.image!='pic.jpeg':
            user.image.delete()
        user.image=request.FILES['myfile']
        user.save()
    return redirect('/updateprofile')
