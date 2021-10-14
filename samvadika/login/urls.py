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
    path('findpeople/',Find_people_check,name='find_people'),
    path('notifications/', Notifications,name='nofitications'),
    path('saveditems/',Saved_items,name='saveditems'),
    path('updateprofile/',Update_profile,name='updateprofile'),
    path('answer/',answer,name='answer'),
    path('updateprofile/update_name',update_name,name='update_name'),
    path('updateprofile/update_email',update_email,name='update_email'),
    path('updateprofile/update_pwd',update_pwd,name='update_pwd'),
    path('updateprofile/update_img',update_img,name='update_img'),
    path('findpeople/Updateinterests',Updateinterests,name='updateinterests'),
    #path('user_data/',UserInterestInfo, name='userinterestinfo')
]
