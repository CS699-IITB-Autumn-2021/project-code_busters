from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import *
import random


User=get_user_model()
# Create your views here.
def index(request):

    print(request.user)
    

    if request.user.is_anonymous:
       return redirect('/login')


    q=Question.objects.order_by('-pub_date')
    
    

    
    return render(request,'index.html',{"query":q , "user":request.user })
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
        return render(request,'index.html')
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
            return render(request, 'index.html')
def User_logout(request):
    logout(request)
    return render(request,'login.html')

def posted(request):
    print("did we reach here")
    count = random.randint(0,200000000)
    if request.method=="POST":   
        samvad = request.POST['samvad']

        q = Question( question=samvad,threadid=count,user_name=request.user)
        q.save()
    
        print(samvad)


    return redirect('/')