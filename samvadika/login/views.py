from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import random
import datetime
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
        
        q=Question.objects.order_by('-pub_date')
        for eq in q:
            qtag=Tag.objects.filter(threadid=eq.threadid)
            print(qtag[0].tag_name)
            if Reply.objects.filter(threadid=eq.threadid).exists():
                rp=Reply.objects.filter(threadid=eq.threadid)
                l.append([eq,rp,qtag])
            else:
                l.append([eq,'',qtag])
        
        s=Save.objects.filter(user_name=request.user)

        return render(request,'index.html',{"query":l , "user":u,"save":s})

def signup(request):
    return render(request, 'signup.html')

def saving(request):

    
    try:
        id = Question.objects.get(threadid=request.GET['threadid'])    
        s= Save(threadid=id,user_name=request.user)
        s.save()
        print(id.threadid)
        print(id.user_name)
        print(timezone.now())
        st = str(request.user) + " has saved the question (ThreadId - "+ str(id.threadid) +") posted by you."
        print(st)
        n = Notify(message=st,user_name=id.user_name)
        n.save()
        
        return HttpResponse("SUCCESS")

    except:
        id = Question.objects.get(threadid=request.GET['threadid'])
        Save.objects.get(threadid=id,user_name=request.user).delete()
        return HttpResponse("Failed")



def User_login(request):
        return    render(request, 'login.html')

def remove(request):
    id = request.GET['threadid']
    id = Question.objects.get(threadid=id)

    Save.objects.get(threadid=id,user_name=request.user).delete()

    return redirect("/saveditems")


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
        tag_names=request.POST.getlist('tag')
        u=User.objects.get(user_name=request.user)
        u.score+=10
       
        q = Question( question=samvad,user_name=request.user)
        q.save()

        q = Question.objects.get(question=samvad)

        n = Notify(message="You gained 10 points on posting question (Threadid - " + str(q.threadid)+"). Now your score is "+str(u.score),user_name=request.user)
        u.save()
        n.save()

        

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

    n = Notify.objects.filter(user_name=request.user)
    s=[]
    for x in n:
        s.append(x)

    s.reverse()

    return render(request, 'notifications.html',{"notify":s})

def Saved_items(request):

    s=Save.objects.filter(user_name=request.user)

    l=[]

    for q in s:
        
        l.append(Question.objects.get(threadid=q.threadid.threadid))

    l.reverse()

     

    return render(request, 'saveditems.html',{"save":l})

def Update_profile(request):
    return render(request, 'updateprofile.html')


def answer(request):
    if request.method=="POST":   
        r = request.POST['ans']
        thread= request.POST['threadid']
        
    u=User.objects.get(user_name=request.user)
    i= Question.objects.get(threadid=thread)

    u = Reply(reply=r,threadid=i,user_name=request.user )
    u.save()
    u=User.objects.get(user_name=request.user)
    u.score+=10
    u.save()
    n = Notify(message="You gained 10 points on answering a question (Threadid - "+ str(i.threadid) +"). Now your score is "+str(u.score),user_name=request.user)
    n.save()
    st =  str(request.user) + " has answered the question (ThreadId - "+ str(i.threadid) +") posted by you."
    print(st)
    n = Notify(message=st,user_name=i.user_name)
    n.save()
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

            hobby={}

            
            print(len(li))
            send=[]
            for i in li:
                print(i[0]," ",i[1] )
                hobby[i[0]]=[]
            
            for i in li:
                hobby[i[0]].extend(i[1])

            for i in hobby.keys():
                hobby[i] = set(hobby[i])

            for k in hobby.keys():
                send.append([k, hobby[k]])

            send = list(send)
            # for i in range(0,len(li)):
            #     #print( li[i])
            #     print( li[i][i])
            #     print( li[i][1][i].hobby_name)

            # for x in li:
            #     hobby[x[0][0]].append(x[0][1][0].hobby_name)

            # for x in li:
            #     hobby[x[0][0]] = set(hobby[x[0][0]])

            # for keys in hobby.keys():
            #     print( hobby[keys] ) 
            # print("printed dictionary")
            
            return render(request,'findpeople.html',{"query":send}) 
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

def filterbytags(request):
    return render(request, 'filterquestions.html')

def save_upvote(request):
    if request.method == 'POST':
        replyid = request.POST['replyid']
        reply = Reply.objects.get(pk=replyid)
        user = request.user
        check_upvotes=UpVote.objects.filter(reply=reply,user=user).count()
        check_downvotes=DownVote.objects.filter(reply=reply,user=user).count()
        if check_upvotes > 0:
            UpVote.objects.filter(reply = reply,user=user).delete()
            return JsonResponse({'bool':False,'other':False})
        elif(check_downvotes > 0):
            DownVote.objects.filter(reply = reply,user=user).delete()
            UpVote.objects.create(
                reply = reply,
                user = user
            )
            return JsonResponse({'bool':True,'other':True})
        else:
            UpVote.objects.create(
                reply = reply,
                user = user
            )
            return JsonResponse({'bool':True,'other':False})

def save_downvote(request):
    if request.method == 'POST':
        replyid = request.POST['replyid']
        reply = Reply.objects.get(pk=replyid)
        user = request.user
        check_downvotes=DownVote.objects.filter(reply=reply,user=user).count()
        check_upvotes=UpVote.objects.filter(reply=reply,user=user).count()
        if check_downvotes > 0:
            DownVote.objects.filter(reply = reply,user=user).delete()
            return JsonResponse({'bool':False,'other':False})
        elif(check_upvotes > 0):
            UpVote.objects.filter(reply = reply,user=user).delete()
            DownVote.objects.create(
                reply = reply,
                user = user
            )
            return JsonResponse({'bool':True,'other':True})
        else:
            DownVote.objects.create(
                reply = reply,
                user = user
            )
            return JsonResponse({'bool':True,'other':False})

def save_like(request):
    if request.method == 'POST':
        threadid = request.POST['threadid']
        question = Question.objects.get(pk=threadid)
        user = request.user
        check_likes = Like.objects.filter(question = question,user=user).count()
        check_dislikes=Dislike.objects.filter(question = question,user=user).count()        
        if check_likes > 0:
            Like.objects.filter(question = question,user=user).delete()
            return JsonResponse({'bool':False,'other':False})
        elif check_dislikes > 0:
            Dislike.objects.filter(question = question,user=user).delete()
            Like.objects.create(
                question = question,
                user = user
            )
            return JsonResponse({'bool':True,'other':True})
        else:
            Like.objects.create(
                question = question,
                user = user
            )
            return JsonResponse({'bool':True, 'other':False})

def save_dislike(request):
    if request.method == 'POST':
        threadid = request.POST['threadid']
        question = Question.objects.get(pk=threadid)
        user = request.user
        check_dislikes=Dislike.objects.filter(question = question,user=user).count()
        check_likes = Like.objects.filter(question = question,user=user).count()
        if check_dislikes > 0 :            
            Dislike.objects.filter(question = question,user=user).delete()
            return JsonResponse({'bool':False,'other':False})
        
        elif check_likes > 0 :
            Like.objects.filter(question = question,user=user).delete()
            Dislike.objects.create(
                question = question,
                user = user
            )
            return JsonResponse({'bool':True,'other':True})
        else:
            Dislike.objects.create(
                question = question,
                user = user
            )
            return JsonResponse({'bool':True,'other':False})