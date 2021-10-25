from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import random
import datetime


User=get_user_model()
# Create your views here.
def index(request):
    """Display the Samvadika home page if the user is authenticated otherwise through user to the login webpage. It show all the question with their threadid, published date, question tag along with 
    reply, save-item, like and dislike option.
    :param request: contains the metadata about the request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Samvadika home webpage for authenticated user and login webpage for unauthenticated user.
    :rtype: HttpResponse object - for authenticated user, HttpResponseRedirect object - for unauthenticated user
    """
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

        print(l)

        return render(request,'index.html',{"query":l , "user":u,"save":s})

def signup(request):
    """Take User to the Signup Webpage.
    :param request: contains the metadata of the signup request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Signup webpage for new registration.
    :rtype: HttpResponse object
    """
    return render(request, 'signup.html')

def saving(request):

    
    try:
        id = Question.objects.get(threadid=request.GET['threadid'])    
        s= Save(threadid=id,user_name=request.user)
        s.save()
        print(id.threadid)
        print(id.user_name)
        print(timezone.now())

        if(request.user!= id.user_name):
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
    """Take user to the login webpage.
    :param request: contains the metadata of the login request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Login webpage.
    :rtype: HttpResponse object
    """
    return    render(request, 'login.html')

def remove(request):
    id = request.GET['threadid']
    id = Question.objects.get(threadid=id)

    Save.objects.get(threadid=id,user_name=request.user).delete()

    return redirect("/saveditems")


def remove(request):
    id = request.GET['threadid']
    id = Question.objects.get(threadid=id)

    Save.objects.get(threadid=id,user_name=request.user).delete()

    return redirect("/saveditems")


