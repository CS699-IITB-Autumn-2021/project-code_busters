from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import random

#f2

User=get_user_model()
# Create your views here.
def index(request):

    print(request.user)

    if request.user.is_anonymous:
       return redirect('/login')

   

    else :
        l=[]
        u=User.objects.get(user_name=request.user)
        sav = SaveQuestion.objects.filter(user_name=request.user)
        s=[]
        try:
            for my in sav:
                
               s.append(my.threadid.threadid)

        except:
            print("no value")


        print(s)   

        q=Question.objects.order_by('-pub_date')
        for eq in q:
            qtag=Tag.objects.filter(threadid=eq.threadid)
            print(qtag[0].tag_name)
            if Reply.objects.filter(threadid=eq.threadid).exists():
                rp=Reply.objects.filter(threadid=eq.threadid)
                l.append([eq,rp,qtag])
            else:
                l.append([eq,'',qtag])
        
       
        return render(request,'index.html',{"query":l , "user":u , "save":s })

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
        if User.objects.filter(user_name=username).exists():
            messages.warning(request, 'Username already taken')
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

        user = User.objects.get(user_name=request.user)
        user.score = user.score + 10
        user.save()

        tag_names=request.POST.getlist('tag')

        q = Question( question=samvad,user_name=request.user)
        q.save()
        for tag_name in tag_names:
            tg=Tag(tag_name=tag_name,threadid=q)
            tg.save()
        print(samvad)
    return redirect('/')

def Find_people_check(request):
    l =  []
    temp = ""
    user = request.user
    if not user.interest_form_submitted:
        #temp = 'interestsform.html'
        return render(request, 'interestsform.html')
    else:
        l = User.objects.all()
        li = []
        for h in l:
            if Hobby.objects.filter(user_name=h).exists():
                rp=Hobby.objects.filter(user_name=h)
                if h != user:
                    li.append([h,rp])
            else:
                li.append([h,''])

        #temp = 'findpeople.html'

        return render(request,'findpeople.html',{"query":li}) 

def Notifications(request):
    return render(request, 'notifications.html')

def Saved_items(request):

    try:
        if request.method=="GET":   
            thread=request.GET['threadid']
       
            i= Question.objects.get(threadid=thread)
        
            s= SaveQuestion(threadid=i,user_name=request.user)
      
            s.save()
       

            return redirect('/')
    except:
        u=User.objects.get(user_name=request.user)
        print(u.score)

        save = SaveQuestion.objects.filter(user_name=request.user)
        s=[]
        for x in save:
            
            
            q = Question.objects.get(threadid=x.threadid.threadid)
            s.append(q)

            s = s[::-1]
            


    
        return render(request,'saveditems.html',{"user":u , "save":s})

def Update_profile(request):
    return render(request, 'updateprofile.html')


def answer(request):
    if request.method=="POST":   
        r = request.POST['ans']
        thread= request.POST['threadid']
        

   
    i= Question.objects.get(threadid=thread)

    u = Reply(reply=r,threadid=i,user_name=request.user )
    u.save()

    user = User.objects.get(user_name=request.user)
    user.score = user.score + 10
    user.save()
   
  
    
    return redirect('/')
    
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


def Updateinterests(request):
    if request.method=="POST":  
        user=User.objects.get(user_name=request.user)
        interest_list=request.POST.getlist('hobbies_list')
        user.fb_link+=request.POST.get('fb_url')
        user.linkedin_link+=request.POST.get('linkedin_url')
        user.interest_form_submitted = True

        for hobby in interest_list:
            h = Hobby(hobby_name=hobby,user_name=request.user)
            h.save()
          
        user.save()
    
        
    return redirect('/findpeople')

def filter_people(request):
    if request.method=="POST": 
        if 'find_people_sumbit' in request.POST: 
            interest_filter_list=request.POST.getlist('hobbies_filter_list')
            user = request.user                                                                                                                                                                                                                                                                                                                              
            l = User.objects.all()
            li = []
               
            for filter_hobby in interest_filter_list:
             
                for h in l:
                    if Hobby.objects.filter(user_name=h, hobby_name=filter_hobby).exists():
                        rp=Hobby.objects.filter(user_name=h)
                        if h != user:
                            li.append([h,rp])
            return render(request,'findpeople.html',{"query":li}) 
        else:
            return redirect('/findpeople')


def Reset_filter_people(request):
    return redirect('/findpeople')

def filter_questions(request):
    if request.method=="POST":  
        if 'filter_multiple' in request.POST:
    
            tag_filter_list=request.POST.getlist('tag_filter_list')     
            print(tag_filter_list)                                                                                                                                                                                                                                                                                     
            q = Question.objects.all()
            li = []
               
            for qn_tag in tag_filter_list:
             
                for qn in q:
                    if Tag.objects.filter(tag_name=qn_tag,threadid=qn.threadid).exists():
                        rp=Tag.objects.filter(threadid=qn.threadid)
                        li.append([qn,rp])
            return render(request,'filterquestions.html',{"query":li}) 
        
        else:
            return redirect('/')


def reset_filter_questions(request):
    return redirect('/')

def saving(request):
    print("I am defined")
    try:
        if request.method=="GET":   
            thread=request.GET['threadid']
       
            i= Question.objects.get(threadid=thread)
        
            s= SaveQuestion(threadid=i,user_name=request.user)
      
            s.save()
            return HttpResponse("SUCCESS")
    except:  

        thread=request.GET['threadid']
        print(thread," i will delete this ")
        i= Question.objects.get(threadid=thread)
        s= SaveQuestion.objects.get(threadid=i,user_name=request.user).delete()
    


        return HttpResponse("FAILED")

def remove(request):  
    thread=request.GET['threadid']
    
    i= Question.objects.get(threadid=thread)
    s= SaveQuestion.objects.get(threadid=i,user_name=request.user).delete()

    return redirect('/saveditems')
    

   

def filterbytags(request):
    return render(request, 'filterquestions.html')

