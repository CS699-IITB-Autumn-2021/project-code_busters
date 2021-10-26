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
    """Display the Samvadika home page if the user is authenticated otherwise takes user to the login webpage. It shows all the question with their thread ID, published date and question tag along with 
    reply, save-item, like and dislike option.
    :param request: contains the metadata about the request e.g. HTTP request method used, IP address of the client etc.
    :type request: HttpRequest object
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
                l.append([eq,rp,qtag,len(rp)])
            else:
                l.append([eq,'',qtag,0])
        
        s=Save.objects.filter(user_name=request.user)

        print(l)

        return render(request,'index.html',{"query":l , "user":u,"save":s})

def signup(request):
    """Takes user to the Signup Webpage.
    :param request: contains the metadata of the signup request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Signup webpage for new registration.
    :rtype: HttpResponse object
    """
    return render(request, 'signup.html')

def saving(request):
    """Saves a particular question for the user.
    :param request: contains the metadata of the signup request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: A response denoting if the question has been saved successfully or not.
    :rtype: HttpResponse object
    """
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
    """Takes user to the login webpage.
    :param request: contains the metadata of the login request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Login webpage.
    :rtype: HttpResponse object
    """
    return    render(request, 'login.html')

def remove(request):
    """Removes an already saved question from the Saved Items page
    :param request: contains the metadata of the question posting request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Saved Items webpage.
    :rtype: HttpResponseRedirect object
    """
    id = request.GET['threadid']
    id = Question.objects.get(threadid=id)

    Save.objects.get(threadid=id,user_name=request.user).delete()

    return redirect("/saveditems")

def action_(request):
    """Authenticate the user by confirming their Email ID and password. If there is mismatch then it displays the warning and takes user to login page. On successful login, the user is redirected to samvadika home page.
    :param request: contains the metadata of the login action request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Successfully registers the new user by storing the details in the database. A warning message is displayed if there is a mismatch in password and confirm password fields, or if the email or username is already in use. Otherwise the user is redirected to the home page.
    :param request: contains the metadata of the signup action request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Logs out user and redirects to login page.
    :param request: contains the metadata of the logout request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Login webpage.
    :rtype: HttpResponse object
    """
    logout(request)
    return render(request,'login.html')

def posted(request):
    """Stores the posted question in the database and redirects user to the home page.
    :param request: contains the metadata of the question posting request e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Displays interest form initially and after filling up the form, it display the list of all the users with their hobbies.
    :param request: contains the metadata of the request to find the people e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Displays all the notifications like getting a response for a question posted by the user, upvotes or downvotes received for replies, etc.
    :param request: contains the metadata of the request to goto Notifications webpage e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Displays all the questions which are saved by the user.
    :param request: contains the metadata of the request to the Saved item webpage e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
            x.append([eq,rp,qtag,len(rp)])
        else:
            x.append([eq,'',qtag,],0)
        
        print(x)

    return render(request, 'saveditems.html',{"user":u,"query":x})


def Update_profile(request):
    """Takes user to the update profile page from where he/she updates the details.
    :param request: contains the metadata of the request to update profile e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: updateprofile webpage which provide the options to update the user profile.
    :rtype: HttpResponse object
    """
    return render(request, 'updateprofile.html')