def action_(request):
    """Authenticate the user by confirming there Email ID and password. If there is mismatch then it display the warning and take user to login page otherwise on successfully login it
    user to samvadika home page.
    :param request: contains the metadata of the login action request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Samvadika home webpage if user is authenticated or Login webpage for unauthenticated user.
    :rtype: HttpResponse object - if user is unauthenticated, HttpResponseRedirect object - if user is authenticated
    """
    username=request.POST.get('email')
    password=request.POST.get('password')
    
    user=authenticate(request,email=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('/')
    else:
        messages.warning(request, 'Incorrect Email or Password')
        return render(request, 'login.html')


def register(request):
    """Successfully register the new user by storing it details in the database. If there is some mismatch in password and confirm password or the email and username 
    which new user used to register himself already be in use then it display warning message and user to signup page otherwise it take user to home page. 
    :param request: contains the metadata of the signup action request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Samvadika home webpage if user is successfully registered otherwise signup webpage.
    :rtype: HttpResponse object
    """
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

            u = User.objects.get(user_name=username)

            n = Notify(message="You have gained 5 bonus points on joining SAMVADIKA" , user_name=u)
            n.save()
            return redirect('/')
def User_logout(request):
    """Logout user and take him to login page.
    :param request: contains the metadata of the logout request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Login webpage.
    :rtype: HttpResponse object
    """
    logout(request)
    return render(request,'login.html')

def posted(request):
    """Store the posted question in the database and redirect user to the home page.
    :param request: contains the metadata of the question posting request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Samvadika home webpage.
    :rtype: HttpResponseRedirect object
    """
   
    if request.method=="POST":   
        samvad = request.POST['samvad']
        tag_names=request.POST.getlist('tag')
        u=User.objects.get(user_name=request.user)
        u.score+=10
        u.save()

        q = Question( question=samvad,user_name=request.user)
        q.save()

        q = Question.objects.get(question=samvad)

        n = Notify(message="You gained 10 points on posting question (Threadid - " + str(q.threadid)+"). Now your score is "+str(u.score),user_name=request.user)
        n.save()

        

        for tag_name in tag_names:
            tg=Tag(tag_name=tag_name,threadid=q)
            tg.save()
        print(samvad)
    return redirect('/')

def Find_people_check(request):
    """Display Interest form for the first time to the user and after fillup that form it display the list of all the user with their hobbies.
    :param request: contains the metadata of the request to find the people e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: interestsform webpage if user not fill his/her interest otherwise findpeople webpage with list of all user with their hobbies.
    :rtype: HttpResponse object
    """

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
    """
    :param request: contains the metadata of the request to goto Notifications webpage e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Notifications webpage which display all the notifications to the user.
    :rtype: HttpResponse object
    """

    n = Notify.objects.filter(user_name=request.user)
    s=[]
    for x in n:
        s.append(x)

    s.reverse()

    return render(request, 'notifications.html',{"notify":s})

def Saved_items(request):
    """Display all the questions which are saved by the user.
    :param request: contains the metadata of the request to the Saved item webpage e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Saveditem webpage that shows all the item saved by the user.
    :rtype: HttpResponse object
    """

    s=Save.objects.filter(user_name=request.user)

    l=[]
    u=User.objects.get(user_name=request.user)
    for q in s:
        
        l.append(Question.objects.get(threadid=q.threadid.threadid))

    l.reverse()

    x=[]
    for eq in l:
        qtag=Tag.objects.filter(threadid=eq.threadid)
        print(qtag[0].tag_name)
        if Reply.objects.filter(threadid=eq.threadid).exists():
            rp=Reply.objects.filter(threadid=eq.threadid)
            x.append([eq,rp,qtag])
        else:
            x.append([eq,'',qtag])
        
        print(x)

    return render(request, 'saveditems.html',{"user":u,"query":x})


def Update_profile(request):
    """Take user to the update profile page from where he/she update his details.
    :param request: contains the metadata of the request to update profile e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: updateprofile webpage which provide the options to update the user profile.
    :rtype: HttpResponse object
    """
    return render(request, 'updateprofile.html')


def answer(request):
    """Store the replies to the question in the database and redirect user to the home page. 
    :param request: contains the metadata of the request to answering the question(reply) e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Samvadika home webpage.
    :rtype: HttpResponseRedirect object
    """
    if request.method=="POST":   
        r = request.POST['ans']
        thread= request.POST['threadid']
        
    u=User.objects.get(user_name=request.user)

    i= Question.objects.get(threadid=thread)

    u = Reply(reply=r,threadid=i,user_name=request.user )
    u.save()
    u=User.objects.get(user_name=request.user)
    
    if(request.user != i.user_name):
        n = Notify(message="You gained 10 points on answering a question (Threadid - "+ str(i.threadid) +") posted by "+ str(i.user_name) +". Now your score is "+str(u.score),user_name=request.user)
        n.save()
        st =  str(request.user) + " has answered the question (ThreadId - "+ str(i.threadid) +") posted by you."
        print(st)
        n = Notify(message=st,user_name=i.user_name)
        n.save()
        u.score+=10
        u.save()
    return redirect('/')
    
def update_name(request):
    """Update the user name.
    :param request: contains the metadata of the request to update name of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: updateprofile webpage with updated user name.
    :rtype: HttpResponseRedirect object
    """
    print("did we reach here")
    
    if request.method=="POST":   
        name=request.POST['first_name']
        user=User.objects.get(user_name=request.user)
        user.first_name=name
        user.save()
    
        print('name changed')
    return redirect('/updateprofile')
def update_email(request):
    """Update the email of the user.
    :param request: contains the metadata of the request to update email of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: updateprofile webpage with updated user email.
    :rtype: HttpResponseRedirect object
    """
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
    """Update the password of the user.
    :param request: contains the metadata of the request to update password of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: updateprofile webpage with updated password.
    :rtype: HttpResponseRedirect object
    """
    print("did we reach here pwd block")
    
    if request.method=="POST":
        pwd=request.POST.get('password')
        user=User.objects.get(user_name=request.user)
        user.set_password(pwd)
        user.save()
        print('password changed')
    return redirect('/updateprofile')



def update_fb_link(request):
    """Changed the Facebook profile link of the user.
    :param request: contains the metadata of the request to changed hobbies of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: updateprofile webpage with updated Facebook Profile link.
    :rtype: HttpResponseRedirect object
    """
    user=User.objects.get(user_name=request.user)
    if not user.interest_form_submitted:
        return redirect('/findpeople')
    if request.method=="POST":
        user.fb_link='https://www.facebook.com/'+request.POST.get('fb_url')
        user.save()
    return redirect('/updateprofile')

def update_linkedin_link(request):
    """Changed the LinkedIn profile link of the user.
    :param request: contains the metadata of the request to changed hobbies of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: updateprofile webpage with updated LinkedIn Profile link.
    :rtype: HttpResponseRedirect object
    """
    user=User.objects.get(user_name=request.user)
    if request.method=="POST":
        user.fb_link='https://www.linkedin.com/in/'+request.POST.get('linkedin_url')
        user.save()
    return redirect('/updateprofile')

def update_hobbies(request):
    """Changed the Hobbies of the user.
    :param request: contains the metadata of the request to changed hobbies of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return:updateprofile webpage with updated user hobbies.
    :rtype: HttpResponseRedirect object
    """
    if request.method=="POST":
        user=User.objects.get(user_name=request.user)
        hobby_obj=Hobby.objects.filter(user_name=user)
        for obj in hobby_obj:
            obj.delete()
        interest_list=request.POST.getlist('hobbies_list')
        for hobby in interest_list:
            h = Hobby(hobby_name=hobby,user_name=request.user)
            h.save()

    return redirect('/updateprofile')

def update_img(request):
    """Update the profile picture of the user.
    :param request: contains the metadata of the request to update image of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: updateprofile webpage with updated user image.
    :rtype: HttpResponseRedirect object
    """
    print("did we reach here img block")
    
    if request.method=="POST":
        user=User.objects.get(user_name=request.user)
        if user.image!='pic.jpeg':
            user.image.delete()
        user.image=request.FILES['myfile']
        user.save()
    return redirect('/updateprofile')


def Updateinterests(request):
    """Update the user interests i.e. hobbies with there social media link like Facebook link, LinkedIn link. So that it is easier to find the people of same kind of interest and to link with them through social media.
    :param request: contains the metadata of the request to update interests of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: findpeople webpage where user see all users interest and option to contact him e.g. facebook, LinkedIn.
    :rtype: HttpResponseRedirect object
    """
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
    """Filter the people by hobbies. It also allow to display multiple hobby users at a time.
    :param request: contains the metadata of the request to filter user by their hobbies e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: findpeople webpage with list of all filtered user.
    :rtype: HttpResponse object
    """
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
    """Reset the filter to find people and allow user to adjust filter from starting.
    :param request: contains the metadata of the request to reset filter to find people e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: findpeople webpage.
    :rtype: HttpResponseRedirect object
    """
    return redirect('/findpeople')

def filter_questions(request):
    """Filter the questions by the tags and show all filtered question with their replies.  
    :param request: contains the metadata of the request to filter questions by the tags e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: filterquestions webpage with list of all filtered question with their replies.
    :rtype: HttpResponse object
    """
    if request.method=="POST":  
        if 'filter_multiple' in request.POST:
    
            tag_filter_list=request.POST.getlist('tag_filter_list')     
            print(tag_filter_list)                                                                                                                                                                                                                                                                                     
            q = Question.objects.all()
            li=[]
               
            for qn_tag in tag_filter_list:
             
                for qn in q:
                    if Tag.objects.filter(tag_name=qn_tag,threadid=qn.threadid).exists():
                        rp=Tag.objects.filter(threadid=qn.threadid)
                        li.append([qn,rp])
            return render(request,'filterquestions.html',{"query":li}) 
        
        else:
            return redirect('/')


def reset_filter_questions(request):
    """Reset the filter to find people and allow user to adjust filter from starting.
    :param request: contains the metadata of the request to reset filter to find question e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: Home webpage from where user reset question tag for filter.
    :rtype: HttpResponseRedirect object
    """
    return redirect('/')

def filterbytags(request):
    """Through the user to the webpage from where user filter the questions by specifying tag.
    :param request: contains the metadata of the request for the tag filter e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: filterquestions webpage through which user choose the tag to filter the questions.
    :rtype: HttpResponseRedirect object
    """
    return render(request, 'filterquestions.html')



def save_upvote(request):
    """
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return:
    :rtype:
    """
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

            if (reply.user_name!= request.user):
                u = User.objects.get(user_name=reply.user_name)
                u.score+=5
                u.save()
            
                st = str(request.user) + " has UpVoted your Reply on the Question (Threadid - "+ str(reply.threadid.threadid) +"). As a result you have gained 5 points and now your new score is "+str(u.score)
                print(st)
                n=Notify(message=st,user_name=reply.user_name)
                n.save()
            return JsonResponse({'bool':True,'other':False})

def save_downvote(request):
    """
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return:
    :rtype:
    """

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
        if (reply.user_name!= request.user):

            u = User.objects.get(user_name=reply.user_name)
            u.score-=5
            u.save()
            
            st = str(request.user) + " has DownVoted your Reply on the Question (Threadid - "+ str(reply.threadid.threadid) +"). As a result you lost 5 points and now your new Score is "+str(u.score)
            print(st)
            n=Notify(message=st,user_name=reply.user_name)
            n.save()
        
            return JsonResponse({'bool':True,'other':False})

def save_like(request):

    """
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return:
    :rtype:
    """
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
            
            print(question.user_name)
            if ( request.user != question.user_name):
                st = str(request.user) +" has liked your Question (Threadid -"+ str(threadid) +") posted by you."
                print(st)
                n = Notify(message=st,user_name=question.user_name)
                n.save()
            
            return JsonResponse({'bool':True, 'other':False})

def save_dislike(request):
    """
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return:
    :rtype:
    """

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
            if ( request.user != question.user_name):
                st = str(request.user) +" has Disliked the Question (Threadid -"+ str(threadid) +") posted by you."
                print(st)
                n = Notify(message=st,user_name=question.user_name)
                n.save()

            return JsonResponse({'bool':True,'other':False})