from django.conf.urls import url
from django.urls import path
from .views import *
urlpatterns = [

    path('',index,name='index'),
    path('signup/',signup,name='signup'),
    path('login/',User_login,name='user_login'),
    path('logout',User_logout,name='logout'),
    path('action',action_,name='action_'),
    path('register',register,name='register'),
    path('posted',posted,name='posted') ,
]