def answer(request):
    """Stores the replies to the question in the database and redirects user to the home page. 
    :param request: contains the metadata of the request to answering the question(reply) e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
        u.score+=10
        u.save()
        n = Notify(message="You gained 10 points on answering a question (Threadid - "+ str(i.threadid) +") posted by "+ str(i.user_name) +". Now your score is "+str(u.score),user_name=request.user)
        n.save()
        st =  str(request.user) + " has answered the question (ThreadId - "+ str(i.threadid) +") posted by you."
        print(st)
        n = Notify(message=st,user_name=i.user_name)
        n.save()        
    return redirect('/')
    
def update_name(request):
    """Updates the user name.
    :param request: contains the metadata of the request to update name of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Updates the email of the user.
    :param request: contains the metadata of the request to update email of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Updates the password of the user.
    :param request: contains the metadata of the request to update password of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Changes the Facebook profile link of the user.
    :param request: contains the metadata of the request to changed hobbies of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Changes the LinkedIn profile link of the user.
    :param request: contains the metadata of the request to changed hobbies of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Changes the Hobbies of the user.
    :param request: contains the metadata of the request to changed hobbies of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Updates the profile picture of the user.
    :param request: contains the metadata of the request to update image of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Updates the user interests i.e. hobbies with there social media link like Facebook link, LinkedIn link. So that it is easier to find the people of same kind of interest and to link with them through social media.
    :param request: contains the metadata of the request to update interests of the user e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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
    """Filters the people by hobbies. It also supports filtering people by multiple hobbies.
    :param request: contains the metadata of the request to filter user by their hobbies e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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

            send=[]
            for i in li:
                hobby[i[0]]=[]
            
            for i in li:
                hobby[i[0]].extend(i[1])

            for i in hobby.keys():
                hobby[i] = set(hobby[i])

            for k in hobby.keys():
                send.append([k, hobby[k]])

            send = list(send)
            return render(request,'findpeople.html',{"query":send,"selected_hobbies_list":interest_filter_list}) 
        else:
            return redirect('/findpeople')


def Reset_filter_people(request):
    """Resets the filter to find people and allow users to adjust filter from starting.
    :param request: contains the metadata of the request to reset filter to find people e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: findpeople webpage.
    :rtype: HttpResponseRedirect object
    """
    return redirect('/findpeople')

def filter_questions(request):
    """Filters the questions by tags and show all filtered question with their replies.  
    :param request: contains the metadata of the request to filter questions by the tags e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
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

            qn_tags={}
            send=[]
            for i in li:
                qn_tags[i[0]]=[]
            
            for i in li:
                qn_tags[i[0]].extend(i[1])

            for i in qn_tags.keys():
                qn_tags[i] = set(qn_tags[i])

            for k in qn_tags.keys():
                send.append([k, qn_tags[k]])

            send = list(send)
            return render(request,'filterquestions.html',{"query":send,"selected_tag_list":tag_filter_list}) 
        
        else:
            return redirect('/')


def reset_filter_questions(request):
    """Resets the filter to find people and allow user to adjust filter from starting.
    :param request: contains the metadata of the request to reset filter to find question e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Home webpage from where user resets question tag for filter.
    :rtype: HttpResponseRedirect object
    """
    return redirect('/')

def filterbytags(request):
    """Takes the user to the webpage from where user filters the questions by specifying tag.
    :param request: contains the metadata of the request for the tag filter e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: filterquestions webpage through which user chooses the tag to filter the questions.
    :rtype: HttpResponseRedirect object
    """
    return render(request, 'filterquestions.html')



def save_upvote(request):
    """Saves the particular upvote in the database if the user has not already upvoted. The upvote entry is deleted if the user had already upvoted previously.
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Two boolean values as a JsonResponse object which indicates if the user had already upvoted and if he/she had already downvoted.
    :rtype: JsonResponse object
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
            if (reply.user_name!= request.user):
                u = User.objects.get(user_name=reply.user_name)
                u.score+=10
                u.save()
            
                st = str(request.user) + " has UpVoted your Reply on the Question (Threadid - "+ str(reply.threadid.threadid) +"). As a result you have gained 5 points and now your new score is "+str(u.score)
                n=Notify(message=st,user_name=reply.user_name)
                n.save()
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
    """Saves the particular downvote in the database if the user has not already downvoted. The downvote entry is deleted if the user had already downvoted previously.
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Two boolean values as a JsonResponse object which indicates if the user had already upvoted and if he/she had already downvoted.
    :rtype: JsonResponse object
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
            if (reply.user_name!= request.user):
                u = User.objects.get(user_name=reply.user_name)
                u.score-=10
                u.save()
                
                st = str(request.user) + " has DownVoted your Reply on the Question (Threadid - "+ str(reply.threadid.threadid) +"). As a result you lost 5 points and now your new Score is "+str(u.score)
                n=Notify(message=st,user_name=reply.user_name)
                n.save()
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
    """Saves the like in the database when the user likes a question. A new entry is created in the database if the user has not already liked. The like entry is deleted if the user had already liked previously.
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Two boolean values as a JsonResponse object which indicates if the user had already liked and if he/she had already disliked.
    :rtype: JsonResponse object
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
    """Saves the dislike in the database when the user dislikes a question. A new entry is created in the database if the user has not already disliked. The dislike entry is deleted if the user had already disliked previously.
    :param request: contains the metadata of the request to save upvote e.g. HTTP request method used, The IP address of the client etc.
    :type request: HttpRequest object
    ...
    :return: Two boolean values as a JsonResponse object which indicates if the user had already liked and if he/she had already disliked.
    :rtype: JsonResponse object
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